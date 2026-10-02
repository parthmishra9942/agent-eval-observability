from agent_eval.tracer import ExecutionTracer, AgentStepTrace
from agent_eval.llm_judge import LLMJudgeEngine
from agent_eval.regression_runner import RegressionBenchmarkRunner

def test_tracer_and_judge():
    tracer = ExecutionTracer()
    steps = [
        AgentStepTrace(
            step_num=1,
            action_type="tool_call",
            tool_name="database_lookup",
            input_payload="select count(*) from users",
            output_payload="total_users: 1420",
            latency_ms=45.0,
            token_usage={"prompt": 80, "completion": 20}
        )
    ]
    run = tracer.trace_run("run_001", "How many users?", "There are 1420 users in database.", steps)
    assert run.total_latency_ms == 45.0

    judge = LLMJudgeEngine()
    result = judge.evaluate(run, expected_outcome="1420 users")
    assert result["status"] == "PASS"
    assert result["metrics"]["faithfulness"] > 0.8

def test_regression_runner_pass():
    runner = RegressionBenchmarkRunner(min_pass_rate=0.75)
    suite = [
        {
            "id": "test_1",
            "query": "Find order #99 status",
            "evidence": "Order 99 is shipped",
            "output": "Order 99 has been shipped.",
            "expected": "shipped"
        }
    ]
    summary = runner.run_suite(suite)
    assert summary["suite_status"] == "PASSED"
    assert summary["pass_rate"] == 1.0
