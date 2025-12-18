from guardrails.engine.rule_engine import RuleEngine
from guardrails.core.enums import Action


class GuardedPipeline:
    """
    Full Input → LLM → Output pipeline with guardrails.
    """

    def __init__(
        self,
        input_rules: list,
        output_rules: list,
        llm_callable
    ):
        self.input_engine = RuleEngine(input_rules)
        self.output_engine = RuleEngine(output_rules)
        self.llm = llm_callable

    def run(self, user_input: str) -> dict:
        # 1️⃣ INPUT GUARDRAILS
        input_eval = self.input_engine.evaluate(user_input)

        if input_eval["final_action"] == Action.BLOCK:
            return {
                "status": "BLOCKED",
                "stage": "input",
                "final_action": Action.BLOCK,
                "confidence": 0.0,
                "message": "Input blocked by safety guardrails",
                "details": input_eval["results"]
            }

        # 2️⃣ LLM CALL (UNTRUSTED)
        raw_output = self.llm(user_input)

        # 3️⃣ OUTPUT GUARDRAILS
        output_eval = self.output_engine.evaluate(raw_output)

        return {
            "status": "OK",
            "stage": "output",
            "final_action": output_eval["final_action"],
            "confidence": output_eval["confidence"],
            "response": output_eval["final_text"],
            "details": output_eval["results"]
        }
