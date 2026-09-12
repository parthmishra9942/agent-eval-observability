from typing import Dict, Any
from agent_eval.tracer import TrajectoryRun

class LLMJudgeEngine:
    """Scores agent trajectories using multi-dimensional rubrics."""
    def evaluate(self, run: TrajectoryRun, expected_outcome: str) -> Dict[str, Any]:
        # Faithfulness check: ensure assertions align with step outputs
        evidence_text = " ".join([s.output_payload for s in run.steps]).lower()
        output_words = run.final_output.lower().split()
        supported = [w for w in output_words if w in evidence_text or len(w) <= 3]
        faithfulness = round(len(supported) / max(len(output_words), 1), 3)

        # Answer relevance check: comparison with task prompt and expected outcome
        expected_terms = set(expected_outcome.lower().split())
        actual_terms = set(run.final_output.lower().split())
        overlap = len(expected_terms.intersection(actual_terms))
        relevance = round(overlap / max(len(expected_terms), 1), 3)

        # Tool precision: ratio of successful tool steps
        tool_steps = [s for s in run.steps if s.action_type == "tool_call"]
        successful_tools = [s for s in tool_steps if "error" not in s.output_payload.lower()]
        tool_precision = round(len(successful_tools) / max(len(tool_steps), 1), 3) if tool_steps else 1.0

        overall_score = round((faithfulness * 0.4) + (relevance * 0.4) + (tool_precision * 0.2), 3)
        passed = overall_score >= 0.70

        return {
            "run_id": run.run_id,
            "overall_score": overall_score,
            "status": "PASS" if passed else "FAIL",
            "metrics": {
                "faithfulness": faithfulness,
                "answer_relevance": relevance,
                "tool_precision": tool_precision
            },
            "telemetry": {
                "latency_ms": run.total_latency_ms,
                "cost_usd": run.total_cost_usd
            }
        }
