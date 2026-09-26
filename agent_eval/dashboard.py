from typing import Dict, Any

class ObservabilityDashboard:
    """Generates ASCII terminal summary for CI/CD status reporting."""
    @staticmethod
    def render(suite_summary: Dict[str, Any]) -> str:
        lines = []
        lines.append("=" * 64)
        lines.append("       📊 AGENT EVALUATION & OBSERVABILITY REPORT        ")
        lines.append("=" * 64)
        lines.append(f"Suite Status:       {suite_summary['suite_status']}")
        lines.append(f"Pass Rate:          {suite_summary['pass_rate'] * 100:.1f}% ({suite_summary['total_evaluated']} runs)")
        lines.append(f"Average Latency:    {suite_summary['average_latency_ms']} ms")
        lines.append(f"Total Token Cost:   ${suite_summary['total_cost_usd']:.6f} USD")
        lines.append("-" * 64)
        lines.append(f"{'Run ID':<15} | {'Score':<8} | {'Status':<6} | {'Faithful':<8} | {'Latency':<8}")
        lines.append("-" * 64)
        for r in suite_summary["eval_results"]:
            lines.append(f"{r['run_id']:<15} | {r['overall_score']:<8.2f} | {r['status']:<6} | {r['metrics']['faithfulness']:<8.2f} | {r['telemetry']['latency_ms']}ms")
        lines.append("=" * 64)
        return "\n".join(lines)
