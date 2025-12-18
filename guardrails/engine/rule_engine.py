from guardrails.core.enums import Action
from guardrails.core.rule_result import RuleResult


class RuleEngine:
    """
    Aggregates guardrail rules, resolves actions,
    applies rewrites, and computes confidence score.
    """

    ACTION_PRIORITY = {
        Action.BLOCK: 4,
        Action.REWRITE: 3,
        Action.WARN: 2,
        Action.ALLOW: 1,
    }

    CONFIDENCE_PENALTY = {
        Action.ALLOW: 0.0,
        Action.WARN: 0.2,
        Action.REWRITE: 0.4,
        Action.BLOCK: 1.0,
    }

    def __init__(self, rules: list):
        self.rules = rules

    def evaluate(self, text: str, context: dict | None = None) -> dict:
        results: list[RuleResult] = []

        for rule in self.rules:
            result = rule.check(text, context=context)
            results.append(result)

        final_action = self._resolve_action(results)
        final_text = self._apply_rewrite(text, results, final_action)
        confidence = self._compute_confidence(results)

        return {
            "final_action": final_action,
            "final_text": final_text,
            "confidence": confidence,
            "results": results
        }

    def _resolve_action(self, results: list[RuleResult]) -> Action:
        highest_priority = 0
        chosen_action = Action.ALLOW

        for result in results:
            priority = self.ACTION_PRIORITY.get(result.action, 0)
            if priority > highest_priority:
                highest_priority = priority
                chosen_action = result.action

        return chosen_action

    def _compute_confidence(self, results: list[RuleResult]) -> float:
        confidence = 1.0

        for result in results:
            penalty = self.CONFIDENCE_PENALTY.get(result.action, 0.0)
            confidence -= penalty

        return max(0.0, round(confidence, 2))

    def _apply_rewrite(
        self,
        text: str,
        results: list[RuleResult],
        final_action: Action
    ) -> str:
        if final_action not in {Action.WARN, Action.REWRITE}:
            return text

        disclaimer = (
            "⚠️ Note: I may be mistaken, but based on general knowledge:\n\n"
        )

        softened = self._soften_language(text)

        verification = (
            "\n\nIt's a good idea to verify this information "
            "using reliable or official sources."
        )

        return disclaimer + softened + verification

    def _soften_language(self, text: str) -> str:
        replacements = {
            "definitely": "likely",
            "always": "often",
            "never": "rarely",
            "100%": "very likely",
            "guaranteed": "not guaranteed",
        }

        softened_text = text
        for hard, soft in replacements.items():
            softened_text = softened_text.replace(hard, soft)

        return softened_text
