from fastapi import FastAPI
from pydantic import BaseModel

from guardrails.engine.pipeline import GuardedPipeline
from guardrails.input_rules.injection_rule import InjectionDetectionRule
from guardrails.input_rules.safety_policy_rule import SafetyPolicyRule
from guardrails.output_rules.hallucination_rule import HallucinationDetectionRule


# -----------------------
# Mock LLM (replace later)
# -----------------------
def mock_llm(prompt: str) -> str:
    if "jobs" in prompt.lower():
        return "According to a study from MIT University, 90% of humans will lose jobs."
    return "AI is a branch of computer science."


# -----------------------
# Pipeline Initialization
# -----------------------
pipeline = GuardedPipeline(
    input_rules=[
        InjectionDetectionRule(),
        SafetyPolicyRule()
    ],
    output_rules=[
        HallucinationDetectionRule()
    ],
    llm_callable=mock_llm
)

# -----------------------
# FastAPI App
# -----------------------
app = FastAPI(
    title="Prompt Guardrails & Hallucination Control API",
    version="1.0.0"
)


class PromptRequest(BaseModel):
    prompt: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/guarded-chat")
def guarded_chat(request: PromptRequest):
    result = pipeline.run(request.prompt)

    return {
        "final_action": str(result.get("final_action")),
        "confidence": result.get("confidence"),
        "response": result.get("response", result.get("message")),
        "details": [str(r) for r in result.get("details", [])]
    }
