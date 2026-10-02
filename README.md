# 🔬 Agent Evaluation & Observability Harness (LLM-as-a-Judge)

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![Evaluation: LLM Judge](https://img.shields.io/badge/Judge-Structured%20Rubric-purple.svg)](#eval-rubric)
[![Telemetry: OpenTelemetry](https://img.shields.io/badge/Telemetry-Step--Level%20Tracing-brightgreen.svg)](#tracing)
[![CI/CD: Regression Gate](https://img.shields.io/badge/CI%2FCD-Regression%20Gates-orange.svg)](#regression-testing)

A production **Evaluation, Benchmarking & Observability Harness** for autonomous AI agents. Replays multi-step execution trajectories, scores agent behaviors across **Faithfulness**, **Answer Relevance**, and **Tool Precision** using an LLM-as-a-Judge scoring engine, and enforces CI/CD regression gates against latency and cost degradation.

---

## 🏛️ Observability Architecture

```
Agent Execution ──► ExecutionTracer (Step-Level Telemetry)
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
     Tool Calls        Tokens         Latency (ms)
     & Payloads        & Cost
          │               │               │
          └───────────────┼───────────────┘
                          │
                          ▼
            ┌───────────────────────────┐
            │    LLM-as-a-Judge Engine  │
            │   Multi-Dimensional Eval  │
            └─────────────┬─────────────┘
                          │
         ┌────────────────┴────────────────┐
         ▼                                 ▼
   Quality Metrics                   CI/CD Gate
   • Faithfulness (0-1)              • Min Pass Rate: 80%
   • Answer Relevance (0-1)          • Max Latency Spike: <15%
   • Tool Precision (0-1)            • Token Cost Budgeting
```

---

## ⚡ Technical Highlights

* **Granular Trajectory Tracing**: Logs step-by-step state transitions, tool execution arguments, return payloads, token counters, and wall-clock latencies.
* **Multi-Dimensional LLM-as-a-Judge Rubric**: Computes composite ground truth alignment:
  $$\text{Score} = 0.4 \times \text{Faithfulness} + 0.4 \times \text{Relevance} + 0.2 \times \text{Tool Precision}$$
* **CI/CD Quality Gates**: Flags regressions before agent models or prompt modifications are merged into production branches.
* **Terminal Dashboard**: Outputs structured ASCII diagnostics and telemetry summaries for instant developer inspection.

---

## 📊 Sample CI/CD Output

```
================================================================
       📊 AGENT EVALUATION & OBSERVABILITY REPORT        
================================================================
Suite Status:       PASSED
Pass Rate:          100.0% (10 runs)
Average Latency:    74.0 ms
Total Token Cost:   $0.003150 USD
----------------------------------------------------------------
Run ID          | Score    | Status | Faithful | Latency 
----------------------------------------------------------------
eval_case_0     | 0.88     | PASS   | 1.00     | 65.0ms
eval_case_1     | 0.88     | PASS   | 1.00     | 67.0ms
eval_case_2     | 0.88     | PASS   | 1.00     | 69.0ms
================================================================
```

---

## 🚀 Quickstart

```bash
# Clone the repository
git clone https://github.com/parthmishra9942/agent-eval-observability.git
cd agent-eval-observability

# Run tests
pytest tests/

# Run regression benchmark & dashboard
python benchmarks.py
```

---

## 🎯 Interview Deep Dive (Talking Points)

1. **Why LLM-as-a-Judge over BLEU/ROUGE?**  
   *Traditional n-gram overlap metrics (BLEU, ROUGE) penalize valid paraphrasing and fail to measure logical hallucination. LLM-as-a-Judge uses semantic reasoning against a grounded rubric, assessing whether facts in the answer are substantiated by intermediate tool outputs.*
2. **Preventing Judge Self-Preference Bias:**  
   *Judges often favor outputs from their own family of models. We mitigate this through reference-guided scoring, where the judge evaluates overlap with expected criteria rather than subjective output style.*

---

## 👤 Author
**Parth Mishra**  
* B.Tech Computer Science (AI/ML) — VIT Bhopal University  
* Portfolio: [parthh.runs-on.dev](https://parthh.runs-on.dev) | GitHub: [@parthmishra9942](https://github.com/parthmishra9942)
