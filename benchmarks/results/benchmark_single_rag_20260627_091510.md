# Full Benchmark Results (Single-Agent with RAG vs Multi-Agent)

- Generated at: `2026-06-27T09:15:10.006421`
- Create prompts: `30`
- Concurrent rooms for latency suite: `5`

## 1. Correctness and Budget Accuracy

| Metric | Single-Agent (RAG) | Multi-Agent |
|---|---:|---:|
| Avg verified place rate | 98.55% | 100.00% |
| Avg hallucination rate | 1.45% | 0.00% |
| Avg budget delta (VND) | 204000 | 0 |

## 2. Consistency

- Single-agent (RAG) average consistency violations per create case: `0.23`
- Multi-agent average consistency violations per create case: `4.6`
- Single-agent (RAG) average consistency violations in 10-turn sessions: `1`
- Multi-agent average consistency violations in 10-turn sessions: `7`

## 3. State Retention

- Single-agent (RAG) average state retention pass rate: `100.00%`
- Multi-agent average state retention pass rate: `100.00%`

## 4. Latency

| Workflow | Single-Agent (RAG) Avg (s) | Multi-Agent Avg (s) |
|---|---:|---:|
| Create | 44.285 | 95.627 |
| Refine | 43.882 | 54.740 |
| Budget | 20.079 | 0.000 |

## 5. User-Perceived Usefulness (Automated Proxy)

- Single-agent (RAG) average usefulness score: `4.76/5`
- Multi-agent average usefulness score: `3.65/5`
- Note: this is an automated proxy derived from clarity, trustworthiness, and consistency signals; replace with a real Likert survey when human participants are available.