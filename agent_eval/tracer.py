import time
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class AgentStepTrace:
    step_num: int
    action_type: str
    tool_name: Optional[str]
    input_payload: str
    output_payload: str
    latency_ms: float
    token_usage: Dict[str, int] = field(default_factory=lambda: {"prompt": 0, "completion": 0})

@dataclass
class TrajectoryRun:
    run_id: str
    task_prompt: str
    final_output: str
    steps: List[AgentStepTrace] = field(default_factory=list)
    total_latency_ms: float = 0.0
    total_cost_usd: float = 0.0

class ExecutionTracer:
    """Records granular step-level telemetry for agent executions."""
    def __init__(self, cost_per_1k_input: float = 0.0015, cost_per_1k_output: float = 0.0020):
        self.cost_in = cost_per_1k_input
        self.cost_out = cost_per_1k_output

    def trace_run(self, run_id: str, prompt: str, final_output: str, steps: List[AgentStepTrace]) -> TrajectoryRun:
        total_lat = sum(s.latency_ms for s in steps)
        total_p_tokens = sum(s.token_usage.get("prompt", 0) for s in steps)
        total_c_tokens = sum(s.token_usage.get("completion", 0) for s in steps)
        cost = (total_p_tokens / 1000.0 * self.cost_in) + (total_c_tokens / 1000.0 * self.cost_out)
        return TrajectoryRun(
            run_id=run_id,
            task_prompt=prompt,
            final_output=final_output,
            steps=steps,
            total_latency_ms=round(total_lat, 2),
            total_cost_usd=round(cost, 6)
        )
