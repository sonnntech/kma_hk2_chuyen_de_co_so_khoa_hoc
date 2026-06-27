# Ten de tai

**Ap dung nghien cuu ban thuc nghiem de danh gia co che dam bao tinh toan ven va truy vet du lieu trong he thong Data Pipeline**

> Blockchain trong de tai nay chi la **case study ky thuat** va la **treatment** duoc dua vao Data Pipeline de quan sat tac dong. Muc tieu chinh cua de tai la the hien cach ap dung **Quasi-experimental Research** vao mot bai toan an toan thong tin: phat hien thay doi trai phep va truy vet sai lech du lieu trong Data Pipeline.

## Bao cao ra soat theo Chuong 10: Quasi-experimental Research

### 1. Nhan xet tong quan

Ban thao cu hien co nen tang ky thuat tot: mo ta ro Data Pipeline, Data Integrity, Data Lineage, hash, ledger dang hash chain, tamper scenarios, verification engine, benchmark va dashboard. Tuy nhien, neu giang vien doc theo goc nhin Chuong 10, ban thao cu de tao an tuong rang de tai la **xay dung mot mo hinh Blockchain** hon la **thiet ke mot nghien cuu ban thuc nghiem**.

Cau hoi can dat cho toan bo bao cao la:

> Neu giang vien doc phan nay, ho co thay ro phan nay phan anh Quasi-experimental Research khong?

Theo tieu chi do, ban thao cu con thieu cac cau phan nghien cuu sau:

| Yeu cau Chuong 10 | Tinh trang trong ban thao cu | Van de can sua |
|---|---|---|
| Research problem | Co noi ve mat toan ven du lieu, nhung chua dong khung thanh bai toan nghien cuu an toan thong tin | Can neu ro van de can do luong va kiem dinh |
| Research gap | Chua tach ro khoang trong nghien cuu | Can chi ra pipeline thuong co quality/logging nhung thieu bang chung tamper-evident co the kiem chung sau xu ly |
| Research questions | Chua co cau hoi nghien cuu rieng | Can viet RQ gan voi hieu qua phat hien, truy vet va overhead |
| Research hypotheses | Chua co gia thuyet kiem dinh | Can viet H1/H2/H3 de co the do bang thuc nghiem |
| Ly do dung quasi-experiment | Chua co | Can giai thich vi sao khong the true experiment: moi truong Databricks, compute state, pipeline data, cold start, snowflake environment |
| Treatment/control | Co baseline/secured duration nhung chua trinh bay nhu treatment va control | Can dinh nghia control pipeline va treatment pipeline |
| Bien doc lap/phu thuoc | Chua co | Can liet ke ro |
| Metrics | Co nhung phan tan | Can gom lai thanh measurement metrics |
| Experimental procedure | Co notebook sequence nhung chua viet nhu quy trinh thuc nghiem | Can viet theo buoc pre-test/post-test va tamper scenarios |
| Uncontrolled variables | Moi co nhac cold start | Can liet ke day du |
| Bias/validity threats | Chua co muc rieng | Can danh gia internal, external, construct, conclusion validity |
| Methodological limitations | Moi co gioi han ky thuat | Can them gioi han phuong phap |
| Future work cho quasi-design | Chua tap trung | Can neu cach tang control, replication, randomization, external ledger |

### 2. Huong refactor

Bao cao duoc to chuc lai de moi phan ky thuat deu phuc vu thiet ke nghien cuu ban thuc nghiem:

1. Dat bai toan la mot van de cyber security: phat hien va truy vet thay doi trai phep trong Data Pipeline.
2. Xac dinh khoang trong: pipeline thong thuong co kiem tra chat luong va log van hanh, nhung thieu evidence doc lap de kiem chung lai trang thai du lieu sau khi xu ly.
3. Dinh nghia cau hoi va gia thuyet co the do luong.
4. Bien mo hinh Blockchain/hash chain thanh treatment.
5. Dung pipeline khong co ledger/verification lam control.
6. Do cac bien phu thuoc: detection status, first broken block, lineage traceability, duration, overhead.
7. Ghi ro cac bien khong kiem soat duoc va cac nguy co validity theo Chuong 10.
8. Gioi han ket luan: ket qua goi y hieu qua trong moi truong thu nghiem, khong khang dinh quan he nhan qua manh nhu true experiment.

---

# Noi dung bao cao da refactor

## CHUONG 1. DAT VAN DE NGHIEN CUU VA CO SO PHUONG PHAP BAN THUC NGHIEM

### 1.1. Research problem

Data Pipeline la chuoi xu ly du lieu tu nguon phat sinh den cac tang luu tru va phan tich. Du lieu co the di qua cac buoc ingestion, validation, transformation, aggregation va serving. Trong moi buoc, du lieu co nguy co bi thay doi do loi ky thuat, mapping sai schema, overwrite nham, thao tac co quyen cao hoac can thiep trai phep.

Van de nghien cuu cua de tai la:

> Lam the nao co the danh gia mot co che bao mat giup phat hien thay doi trai phep va truy vet vi tri sai lech trong Data Pipeline, trong khi moi truong pipeline thuc te khong cho phep kiem soat hoan toan tat ca bien anh huong?

Day la bai toan an toan thong tin vi no lien quan den ba muc tieu:

| Muc tieu bao mat | Bieu hien trong Data Pipeline |
|---|---|
| Data Integrity | Du lieu hien tai phai khop voi trang thai da duoc ghi nhan sau xu ly. |
| Tamper Evidence | Neu du lieu, metadata hoac bang chung bi sua, he thong phai phat hien duoc. |
| Traceability | Khi phat hien sai lech, he thong phai truy ve duoc pipeline run, stage va transformation lien quan. |

Blockchain khong phai muc tieu chinh cua de tai. Blockchain dang hash chain chi duoc su dung nhu **case study treatment** de danh gia xem mot co che tamper-evident co cai thien kha nang phat hien va truy vet trong pipeline hay khong.

### 1.2. Research gap

Nhieu Data Pipeline da co cac co che Data Quality nhu schema validation, type casting, mandatory field check, deduplication va kiem tra quan he nghiep vu:

$$
\text{amount} = \text{quantity} \times \text{unit\_price}
$$

Tuy nhien, cac co che nay thuong chi xac nhan du lieu dung tai thoi diem xu ly. Sau khi pipeline hoan tat, du lieu van co the bi sua, xoa, chen them hoac thay doi metadata. Neu he thong chi luu trang thai hien tai va log van hanh thong thuong, qua trinh audit kho xac dinh du lieu hien tai co con khop voi trang thai da duoc pipeline tao ra hay khong.

Khoang trong nghien cuu nam o cho:

| Khoang trong | He qua |
|---|---|
| Thieu bang chung toan ven doc lap voi du lieu nghiep vu | Kho phat hien thay doi sau xu ly. |
| Log van hanh khong du rang buoc bang hash | Metadata co the bi sua ma khong de lai dau vet ro rang. |
| Lineage va integrity thuong tach roi | Biet co loi nhung kho truy ve stage/transformation gay anh huong. |
| Benchmark bao mat chua gan voi thiet ke ban thuc nghiem | Kho danh gia trade-off giua detection va overhead. |

De tai lap khoang trong nay bang cach thiet ke mot nghien cuu ban thuc nghiem so sanh pipeline control voi pipeline treatment co hash-linked ledger, verification engine va lineage events.

### 1.3. Research questions

De tai tap trung vao cac cau hoi nghien cuu sau:

| Ma | Cau hoi nghien cuu |
|---|---|
| RQ1 | Treatment hash-linked ledger co giup phat hien thay doi trai phep trong du lieu, block payload va chain link cua Data Pipeline khong? |
| RQ2 | Treatment co giup xac dinh first broken block, pipeline stage va lineage event lien quan khi xay ra sai lech khong? |
| RQ3 | Chi phi thoi gian cua treatment so voi control pipeline la bao nhieu khi kich thuoc du lieu thay doi? |
| RQ4 | Nhung bien nao trong moi truong Databricks/Data Pipeline khong the kiem soat hoan toan va chung anh huong nhu the nao den gia tri noi tai cua ket qua? |

### 1.4. Research hypotheses

Gia thuyet duoc viet theo huong co the do luong trong thuc nghiem:

| Ma | Gia thuyet |
|---|---|
| H1 | Pipeline co hash-linked ledger va verification engine phat hien duoc cac tamper scenarios da dinh nghia, trong khi control pipeline khong co co che doc lap de phat hien sau xu ly. |
| H2 | Khi phat hien sai lech, treatment xac dinh duoc first broken block va lien ket duoc voi lineage event tuong ung. |
| H3 | Treatment lam tang thoi gian xu ly so voi control pipeline; overhead tang khi record count tang. |
| H4 | Do moi truong thuc nghiem khong kiem soat hoan toan compute state, cold start va dac thu Databricks workspace, ket qua chi cho phep ket luan ban thuc nghiem, khong phai ket luan nhan qua manh nhu true experiment. |

### 1.5. Justification for Quasi-experimental Research

Theo Chuong 10, quasi-experiment duoc su dung khi gia thuyet co the kiem dinh, nhung mot hoac mot so bien doc lap khong the kiem soat hoan toan do quy mo, moi truong van hanh, chi phi, dao duc hoac gioi han mau.

De tai nay khong phu hop voi true experiment vi:

| Driver theo Chuong 10 | Bieu hien trong de tai | Cach giam thieu |
|---|---|---|
| Cyber environment diversity | Databricks workspace, Delta Table, runtime, cluster state va cach scheduling tao thanh moi truong "snowflake" | Mo ta ro moi truong, dung seed co dinh, luu notebook va repository. |
| Users/background noise | Thao tac notebook, dashboard export, reset baseline va tamper confirmation phu thuoc quy trinh nguoi van hanh | Dinh nghia procedure co thu tu, widget `CONFIRM_TAMPER = YES`, ghi lineage/metrics. |
| Operational environment | Pipeline chay tren nen tang cloud-managed, khong kiem soat hoan toan cold start, resource allocation va I/O latency | Tach warm-up, lap lai benchmark, luu duration va is_warmup. |
| Population limitation | Khong co nhieu to chuc/cluster/dataset thuc te de randomize | Gioi han ket luan vao artifact va dataset thu nghiem. |
| Scale limitation | Dataset lon lam hashing ton chi phi; MVP khong the mo phong moi quy mo san xuat | Do nhieu record count, de xuat Merkle Tree va partition hash. |

Vi vay, thiet ke nghien cuu phu hop la **quasi-experimental pre-test/post-test with non-equivalent control**, trong do:

- Control la Data Pipeline chay khong co ledger/verification.
- Treatment la Data Pipeline cung logic xu ly nhung bo sung hash, ledger, lineage va verification.
- Pre-test la baseline run va trang thai `NONE`.
- Post-test la cac tamper scenarios va verification sau khi treatment duoc ap dung.
- Do khong the randomize hoan toan compute state, run order va nen tang Databricks, ket qua phai kem theo danh sach uncontrolled variables va validity threats.

### 1.6. Treatment and control setup

| Thanh phan | Control setup | Treatment setup |
|---|---|---|
| Pipeline logic | Source -> Bronze -> Silver -> Gold | Source -> Bronze -> Silver -> Gold |
| Data generation | Dataset giao dich gia lap, seed co dinh | Cung dataset va seed |
| Data quality | Validation, deduplication, normalization, aggregation | Giu nguyen |
| Evidence | Khong tao ledger hash chain | Tao `blockchain_ledger` cho moi stage |
| Lineage | Co the co log xu ly co ban | Ghi `lineage_events` co input/output hash va record count |
| Verification | Khong co co che doc lap sau xu ly | Kiem tra record count, batch hash, schema hash, block hash, previous hash |
| Tamper detection | Phu thuoc quan sat/kiem tra thu cong | Tra ve trang thai `VALID`, `DATA_TAMPERED`, `RECORD_COUNT_MISMATCH`, `BLOCK_TAMPERED`, `CHAIN_BROKEN` |
| Benchmark | `baseline_duration_ms` | `secured_duration_ms`, `verification_duration_ms`, `overhead_percent` |

Treatment khong duoc hieu la "Blockchain la muc tieu". Treatment chi la can thiep ky thuat de kiem tra gia thuyet ve kha nang phat hien va truy vet trong pipeline.

### 1.7. Independent variables

| Bien doc lap | Gia tri/Cap do | Vai tro |
|---|---|---|
| Security mechanism | Control: khong ledger; Treatment: hash-linked ledger + verification | Bien can thiep chinh. |
| Tamper scenario | `NONE`, modify amount, delete row, insert row, modify ledger hash, modify transformation, modify previous hash | Kiem tra kha nang phat hien cac dang sai lech. |
| Pipeline stage | SOURCE, BRONZE, SILVER, GOLD | Xac dinh diem sinh evidence va diem phat hien loi. |
| Record count | 1.000, 5.000, 10.000, 50.000 | Danh gia overhead theo kich thuoc du lieu. |
| Run condition | Warm-up vs measured run | Giam anh huong cold start khi phan tich benchmark. |

### 1.8. Dependent variables

| Bien phu thuoc | Y nghia |
|---|---|
| Verification status | Ket qua phat hien sai lech: `VALID` hoac cac trang thai loi. |
| Detection correctness | Trang thai thuc te co khop trang thai ky vong cua tamper scenario khong. |
| First broken block | Block dau tien vi pham record count, batch hash, block hash hoac chain link. |
| Traceability result | Kha nang truy ve `pipeline_run_id`, stage, target table va lineage event. |
| Baseline duration | Thoi gian control pipeline. |
| Secured duration | Thoi gian treatment pipeline co hashing va ledger. |
| Verification duration | Thoi gian kiem chung sau xu ly. |
| Security overhead | Ty le tang thoi gian khi ap dung treatment. |

### 1.9. Measurement metrics

| Metric | Cong thuc/Cach do | Gan voi RQ |
|---|---|---|
| Detection rate | So tamper scenarios duoc phat hien / tong so tamper scenarios | RQ1 |
| Detection correctness | So ket qua dung trang thai ky vong / tong so lan kiem chung | RQ1 |
| First broken block accuracy | So lan xac dinh dung block dau tien bi loi / tong so lan co loi | RQ2 |
| Traceability completeness | Du cac truong `pipeline_run_id`, stage, target table, transformation, lineage status | RQ2 |
| Baseline duration | `baseline_duration_ms` | RQ3 |
| Secured duration | `secured_duration_ms` | RQ3 |
| Verification duration | `verification_duration_ms` | RQ3 |
| Overhead | `(secured_duration_ms - baseline_duration_ms) / baseline_duration_ms * 100` | RQ3 |

Cong thuc overhead:

$$
\text{Overhead}(\%) =
\frac{\text{secured\_duration\_ms} - \text{baseline\_duration\_ms}}
{\text{baseline\_duration\_ms}}
\times 100
$$

### 1.10. Experimental procedure

Quy trinh thuc nghiem gom cac buoc:

1. Thiet lap moi truong Databricks, Delta Table va repository source control.
2. Sinh dataset giao dich gia lap bang seed co dinh de dam bao tinh tai lap.
3. Chay control pipeline Source -> Bronze -> Silver -> Gold va ghi `baseline_duration_ms`.
4. Chay treatment pipeline cung logic xu ly, bo sung canonicalization, hashing, ledger va lineage.
5. Ghi bốn block cho moi pipeline run: SOURCE, BRONZE, SILVER, GOLD.
6. Chay verification voi scenario `NONE` de xac nhan trang thai sach.
7. Ap dung tung tamper scenario co kiem soat.
8. Chay verification sau moi tamper scenario.
9. Ghi ket qua vao `verification_results` va benchmark vao `experiment_metrics`.
10. Doi chieu ket qua thuc te voi trang thai ky vong.
11. Phan tich overhead theo record count va tach warm-up ra khoi lan do chinh.
12. Ghi nhan uncontrolled variables, bias va validity threats.

Thu tu notebook:

```text
00_setup_environment.py
01_generate_source_data.py
02_bronze_ingestion.py
03_silver_transformation.py
04_gold_aggregation.py
05_verify_integrity.py
06_run_tamper_scenarios.py
07_experiment_and_metrics.py
```

### 1.11. Uncontrolled variables

Day la cac bien khong kiem soat hoan toan, lam cho de tai mang ban chat quasi-experimental:

| Bien khong kiem soat | Anh huong co the co | Cach ghi nhan/giam thieu |
|---|---|---|
| Databricks cold start | Lam tang latency bat thuong | Dung warm-up run, cot `is_warmup`. |
| Cluster resource allocation | Anh huong duration va overhead | Ghi moi truong chay, lap lai benchmark. |
| Delta Table I/O state | Cache, compaction, storage latency lam sai khac thoi gian | Do nhieu lan, khong ket luan qua muc tu mot lan do. |
| Notebook execution order | Chay sai thu tu co the lam sai baseline/tamper state | Dinh nghia procedure va reset baseline. |
| Dataset synthetic | Khong dai dien day du du lieu san xuat | Gioi han ket luan vao dataset thu nghiem. |
| Admin privilege/trust boundary | Admin co the sua ca data va ledger | Neu ro ledger cung workspace chi dat tamper-evident noi bo. |
| Dashboard export time | Dashboard co the chi phan anh mot thoi diem | Ghi timestamp export va truy van bang goc khi can so lieu chinh xac. |

### 1.12. Bias and validity threats

| Loai threat | Mo ta | Tac dong den nghien cuu | Giam thieu |
|---|---|---|---|
| Internal validity | Compute state, cold start va cache co the anh huong duration | Kho quy toan bo overhead cho treatment | Tach warm-up, lap lai benchmark, ghi ro run condition. |
| Construct validity | "Blockchain" trong MVP chi la hash chain, khong co consensus/smart contract | Neu goi la Blockchain day du se gay sai lech khái niệm | Dinh nghia ro la hash-linked ledger tamper-evident. |
| External validity | Dataset gia lap va mot Databricks workspace khong dai dien moi pipeline | Ket qua kho tong quat hoa sang moi he thong san xuat | Neu pham vi ap dung va future work mo rong moi truong. |
| Conclusion validity | So lan do va so moi truong con han che | Ket luan thong ke yeu | Khong khang dinh nhan qua manh; bao cao nhu bang chung ban thuc nghiem. |
| Selection bias | Khong randomize nhieu cluster, dataset, user population | Treatment/control co the bi anh huong boi thu tu chay | Dung cung dataset, cung logic pipeline, seed co dinh. |
| Instrumentation threat | Cach tinh batch hash, schema hash va duration co the anh huong ket qua | Loi instrument co the bi nham la loi he thong | Viet unit test va mo ta cong thuc hashing. |

### 1.13. Methodological limitations

Gioi han phuong phap cua de tai:

1. Khong co random assignment hoan toan giua treatment va control.
2. Chi kiem tra tren mot loai pipeline va dataset giao dich gia lap.
3. Tamper scenarios la cac kich ban duoc dinh nghia truoc, chua bao phu tat ca hanh vi insider hoac attacker thuc.
4. Benchmark bi anh huong boi nen tang cloud-managed va cold start.
5. Ledger nam trong cung Databricks workspace voi du lieu, nen chua tach hoan toan trust boundary.
6. Ket qua cho phep noi treatment co lien quan den viec cai thien detection/traceability trong dieu kien thu nghiem, nhung khong du de khang dinh nhan qua manh nhu true experiment.

### 1.14. Future work to improve the quasi-experimental design

| Huong cai thien | Tac dung doi voi quasi-experimental design |
|---|---|
| Chay tren nhieu workspace/cluster khac nhau | Tang external validity va giam phu thuoc snowflake environment. |
| Randomize thu tu control/treatment runs | Giam selection/order bias. |
| Tang so lan lap benchmark | Tang conclusion validity. |
| Dung dataset thuc hoac nhieu mien du lieu | Tang kha nang tong quat hoa. |
| Tach ledger sang he thong doc lap | Giam confounding do cung trust boundary. |
| Ky so block hoac checkpoint hash len blockchain cong khai/private chain | Tang muc bao dam tamper-evident. |
| Dung Merkle Tree/partition hash | Giam overhead va kiem tra kha nang scale. |
| Bo sung red-team/insider tamper exercise | Tien gan hon voi hanh vi tan cong thuc. |

---

## CHUONG 2. NEN TANG KY THUAT PHUC VU THIET KE BAN THUC NGHIEM

### 2.1. Tong quan Data Pipeline trong bai toan an toan thong tin

Data Pipeline la tap hop cac buoc xu ly du lieu theo luong, trong do du lieu duoc thu thap tu nguon, kiem tra, bien doi, chuan hoa va luu tru tai cac tang phuc vu phan tich hoac van hanh. Pipeline co the chay batch, streaming hoac kien truc lai tuy yeu cau latency, throughput va consistency.

Kien truc pipeline trong de tai theo Medallion Architecture:

```text
source_transactions
        |
        v
bronze_transactions
        |
        v
silver_transactions
        |
        v
gold_daily_summary
```

| Tang | Vai tro |
|---|---|
| Source | Luu du lieu giao dich gia lap. |
| Bronze | Bo sung `pipeline_run_id`, `ingestion_time`, `source_table`. |
| Silver | Deduplicate, validate, normalize kieu du lieu va tinh lai `amount`. |
| Gold | Tong hop theo `transaction_date` va `product`. |

Trong thiet ke ban thuc nghiem, pipeline nay la doi tuong quan sat. Control va treatment dung cung logic Source -> Bronze -> Silver -> Gold de giam sai khac khong can thiet.

### 2.2. Nguy co mat toan ven du lieu trong pipeline

| Vi tri | Nguy co | Tac dong den nghien cuu |
|---|---|---|
| Truyen du lieu vao pipeline | Loi mang, loi dinh dang, mapping sai schema, ghi de file | Can co baseline evidence o Source/Bronze. |
| Xu ly ETL/ELT | Loi join, type casting, null handling, deduplication, aggregation | Can ghi input/output hash va record count cua transformation. |
| Luu tru sau xu ly | UPDATE, DELETE, INSERT, overwrite nham, thao tac admin | Can verification sau khi pipeline hoan tat. |
| Metadata/audit log | Sua log, sua batch hash, sua previous hash | Can block hash va chain link de phat hien metadata tampering. |

### 2.3. Co che hash va canonicalization

Hàm băm mật mã chuyển dữ liệu đầu vào thành digest cố định. De tai dung SHA-256 de tao row hash, batch hash, schema hash va block hash.

Truoc khi hash, du lieu can canonicalize de cung mot gia tri logic tao cung bieu dien:

| Kieu du lieu | Quy tac chuan hoa |
|---|---|
| Null | Chuyen thanh token co dinh. |
| Decimal | Dung scale co dinh. |
| Timestamp | Dung format thong nhat va timezone xac dinh. |
| String | Escape ky tu phan cach va chuan hoa bieu dien. |
| Record | Sap xep cot theo thu tu co dinh. |
| Batch | Sap xep row hash hoac sort key on dinh truoc khi tao batch hash. |

Dieu kien verification:

$$
\mathcal{V}(D_t, E_t) =
\begin{cases}
\text{VALID}, &
\left|D_t\right| = E_{\text{count}}
\land H(D_t) = E_{\text{hash}}
\land S(D_t) = E_{\text{schema}} \\
\text{INVALID}, & \text{otherwise}
\end{cases}
$$

### 2.4. Lineage nhu bien do traceability

Data Lineage mo ta nguon goc, dong di chuyen va lich su transformation cua du lieu. Trong de tai, lineage khong chi la tinh nang ky thuat ma la bien do cho RQ2.

Mot lineage event toi thieu:

```text
pipeline_run_id
source_stage
target_stage
source_table
target_table
transformation_name
input_record_count
output_record_count
input_batch_hash
output_batch_hash
started_at
finished_at
status
error_message
```

Khi verification fail, traceability duoc danh gia theo chuoi:

```text
verification_results
    -> first broken block
    -> pipeline_run_id + stage
    -> lineage_events
    -> source/target table + transformation context
```

### 2.5. Hash-linked ledger la treatment, khong phai muc tieu nghien cuu

Blockchain trong de tai duoc gioi han thanh ledger dang chuoi block lien ket bang hash. Moi block chua payload, hash cua block truoc va hash cua block hien tai:

$$
H_n = \text{SHA256}(\text{Payload}_n \parallel H_{n-1})
$$

Payload block:

$$
\text{Payload}_n =
\text{Canonicalize}(\text{stage\_metadata}, \text{record\_count},
\text{batch\_hash}, \text{schema\_hash}, \text{transformation})
$$

Block hash:

$$
\text{BlockHash}_n =
\text{SHA256}(\text{Payload}_n \parallel \text{PreviousHash}_n)
$$

Genesis block dung previous hash co dinh:

```text
0000000000000000000000000000000000000000000000000000000000000000
```

MVP khong trien khai consensus, smart contract hay mang blockchain phi tap trung. Vi vay, construct dung trong nghien cuu la **hash-linked tamper-evident ledger**.

### 2.6. Trang thai verification

| Dieu kien sai lech | Trang thai |
|---|---|
| Khong co sai lech | `VALID` |
| `actual_batch_hash != expected_batch_hash` | `DATA_TAMPERED` |
| `actual_record_count != expected_record_count` | `RECORD_COUNT_MISMATCH` |
| `recalculated_block_hash != stored_block_hash` | `BLOCK_TAMPERED` |
| `previous_hash != previous.block_hash` | `CHAIN_BROKEN` |

Verification engine kiem tra theo thu tu block index de xac dinh first broken block.

---

## CHUONG 3. THIET KE VA TRIEN KHAI THUC NGHIEM BAN THUC NGHIEM

### 3.1. Moi truong va artifact thuc nghiem

| Thanh phan | Cong nghe |
|---|---|
| Nen tang | Databricks Free Edition |
| Ngon ngu | Python, PySpark, SQL |
| Luu tru | Delta Table |
| Hash | SHA-256 |
| Pipeline | Source -> Bronze -> Silver -> Gold |
| Ledger | `blockchain_ledger` |
| Lineage | `lineage_events` |
| Verification output | `verification_results` |
| Benchmark output | `experiment_metrics` |
| Dashboard | Databricks SQL dashboard |
| Source Control | GitHub repository: `https://github.com/sonnntech/kma_hk2_chuyen_de_co_so_khoa_hoc` |

Repository dong vai tro artifact ky thuat giup kiem tra kha nang tai lap ket qua va doi chieu giua thiet ke nghien cuu voi trien khai.

### 3.2. Module trien khai

| Module | Chuc nang |
|---|---|
| `canonicalization.py` | Chuan hoa null, decimal, timestamp, string va record truoc khi hash. |
| `hashing.py` | Tinh row hash, schema hash va batch hash. |
| `models.py` | Dinh nghia `LedgerBlock` va payload block. |
| `ledger.py` | Tao block, tinh block hash, ghi va doc ledger. |
| `pipeline.py` | Xu ly Source -> Bronze -> Silver -> Gold. |
| `lineage.py` | Ghi lineage event SUCCESS/FAILED. |
| `verification.py` | Kiem tra record count, data hash, block hash va chain link. |
| `tamper.py` | Cai dat tamper scenarios va reset baseline. |
| `metrics.py` | Tinh benchmark metrics va overhead. |

### 3.3. Evidence points trong treatment pipeline

Moi stage sinh batch hash tu du lieu da canonicalize:

| Stage | Sort key kiem chung | Muc tieu evidence |
|---|---|---|
| SOURCE | `transaction_id` | Ghi nhan snapshot du lieu dau vao. |
| BRONZE | `transaction_id` | Ghi nhan du lieu sau ingestion metadata. |
| SILVER | `transaction_id` | Ghi nhan du lieu sau validation va normalization. |
| GOLD | `transaction_date`, `product` | Ghi nhan du lieu tong hop. |

Moi pipeline run tao bon block:

```text
SOURCE -> BRONZE -> SILVER -> GOLD
```

Block luu stage metadata, target table, record count, batch hash, schema hash, transformation, previous hash, block hash va created time.

### 3.4. Tamper scenarios

| Kich ban | Vector tan cong | Trang thai ky vong | Bien phu thuoc duoc quan sat |
|---|---|---|---|
| `NONE` | Khong sua du lieu | `VALID` | False positive rate |
| `MODIFY_TRANSACTION_AMOUNT` | Sua gia tri giao dich | `DATA_TAMPERED` | Detection correctness |
| `DELETE_TRANSACTION` | Xoa mot dong du lieu | `RECORD_COUNT_MISMATCH` | Detection correctness |
| `INSERT_FAKE_TRANSACTION` | Chen dong gia | `RECORD_COUNT_MISMATCH` | Detection correctness |
| `MODIFY_LEDGER_BATCH_HASH` | Sua batch hash trong ledger | `DATA_TAMPERED` hoac block-related failure tuy thu tu kiem tra | Detection correctness |
| `MODIFY_LEDGER_TRANSFORMATION` | Sua metadata transformation | `BLOCK_TAMPERED` | Detection correctness |
| `MODIFY_LEDGER_PREVIOUS_HASH` | Sua lien ket block | `CHAIN_BROKEN` | Detection correctness |
| `RESET_BASELINE` | Tao lai run sach | `VALID` | Recovery/reproducibility |

Notebook tamper yeu cau widget:

```text
CONFIRM_TAMPER = YES
```

Rang buoc nay giup giam bias do thao tac nham khi chay thuc nghiem.

### 3.5. Benchmark design

Benchmark so sanh control va treatment:

| Chi so | Y nghia |
|---|---|
| `baseline_duration_ms` | Thoi gian chay pipeline khong co ledger/verification. |
| `secured_duration_ms` | Thoi gian chay pipeline co hashing va ledger. |
| `verification_duration_ms` | Thoi gian kiem chung du lieu hien tai so voi ledger. |
| `overhead_percent` | Chi phi tang them khi bo sung co che bao mat. |
| `is_warmup` | Danh dau lan chay khoi dong de tach khoi phan tich chinh. |

Truy van lay so lieu chinh xac:

```sql
SELECT
    record_count,
    COUNT(*) AS measured_runs,
    AVG(baseline_duration_ms) AS avg_baseline_duration_ms,
    AVG(secured_duration_ms) AS avg_secured_duration_ms,
    AVG(verification_duration_ms) AS avg_verification_duration_ms,
    AVG(overhead_percent) AS avg_overhead_percent,
    percentile_approx(overhead_percent, 0.5) AS median_overhead_percent
FROM experiment_metrics
WHERE is_warmup = false
GROUP BY record_count
ORDER BY record_count;
```

### 3.6. Dashboard observations

Dashboard export tu Databricks tai thoi diem **2026-06-20 08:15 UTC** ghi nhan:

| KPI | Gia tri |
|---|---:|
| Tong so pipeline runs | 15 |
| Tong so ledger blocks | 60 |
| So block xac thuc thanh cong | 56 |
| So pipeline runs co ket qua verification tren dashboard | 14 |
| So runs phat hien loi trong dashboard hien tai | 0 |
| So runs khong phat hien loi trong dashboard hien tai | 14 |
| Ti le loi hien thi tren dashboard | 0,00% |

Ledger overview cho thay moi pipeline run sinh 4 block theo thu tu SOURCE, BRONZE, SILVER va GOLD. Voi run benchmark 50.000 records, SOURCE, BRONZE va SILVER ghi nhan 50.000 records; GOLD ghi nhan 1.825 records sau aggregation theo ngay va san pham.

Lineage mau:

| Luong xu ly | Input records | Output records | Status |
|---|---:|---:|---|
| SOURCE -> BRONZE | 10.000 | 10.000 | SUCCESS |
| BRONZE -> SILVER | 10.000 | 10.000 | SUCCESS |
| SILVER -> GOLD | 10.000 | 1.825 | SUCCESS |

Verification latency trong cac dong gan nhat dao dong tu 24.000 ms den 31.000 ms. Co mot diem latency lon bat thuong, phu hop voi uncontrolled variable ve cold start hoac compute wait. Vi vay, ket luan benchmark phai dua tren bang `experiment_metrics` va loai warm-up.

### 3.7. Phan tich ket qua theo cau hoi nghien cuu

#### 3.7.1. RQ1: Kha nang phat hien thay doi trai phep

Treatment phat hien bon nhom sai lech:

| Nhom sai lech | Co che phat hien |
|---|---|
| Sua noi dung du lieu | Batch hash hien tai khac batch hash da luu. |
| Xoa hoac chen du lieu | Record count hien tai khac record count da luu. |
| Sua metadata block | Recalculated block hash khac stored block hash. |
| Sua lien ket chuoi | `previous_hash` khong khop block hash cua block truoc. |

Control pipeline khong co ledger/verification doc lap, nen khong co co che tu dong de xac nhan du lieu sau xu ly con khop voi trang thai ban dau. Day la khac biet chinh giua control va treatment.

Dashboard hien tai o trang thai sach:

| Chi so phat hien | Gia tri |
|---|---:|
| Tong so verification runs hien thi | 14 |
| Runs co phat hien loi | 0 |
| Runs khong phat hien loi | 14 |
| First broken block | Khong co |
| Tamper event | Khong co |

Ket qua nay xac nhan scenario `NONE` sau reset/benchmark, khong thay the cho bang chung cua cac tamper scenarios. Cac tamper scenarios can duoc chay rieng de danh gia detection correctness.

#### 3.7.2. RQ2: Kha nang truy vet sai lech

Lineage events ghi nhan duong di SOURCE -> BRONZE -> SILVER -> GOLD theo `pipeline_run_id`. Khi verification fail, treatment dung first broken block de truy ve:

```text
pipeline_run_id
pipeline_stage
target_table
transformation_name
input/output record count
input/output batch hash
status
```

Vi vay, traceability khong chi la biet "co loi", ma la xac dinh loi nam o stage nao va transformation nao can duoc kiem tra.

#### 3.7.3. RQ3: Chi phi overhead

Quan sat dashboard cho thay Security Overhead tang theo kich thuoc du lieu. PDF export chi hien thi bieu do cot, khong hien thi duration chi tiet; bang sau chi la gia tri xap xi theo bieu do:

| Record count | Quan sat tu dashboard | Overhead xap xi |
|---:|---|---:|
| 1.000 | Overhead thap hon nhom 10.000 va 50.000 | khoang 160% |
| 5.000 | Overhead gan muc 1.000 | khoang 155-160% |
| 10.000 | Overhead tang so voi 1.000 va 5.000 | khoang 180% |
| 50.000 | Overhead cao nhat trong bieu do | khoang 220% |

Theo Chuong 10, can than trong ket luan vi duration chiu anh huong cua uncontrolled variables nhu cold start, cache va compute allocation.

#### 3.7.4. RQ4: Tac dong cua uncontrolled variables

Ket qua thuc nghiem co gia tri nhu bang chung ban thuc nghiem trong moi truong duoc mo ta, nhung chua du de tong quat hoa cho moi Data Pipeline san xuat. Cac uncontrolled variables phai duoc xem la mot phan cua ket qua, khong phai loi bi bo qua.

### 3.8. Data Governance Architecture duoi goc nhin methodology

| Mien Governance | Co che trong treatment | Vai tro trong nghien cuu |
|---|---|---|
| Data Quality | Schema validation, deduplication, type normalization, consistency check | Giu pipeline logic on dinh giua control/treatment. |
| Data Lineage | Source/target stage, transformation, record count, batch hash, execution time, status | Bien do traceability. |
| Data Integrity | SHA-256 batch hash, schema hash, record count verification, block hash | Bien do detection. |
| Data Auditing | Verification history, failure reason, first broken block, pipeline run ID | Bang chung thuc nghiem. |
| Monitoring | Dashboard KPI cho pipeline runs, ledger blocks, verification status, latency, overhead | Cong cu quan sat ket qua. |

---

## CHUONG 4. KET LUAN THEO PHUONG PHAP BAN THUC NGHIEM

### 4.1. Ket luan chinh

De tai da ap dung Quasi-experimental Research vao bai toan an toan thong tin trong Data Pipeline. Thay vi xem Blockchain la muc tieu, de tai xem hash-linked ledger la treatment de danh gia tac dong len detection, traceability va overhead.

Ket qua chinh:

1. Treatment tao duoc evidence tai cac stage SOURCE, BRONZE, SILVER, GOLD.
2. Verification engine co co che phat hien sai lech o data hash, record count, block payload va chain link.
3. Lineage events giup truy ve pipeline run, stage va transformation lien quan khi verification fail.
4. Security overhead tang theo record count, vi hashing va verification tao chi phi tinh toan bo sung.
5. Do moi truong Databricks, cold start, compute allocation va dataset synthetic khong duoc kiem soat hoan toan, ket luan phai duoc dat trong khung quasi-experimental.

### 4.2. Gioi han ket luan

De tai khong khang dinh rang treatment la giai phap toi uu cho moi Data Pipeline. De tai chi cho thay trong moi truong thuc nghiem duoc mo ta, treatment hash-linked ledger co the tao bang chung tamper-evident va ho tro truy vet sai lech, voi chi phi overhead can duoc do va quan ly.

MVP khong phai blockchain phi tap trung day du. Khong co consensus, smart contract, nhieu node doc lap hay threat model cua public blockchain. Ten goi chinh xac ve methodology la **quasi-experimental evaluation of a hash-linked tamper-evident ledger for Data Pipeline integrity and lineage**.

### 4.3. Huong phat trien

Huong phat trien nen tap trung vao viec cai thien thiet ke ban thuc nghiem:

| Huong phat trien | Gia tri phuong phap |
|---|---|
| Lap lai thuc nghiem tren nhieu Databricks workspace/cluster | Tang external validity. |
| Randomize thu tu chay control va treatment | Giam order bias. |
| Tang so lan do cho moi record count | Tang conclusion validity. |
| Bo sung dataset thuc va nhieu mien du lieu | Tang generalizability. |
| Externalize ledger hoac checkpoint hash sang he thong doc lap | Giam trust-boundary confounder. |
| Ky so block | Tang do tin cay cua evidence. |
| Merkle Tree hoac partition-level hash | Giam overhead voi du lieu lon. |
| Red-team/insider exercise | Danh gia gan hon voi hanh vi tan cong thuc. |

---

# Ghi chu: Moi phan phan anh Chuong 10 nhu the nao

| Phan | Lien he voi Chuong 10 |
|---|---|
| 1.1 Research problem | Dat de tai la bai toan cyber security co gia thuyet kiem dinh, khong phai mo ta giai phap Blockchain. |
| 1.2 Research gap | Chi ra khoang trong can do luong: thieu evidence tamper-evident va traceability sau xu ly. |
| 1.3 Research questions | Bien muc tieu thanh cau hoi co the quan sat bang experiment. |
| 1.4 Research hypotheses | Dinh nghia gia thuyet H1-H4 de kiem dinh bang control/treatment. |
| 1.5 Justification | Giai thich vi sao true experiment khong kha thi va vi sao quasi-experiment la lua chon dung. |
| 1.6 Treatment/control | The hien thiet ke so sanh non-equivalent control va treatment. |
| 1.7-1.9 Variables/metrics | Lam ro bien doc lap, bien phu thuoc va metric, dung yeu cau cot loi cua experiment. |
| 1.10 Procedure | Chuyen notebook sequence thanh quy trinh thuc nghiem co pre-test/post-test va tamper scenarios. |
| 1.11 Uncontrolled variables | Thuc hien yeu cau Chuong 10: kiem soat duoc thi kiem soat, khong kiem soat duoc thi document. |
| 1.12 Validity threats | Danh gia internal, external, construct, conclusion validity cua quasi-experiment. |
| 1.13 Limitations | Gioi han ket luan de tranh claim nhan qua qua manh. |
| 1.14 Future work | Neu cach tang control, replication va validity trong cac lan nghien cuu sau. |
| Chuong 2 | Giu noi dung ky thuat nhung dong khung thanh co so do luong treatment. |
| Chuong 3 | Trinh bay trien khai nhu experiment: setup, scenarios, metrics, observations. |
| Chuong 4 | Ket luan theo muc bang chung cua quasi-experiment, khong chuyen thanh Design Science hay Case Study. |
