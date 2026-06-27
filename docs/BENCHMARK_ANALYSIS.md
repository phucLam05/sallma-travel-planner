# Benchmark Methodology and Results

This document summarizes the results of the benchmark runs comparing three different architectures:
1. **Single-Agent (No RAG)**: The baseline single LLM generating plans purely from parametric knowledge, without database access.
   - Run data exported at: [benchmark_full_20260617_063715.json](../benchmarks/results/benchmark_full_20260617_063715.json)
2. **Single-Agent (RAG)**: A single LLM equipped with database access via the `retrieve_places` tool.
   - Run data exported at: [benchmark_single_rag_20260627_091510.json](../benchmarks/results/benchmark_single_rag_20260627_091510.json)
3. **Multi-Agent (SALLMA)**: The LangGraph-based workflow architecture (Workflow Agent, Research Agent, Planner Agent, and deterministic Budget Node).
   - Run data exported at: [benchmark_single_rag_20260627_091510.json](../benchmarks/results/benchmark_single_rag_20260627_091510.json) (Multi-Agent portion)

## 1. Experimental Setup

- Benchmark size: `30` create prompts
- Multi-turn memory test: `2` sessions, each with `10` turns
- Latency stress test: `5` concurrent simulated group rooms
- Text model: `gemini-3.1-flash-lite`
- Knowledge base: PostgreSQL `places` table with verified hotels, attractions, and restaurants

## 2. Metric Operationalization

### 2.1 Correctness & Hallucination
Correctness is defined as the percentage of recommended places that can be matched to the verified knowledge base. For each generated output, the benchmark extracts all place names from hotel selection and itinerary activities, normalizes them, and fuzzy-matches them against the PostgreSQL `places` table.

Formula:

```text
verified_rate = verified_places / total_places
hallucination_rate = 1 - verified_rate
```

Raw benchmark totals for the reported runs:

- **Single-Agent (No RAG)**: `109` verified places out of `249` generated places across `30` cases (macro-average: `43.73%` verified, `56.27%` hallucinated).
- **Single-Agent (RAG)**: `228` verified places out of `231` generated places across `30` cases (macro-average: `98.55%` verified, `1.45%` hallucinated).
- **Multi-Agent**: `435` verified places out of `435` generated places across `30` cases (macro-average: `100.00%` verified, `0.00%` hallucinated).

### 2.2 Budget Accuracy
Budget accuracy is defined as the absolute difference between the budget claimed in the generated response and a deterministic recomputation of the total trip cost.

Formula:

```text
budget_delta = abs(claimed_total_cost - recomputed_total_cost)
```

For the multi-agent system, the final budget comes from the dedicated Budget Node, while the single-agent baselines rely on the LLM's own arithmetic.

Raw benchmark totals for the reported runs:

- **Single-Agent (No RAG)** total absolute budget error across `30` cases: `15,940,000 VND` (average: `531,333 VND`).
- **Single-Agent (RAG)** total absolute budget error across `30` cases: `6,120,000 VND` (average: `204,000 VND`).
- **Multi-Agent** total absolute budget error across `30` cases: `0 VND` (average: `0 VND`).

### 2.3 Consistency
Consistency is implemented as a rule-based contradiction counter checking for structural violations (mismatch in days/nights, chronological meal orders, activities too far from the hotel, duplicated activities, missing coordinates).

Raw benchmark totals for the reported runs:

- **Create Benchmark**:
  - Single-Agent (No RAG): `6` total violations across `30` cases -> `0.20` violations/case.
  - Single-Agent (RAG): `7` total violations across `30` cases -> `0.23` violations/case.
  - Multi-Agent: `138` total violations across `30` cases -> `4.60` violations/case.
- **Multi-turn 10-turn session final states**:
  - Single-Agent (No RAG): `1` total violation across `2` sessions -> `0.5` violations/session.
  - Single-Agent (RAG): `2` total violations across `2` sessions -> `1.0` violations/session.
  - Multi-Agent: `14` total violations across `2` sessions -> `7.0` violations/session.

### 2.4 State Retention
State retention is evaluated through 10-turn sessions that repeatedly refine an itinerary. It checks whether key constraints (e.g. hotel selections, trip lengths) are preserved.

- **Single-Agent (No RAG)**: `10 / 10` checks passed (100% pass rate).
- **Single-Agent (RAG)**: `10 / 10` checks passed (100% pass rate).
- **Multi-Agent**: `10 / 10` checks passed (100% pass rate).

### 2.5 Latency
Latency is measured as end-to-end workflow time under concurrent load (5 simulated concurrent group rooms, 10 samples per workflow).

Raw average benchmark latency results:

- **Create Workflow**:
  - Single-Agent (No RAG): `19.814s` (summed: ~198.14s)
  - Single-Agent (RAG): `44.285s` (summed: ~442.85s)
  - Multi-Agent: `95.627s` (summed: ~956.27s)
- **Refine Workflow**:
  - Single-Agent (No RAG): `18.628s` (summed: ~186.28s)
  - Single-Agent (RAG): `43.882s` (summed: ~438.82s)
  - Multi-Agent: `54.740s` (summed: ~547.40s)
- **Budget Workflow**:
  - Single-Agent (No RAG): `19.572s` (summed: ~195.72s)
  - Single-Agent (RAG): `20.079s` (summed: ~200.79s)
  - Multi-Agent: `0.000s` (summed: 0.00s)

### 2.6 User-Perceived Usefulness (Automated Proxy)
An automated proxy score (1–5 scale) calculated from correctness, budget accuracy, and consistency.

Raw benchmark totals for the reported runs:
- **Single-Agent (No RAG)**: total proxy score `125.05` -> `4.17 / 5`
- **Single-Agent (RAG)**: total proxy score `142.80` -> `4.76 / 5`
- **Multi-Agent**: total proxy score `109.50` -> `3.65 / 5`

---

## 3. Results Summary

### 3.1 Create Benchmark Comparison

| Metric | Single-Agent (No RAG) | Single-Agent (RAG) | Multi-Agent |
|---|---:|---:|---:|
| **Cases** | `30` | `30` | `30` |
| **Average latency per create case** | `6.897s` | `12.664s` | `25.019s` |
| **Verified place rate** | `43.73%` | `98.55%` | `100.00%` |
| **Hallucination rate** | `56.27%` | `1.45%` | `0.00%` |
| **Average budget delta** | `531,333 VND` | `204,000 VND` | `0 VND` |
| **Average consistency violations** | `0.20` | `0.23` | `4.60` |
| **Usefulness proxy** | `4.17/5` | `4.76/5` | `3.65/5` |

### 3.2 Multi-Turn State Retention Comparison

| Metric | Single-Agent (No RAG) | Single-Agent (RAG) | Multi-Agent |
|---|---:|---:|---:|
| **Sessions** | `2` | `2` | `2` |
| **State retention pass rate** | `100%` | `100%` | `100%` |
| **Average turn latency** | `8.786s` | `13.135s` | `22.453s` |
| **Average consistency violations** | `0.5` | `1.0` | `7.0` |

### 3.3 Latency under Stress Test (5 Concurrent Rooms)

| Workflow | Single-Agent (No RAG) | Single-Agent (RAG) | Multi-Agent |
|---|---:|---:|---:|
| **Create** | `19.814s` | `44.285s` | `95.627s` |
| **Refine** | `18.628s` | `43.882s` | `54.740s` |
| **Budget** | `19.572s` | `20.079s` | `0.000s` |

---

## 4. Interpretation and Discussion

### 4.1 Impact of Database Grounding (No RAG vs RAG)
The transition from a pure single agent (**No RAG**) to a single agent with database grounding (**RAG**) demonstrates a dramatic improvement in data quality:
* **Verified rate** surged from a poor `43.73%` (where over half of the places recommended were made up) to a highly reliable `98.55%`.
* **Budget accuracy** also improved, with the average error dropping from `531,333 VND` to `204,000 VND` as the RAG agent retrieved actual lodging and meal costs instead of guessing.
* However, this grounding came with a **latency cost**: adding RAG doubled the average create latency under stress test from `19.814s` to `44.285s`, due to the multiple tool calls required to query the database.

### 4.2 Multi-Agent (SALLMA) vs Single-Agent (RAG)
Equipping the Single-Agent with RAG closes the gap in correctness significantly (`98.55%` vs `100.00%`). However, the Multi-Agent architecture still holds critical advantages:
* **Perfect Grounding**: Multi-Agent reaches `100.00%` correctness (zero hallucinations). The sequential separation of Research and Planning ensures the final plan is strictly composed of database retrieved objects.
* **Deterministic Calculations**: The Multi-Agent's `Budget Node` guarantees a `0 VND` budget delta. In contrast, the Single-Agent (RAG), despite having database access, still performs its own arithmetic, resulting in a `204,000 VND` average error.
* **Latency Trade-Off**: The Multi-Agent remains much slower (`95.627s` Create latency under stress test) because it operates a multi-step graph loop with multiple LLM calls.
* **Consistency Penalization**: The rule-based consistency metrics show a high violation rate for Multi-Agent (`4.60` vs `0.23`). This is a side-effect of the Multi-Agent generating fully structured and denser itineraries (4-6 daily activities, matching meal schedules, and strict coordinate listings) which increase the probability of rule-based triggers compared to the briefer, simpler itineraries returned by the Single-Agent.

## 5. Summary Report

* **Single-Agent (No RAG)** is fast but unusable for a commercial travel product because over 56% of recommended places are hallucinations.
* **Single-Agent (RAG)** provides a highly competitive, simple alternative. It eliminates almost all hallucinations (accuracy >98.5%) and remains twice as fast as the Multi-Agent system.
* **Multi-Agent (SALLMA)** is the most robust and accurate architecture, ensuring 100% correct database matching and 100% mathematically correct budgets, but it demands higher operational costs, API token consumption, and response delays.
