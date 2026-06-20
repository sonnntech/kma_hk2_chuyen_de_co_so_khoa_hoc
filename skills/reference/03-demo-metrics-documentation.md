# Tasks 08-10: Tamper Demo, Metrics, and Documentation

Use this reference for attack scenarios, reset behavior, benchmark experiments,
dashboard queries, runbook, and demo script work.

## Task 08 - Tamper Scenarios and Reset

### Goal

Create direct tamper scenarios for live demonstration.

### Branch

```text
feature/task-08-tamper-scenarios
```

### Files

```text
notebooks/06_run_tamper_scenarios.py
sql/tamper_scenarios.sql
src/blockchain_pipeline/tamper.py
```

### Scenarios

1. Modify one transaction.
2. Delete one transaction.
3. Insert one fake transaction.
4. Modify batch hash in ledger.
5. Modify transformation metadata in ledger.
6. Modify previous hash.
7. Reset to a clean baseline.

### Acceptance

- Each scenario runs independently.
- Before/after data is displayed.
- Verification detects the expected error type.
- Reset can restore demo state.
- Destructive scenarios require widget confirmation.

### Prompt

```text
Hãy đọc README.md và CODEX_PLAN.md.

Chỉ thực hiện Task 08 – Tamper scenarios và reset.

Yêu cầu:
- Mỗi scenario là một hàm riêng.
- Notebook dùng widget để chọn scenario.
- Có tham số CONFIRM_TAMPER để tránh chạy nhầm.
- Hiển thị dữ liệu trước và sau khi sửa.
- Sau khi chạy, gọi verification và hiển thị kết quả.
- Có reset scenario để khôi phục dữ liệu demo.
- Không sửa cấu trúc cốt lõi của hashing và ledger nếu không cần.
```

## Task 09 - Benchmark and Experiment Metrics

### Goal

Create real experiment metrics for project evaluation.

### Branch

```text
feature/task-09-experiment-metrics
```

### Files

```text
src/blockchain_pipeline/metrics.py
notebooks/07_experiment_and_metrics.py
tests/test_metrics.py
```

### Experiment Sizes

```text
1,000 rows
5,000 rows
10,000 rows
50,000 rows
```

Run each size at least three times.

### Metrics

- Baseline pipeline duration.
- Secured pipeline duration.
- Verification duration.
- Processing overhead percentage.
- Detection accuracy.
- Metadata record count.

### Acceptance

- Results are written to `experiment_metrics`.
- Conclusions are not based on a single run.
- Warm-up is separated or explicitly documented.
- Median or average is clear.
- Baseline duration equal to zero is handled.
- Metrics are generated from real runs, not fabricated.

### Prompt

```text
Hãy đọc README.md và CODEX_PLAN.md.

Chỉ thực hiện Task 09 – Benchmark và experimental metrics.

Yêu cầu:
- Benchmark baseline pipeline và secured pipeline.
- Chạy các mức 1k, 5k, 10k, 50k; mỗi mức tối thiểu ba lần.
- Đo pipeline duration, verification duration và overhead.
- Ghi kết quả vào experiment_metrics.
- Tách warm-up khỏi lần đo chính hoặc ghi chú rõ.
- Không giả lập số liệu; tất cả số liệu phải sinh từ lần chạy thật.
- Có kiểm tra công thức overhead.
```

## Task 10 - Dashboard and Final Documentation

### Goal

Finish dashboard queries, run documentation, and presentation materials.

### Branch

```text
feature/task-10-dashboard-documentation
```

### Files

```text
sql/dashboard_queries.sql
RUNBOOK.md
DEMO_SCRIPT.md
README.md
```

### Dashboard KPIs

- Total pipeline runs.
- Total blocks.
- Successful verifications.
- Detected tamper events.
- Verification latency.
- Processing overhead.
- Lineage SOURCE -> BRONZE -> SILVER -> GOLD.
- First broken block.

### RUNBOOK Requirements

- How to clone GitHub repo into Databricks.
- How to configure catalog/schema.
- Notebook run order.
- How to reset demo.
- Common error handling.

### DEMO_SCRIPT Requirements

- 10-15 minute presentation script.
- Short speaker notes for each step.
- Expected result on each screen.
- Backup plan if Databricks quota is exhausted.

### Acceptance

- Another person can rerun the demo from documentation.
- Dashboard SQL runs against configured schema.
- Clean demo and tamper demo scripts exist.
- README reflects final code structure.

### Prompt

```text
Hãy đọc README.md và CODEX_PLAN.md.

Chỉ thực hiện Task 10 – Dashboard và tài liệu hoàn thiện.

Yêu cầu:
- Tạo dashboard_queries.sql với các KPI đã mô tả.
- Tạo RUNBOOK.md hướng dẫn chạy từ đầu trên Databricks.
- Tạo DEMO_SCRIPT.md cho phần trình bày 10–15 phút.
- Cập nhật README theo cấu trúc project thực tế.
- Không thay đổi logic hashing, ledger hoặc verification nếu không có lỗi rõ ràng.
- Cuối cùng lập checklist nghiệm thu toàn bộ MVP.
```
