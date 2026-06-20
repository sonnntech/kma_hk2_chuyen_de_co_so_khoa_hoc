# Working Rules

## Purpose

This repository is built task-by-task so each feature can be reviewed, tested,
run on Databricks, and merged before the next feature starts.

## Global Rules

1. Read `README.md` and the relevant skill reference before editing.
2. Do not work directly on `main`.
3. Use one branch per task.
4. Solve only the active task.
5. Do not implement future task behavior early.
6. Include tests or a clear manual Databricks verification path.
7. Put business logic in `src/blockchain_pipeline/`.
8. Keep notebooks thin: import functions, call them, display results.
9. Do not use real personal data.
10. Do not hard-code catalog, schema, or table names outside config.
11. Run on Databricks before merging.

## Branch Names

```text
feature/task-01-project-scaffold
feature/task-02-source-data
feature/task-03-medallion-pipeline
feature/task-04-canonical-hashing
feature/task-05-blockchain-ledger
feature/task-06-data-lineage
feature/task-07-integrity-verification
feature/task-08-tamper-scenarios
feature/task-09-experiment-metrics
feature/task-10-dashboard-documentation
```

## Commit Conventions

```text
feat: ...
fix: ...
test: ...
docs: ...
refactor: ...
```

## Per-Task Workflow

```text
1. Create task branch from latest main.
2. Confirm the active task prompt.
3. Inspect repository state.
4. List expected file changes.
5. Implement the task.
6. Run unit tests or targeted checks.
7. Push branch.
8. Pull branch into Databricks.
9. Run notebooks manually.
10. Record errors and results.
11. Fix minimal issues.
12. Open Pull Request.
13. Review diff.
14. Merge into main.
15. Move to the next task only after Databricks succeeds.
```

## Pre-Code Planning Prompt

Use before large changes:

```text
Trước khi sửa code, hãy:

1. Đọc README.md và CODEX_PLAN.md.
2. Kiểm tra cấu trúc repository hiện tại.
3. Xác nhận task đang thực hiện và các task không được thực hiện trước.
4. Liệt kê file dự kiến tạo hoặc sửa.
5. Nêu các giả định kỹ thuật.
6. Nêu rủi ro có thể ảnh hưởng Databricks Free Edition.
7. Chờ tôi xác nhận kế hoạch trước khi bắt đầu thay đổi lớn.
```

In this skill layout, treat `SKILL.md` plus `skills/reference/*.md` as the
replacement for `CODEX_PLAN.md`.

## Debug Prompt

```text
Hãy debug lỗi này theo phạm vi tối thiểu.

Yêu cầu:
1. Đọc log đầy đủ và xác định root cause.
2. Không viết lại toàn bộ project.
3. Nêu file, hàm và dòng logic có vấn đề.
4. Đề xuất bản sửa nhỏ nhất.
5. Bổ sung test tái hiện lỗi trước khi sửa nếu có thể.
6. Sau khi sửa, chạy lại test liên quan.
7. Tóm tắt root cause, thay đổi và cách xác minh trên Databricks.

Log lỗi:
<dán log vào đây>
```

## Review Prompt

```text
Hãy review thay đổi hiện tại như một Senior Data Engineer.

Kiểm tra:
- Có vượt phạm vi task không.
- Có hard-code catalog/schema/table name không.
- Hash có deterministic không.
- Có phụ thuộc thứ tự partition của Spark không.
- Notebook có chứa quá nhiều business logic không.
- Có rủi ro collect dữ liệu lớn về driver không.
- Có xử lý rerun/idempotency không.
- Có unit test cho logic quan trọng không.
- Có làm sai ý nghĩa blockchain hoặc data lineage không.
- Có đưa dữ liệu nhạy cảm vào repository không.

Hãy trả về:
1. Blocking issues.
2. Non-blocking improvements.
3. Test còn thiếu.
4. Verdict: APPROVE hoặc REQUEST CHANGES.
```

## Full MVP Definition of Done

- [ ] Source -> Bronze -> Silver -> Gold runs successfully.
- [ ] Synthetic data is reproducible.
- [ ] Row hash, batch hash, and schema hash are stable.
- [ ] Each pipeline stage creates one verification block.
- [ ] Blocks are linked correctly through `previous_hash`.
- [ ] Data lineage is recorded.
- [ ] Verification detects data tampering.
- [ ] Verification detects ledger tampering.
- [ ] Reset can restore the demo to a clean state.
- [ ] Benchmarks cover multiple data sizes.
- [ ] Real overhead metrics exist.
- [ ] Dashboard queries exist.
- [ ] `RUNBOOK.md` and `DEMO_SCRIPT.md` exist.
- [ ] Core unit tests pass.
- [ ] `README.md` reflects the actual run procedure.
- [ ] No secrets or sensitive data are committed.
