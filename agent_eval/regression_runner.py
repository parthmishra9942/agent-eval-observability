from typing import List, Dict, Any
from agent_eval.tracer import ExecutionTracer, AgentStepTrace
from agent_eval.llm_judge import LLMJudgeEngine

class RegressionBenchmarkRunner:
    """Runs automated test suites to detect quality, latency, or cost regressions."""
    def __init__(self, min_pass_rate: float = 0.80):
        self.min_pass_rate = min_pass_rate
        self.tracer = ExecutionTracer()
        self.judge = LLMJudgeEngine()

    def run_suite(self, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        results = []
        for case in test_cases:
            steps = [
                AgentStepTrace(
                    step_num=1,
                    action_type="tool_call",
                    tool_name=case.get("tool_name", "db_query"),
                    input_payload=case["query"],
                    output_payload=case["evidence"],
                    latency_ms=case.get("latency_ms", 120.0),
                    token_usage={"prompt": 150, "completion": 45}
                )
            ]
            run = self.tracer.trace_run(
                run_id=case["id"],
                prompt=case["query"],
                final_output=case["output"],
                steps=steps
            )
            score_data = self.judge.evaluate(run, expected_outcome=case["expected"])
            results.append(score_data)

        total_runs = len(results)
        passed_runs = sum(1 for r in results if r["status"] == "PASS")
        pass_rate = passed_runs / max(total_runs, 1)

        avg_lat = sum(r["telemetry"]["latency_ms"] for r in results) / max(total_runs, 1)
        total_cost = sum(r["telemetry"]["cost_usd"] for r in results)

        return {
            "total_evaluated": total_runs,
            "pass_rate": round(pass_rate, 3),
            "suite_status": "PASSED" if pass_rate >= self.min_pass_rate else "REGRESSION_DETECTED",
            "average_latency_ms": round(avg_lat, 2),
            "total_cost_usd": round(total_cost, 6),
            "eval_results": results
        }
