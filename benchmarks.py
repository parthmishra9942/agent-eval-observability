import time
import sys
sys.stdout.reconfigure(encoding='utf-8')
from agent_eval.regression_runner import RegressionBenchmarkRunner
from agent_eval.dashboard import ObservabilityDashboard

print("=== Agent Evaluation Regression Runner Benchmark ===")
runner = RegressionBenchmarkRunner(min_pass_rate=0.80)

suite = [
    {
        "id": f"eval_case_{i}",
        "query": f"Retrieve telemetry metrics for node-{i}",
        "evidence": f"Node-{i} health status is healthy with cpu utilization 22%",
        "output": f"Node-{i} is healthy with 22% CPU utilization.",
        "expected": "healthy 22% cpu",
        "latency_ms": 65.0 + (i * 2)
    }
    for i in range(10)
]

t0 = time.perf_counter()
summary = runner.run_suite(suite)
t1 = time.perf_counter()

print(ObservabilityDashboard.render(summary))
print(f"Total Evaluation Time for 10 Trajectories: {(t1 - t0)*1000:.2f} ms")
