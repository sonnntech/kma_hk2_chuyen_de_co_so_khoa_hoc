# Tên đề tài

**Nghiên cứu xây dựng mô hình Hash-linked Ledger dạng Blockchain nhằm
kiểm chứng tính toàn vẹn và truy vết dữ liệu trong hệ thống Data
Pipeline**

## I. Mục tiêu nghiên cứu của đề tài

### 1. Mục tiêu tổng quát

Đề tài tập trung nghiên cứu bài toán kiểm chứng tính toàn vẹn dữ liệu
(**Data Integrity**) và truy vết dữ liệu (**Data Lineage**) trong hệ
thống **Data Pipeline**. Trên cơ sở đó, đề tài đề xuất một mô hình
**Hash-linked Ledger** dạng Blockchain theo hướng **tamper-evident**, sử
dụng hàm băm **SHA-256**, liên kết block bằng `previous_hash` và ghi
nhận metadata xử lý theo từng pipeline run.

Mục tiêu của mô hình là tạo ra một lớp bằng chứng kỹ thuật giúp kiểm
chứng trạng thái dữ liệu sau khi pipeline hoàn tất, phát hiện các sai
lệch hoặc sửa đổi không hợp lệ, đồng thời hỗ trợ xác định stage,
transformation và pipeline run liên quan khi xảy ra sự cố.

Phạm vi nghiên cứu không hướng tới xây dựng một mạng Blockchain phi tập
trung hoàn chỉnh. Mô hình không triển khai **Consensus** hoặc **Smart
Contract**, mà tập trung khai thác đặc tính cốt lõi của chuỗi hash để
phục vụ kiểm chứng dữ liệu trong phạm vi Data Pipeline.

### 2. Mục tiêu cụ thể

| Nhóm mục tiêu | Nội dung |
|---|---|
| Tổng quan nền tảng | Phân tích kiến trúc Data Pipeline, vai trò của pipeline trong xử lý dữ liệu hiện đại và các yêu cầu Data Governance liên quan. |
| Phân tích rủi ro | Xác định các nguy cơ làm mất toàn vẹn dữ liệu trong quá trình ingestion, ETL/ELT, lưu trữ và truy cập dữ liệu. |
| Cơ chế kiểm chứng toàn vẹn | Nghiên cứu cách sử dụng hàm băm, chuẩn hóa dữ liệu, record count và schema hash để tạo bằng chứng kiểm chứng dữ liệu. |
| Cơ chế truy vết | Nghiên cứu Data Lineage theo pipeline run, transformation, input/output record count, batch hash và trạng thái xử lý. |
| Ledger dạng Blockchain | Phân tích cách tổ chức ledger dạng chuỗi block liên kết bằng hash để phát hiện sửa đổi dữ liệu và metadata kiểm chứng. |
| Mô hình thử nghiệm | Xây dựng pipeline Source -> Bronze -> Silver -> Gold, tích hợp ledger, cơ chế kiểm chứng, tamper scenarios, benchmark và dashboard. |
| Đánh giá | Đánh giá khả năng phát hiện sai lệch, khả năng truy vết và chi phí overhead khi bổ sung cơ chế kiểm chứng. |

### 3. Phương pháp nghiên cứu và hướng ứng dụng

Đề tài được thực hiện theo hướng nghiên cứu ứng dụng, kết hợp giữa phân
tích lý thuyết, thiết kế mô hình và xây dựng thử nghiệm kỹ thuật. Trước
hết, đề tài phân tích các rủi ro mất toàn vẹn dữ liệu trong Data
Pipeline, đặc biệt ở các giai đoạn ingestion, transformation, storage và
serving. Tiếp theo, đề tài đề xuất kiến trúc Hash-linked Ledger để ghi
nhận bằng chứng kiểm chứng gồm record count, schema hash, batch hash,
block hash và lineage metadata.

Trên cơ sở mô hình đề xuất, đề tài xây dựng prototype trên Databricks
với pipeline Source -> Bronze -> Silver -> Gold. Prototype được dùng
để kiểm thử các kịch bản sửa đổi dữ liệu có kiểm soát, đánh giá khả năng
phát hiện sai lệch, khả năng truy vết theo pipeline run và chi phí xử lý
bổ sung khi tích hợp cơ chế kiểm chứng.

## II. Đề cương chi tiết 3 chương

## CHƯƠNG 1

## TỔNG QUAN VỀ KIỂM CHỨNG TÍNH TOÀN VẸN VÀ TRUY VẾT DỮ LIỆU TRONG HỆ THỐNG DATA PIPELINE

### 1.1. Tổng quan về hệ thống Data Pipeline

#### 1.1.1. Khái niệm hệ thống Data Pipeline

Data Pipeline là tập hợp các bước xử lý dữ liệu được tổ chức theo luồng,
trong đó dữ liệu được thu thập từ nhiều nguồn, được kiểm tra, biến đổi,
chuẩn hóa và lưu trữ tại các tầng phục vụ phân tích hoặc vận hành.
Pipeline có thể chạy theo Batch, Streaming hoặc kiến trúc lai tùy thuộc
yêu cầu Latency, Throughput và tính nhất quán dữ liệu.

Trong hệ thống dữ liệu hiện đại, Data Pipeline đóng vai trò cầu nối giữa
hệ thống phát sinh dữ liệu và các nền tảng khai thác dữ liệu như Data
Lake, Data Warehouse, Lakehouse, BI Dashboard hoặc hệ thống Machine
Learning. Độ tin cậy của pipeline ảnh hưởng trực tiếp đến độ tin cậy của
báo cáo, mô hình phân tích và quyết định nghiệp vụ.

#### 1.1.2. Kiến trúc tổng thể của hệ thống Data Pipeline

Một kiến trúc Data Pipeline điển hình gồm các tầng sau:

| Thành phần              | Vai trò                                                                                      |
|:------------------------|:---------------------------------------------------------------------------------------------|
| Data Source             | Nơi phát sinh dữ liệu gốc, bao gồm database, file, API, event stream hoặc log hệ thống.      |
| Ingestion Layer         | Thu thập dữ liệu từ nguồn, ghi nhận metadata đầu vào và chuyển dữ liệu vào vùng xử lý.       |
| Processing Layer        | Thực hiện ETL/ELT, validation, deduplication, enrichment, aggregation và chuẩn hóa dữ liệu.  |
| Storage Layer           | Lưu trữ dữ liệu theo các mức raw, cleaned, curated hoặc analytical.                          |
| Serving Layer           | Cung cấp dữ liệu cho reporting, dashboard, auditing, analytics hoặc downstream applications. |
| Monitoring & Governance | Theo dõi chất lượng dữ liệu, lineage, quyền truy cập, audit log và trạng thái vận hành.      |

Kiến trúc **Medallion Architecture** phân tách dữ liệu theo các tầng
Bronze, Silver và Gold. Bronze lưu dữ liệu gần nguồn, Silver lưu dữ liệu
đã kiểm tra và chuẩn hóa, Gold lưu dữ liệu tổng hợp phục vụ phân tích.

#### 1.1.3. Vai trò của Data Pipeline trong đảm bảo chất lượng dữ liệu

Data Pipeline thực thi các quy tắc **Data Quality** như schema
validation, type casting, mandatory field validation, deduplication và
kiểm tra tính nhất quán toán học. Ví dụ, dữ liệu giao dịch cần bảo đảm
quan hệ:

$$\text{amount} = \text{quantity} \times \text{unit\_price}$$

Pipeline thường chỉ kiểm soát chất lượng tại thời điểm xử lý nếu không
có cơ chế kiểm chứng độc lập sau khi dữ liệu đã được ghi. Rủi ro còn lại
nằm ở các thao tác sửa, xóa, chèn hoặc thay đổi metadata sau xử lý. Bài
toán toàn vẹn dữ liệu yêu cầu thêm một lớp kiểm chứng để xác nhận trạng
thái dữ liệu hiện tại có khớp với trạng thái đã được ghi nhận trước đó
hay không.

### 1.2. Các nguy cơ mất toàn vẹn dữ liệu trong hệ thống Data Pipeline

#### 1.2.1. Nguy cơ thay đổi dữ liệu trong quá trình truyền dẫn

Dữ liệu có thể bị thay đổi khi truyền từ nguồn vào pipeline do lỗi mạng,
lỗi mã hóa, lỗi định dạng, ghi đè file, mapping sai schema hoặc can
thiệp trái phép. Rủi ro này làm dữ liệu đầu vào khác với dữ liệu phát
sinh ban đầu, dẫn đến toàn bộ các tầng xử lý sau đó kế thừa sai lệch.

Kiểm soát nguy cơ này yêu cầu một cơ chế xác thực chéo tại điểm tiếp
nhận bằng cách đối chiếu giá trị toàn vẹn gốc với các phân đoạn dữ liệu
sau khi truyền, đồng thời ghi nhận bằng chứng kiểm toán đủ độc lập để
phát hiện sai lệch trong quá trình vận chuyển dữ liệu.

#### 1.2.2. Nguy cơ thay đổi dữ liệu trong quá trình xử lý ETL

ETL/ELT có thể làm sai lệch dữ liệu do lỗi transformation, lỗi join, lỗi
type casting, xử lý null không nhất quán, deduplication sai khóa hoặc
aggregation sai logic nghiệp vụ. Sai lệch trong ETL có tính lan truyền
vì tầng dữ liệu sau phụ thuộc trực tiếp vào tầng dữ liệu trước.

Kiểm soát toàn vẹn trong ETL cần ghi nhận trạng thái dữ liệu trước và
sau mỗi transformation. Các chỉ số tối thiểu gồm record count, schema
hash, batch hash và mô tả transformation.

#### 1.2.3. Nguy cơ thay đổi dữ liệu trong quá trình lưu trữ dữ liệu

Dữ liệu đã lưu vẫn có thể bị thay đổi thông qua UPDATE, DELETE, INSERT,
overwrite nhầm hoặc thao tác của người dùng có quyền cao. Nếu hệ thống
chỉ lưu trạng thái hiện tại, quá trình kiểm toán không có cơ sở để xác
định dữ liệu có còn khớp với thời điểm pipeline hoàn tất hay không.

Một cơ chế audit đáng tin cậy cần tách bằng chứng kiểm chứng khỏi dữ
liệu nghiệp vụ. Khi dữ liệu bị sửa, hệ thống tính lại fingerprint và so
sánh với bằng chứng đã ghi.

#### 1.2.4. Nguy cơ từ truy cập trái phép vào hệ thống dữ liệu

Threat Model của hệ thống cần xét cả dữ liệu nghiệp vụ và metadata kiểm
chứng. Người tấn công hoặc insider threat có thể sửa dữ liệu, sửa log,
sửa batch hash hoặc phá liên kết giữa các bản ghi kiểm chứng. Nếu ledger
và dữ liệu nằm trong cùng một trust boundary, tài khoản quản trị cấp cao
vẫn có khả năng thay đổi cả hai.

Ràng buộc Zero Trust đặt ra yêu cầu: mọi trạng thái dữ liệu phải có bằng
chứng kiểm chứng độc lập, mọi block kiểm chứng phải tự xác thực được
payload, và mọi block sau phải ràng buộc với block trước thông qua hash.

### 1.3. Tổng quan về cơ chế kiểm chứng tính toàn vẹn dữ liệu

#### 1.3.1. Kiểm chứng tính toàn vẹn dữ liệu bằng hàm băm

Hàm băm mật mã chuyển dữ liệu đầu vào có độ dài bất kỳ thành chuỗi đầu
ra có độ dài cố định. SHA-256 tạo digest 256 bit, thường biểu diễn bằng
64 ký tự hexadecimal. Các thuộc tính quan trọng gồm deterministic
output, avalanche effect và khả năng chống tìm tiền ảnh trong phạm vi
ứng dụng kiểm chứng dữ liệu.

Trước khi băm, dữ liệu cần được canonicalize. Cùng một giá trị logic
phải tạo cùng chuỗi biểu diễn bất kể khác biệt về kiểu dữ liệu,
timezone, scale decimal hoặc thứ tự dictionary. Quy tắc canonicalization
thường bao gồm:

| Kiểu dữ liệu | Quy tắc chuẩn hóa                                                |
|:-------------|:-----------------------------------------------------------------|
| Null         | Chuyển thành token cố định.                                      |
| Decimal      | Dùng scale cố định.                                              |
| Timestamp    | Dùng format thống nhất và timezone xác định.                     |
| String       | Escape ký tự phân cách và chuẩn hóa biểu diễn.                   |
| Record       | Sắp xếp theo thứ tự cột cố định.                                 |
| Batch        | Sắp xếp row hash hoặc sort key ổn định trước khi tạo batch hash. |

#### 1.3.2. Kiểm chứng thay đổi dữ liệu trong hệ thống xử lý dữ liệu

Kiểm chứng dữ liệu là quá trình tính lại fingerprint của dữ liệu hiện
tại và so sánh với fingerprint đã lưu. Một cơ chế kiểm chứng đầy đủ cần
thỏa mãn đồng thời tập điều kiện:

$$\mathcal{V}(D_t, E_t) =
\begin{cases}
\text{VALID}, &
\left|D_t\right| = E_{\text{count}}
\land H(D_t) = E_{\text{hash}}
\land S(D_t) = E_{\text{schema}} \\
\text{INVALID}, & \text{otherwise}
\end{cases}$$

Record count phát hiện xóa hoặc chèn dòng. Batch hash phát hiện sửa nội
dung khi số dòng không đổi. Schema hash phát hiện thay đổi cấu trúc dữ
liệu.

#### 1.3.3. Vai trò của kiểm chứng dữ liệu trong hệ thống Data Pipeline

Verification cung cấp bằng chứng kỹ thuật cho trạng thái dữ liệu sau
pipeline. Hệ thống không chỉ tạo dữ liệu đầu ra, mà còn tạo được bằng
chứng để xác định dữ liệu đầu ra có còn khớp với trạng thái đã ghi nhận
hay không.

Các trạng thái kiểm chứng cần rõ ràng để phục vụ monitoring và incident
response:

| Trạng thái              | Ý nghĩa                                                 |
|:------------------------|:--------------------------------------------------------|
| `VALID`                 | Dữ liệu, record count, block hash và chain link hợp lệ. |
| `DATA_TAMPERED`         | Batch hash hiện tại khác batch hash đã lưu.             |
| `RECORD_COUNT_MISMATCH` | Số bản ghi hiện tại khác số bản ghi đã lưu.             |
| `BLOCK_TAMPERED`        | Payload block bị thay đổi hoặc block hash không khớp.   |
| `CHAIN_BROKEN`          | `previous_hash` không trỏ đúng block trước.             |

### 1.4. Tổng quan về cơ chế truy vết dữ liệu trong hệ thống Data Pipeline

#### 1.4.1. Khái niệm truy vết dữ liệu (Data Lineage)

Data Lineage mô tả nguồn gốc, dòng di chuyển và lịch sử transformation
của dữ liệu. Lineage trả lời các câu hỏi: dữ liệu đến từ đâu, đi qua
transformation nào, được ghi vào đâu, chạy trong lần thực thi pipeline
nào và trạng thái xử lý ra sao.

#### 1.4.2. Vai trò của truy vết dữ liệu trong quản lý dữ liệu

Trong quản trị dữ liệu, lineage là nền tảng cho auditability, impact
analysis, root cause analysis và regulatory compliance. Khi dữ liệu phân
tích sai, lineage giúp xác định upstream source, transformation liên
quan và downstream asset bị ảnh hưởng.

Một lineage event tối thiểu cần chứa:

``` text
pipeline_run_id source_stage target_stage source_table target_table
transformation_name input_record_count output_record_count
input_batch_hash output_batch_hash started_at finished_at status
error_message
```

#### 1.4.3. Ứng dụng truy vết dữ liệu trong phát hiện thay đổi dữ liệu

Lineage cung cấp ngữ cảnh để giải thích kết quả verification. Batch hash
xác định trạng thái dữ liệu bị sai lệch; lineage xác định
transformation, stage và tài sản dữ liệu liên quan. Kết hợp hai cơ chế
tạo thành chuỗi phân tích:

$$\text{VerificationFailure}
\rightarrow \text{FirstBrokenBlock}
\rightarrow \text{PipelineStage}
\rightarrow \text{LineageEvent}
\rightarrow \text{TransformationContext}$$

### 1.5. Tổng quan về công nghệ Blockchain trong kiểm chứng tính toàn vẹn dữ liệu

#### 1.5.1. Khái niệm công nghệ Blockchain

Blockchain là cấu trúc dữ liệu gồm các block được liên kết tuần tự bằng
hash. Mỗi block chứa payload, hash của block trước và hash của chính
block hiện tại. Quan hệ băm có thể biểu diễn:

$$H_n = \text{SHA256}(\text{Payload}_n \parallel H_{n-1})$$

Trong bài toán Data Pipeline, block không nhất thiết lưu toàn bộ dữ
liệu. Block có thể lưu fingerprint của dữ liệu, metadata transformation
và liên kết tới block trước.

Trong phạm vi đề tài, thuật ngữ Blockchain được sử dụng theo nghĩa là
một cấu trúc ledger gồm các block liên kết tuần tự bằng hàm băm. Vì vậy,
mô hình được xem là một **Hash-linked Ledger dạng Blockchain** phục vụ
kiểm chứng dữ liệu, thay vì một Blockchain phi tập trung đầy đủ như các
hệ thống công khai.

#### 1.5.2. Đặc tính bất biến dữ liệu của Blockchain

Tính bất biến của Blockchain không đến từ việc dữ liệu không thể bị sửa
ở tầng vật lý, mà từ khả năng phát hiện sửa đổi. Khi payload của block
thay đổi, `block_hash` tính lại sẽ khác giá trị đã lưu. Khi block trung
gian bị thay đổi, toàn bộ chuỗi sau đó mất liên kết hợp lệ.

Mức độ bất biến thực tế phụ thuộc trust boundary. Nếu ledger nằm trong
cùng môi trường quản trị với dữ liệu, mô hình đạt mức tamper-evident nội
bộ. Để tăng mức bảo đảm, hệ thống cần externalize ledger, ký số block
hoặc lưu checkpoint hash trên hạ tầng độc lập.

#### 1.5.3. Khả năng ứng dụng Blockchain trong kiểm chứng và truy vết dữ liệu

Blockchain phù hợp với Data Pipeline ở vai trò audit ledger: mỗi stage
sinh một bằng chứng kiểm chứng, các bằng chứng được liên kết tuần tự, cơ
chế xác thực toàn vẹn có thể phát hiện sai lệch trong dữ liệu, block
payload hoặc chain link.

Mô hình này hỗ trợ ba năng lực chính:

| Năng lực        | Cơ chế                                            |
|:----------------|:--------------------------------------------------|
| Data Integrity  | Batch hash, schema hash, record count.            |
| Tamper Evidence | Block hash và previous hash.                      |
| Traceability    | Pipeline run ID, stage metadata và lineage event. |

## CHƯƠNG 2

## PHÂN TÍCH CƠ CHẾ KIỂM CHỨNG TÍNH TOÀN VẸN VÀ TRUY VẾT DỮ LIỆU TRONG HỆ THỐNG DATA PIPELINE DỰA TRÊN CÔNG NGHỆ BLOCKCHAIN

### 2.1. Kiến trúc kiểm chứng tính toàn vẹn dữ liệu trong hệ thống Data Pipeline

#### 2.1.1. Kiểm chứng tính toàn vẹn dữ liệu tại nguồn dữ liệu

Điểm tiếp nhận dữ liệu cần tạo bằng chứng cho trạng thái ban đầu trước
khi dữ liệu bước vào transformation. Bằng chứng này gồm record count,
schema fingerprint và batch hash. Trạng thái tại nguồn trở thành mốc gốc
để đối chiếu các tầng xử lý sau.

Kiểm chứng tại nguồn cần xử lý ba ràng buộc:

| Ràng buộc        | Cách kiểm soát                               |
|:-----------------|:---------------------------------------------|
| Tính đầy đủ      | Đếm số bản ghi hoặc số event được ingest.    |
| Tính đúng schema | Lưu schema hash và validate trường bắt buộc. |
| Tính không đổi   | Sinh batch hash từ dữ liệu đã canonicalize.  |

#### 2.1.2. Kiểm chứng tính toàn vẹn dữ liệu trong quá trình xử lý ETL

Mỗi transformation trong ETL phải tạo bằng chứng trạng thái đầu ra. Với
pipeline nhiều tầng, bằng chứng ở tầng sau cần liên kết với bằng chứng ở
tầng trước để tạo một chuỗi xử lý có thể kiểm toán.

Quy trình kiểm soát:

$$D_{\text{in}}
\xrightarrow{\text{Validate}(schema, rules)}
D_{\text{valid}}
\xrightarrow{\text{Transform}}
D_{\text{out}}
\xrightarrow{\text{Hash} + \text{Metadata}}
E_{\text{stage}}
\xrightarrow{\text{Link}}
B_n$$

ETL integrity không chỉ kiểm tra dữ liệu cuối cùng. Cơ chế đúng phải xác
định được stage nào tạo ra trạng thái sai lệch đầu tiên.

#### 2.1.3. Kiểm chứng tính toàn vẹn dữ liệu trong quá trình lưu trữ dữ liệu

Lớp lưu trữ cần hỗ trợ kiểm chứng sau khi pipeline đã hoàn tất. Tại thời
điểm verification, hệ thống đọc dữ liệu hiện tại, tính lại fingerprint
và so sánh với ledger. Kết quả kiểm chứng được ghi thành lịch sử audit
để phân tích theo thời gian.

Mô hình trạng thái:

$$\text{StoredEvidence} \oplus \text{CurrentDataState}
\rightarrow \text{IntegrityVerification}
\rightarrow \text{VerificationResult}$$

### 2.2. Phân tích cơ chế truy vết dữ liệu trong hệ thống Data Pipeline

#### 2.2.1. Truy vết dữ liệu theo luồng xử lý dữ liệu

Lineage theo luồng xử lý ghi nhận quan hệ upstream/downstream giữa các
stage. Mỗi edge trong lineage graph biểu diễn một transformation:

$$\text{Stage}_A \xrightarrow{\text{transformation}} \text{Stage}_B$$

Thông tin bắt buộc gồm source, target, transformation name, thời điểm
chạy, trạng thái và pipeline run ID.

#### 2.2.2. Truy vết dữ liệu theo lịch sử biến đổi dữ liệu

Lịch sử biến đổi dữ liệu cần lưu cả metadata kỹ thuật và metadata nghiệp
vụ. Metadata kỹ thuật gồm record count, batch hash, schema hash,
execution time và status. Metadata nghiệp vụ gồm tên transformation, mô
tả logic xử lý và mục tiêu dữ liệu đầu ra.

Thiết kế lineage cần hỗ trợ hai truy vấn:

$$\text{ForwardLineage}(S) = \{T \mid S \leadsto T\}$$

$$\text{BackwardLineage}(O) = \{U \mid U \leadsto O\}$$

#### 2.2.3. Truy vết dữ liệu phục vụ kiểm chứng thay đổi dữ liệu

Khi verification trả về lỗi, lineage hỗ trợ khoanh vùng phạm vi:

| Kết quả verification    | Cách dùng lineage                                               |
|:------------------------|:----------------------------------------------------------------|
| `DATA_TAMPERED`         | Xác định stage và transformation tạo dữ liệu bị sai lệch.       |
| `RECORD_COUNT_MISMATCH` | So sánh input/output record count của transformation liên quan. |
| `BLOCK_TAMPERED`        | Kiểm tra metadata transformation bị sửa.                        |
| `CHAIN_BROKEN`          | Xác định vị trí đứt trong chuỗi stage.                          |

### 2.3. Phân tích cơ chế phát hiện sửa đổi dữ liệu bằng Blockchain

#### 2.3.1. Cơ chế liên kết khối dữ liệu bằng hàm băm

Mỗi block kiểm chứng chứa payload đại diện cho trạng thái một stage.
Công thức tổng quát:

$$\text{Payload}_n =
\text{Canonicalize}(\text{stage\_metadata}, \text{record\_count},
\text{batch\_hash}, \text{schema\_hash}, \text{transformation})$$

$$\text{BlockHash}_n =
\text{SHA256}(\text{Payload}_n \parallel \text{PreviousHash}_n)$$

$$\text{PreviousHash}_n = \text{BlockHash}_{n-1}$$

Genesis block sử dụng previous hash cố định:

$$\text{PreviousHash}_0 =
\texttt{0000000000000000000000000000000000000000000000000000000000000000}$$

#### 2.3.2. Cơ chế kiểm chứng dữ liệu bằng Blockchain

Verification engine kiểm tra bốn điều kiện:

| Điều kiện                              | Lỗi phát hiện          |
|:---------------------------------------|:-----------------------|
| Current record count khớp ledger       | Xóa hoặc chèn dữ liệu. |
| Current batch hash khớp ledger         | Sửa nội dung dữ liệu.  |
| Recalculated block hash khớp ledger    | Sửa metadata block.    |
| Current previous hash khớp block trước | Phá liên kết chuỗi.    |

Điều kiện được kiểm tra theo thứ tự block index để xác định first broken
block.

#### 2.3.3. Vai trò của Blockchain trong phát hiện sửa đổi không hợp lệ dữ liệu

Hash chain biến mỗi stage thành một điểm kiểm chứng có ràng buộc toán
học với stage trước đó. Người tấn công không thể sửa một block mà không
làm thay đổi block hash; sửa previous hash sẽ làm đứt chain link; sửa dữ
liệu sẽ làm batch hash hiện tại khác bằng chứng đã lưu.

### 2.4. Phân tích mô hình tích hợp Blockchain trong hệ thống Data Pipeline

#### 2.4.1. Mô hình tích hợp Blockchain tại tầng thu thập dữ liệu

Tầng thu thập tạo block đầu tiên cho dữ liệu vừa ingest. Block này đóng
vai trò baseline evidence. Mọi transformation sau đó phải liên kết tới
baseline này thông qua hash chain.

#### 2.4.2. Mô hình tích hợp Blockchain tại tầng xử lý dữ liệu

Tầng xử lý tạo block sau mỗi transformation chính. Thiết kế này giúp
verification xác định chính xác stage đầu tiên bị sai lệch thay vì chỉ
phát hiện sai lệch ở output cuối.

#### 2.4.3. Mô hình tích hợp Blockchain tại tầng lưu trữ dữ liệu

Tầng lưu trữ phân tích tạo block cho curated hoặc aggregated dataset.
Đây là lớp trực tiếp phục vụ dashboard và báo cáo, nên verification tại
tầng này bảo vệ tính đúng đắn của chỉ số phân tích.

### 2.5. Phân tích yêu cầu xây dựng mô hình kiểm chứng tính toàn vẹn và truy vết dữ liệu

#### 2.5.1. Yêu cầu về hiệu năng hệ thống

Cơ chế kiểm chứng tạo chi phí tính toán bổ sung. Benchmark cần đo tối
thiểu ba nhóm Duration:

| Chỉ số                | Ý nghĩa                                               |
|:----------------------|:------------------------------------------------------|
| Baseline Duration     | Thời gian chạy pipeline không có ledger/verification. |
| Secured Duration      | Thời gian chạy pipeline có hashing và ledger.         |
| Verification Duration | Thời gian kiểm chứng dữ liệu hiện tại so với ledger.  |
| overhead              | Phần chi phí tăng thêm khi bổ sung cơ chế bảo mật.    |

Công thức:

$$\text{overhead}(\%) =
\frac{\text{secured\_duration\_ms} - \text{baseline\_duration\_ms}}
{\text{baseline\_duration\_ms}}
\times 100$$

#### 2.5.2. Yêu cầu về khả năng mở rộng hệ thống

Batch hash phải deterministic nhưng không được phụ thuộc Spark partition
order. Với dữ liệu lớn, thiết kế nên dùng partition-level hash hoặc
Merkle Tree để giảm áp lực lên Driver. Mô hình MVP có thể dùng cách tính
đơn giản hơn nếu dataset nằm trong giới hạn thử nghiệm, nhưng tài liệu
cần nêu rõ giới hạn đó.

#### 2.5.3. Yêu cầu về khả năng kiểm chứng dữ liệu

Hệ thống cần trả lời được bảy câu hỏi kiểm chứng:

1.  Dữ liệu hiện tại có khớp batch hash đã lưu không?

2.  Record count hiện tại có khớp record count đã lưu không?

3.  Schema hiện tại có khớp schema hash đã lưu không?

4.  Payload block có bị sửa không?

5.  Chain link có bị đứt không?

6.  First broken block là block nào?

7.  Pipeline run nào và stage nào bị ảnh hưởng?

## CHƯƠNG 3

## XÂY DỰNG MÔ HÌNH ỨNG DỤNG BLOCKCHAIN KIỂM CHỨNG TÍNH TOÀN VẸN VÀ TRUY VẾT DỮ LIỆU TRONG HỆ THỐNG DATA PIPELINE

Các hình minh họa trong chương này được bố trí theo đúng trình tự thực nghiệm: môi trường triển khai, pipeline xử lý dữ liệu, ledger kiểm chứng, lineage, tamper scenarios, dashboard và benchmark. Khi hoàn thiện báo cáo, người viết thay dòng **[Chèn hình tại đây]** bằng ảnh chụp tương ứng từ Databricks.

### 3.1. Đề xuất kiến trúc tổng thể mô hình

#### 3.1.1. Kiến trúc hệ thống Data Pipeline thử nghiệm

Mô hình thử nghiệm được triển khai trên Databricks với Python, PySpark,
SQL và Delta Table. Dataset là dữ liệu giao dịch giả lập, sinh bằng seed
cố định để tái lập kết quả. Pipeline vật lý gồm bốn bảng:

``` text
source_transactions -> bronze_transactions -> silver_transactions -> gold_daily_summary
```

| Tầng   | Vai trò triển khai                                                  |
|:-------|:--------------------------------------------------------------------|
| Source | Lưu dữ liệu giao dịch giả lập.                                      |
| Bronze | Bổ sung `pipeline_run_id`, `ingestion_time`, `source_table`.        |
| Silver | Deduplicate, validate, normalize kiểu dữ liệu và tính lại `amount`. |
| Gold   | Tổng hợp theo `transaction_date` và `product`.                      |


**[Chèn hình tại đây]**

*Hình 3.1. Kiến trúc pipeline thử nghiệm Source → Bronze → Silver → Gold trên Databricks.*

> Gợi ý chụp: có thể chụp sơ đồ tự vẽ hoặc màn hình notebook thể hiện luồng xử lý giữa bốn tầng dữ liệu.

#### 3.1.2. Kiến trúc tích hợp Blockchain trong hệ thống

Mỗi pipeline run tạo bốn block trong `blockchain_ledger`:

``` text
SOURCE -> BRONZE -> SILVER -> GOLD
```

Block lưu stage metadata, target table, record count, batch hash, schema
hash, transformation, previous hash, block hash và created time. Block
SOURCE là genesis block với previous hash gồm 64 ký tự `0`; các block
sau trỏ tới block hash của stage trước.


**[Chèn hình tại đây]**

*Hình 3.2. Cơ chế liên kết các block trong `blockchain_ledger` bằng `previous_hash` và `block_hash`.*

> Gợi ý chụp: nên chụp bảng ledger hoặc sơ đồ thể hiện SOURCE → BRONZE → SILVER → GOLD với hash nối tiếp nhau.

#### 3.1.3. Thành phần kiểm chứng tính toàn vẹn dữ liệu

| Module                | Chức năng                                                            |
|:----------------------|:---------------------------------------------------------------------|
| `canonicalization.py` | Chuẩn hóa null, decimal, timestamp, string và record trước khi hash. |
| `hashing.py`          | Tính row hash, schema hash và batch hash.                            |
| `models.py`           | Định nghĩa `LedgerBlock` và payload block.                           |
| `ledger.py`           | Tạo block, tính block hash, ghi và đọc ledger.                       |
| `pipeline.py`         | Xử lý Source → Bronze → Silver → Gold.                            |
| `lineage.py`          | Ghi lineage event SUCCESS/FAILED.                                    |
| `verification.py`     | Kiểm tra record count, data hash, block hash và chain link.          |
| `tamper.py`           | Cài đặt tamper scenarios và reset baseline.                          |
| `metrics.py`          | Tính benchmark metrics và overhead.                                  |

### 3.2. Xây dựng cơ chế kiểm chứng tính toàn vẹn dữ liệu trong mô hình đề xuất

#### 3.2.1. Sinh giá trị băm dữ liệu tại các điểm xử lý

Mỗi stage sinh một batch hash từ dữ liệu đã canonicalize. Các cột được
xử lý theo thứ tự ổn định; batch hash được tính theo thứ tự dòng xác
định để loại bỏ phụ thuộc vào Spark partition order.

Các điểm sinh hash:

| Stage  | Sort key kiểm chứng           | Mục tiêu                                          |
|:-------|:------------------------------|:--------------------------------------------------|
| SOURCE | `transaction_id`              | Ghi nhận snapshot dữ liệu đầu vào.                |
| BRONZE | `transaction_id`              | Ghi nhận dữ liệu sau Ingestion metadata.          |
| SILVER | `transaction_id`              | Ghi nhận dữ liệu sau validation và normalization. |
| GOLD   | `transaction_date`, `product` | Ghi nhận dữ liệu tổng hợp.                        |

#### 3.2.2. Lưu trữ giá trị kiểm chứng trên Blockchain

Ledger lưu bằng chứng kiểm chứng trong bảng `blockchain_ledger`. Payload
block không bao gồm `block_hash`; `block_hash` được tính từ payload đã
canonicalize. Cấu trúc này cho phép phát hiện thay đổi trong payload.

``` text
block_hash = SHA256(canonicalized_block_payload)
```

#### 3.2.3. Kiểm tra phát hiện thay đổi dữ liệu

Notebook `05_verify_integrity.py` gọi verification engine để đọc block
theo `pipeline_run_id`, tính lại trạng thái dữ liệu hiện tại và ghi kết
quả vào `verification_results`.

Quy tắc phát hiện:

| Điều kiện sai lệch                             | Trạng thái              |
|:-----------------------------------------------|:------------------------|
| `actual_record_count != expected_record_count` | `RECORD_COUNT_MISMATCH` |
| `actual_batch_hash != expected_batch_hash`     | `DATA_TAMPERED`         |
| `recalculated_block_hash != stored_block_hash` | `BLOCK_TAMPERED`        |
| `previous_hash != previous.block_hash`         | `CHAIN_BROKEN`          |

### 3.3. Xây dựng cơ chế truy vết dữ liệu trong mô hình đề xuất

#### 3.3.1. Ghi nhận lịch sử biến đổi dữ liệu

Bảng `lineage_events` lưu lineage event cho từng transformation. Event
bao gồm pipeline run ID, source stage, target stage, source table,
target table, transformation name, input/output record count,
input/output batch hash, execution time, status và error message.

#### 3.3.2. Lưu trữ thông tin truy vết trên Blockchain

MVP tách hai loại thông tin:

| Thành phần          | Nội dung lưu                                                          |
|:--------------------|:----------------------------------------------------------------------|
| `blockchain_ledger` | Bằng chứng toàn vẹn, hash, record count, schema hash, block link.     |
| `lineage_events`    | Ngữ cảnh xử lý, transformation, source/target, thời gian, trạng thái. |

Ledger không thay thế lineage. Ledger cung cấp bằng chứng kiểm chứng,
trong khi lineage cung cấp bối cảnh để giải thích nguồn gốc và phạm vi
ảnh hưởng của sai lệch.

#### 3.3.3. Kiểm chứng lịch sử biến đổi dữ liệu

Lịch sử biến đổi được kiểm chứng thông qua quan hệ giữa output batch
hash của lineage và batch hash trong ledger. Khi output data bị sửa,
verification phát hiện batch hash sai lệch. Khi metadata transformation
trong block bị sửa, block hash không còn hợp lệ.

### 3.4. Xây dựng mô hình thử nghiệm hệ thống

#### 3.4.1. Môi trường triển khai thử nghiệm

| Thành phần          | Công nghệ                                                                          |
|:--------------------|:-----------------------------------------------------------------------------------|
| Nền tảng            | Databricks Free Edition                                                            |
| Ngôn ngữ            | Python, PySpark, SQL                                                               |
| Lưu trữ             | Delta Table                                                                        |
| Hash                | SHA-256                                                                            |
| Pipeline            | Source → Bronze → Silver → Gold                                                       |
| Ledger              | `blockchain_ledger`                                                                |
| Lineage             | `lineage_events`                                                                   |
| Verification output | `verification_results`                                                             |
| Benchmark output    | `experiment_metrics`                                                               |
| Dashboard           | Databricks SQL dashboard                                                           |
| Source Control      | GitHub repository: `https://github.com/sonnntech/kma_hk2_chuyen_de_co_so_khoa_hoc` |


**[Chèn hình tại đây]**

*Hình 3.3. Môi trường triển khai thực nghiệm trên Databricks.*

> Gợi ý chụp: chụp Workspace hoặc notebook đang attached compute; tránh để lộ token, URL riêng tư hoặc thông tin nhạy cảm.

Mã nguồn mô hình thử nghiệm, notebook Databricks, unit test, SQL
dashboard và tài liệu chạy lại được quản lý tại GitHub:

``` text
https://github.com/sonnntech/kma_hk2_chuyen_de_co_so_khoa_hoc
```

Repository này đóng vai trò artifact kỹ thuật của đề tài, hỗ trợ kiểm
tra khả năng tái lập kết quả thực nghiệm và đối chiếu giữa mô hình kiến
trúc với phần triển khai.

Thứ tự notebook:

``` text
00_setup_environment.py 01_generate_source_data.py
02_bronze_ingestion.py 03_silver_transformation.py
04_gold_aggregation.py 05_verify_integrity.py 06_run_tamper_scenarios.py
07_experiment_and_metrics.py
```


**[Chèn hình tại đây]**

*Hình 3.4. Danh sách notebook triển khai pipeline, kiểm chứng toàn vẹn, tamper scenarios và benchmark.*

> Gợi ý chụp: chụp thư mục notebook trong Databricks Workspace để chứng minh quy trình thực nghiệm có thứ tự.


**[Chèn hình tại đây]**

*Hình 3.5. Dữ liệu mẫu sau khi được xử lý qua các tầng Source, Bronze, Silver và Gold.*

> Gợi ý chụp: chạy SELECT LIMIT 10 trên các bảng `source_transactions`, `bronze_transactions`, `silver_transactions` và `gold_daily_summary`.

#### 3.4.2. Xây dựng kịch bản kiểm thử thay đổi dữ liệu

| Kịch bản                       | Vector tấn công             | Trạng thái kỳ vọng      |
|:-------------------------------|:----------------------------|:------------------------|
| `NONE`                         | Không sửa dữ liệu           | `VALID`                 |
| `MODIFY_TRANSACTION_AMOUNT`    | Sửa giá trị giao dịch       | `DATA_TAMPERED`         |
| `DELETE_TRANSACTION`           | Xóa một dòng dữ liệu        | `RECORD_COUNT_MISMATCH` |
| `INSERT_FAKE_TRANSACTION`      | Chèn dòng giả               | `RECORD_COUNT_MISMATCH` |
| `MODIFY_LEDGER_BATCH_HASH`     | Sửa batch hash trong ledger | `DATA_TAMPERED`         |
| `MODIFY_LEDGER_TRANSFORMATION` | Sửa metadata transformation | `BLOCK_TAMPERED`        |
| `MODIFY_LEDGER_PREVIOUS_HASH`  | Sửa liên kết block          | `CHAIN_BROKEN`          |
| `RESET_BASELINE`               | Tạo lại run sạch            | `VALID`                 |


**[Chèn hình tại đây]**

*Hình 3.6. Cấu hình và thực thi kịch bản tamper có kiểm soát trong notebook `06_run_tamper_scenarios.py`.*

> Gợi ý chụp: chụp widget chọn scenario và tham số `CONFIRM_TAMPER = YES`, nhưng không chụp thông tin nhạy cảm.

Notebook tamper yêu cầu widget `CONFIRM_TAMPER = YES` để tránh thao tác
phá dữ liệu ngoài ý muốn.


**[Chèn hình tại đây]**

*Hình 3.7. Kết quả kiểm chứng sau kịch bản sửa dữ liệu, trạng thái trả về `DATA_TAMPERED` hoặc `RECORD_COUNT_MISMATCH`.*

> Gợi ý chụp: nên chọn một kịch bản dễ hiểu như `MODIFY_TRANSACTION_AMOUNT`, `DELETE_TRANSACTION` hoặc `INSERT_FAKE_TRANSACTION`.

#### 3.4.3. Triển khai thử nghiệm mô hình đề xuất

Dashboard export từ Databricks tại thời điểm **2026-06-20 08:15 UTC**
ghi nhận kết quả sau:

| KPI                                                     | Giá trị |
|:--------------------------------------------------------|--------:|
| Tổng số pipeline runs                                   |      15 |
| Tổng số ledger blocks                                   |      60 |
| Số block xác thực thành công                            |      56 |
| Số pipeline runs có kết quả verification trên dashboard |      14 |
| Số runs phát hiện lỗi trong dashboard hiện tại          |       0 |
| Số runs không phát hiện lỗi trong dashboard hiện tại    |      14 |
| Tỉ lệ lỗi hiển thị trên dashboard                       |   0,00% |


**[Chèn hình tại đây]**

*Hình 3.8. Dashboard tổng hợp số pipeline runs, ledger blocks, verification runs và trạng thái lỗi.*

> Gợi ý chụp: chụp Databricks SQL Dashboard có các KPI chính; đây là hình tổng hợp cho phần thực nghiệm.

Ledger overview cho thấy mỗi pipeline run sinh 4 block theo thứ tự
SOURCE, BRONZE, SILVER và GOLD. Với run benchmark 50.000 records,
SOURCE, BRONZE và SILVER đều ghi nhận 50.000 records; GOLD ghi nhận
1.825 records sau aggregation theo ngày và sản phẩm.


**[Chèn hình tại đây]**

*Hình 3.9. Bảng `blockchain_ledger` ghi nhận bốn block SOURCE, BRONZE, SILVER và GOLD cho mỗi pipeline run.*

> Gợi ý chụp: chụp query có các cột `pipeline_run_id`, `block_index`, `stage`, `record_count`, `previous_hash`, `block_hash`.

Lineage mẫu trên dashboard:

| Luồng xử lý | Input records | Output records | Status |
|---|---:|---:|---|
| SOURCE -> BRONZE | 10.000 | 10.000 | SUCCESS |
| BRONZE -> SILVER | 10.000 | 10.000 | SUCCESS |
| SILVER -> GOLD | 10.000 | 1.825 | SUCCESS |


**[Chèn hình tại đây]**

*Hình 3.10. Bảng `lineage_events` ghi nhận lịch sử biến đổi dữ liệu giữa các stage.*

> Gợi ý chụp: chụp các cột `pipeline_run_id`, `source_stage`, `target_stage`, `transformation_name`, `input_record_count`, `output_record_count`, `status`.

Verification latency trong các dòng gần nhất dao động từ 24.000 ms đến
31.000 ms. Lịch sử dashboard có một điểm latency lớn bất thường, phản
ánh ảnh hưởng của cold start hoặc thời gian chờ compute. Benchmark cần
tách warm-up khỏi các lần đo chính để tránh làm lệch kết luận.


**[Chèn hình tại đây]**

*Hình 3.11. Kết quả kiểm chứng dữ liệu hợp lệ trong bảng `verification_results` với trạng thái `VALID`.*

> Gợi ý chụp: chụp kết quả có `expected_record_count`, `actual_record_count`, `expected_batch_hash`, `actual_batch_hash` và `verification_status`.

### 3.5. Đánh giá hiệu quả mô hình

#### 3.5.1. Đánh giá khả năng phát hiện thay đổi dữ liệu

Verification engine phát hiện bốn nhóm sai lệch:

| Nhóm sai lệch         | Cơ chế phát hiện                                       |
|:----------------------|:-------------------------------------------------------|
| Sửa nội dung dữ liệu  | Batch hash hiện tại khác batch hash đã lưu.            |
| Xóa hoặc chèn dữ liệu | Record count hiện tại khác record count đã lưu.        |
| Sửa metadata block    | Recalculated block hash khác stored block hash.        |
| Sửa liên kết chuỗi    | `previous_hash` không khớp block hash của block trước. |

Dashboard export hiện tại phản ánh trạng thái baseline hợp lệ: không có
tamper event, không có first broken block và 14/14 runs hiển thị không
phát hiện lỗi. Kết quả này xác nhận dữ liệu nhất quán trong điều kiện
không có can thiệp sau xử lý.

| Chỉ số phát hiện          |  Giá trị |
|:--------------------------|---------:|
| Tổng số verification runs |       14 |
| Runs có phát hiện lỗi     |        0 |
| Runs không phát hiện lỗi  |       14 |
| First broken block        | Không có |
| Tamper event              | Không có |

Để đánh giá khả năng phát hiện sửa đổi, đề tài sử dụng thêm các kịch bản
tamper có kiểm soát như sửa giá trị giao dịch, xóa bản ghi, chèn bản ghi
giả, sửa batch hash trong ledger, sửa metadata transformation và sửa
`previous_hash`. Các kịch bản này giúp kiểm tra khả năng phân loại lỗi
và xác định vị trí sai lệch trong chuỗi ledger.


**[Chèn hình tại đây]**

*Hình 3.12. Kết quả phát hiện lỗi liên kết chuỗi sau khi sửa `previous_hash`, trạng thái trả về `CHAIN_BROKEN`.*

> Gợi ý chụp: chụp kết quả verification sau scenario `MODIFY_LEDGER_PREVIOUS_HASH` hoặc kịch bản sửa metadata block để trả về `BLOCK_TAMPERED`.

#### 3.5.2. Đánh giá khả năng truy vết dữ liệu

Lineage events ghi nhận đầy đủ đường đi SOURCE -> BRONZE -> SILVER ->
GOLD theo pipeline run ID. Record count đầu vào/đầu ra cho thấy
transformation GOLD giảm dữ liệu từ 10.000 records xuống 1.825 records
do aggregation. Chỉ số này nhất quán với vai trò của Gold layer trong
Medallion Architecture.

Khi verification phát hiện lỗi, người vận hành dùng `pipeline_run_id`,
`pipeline_stage` và first broken block để truy về lineage event tương
ứng. Quy trình phân tích:

``` text
verification_results -> first broken block -> pipeline_run_id + stage
-> lineage_events -> source/target table + transformation context
```

#### 3.5.3. Đánh giá khả năng áp dụng trong hệ thống thực tế

Mô hình phù hợp với các hệ thống cần auditability, phát hiện thay đổi dữ
liệu sau xử lý và truy vết transformation theo pipeline run. Kiến trúc
có thể tích hợp vào pipeline hiện có vì không yêu cầu thay đổi toàn bộ
dữ liệu nghiệp vụ; hệ thống chỉ bổ sung lớp evidence gồm hash, ledger,
lineage và verification result.

Benchmark dashboard cho thấy Security overhead tăng theo kích thước dữ
liệu. PDF export chỉ hiển thị biểu đồ cột, không hiển thị duration chi
tiết; bảng dưới ghi nhận giá trị xấp xỉ theo biểu đồ, số liệu chính xác
cần truy vấn trực tiếp từ `experiment_metrics`.

| Record count | Quan sát từ dashboard                   | overhead xấp xỉ |
|-------------:|:----------------------------------------|----------------:|
|              | overhead thấp hơn nhóm 10.000 và 50.000 |     khoảng 160% |
|        5.000 | overhead gần mức 1.000                  | khoảng 155-160% |
|       10.000 | overhead tăng so với 1.000 và 5.000     |     khoảng 180% |
|       50.000 | overhead cao nhất trong biểu đồ         |     khoảng 220% |


**[Chèn hình tại đây]**

*Hình 3.13. Kết quả benchmark so sánh `baseline_duration_ms`, `secured_duration_ms`, `verification_duration_ms` và `overhead_percent` theo kích thước dữ liệu.*

> Gợi ý chụp: chụp bảng `experiment_metrics` hoặc biểu đồ overhead trong Databricks SQL Dashboard.

Truy vấn lấy số liệu chính xác:

``` text
SELECT record_count,
COUNT(\*)
AS measured_runs,
AVG(baseline_duration_ms)
AS avg_baseline_duration_ms,
AVG(secured_duration_ms)
AS avg_secured_duration_ms,
AVG(verification_duration_ms)
AS avg_verification_duration_ms,
AVG(overhead_percent)
AS avg_overhead_percent,
percentile_approx(overhead_percent,
0.5)
AS median_overhead_percent
FROM experiment_metrics
WHERE is_warmup
=
false
GROUP
BY record_count
ORDER
BY record_count;
```

Các giới hạn kỹ thuật:

| Giới hạn                                      | Tác động                               | Hướng mở rộng                                                      |
|:----------------------------------------------|:---------------------------------------|:-------------------------------------------------------------------|
| Ledger và dữ liệu nằm cùng workspace          | Admin cấp cao có thể sửa cả hai.       | Externalize ledger hoặc lưu checkpoint hash trên hệ thống độc lập. |
| MVP chưa có consensus                         | Chưa đạt mức Blockchain phi tập trung. | Tích hợp Blockchain network hoặc Smart Contract.                   |
| Batch hash có thể tốn chi phí với dữ liệu lớn | overhead tăng theo record count.       | Partition hash, Merkle Tree, incremental hashing.                  |
| Verification phụ thuộc compute state          | Cold start làm tăng latency.           | Tách warm-up, đo nhiều lần, dùng cluster ổn định.                  |

## Data Governance Architecture

Mô hình đáp ứng các miền Data Governance chính:

| Miền Governance | Cơ chế trong mô hình |
|---|---|
| Data Quality | Schema validation, deduplication, type normalization, consistency check `amount = quantity * unit_price`. |
| Data Lineage | Ghi source/target stage, transformation, record count, batch hash, execution time và status. |
| Data Integrity | SHA-256 batch hash, schema hash, record count verification và block hash. |
| Data Audit | Lưu verification history, failure reason, first broken block và pipeline run ID. |
| Monitoring | Dashboard KPI cho pipeline runs, ledger blocks, verification status, latency và overhead. |

Mô hình trả lời được các câu hỏi vận hành:

1.  Dữ liệu hiện tại có khớp trạng thái đã ghi nhận không?

2.  Sai lệch xảy ra ở stage nào?

3.  Pipeline run nào bị ảnh hưởng?

4.  Bảng nào là target của block lỗi?

5.  First broken block là block nào?

6.  Transformation liên quan là gì?

7.  Security overhead của cơ chế kiểm chứng là bao nhiêu?

Từ kết quả phân tích và thử nghiệm, có thể thấy việc kết hợp SHA-256,
Data Lineage và Hash-linked Ledger có khả năng tạo ra một lớp kiểm chứng
tamper-evident cho Data Pipeline. Mô hình không ngăn chặn tuyệt đối mọi
thay đổi ở tầng vật lý, nhưng cung cấp bằng chứng kỹ thuật để phát hiện
sai lệch, xác định vị trí block đầu tiên bị lỗi và liên hệ lỗi đó với
pipeline run, stage và transformation tương ứng. Hướng phát triển tiếp
theo gồm ký số block, tách ledger khỏi workspace dữ liệu, lưu checkpoint
hash trên hạ tầng độc lập hoặc Blockchain thật, đồng thời thay batch
hash tuyến tính bằng Merkle Tree để cải thiện khả năng mở rộng với dữ
liệu lớn.
