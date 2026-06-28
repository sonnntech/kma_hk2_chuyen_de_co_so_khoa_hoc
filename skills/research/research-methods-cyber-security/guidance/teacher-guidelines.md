Nhằm giúp học viên lớp CHAT4P dịch chuyển tư duy từ việc đơn thuần "phát triển công cụ" (engineering) sang "truy vấn khoa học có hệ thống" (scientific inquiry), GV đã hệ thống hóa các yêu cầu trên lớp và phương pháp luận trong [giáo trình](https://drive.google.com/file/d/10nf3kLEU_YmNdXvYltBh2yVWHhhOgPpn/view?usp=drivesdk) thành bản Guidelines chi tiết dưới đây. Mục tiêu cuối cùng là giúp các HV chuẩn bị tốt nhất cho Đề án tốt nghiệp sắp tới và đạt chuẩn xuất bản tại các hội nghị an toàn thông tin có chất lượng tốt. HV sử dụng tài liệu này như một kim chỉ nam để ánh xạ đề tài của mình vào đúng phương pháp nghiên cứu.

### **PHẦN 1: NGUYÊN TẮC CỐT LÕI (BẮT BUỘC ĐỐI VỚI MỌI ĐỀ TÀI)**

Trước khi bắt tay vào code hay thu thập dữ liệu, tất cả các [đề tài (từ Topic 01 đến Topic 19\)](https://docs.google.com/document/d/1fdP16xojwnz_Bkjq4l_rHBwJuLOwcR9bpuzRqsNc8no/edit?usp=drivesdk) phải tuân thủ các nguyên tắc nền tảng sau:

* **Tư duy bắt đầu từ Câu hỏi Nghiên cứu (RQs):** Câu hỏi nghiên cứu bắt buộc phải là điểm khởi đầu của mọi đề tài. Không được chọn công cụ hoặc giải pháp kỹ thuật trước rồi mới tìm câu hỏi gượng ép cho khớp. Phải đi từ bài toán thực tiễn để định hình câu hỏi, từ đó mới sử dụng cây quyết định để chọn phương pháp luận.  
* **Thấu hiểu và Ánh xạ Phương pháp luận:** Các bạn phải trình bày lại phần lý thuyết của chương phương pháp luận mình đảm nhận một cách đàng hoàng, rõ ràng. Dự án thực tế chỉ đóng vai trò là case minh họa để chứng minh các bạn đã phản ánh đúng tinh thần phương pháp luận vào báo cáo. Báo cáo sẽ bị coi là thất bại nếu khi bảo vệ không giải thích được dự án tuân theo phương pháp luận nào.  
* **Phân tích Yêu cầu & Giới hạn Phạm vi (Scoping):** Với thời lượng thực thi nghiêm ngặt là 4 tuần, các bạn phải biết đóng khung phạm vi nghiên cứu. Quy trình xây dựng không được nhảy ngay vào thiết kế hệ thống mà luôn phải đi qua bước phân tích yêu cầu (requirements). Các bạn cần vẽ toàn bộ quy trình tổng quan (pipeline) nhưng chỉ được tập trung hiện thực hóa hoặc mô phỏng sâu một vài module cốt lõi.  
* **Sự chuẩn xác về Thuật ngữ:**  
  * Phải phân biệt rõ ràng, không nhập nhèm giữa kiến trúc (architecture), pipeline, sơ đồ (diagram), luồng công việc (workflow) và quy trình (process).  
  * Phân biệt chính xác cyber security, network security, information security và information assurance qua sơ đồ.  
  * Làm rõ sự khác biệt giữa an toàn (safety \- chống rủi ro vô tình) và an ninh (security \- chống hành vi tấn công có chủ đích).  
* **Mô hình hóa Mối nguy cơ (Threat Modeling):** Không được tuyên bố hệ thống an toàn một cách chung chung. Báo cáo phải lập hồ sơ mối nguy cơ cụ thể, giả định rõ các thuộc tính của kẻ tấn công đối kháng (kiến thức, mục tiêu, tài nguyên, khả năng suy ứng) để thiết kế phòng thủ.  
* **Đạo đức Khoa học (Ethical Responsibilities):** Bất kỳ công cụ bảo mật nào cũng mang tính chất lưỡng dụng (dual-use). Báo cáo phải xem xét khía cạnh đạo đức, hạn chế rủi ro, giảm thiểu thiệt hại ngoài ý muốn, bảo vệ quyền riêng tư và tuân thủ luật pháp.

### **PHẦN 2: HƯỚNG DẪN ÁNH XẠ CHO TỪNG NHÓM PHƯƠNG PHÁP NGHIÊN CỨU**

Dưới đây là guidelines ánh xạ trực tiếp từ giáo trình vào các đề tài cụ thể để các bạn dễ dàng thực thi:

#### **Nhóm 1: Khảo sát Thám hiểm (Exploratory) & Nghiên cứu Mô tả (Descriptive)**

*(Áp dụng cho Topic: 01, 04, 09, 11, 19\)*

* **Mục tiêu Phương pháp:** Sử dụng để tìm hiểu các hiện tượng chưa có mô hình vật lý hoàn chỉnh nhằm khái quát hóa các thông số thống kê mà không can thiệp làm biến đổi hệ thống. Nhấn mạnh vào việc phân tích dữ liệu, không phải tạo ra thiết kế mới.  
* **Chỉ định thực thi:**  
  * Trọng tâm là phân tích dữ liệu (data analysis). Học viên phải sử dụng kỹ thuật xử lý dữ liệu để trích xuất tri thức (insights).  
  * Nếu sử dụng bộ dữ liệu có sẵn, bắt buộc phải thực hiện phân tích ngược (reverse engineer) để trình bày lại cách thu thập và nguồn gốc dữ liệu.  
  * Chỉ được phép báo cáo hệ số tương quan giữa các hiện tượng. Nghiêm cấm vội vã kết luận quan hệ nhân quả một cách cảm quan.

#### **Nhóm 2: Bán Thực nghiệm (Quasi-experimental) & Nghiên cứu Mô phỏng (Simulation)**

*(Áp dụng cho Topic: 05, 08, 12\)*

* **Mục tiêu Phương pháp:** Dùng khi hệ thống thực tế quá lớn, quá nguy hiểm (như tấn công DDoS), hoặc chứa nhiều yếu tố nhiễu không thể phân bổ ngẫu nhiên. Bán thực nghiệm thường dùng thiết kế đo lường lặp lại (repeated measures) để kiểm soát biến ngoại lai.  
* **Chỉ định thực thi:**  
  * Phải làm rõ khái niệm và chứng minh bán thực nghiệm khác thực nghiệm bình thường ở chỗ nó sử dụng môi trường giả lập, mô phỏng thay vì đo đạc trên hệ thống production.  
  * Báo cáo phải giải thích được lý do dự án phù hợp với cây quyết định chọn phương pháp bán thực nghiệm.  
  * Nghiêm cấm tự lập trình lại các hệ thống phức tạp từ đầu một cách thủ công vì kết quả chưa được kiểm chứng (valid).  
  * Bắt buộc phải sử dụng và cấu hình các thư viện, công cụ hoặc framework mô phỏng có sẵn đã được cộng đồng xác thực để đo đạc. Sự toàn vẹn của mô phỏng phụ thuộc tuyệt đối vào độ trung thực của môi trường nhân tạo.

#### **Nhóm 3: Thực nghiệm Ứng dụng (Applied Experimentation) & Công cụ (Instrumentation)**

*(Áp dụng cho Topic: 03, 06, 16, 17\)*

* **Mục tiêu Phương pháp:** Tập trung đánh giá mức độ cải thiện khi áp dụng một tri thức mới vào giải quyết bài toán vận hành cụ thể. Đánh giá sự ổn định của công cụ đo lường.  
* **Chỉ định thực thi:**  
  * Trọng tâm cốt lõi là đối sánh (benchmarking). Báo cáo phải trả lời sòng phẳng giải pháp đề xuất tốt/xấu thế nào so với baseline và tốt hơn bao nhiêu.  
  * Phải chứng minh thiết kế đối sánh là công bằng (fair), không thiên vị (bias) cho giải pháp của mình.  
  * Phải phân tích và chứng minh đề tài đã chủ động phòng tránh được ít nhất 3 sai lầm/lỗi thường gặp trong benchmarking được thảo luận trong sách.

#### **Nhóm 4: Giả thuyết \- Diễn dịch (Hypothetico-deductive) & Học máy (Machine Learning)**

*(Áp dụng cho Topic: 02, 07, 13, 15, 18\)*

* **Mục tiêu Phương pháp:** Một mô hình khái niệm chung được thách thức bằng các thử nghiệm cụ thể. Thiết kế thực nghiệm đòi hỏi phải có nhóm đối chứng (control group) để đối chiếu với nhóm can thiệp (treatment group).  
* **Chỉ định thực thi:**  
  * Phải định nghĩa rõ ràng giả thuyết vô hiệu và giả thuyết thay thế.  
  * Đối với các đề tài Học máy (Topic 07, 15), phải ưu tiên tính khả diễn giải (Explainability). Việc thấu hiểu logic ra quyết định của thuật toán quan trọng hơn việc chạy đua điểm số độ chính xác. Phân tích rõ sự đánh đổi giữa độ chính xác và độ bền vững (robustness).

#### **Nhóm 5: Lý thuyết (Theoretical) & Đạo đức Khoa học (Scientific Ethics)**

*(Áp dụng cho Topic: 10, 14\)*

* **Mục tiêu Phương pháp:** Bứt học viên ra khỏi dòng lệnh để nhìn bao quát hơn bằng toán học mô hình hóa hoặc triết lý pháp lý.  
* **Chỉ định thực thi:**  
  * Topic 10: Chỉ làm việc trên không gian toán học thuần túy (Math heavy), sử dụng Lý thuyết trò chơi (Game theory) để tìm điểm cân bằng Nash, không cần triển khai hệ thống mạng ảo.  
  * Topic 14: Thúc đẩy suy luận định tính và tư duy pháp lý, tránh xa tư duy chủ nghĩa tin tặc (hacktivism), phân tích tình huống dựa trên báo cáo Menlo Report và nguyên tắc của ACM. Không yêu cầu lập trình.

### **PHẦN 3: YÊU CẦU CHUẨN ĐẦU RA VÀ BÁO CÁO (DELIVERABLES)**

Mục tiêu của phương pháp luận là biến các công cụ rời rạc thành một cây tri thức có hệ thống để người đi sau kế thừa. Các bạn sử dụng các template [LaTeX/Word](https://www.ieee.org/conferences/publishing/templates) chuẩn để soạn thảo văn bản, tuân thủ tuyệt đối các quy định sau:

1. **Cấu trúc Báo cáo:**  
   * Bản thảo phải mô phỏng trực tiếp một bài báo nộp cho hội thảo uy tín, định [dạng IEEE hai cột, độ dài từ 6 đến 8 trang.](https://www.ieee.org/conferences/publishing/templates)  
   * Phản ánh chân thực vòng đời nghiên cứu 7 bước: Vấn đề \-\> Tổng quan/Gap \-\> Câu hỏi nghiên cứu \-\> Phương pháp luận (phải biện minh việc chọn phương pháp) \-\> Thiết kế \-\> Đánh giá thực nghiệm \-\> Kết luận.  
2. **Trực quan hóa Dữ liệu (Visualization):**  
   * Nghiêm cấm sử dụng biểu đồ tròn (pie-chart) mang tính cảm quan.  
   * Bắt buộc sử dụng bảng Markdown, biểu đồ hộp (Box-plot), đa giác tần số (CDF), biểu đồ phân phối tần suất (Histogram), biểu đồ cột hoặc đường chạy tiến trình để thể hiện trực quan kết quả đo đạc thay vì mô tả bằng chữ chung chung.  
3. **Tính Minh bạch và Khả năng Tái lập (Reproducibility & Transparency):**  
   * Báo cáo phải có "Phụ lục Tái lập kết quả" (Reproducibility Appendix) dài khoảng 1 trang, chứa các dòng lệnh thực thi môi trường tự động để người khác có thể tái lập kết quả trong vòng 15 phút.  
   * Bắt buộc công bố chi tiết cấu hình môi trường thử nghiệm (loại máy, CPU, RAM), dữ liệu, mã nguồn, siêu tham số và các tham số ẩn.  
4. **Tính Trung thực Khoa học:**  
   * Học viên phải trung thực công bố cả các trường hợp thử nghiệm thất bại hoặc các chỉ số kết quả thấp. Nghiêm cấm mọi hành vi bóp méo số liệu.  
   * Phần Thảo luận (Discussion) phải phân tích khách quan các lỗ hổng và giới hạn của chính bài kiểm thử.

HV đọc kỹ Guidelines này, soi chiếu vào Đề cương chi tiết (Phụ lục A trong danh sách đề tài) tương ứng với số thứ tự đề tài của mình để triển khai. Nếu có điểm nào trong việc xác định Phương pháp luận còn mơ hồ, chúng ta sẽ trao đổi trực tiếp trên nhóm chat. Chúc các bạn hoàn thành tốt dự án nghiên cứu.