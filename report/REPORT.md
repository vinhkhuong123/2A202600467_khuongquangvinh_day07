# Báo Cáo Lab 7: Embedding & Vector Store

**Họ tên:** Khương Quang Vinh
**Nhóm:** nhóm 61
**Ngày:** [Ngày nộp]

---

## 1. Warm-up (5 điểm)

### Cosine Similarity (Ex 1.1)

**High cosine similarity nghĩa là gì?**
> Hai đoạn văn bản có cosine similarity cao nghĩa là chúng có nội dung ngữ nghĩa tương đồng — vector embedding của chúng gần như cùng hướng trong không gian đa chiều. Giá trị càng gần 1, hai đoạn text càng giống nhau về mặt ý nghĩa.

**Ví dụ HIGH similarity:**
- Sentence A: "Python là ngôn ngữ lập trình bậc cao dễ học."
- Sentence B: "Python là một ngôn ngữ lập trình phổ biến, thân thiện với người mới."
- Tại sao tương đồng: Cả hai câu đều nói về Python là ngôn ngữ lập trình và tính dễ tiếp cận, nên embedding sẽ rất gần nhau.

**Ví dụ LOW similarity:**
- Sentence A: "Python là ngôn ngữ lập trình bậc cao dễ học."
- Sentence B: "Hôm nay trời rất đẹp, trời nắng ấm."
- Tại sao khác: Hai câu thuộc domain hoàn toàn khác nhau (lập trình vs thời tiết), embedding sẽ chỉ về các hướng rất khác trong không gian vector.

**Tại sao cosine similarity được ưu tiên hơn Euclidean distance cho text embeddings?**
> Cosine similarity chỉ đo góc giữa hai vector, không phụ thuộc vào độ dài (magnitude) của chúng. Điều này quan trọng vì hai đoạn text có cùng ý nghĩa nhưng độ dài khác nhau sẽ có vector cùng hướng nhưng khác magnitude — cosine similarity vẫn cho điểm cao, trong khi Euclidean distance sẽ cho khoảng cách lớn.

### Chunking Math (Ex 1.2)

**Document 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**
 *Phép tính:* 
num_chunks = ceil((doc_length - overlap) / (chunk_size - overlap))
= ceil((10000 - 50) / (500 - 50))
= ceil(9950 / 450)`
= ceil(22.11)
*Đáp án:* **23 chunks**

**Nếu overlap tăng lên 100, chunk count thay đổi thế nào? Tại sao muốn overlap nhiều hơn?**
ceil((10000 - 100) / (500 - 100)) = ceil(9900 / 400) = ceil(24.75) = 25 chunks. Chunk count tăng từ 23 lên 25. Overlap nhiều hơn giúp bảo toàn ngữ cảnh giữa các chunk — thông tin nằm ở ranh giới chunk sẽ không bị cắt mất, giúp retrieval chính xác hơn khi query liên quan đến đoạn giao nhau.

---

## 2. Document Selection — Nhóm (10 điểm)

### Domain & Lý Do Chọn

**Domain:** Technical documentation on AI

**Tại sao nhóm chọn domain này?**
> Tài liệu kỹ thuật về AI bao gồm nhiều chủ đề đa dạng (kiến trúc hệ thống, machine learning, RAG, pricing) với cấu trúc markdown rõ ràng (heading, bullet, code block), rất phù hợp để thử nghiệm các chiến lược chunking khác nhau. Domain này cũng chứa cả tiếng Anh và tiếng Việt, giúp kiểm tra khả năng embedding xử lý nội dung song ngữ. Ngoài ra, các câu hỏi kỹ thuật thực tế dễ xây dựng benchmark query để đánh giá retrieval quality.

### Data Inventory

| # | Tên tài liệu | Nguồn | Số ký tự | Metadata đã gán |
|---|--------------|-------|----------|-----------------|
| 1 | embed_ai.md | Product Case Studies | 3386 | domain: product, type: case_study |
| 2 | fast_api.md | Tech Tutorial | 56187 | domain: web_framework, type: documentation |
| 3 | hermes-agent...md | System Design | 14688 | domain: agent_backend, type: architecture |
| 4 | performance_guardrails...md | Quality Assurance | 3655 | domain: evaluation, type: infrastructure |
| 5 | rag_system_design.md | RAG Guide | 2416 | domain: rag, type: architecture |

### Metadata Schema

| Trường metadata | Kiểu | Ví dụ giá trị | Tại sao hữu ích cho retrieval? |
|----------------|------|---------------|-------------------------------|
| topic | str | "rag", "machine_learning", "architecture" | Lọc theo chủ đề kỹ thuật, tránh trả về tài liệu không liên quan (vd: hỏi về RAG nhưng trả về pricing) |
| lang | str | "vi", "en" | Đảm bảo trả về tài liệu đúng ngôn ngữ phù hợp với câu hỏi của người dùng |
| year | int | 2026 | Ưu tiên tài liệu mới nhất, đặc biệt quan trọng trong lĩnh vực AI phát triển nhanh |

---

## 3. Chunking Strategy — Cá nhân chọn, nhóm so sánh (15 điểm)

### Baseline Analysis

Chạy `ChunkingStrategyComparator().compare(text, chunk_size=300)` trên 3 tài liệu đại diện:

| Tài liệu | Strategy | Chunk Count | Avg Length | Preserves Context? |
|-----------|----------|-------------|------------|-------------------|
| 1.md (3 008 chars) | FixedSizeChunker (`fixed_size`) | 11 | 273.45 | Trung bình — cắt cứng giữa câu/đoạn, mất ngữ cảnh ở ranh giới |
| 1.md | SentenceChunker (`by_sentences`) | 11 | 272.0 | Tốt — giữ câu hoàn chỉnh, nhưng có thể gộp câu từ khác section |
| 1.md | RecursiveChunker (`recursive`) | 17 | 175.35 | Tốt — tách theo paragraph/heading trước, chunk gọn |
| hermes...md (14 688 chars) | FixedSizeChunker (`fixed_size`) | 49 | 299.76 | Trung bình — cắt giữa section, chunk đều nhưng mất ngữ cảnh |
| hermes...md | SentenceChunker (`by_sentences`) | 30 | 487.73 | Kém — chunk quá lớn, gộp nhiều section khác nhau |
| hermes...md | RecursiveChunker (`recursive`) | 64 | 227.62 | Tốt — tách theo separator hierarchy, chunk nhỏ gọn |
| ML guide (9 593 chars) | FixedSizeChunker (`fixed_size`) | 32 | 299.78 | Trung bình — cắt cứng |
| ML guide | SentenceChunker (`by_sentences`) | 12 | 797.42 | Kém — chunk rất lớn, gộp nhiều ý khác nhau |
| ML guide | RecursiveChunker (`recursive`) | 45 | 211.31 | Tốt — chunk nhỏ, tách theo paragraph |

### Strategy Của Tôi

**Loại:** SentenceChunker

**Mô tả cách hoạt động:**
> SentenceChunker tách văn bản thành các câu riêng lẻ dựa trên dấu kết thúc câu (`. `, `! `, `? `, `.\n`) bằng regex `(?<=[.!?])(?:\s|\n)`, sau đó nhóm các câu liên tiếp lại thành chunk theo `max_sentences_per_chunk` (mặc định 3). Mỗi chunk chứa tối đa 3 câu liền nhau, đảm bảo mỗi chunk là một đoạn văn bản hoàn chỉnh về mặt ngữ pháp. Khoảng trắng thừa được strip để chunk sạch sẽ. Nếu text chỉ có 1 câu, trả về nguyên văn trong 1 chunk duy nhất.

**Tại sao tôi chọn strategy này cho domain nhóm?**
> Tài liệu kỹ thuật AI thường viết theo cấu trúc câu dài, mỗi câu chứa một ý hoàn chỉnh (định nghĩa, giải thích, bước thực hiện). SentenceChunker giữ nguyên ranh giới câu nên mỗi chunk luôn có ngữ nghĩa trọn vẹn — không cắt giữa chừng một giải thích kỹ thuật, giúp embedding biểu diễn chính xác hơn và retrieval trả về kết quả dễ hiểu hơn so với FixedSizeChunker.


### So Sánh: Strategy của tôi vs Baseline

Tài liệu test: 3 file đại diện từ bộ data nhóm.

**1. `data/1.md` (3 008 chars)**

| Strategy | Chunk Count | Avg Length | Preserves Context? |
|----------|-------------|------------|--------------------|
| FixedSizeChunker (chunk_size=300) | 11 | 273.45 | Trung bình — cắt cứng, có thể cắt giữa câu |
| RecursiveChunker (chunk_size=300) | 17 | 175.35 | Tốt — chunk nhỏ gọn, tách theo paragraph |
| SentenceChunker (của tôi, max_sentences=3)** | 11 | 272.0 | Tốt — giữ nguyên câu hoàn chỉnh, kích thước tương đương FixedSize nhưng không cắt giữa ý |

**2. `data/hermes-agent-pricing-accuracy-architecture-design.md` (14 688 chars)**

| Strategy | Chunk Count | Avg Length | Preserves Context? |
|----------|-------------|------------|--------------------|
| FixedSizeChunker (chunk_size=300) | 49 | 299.76 | Kém — cắt cứng giữa section, heading bị tách khỏi nội dung |
| RecursiveChunker (chunk_size=300) | 64 | 227.62 | Tốt — chunk nhỏ gọn nhờ separator hierarchy |
| SentenceChunker (của tôi, max_sentences=3)** | 30 | 487.73 | Tốt — giữ nguyên ranh giới câu, mỗi chunk là 3 câu hoàn chỉnh, dễ đọc |

**3. `data/machine_learning_guide.md` (9 593 chars)**

| Strategy | Chunk Count | Avg Length | Preserves Context? |
|----------|-------------|------------|--------------------|
| FixedSizeChunker (chunk_size=300) | 32 | 299.78 | Trung bình — cắt cứng giữa đoạn |
| RecursiveChunker (chunk_size=300) | 45 | 211.31 | Tốt — chunk nhỏ, tách theo paragraph |
| SentenceChunker (của tôi, max_sentences=3) | 12 | 797.42 | Trung bình — giữ câu hoàn chỉnh nhưng chunk rất lớn do tài liệu có câu dài |

**Nhận xét tổng hợp:**
- Trên file nhỏ (1.md): SentenceChunker cho kết quả tương đương FixedSizeChunker (cùng 11 chunks, ~272 chars) nhưng ưu điểm là không cắt giữa câu.
- Trên file trung bình (hermes...md): SentenceChunker tạo ít chunk nhất (30 vs 49/64) với avg_length lớn nhất (488 chars) — mỗi chunk chứa đủ ngữ cảnh, phù hợp cho query cần câu trả lời dài.
- Trên file lớn (ML guide): SentenceChunker tạo chunk rất lớn (797 chars) — đây là điểm yếu khi tài liệu có nhiều câu dài liên tiếp, embedding bị "pha loãng" ngữ nghĩa.
- **Đánh đổi chính:** SentenceChunker phù hợp nhất với tài liệu có câu ngắn-trung bình (như hermes...md, 1.md). Với tài liệu câu dài (ML guide), cần giảm `max_sentences_per_chunk` xuống 1-2 để kiểm soát kích thước chunk.

### So Sánh Với Thành Viên Khác

| Thành viên | Strategy | Retrieval Score (/10) | Điểm mạnh | Điểm yếu |
|-----------|----------|----------------------|-----------|----------|
| Tôi | SentenceChunker (`by_sentences`) | 7/10 | 30 chunks, avg 487.73; giữ nguyên câu, dễ đọc | Chunk dài, dễ vượt mức kỳ vọng trên tài liệu nhiều câu |
| Hieu | RecursiveChunker (`recursive`) | 8/10 | 102 chunks, avg 141.68; giữ cấu trúc tốt cho tài liệu dài | Tạo nhiều chunk hơn fixed-size nên top-k cần chọn hợp lý |
| Hải | RecursiveChunker2 (`recursive2`) | 8/10 | 103 chunks, avg 142.60; khá ổn định, giữ ngữ cảnh tốt | Cài đặt custom khó chuẩn hóa hơn strategy gốc |
| Nam | FixedSizeChunker (`fixed_size`) | 6/10 | 92 chunks, avg 199.22; đơn giản, ổn định, dễ triển khai | Dễ cắt giữa ý, giảm chất lượng ngữ cảnh |
| Dung | SentenceChunker (`by_sentences`) | 7/10 | 30 chunks, avg 487.73; giữ nguyên câu, dễ đọc | Chunk dài, dễ vượt mức kỳ vọng trên tài liệu nhiều câu |
| Duc Anh | Custom LLM-guided chunking | 8/10 | 44 chunks, avg 375.09; chọn được policy phù hợp cho tài liệu spec | Phụ thuộc vào prompt/LLM, khó tái lập nếu không chuẩn hóa |


**Strategy nào tốt nhất cho domain này? Tại sao?**
> **RecursiveChunker** là strategy tốt nhất cho domain Technical AI Documentation, đạt 8/10 (Hieu, Hải). Lý do: RecursiveChunker tách theo separator hierarchy (`\n\n` → `\n` → `. ` → ký tự), tạo chunk nhỏ gọn (~142 chars) và giữ nguyên cấu trúc paragraph/heading — phù hợp với tài liệu Markdown dài có nhiều section lồng nhau. FixedSizeChunker (6/10) cắt cứng giữa ý nên retrieval kém nhất. SentenceChunker (7/10, strategy của tôi) giữ câu hoàn chỉnh nhưng chunk quá lớn (488-797 chars) trên tài liệu câu dài, khiến embedding bị pha loãng. Custom LLM-guided chunking (Duc Anh, 8/10) linh hoạt nhưng khó tái lập và phụ thuộc vào prompt.

---

## 4. My Approach — Cá nhân (10 điểm)

Giải thích cách tiếp cận của bạn khi implement các phần chính trong package `src`.

### Chunking Functions

**`SentenceChunker.chunk`** — approach:
> Dùng regex `(?<=[\.!?])(?:\s|\n)` để tách câu — lookbehind match dấu kết thúc câu (`.`, `!`, `?`) theo sau bởi khoảng trắng hoặc xuống dòng. Sau đó strip whitespace thừa, lọc bỏ chuỗi rỗng, và nhóm các câu liên tiếp theo `max_sentences_per_chunk` bằng vòng lặp `range(0, len, step)`. Edge case: text rỗng trả `[]`, text không có dấu kết thúc câu trả nguyên 1 chunk.

**`RecursiveChunker.chunk` / `_split`** — approach:
> Algorithm đệ quy: thử tách text bằng separator đầu tiên trong danh sách, gộp các phần nhỏ lại nếu tổng chưa vượt `chunk_size`. Nếu phần nào vẫn quá lớn, đệ quy xuống separator tiếp theo. Base case: text đã ≤ `chunk_size` thì trả nguyên; hết separator thì cắt cứng theo `chunk_size`.

### EmbeddingStore

**`add_documents` + `search`** — approach:
> Mỗi document được embed bằng `embedding_fn`, tạo record dict gồm `id`, `content`, `embedding`, `metadata` (kèm `doc_id`), rồi append vào `self._store` (và ChromaDB nếu có). Khi search, embed query rồi tính dot product với từng record, sort giảm dần và trả top_k.

**`search_with_filter` + `delete_document`** — approach:
> `search_with_filter` lọc metadata **trước** khi search — dùng list comprehension kiểm tra tất cả key-value trong `metadata_filter` match với record, rồi mới chạy similarity search trên tập đã lọc. `delete_document` dùng list comprehension giữ lại các record có `doc_id` khác, so sánh length trước/sau để trả `True/False`.

### KnowledgeBaseAgent

**`answer`** — approach:
> Theo pattern RAG: retrieve top_k chunks từ store, nối content bằng `\n\n` thành context, rồi xây prompt dạng "Use the following context to answer the question.\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer:". Cuối cùng gọi `llm_fn(prompt)` và trả kết quả trực tiếp.

### Test Results

```
tests/test_solution.py::TestProjectStructure::test_root_main_entrypoint_exists PASSED
tests/test_solution.py::TestProjectStructure::test_src_package_exists PASSED
tests/test_solution.py::TestClassBasedInterfaces::test_chunker_classes_exist PASSED
tests/test_solution.py::TestClassBasedInterfaces::test_mock_embedder_exists PASSED
tests/test_solution.py::TestFixedSizeChunker::test_chunks_respect_size PASSED
tests/test_solution.py::TestFixedSizeChunker::test_correct_number_of_chunks_no_overlap PASSED
tests/test_solution.py::TestFixedSizeChunker::test_empty_text_returns_empty_list PASSED
tests/test_solution.py::TestFixedSizeChunker::test_no_overlap_no_shared_content PASSED
tests/test_solution.py::TestFixedSizeChunker::test_overlap_creates_shared_content PASSED
tests/test_solution.py::TestFixedSizeChunker::test_returns_list PASSED
tests/test_solution.py::TestFixedSizeChunker::test_single_chunk_if_text_shorter PASSED
tests/test_solution.py::TestSentenceChunker::test_chunks_are_strings PASSED
tests/test_solution.py::TestSentenceChunker::test_respects_max_sentences PASSED
tests/test_solution.py::TestSentenceChunker::test_returns_list PASSED
tests/test_solution.py::TestSentenceChunker::test_single_sentence_max_gives_many_chunks PASSED
tests/test_solution.py::TestRecursiveChunker::test_chunks_within_size_when_possible PASSED
tests/test_solution.py::TestRecursiveChunker::test_empty_separators_falls_back_gracefully PASSED
tests/test_solution.py::TestRecursiveChunker::test_handles_double_newline_separator PASSED
tests/test_solution.py::TestRecursiveChunker::test_returns_list PASSED
tests/test_solution.py::TestEmbeddingStore::test_add_documents_increases_size PASSED
tests/test_solution.py::TestEmbeddingStore::test_add_more_increases_further PASSED
tests/test_solution.py::TestEmbeddingStore::test_initial_size_is_zero PASSED
tests/test_solution.py::TestEmbeddingStore::test_search_results_have_content_key PASSED
tests/test_solution.py::TestEmbeddingStore::test_search_results_have_score_key PASSED
tests/test_solution.py::TestEmbeddingStore::test_search_results_sorted_by_score_descending PASSED
tests/test_solution.py::TestEmbeddingStore::test_search_returns_at_most_top_k PASSED
tests/test_solution.py::TestEmbeddingStore::test_search_returns_list PASSED
tests/test_solution.py::TestKnowledgeBaseAgent::test_answer_non_empty PASSED
tests/test_solution.py::TestKnowledgeBaseAgent::test_answer_returns_string PASSED
tests/test_solution.py::TestComputeSimilarity::test_identical_vectors_return_1 PASSED
tests/test_solution.py::TestComputeSimilarity::test_opposite_vectors_return_minus_1 PASSED
tests/test_solution.py::TestComputeSimilarity::test_orthogonal_vectors_return_0 PASSED
tests/test_solution.py::TestComputeSimilarity::test_zero_vector_returns_0 PASSED
tests/test_solution.py::TestCompareChunkingStrategies::test_counts_are_positive PASSED
tests/test_solution.py::TestCompareChunkingStrategies::test_each_strategy_has_count_and_avg_length PASSED
tests/test_solution.py::TestCompareChunkingStrategies::test_returns_three_strategies PASSED
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_filter_by_department PASSED
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_no_filter_returns_all_candidates PASSED
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_returns_at_most_top_k PASSED
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_reduces_collection_size PASSED
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_returns_false_for_nonexistent_doc PASSED
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_returns_true_for_existing_doc PASSED

42 passed in 1.71s
```

**Số tests pass:** 42 / 42

---

## 5. Similarity Predictions — Cá nhân (5 điểm)

*Sử dụng model: OpenAI `text-embedding-3-small`*

| Pair | Sentence A | Sentence B | Dự đoán | Actual Score | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | "Python là ngôn ngữ lập trình bậc cao dễ học." | "Python là một ngôn ngữ lập trình phổ biến, thân thiện với người mới." | high | 0.7809 | Đúng |
| 2 | "Machine learning uses algorithms to learn from data." | "Deep learning is a subset of machine learning." | high | 0.4903 | Đúng |
| 3 | "Python là ngôn ngữ lập trình bậc cao dễ học." | "Hôm nay trời rất đẹp, trời nắng ấm." | low | 0.2384 | Đúng |
| 4 | "Vector databases store embeddings for similarity search." | "The cat sat on the mat." | low | -0.0128 | Đúng |
| 5 | "RAG retrieves relevant documents before generating answers." | "Retrieval-augmented generation improves LLM accuracy." | high | 0.4246 | Đúng |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn nghĩa?**
> Pair 3 bất ngờ nhất — score 0.2384 không quá thấp mặc dù hai câu hoàn toàn khác domain (lập trình vs thời tiết), cho thấy embedding model vẫn tìm được một chút tương đồng cấu trúc ngữ pháp (cả hai đều là câu mô tả tiếng Việt). Pair 1 đạt 0.78 — rất cao, chứng tỏ `text-embedding-3-small` hiểu tốt ngữ nghĩa tiếng Việt, biết rằng "dễ học" và "thân thiện với người mới" là cùng ý. Pair 4 gần -0.01 là thấp nhất, đúng kỳ vọng vì "vector database" và "the cat sat on the mat" hoàn toàn không liên quan cả về ngữ nghĩa lẫn ngôn ngữ.

---

## 6. Results — Cá nhân (10 điểm)

Chạy 5 benchmark queries của nhóm trên implementation cá nhân của bạn trong package `src`. **5 queries phải trùng với các thành viên cùng nhóm.**

### Benchmark Queries & Gold Answers (nhóm thống nhất)

| # | Query | Gold Answer |
|---|-------|-------------|
| 1 | What does Hermes do to handle cache billing correctly? | It separates cache read and cache write tokens, normalizes usage before pricing, and uses route-aware official pricing sources. |
| 2 | What are the four layers in the high-level pricing architecture? | `usage_normalization`, `pricing_source_resolution`, `cost_estimation_and_reconciliation`, and `presentation`. |
| 3 | When should the UI show `included` instead of an estimated dollar amount? | When the billing route is subscription-included or explicitly marked as zero-cost/included, not when the cost is only estimated. |
| 4 | In the ML guide, what are the three main machine learning paradigms? | Supervised learning, unsupervised learning, and reinforcement learning. |
| 5 | In the FastHTML tutorial, what is HTMX used for? | HTMX is used to trigger requests from HTML elements and update parts of the page without reloading the entire page. |

### Kết Quả Của Tôi

**Strategy: SentenceChunker (max_sentences=3) + OpenAI text-embedding-3-small | Store: 68 chunks**

| # | Query | Top-1 Retrieved Chunk (tóm tắt) | Score | Relevant? | Agent Answer (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | What does Hermes do to handle cache billing correctly? | hermes...md: "Hermes should only show dollar costs when they are backed by..." (Goal section) | 0.6401 | Yes | Hermes migrates to canonical usage normalization, route-aware pricing sources, estimate-then-reconcile flow |
| 2 | What are the four layers in the high-level pricing architecture? | hermes...md: "The new system has four layers: 1. usage_normalization..." | 0.5184 | Yes | Four layers: usage_normalization, pricing_source_resolution, cost_estimation_and_reconciliation, presentation |
| 3 | When should the UI show `included` instead of an estimated dollar amount? | hermes...md: "official machine-readable cost source...Subscription..." | 0.4674 | Yes (partial) | When billing route is subscription-included or explicitly zero-cost |
| 4 | In the ML guide, what are the three main ML paradigms? | ML guide: "Three Paradigms: Supervised, Unsupervised, Reinforcement Learning" | 0.6186 |  Yes | Supervised learning, unsupervised learning, and reinforcement learning |
| 5 | In the FastHTML tutorial, what is HTMX used for? | fast_api.md: "Ingestion: Chuyển đổi tài liệu PDF sang Markdown..." | 0.2436 |  No | Chunk không liên quan (RAG system design), không tìm thấy thông tin về HTMX/FastHTML |

**Bao nhiêu queries trả về chunk relevant trong top-3?** 4 / 5

---

## 7. What I Learned (5 điểm — Demo)

### Failure Analysis (Exercise 3.5)

**Query thất bại:** Query 5 — *"In the FastHTML tutorial, what is HTMX used for?"*

**Kết quả:** Top-1 score chỉ 0.2436 (rất thấp so với 0.52–0.64 của các query thành công). Cả 3 chunk trả về đều không liên quan — top-1 là đoạn về RAG ingestion pipeline, top-2 là chunk từ hermes...md.

**Tại sao thất bại?**
- **Data gap (thiếu dữ liệu):** File `fast_api.md` thực tế là tài liệu về RAG system design với LangGraph, không phải FastHTML tutorial. Không có tài liệu nào trong bộ data chứa thông tin về HTMX hay FastHTML.
- **Precision thấp:** Embedding tìm được từ "HTMX" và "FastHTML" không match với bất kỳ chunk nào, nên trả về chunk có score gần 0 — retrieval thực chất là random.
- **Metadata không giúp:** Nếu dùng metadata filter `topic="rag"` sẽ chỉ lọc được file `fast_api.md`, nhưng file này cũng không chứa thông tin về HTMX.
- **Chunk coherence:** Với SentenceChunker, các chunk của `fast_api.md` gộp 3 câu liên tiếp — không có câu nào đề cập HTMX nên không strategy nào có thể cứu vãn.

**Đề xuất cải thiện:**
1. **Bổ sung tài liệu:** Thêm file thực sự về FastHTML/HTMX vào bộ data để query có dữ liệu để match.
2. **Thêm confidence threshold:** Nếu top-1 score < 0.3, trả về "Không tìm thấy thông tin liên quan" thay vì xuất chunk không liên quan — tránh hallucination từ agent.
3. **Kiểm tra benchmark queries:** Đảm bảo mỗi query có gold answer thực sự tồn tại trong bộ data trước khi benchmark.

---

**Điều hay nhất tôi học được từ thành viên khác trong nhóm:**
- RecursiveChunker với separator hierarchy cho kết quả ổn định nhất trên nhiều loại tài liệu (8/10 từ Hieu và Hải). - - Custom LLM-guided chunking của Duc Anh cũng đạt 8/10 — cho thấy việc dùng LLM để quyết định điểm cắt chunk có tiềm năng lớn, dù khó tái lập.

**Điều hay nhất tôi học được từ nhóm khác (qua demo):**
- Việc thiết kế benchmark queries quan trọng không kém việc chọn chunking strategy. Query 5 thất bại cho thấy nếu gold answer không tồn tại trong data thì không strategy nào cứu được — "garbage in, garbage out" áp dụng cả cho RAG pipeline.

**Nếu làm lại, tôi sẽ thay đổi gì trong data strategy?**
- Sẽ kiểm tra kỹ hơn rằng mỗi benchmark query có gold answer nằm trong ít nhất 1 tài liệu. Sẽ thử giảm `max_sentences_per_chunk` xuống 1-2 cho tài liệu có câu dài (như ML guide: avg 797 chars là quá lớn). Và sẽ thêm confidence threshold vào agent để tránh trả về chunk không liên quan khi score thấp.

---

## Tự Đánh Giá

| Tiêu chí | Loại | Điểm tự đánh giá |
|----------|------|-------------------|
| Warm-up | Cá nhân | / 5 |
| Document selection | Nhóm | / 10 |
| Chunking strategy | Nhóm | / 15 |
| My approach | Cá nhân | / 10 |
| Similarity predictions | Cá nhân | / 5 |
| Results | Cá nhân | / 10 |
| Core implementation (tests) | Cá nhân | / 30 |
| Demo | Nhóm | / 5 |
| **Tổng** | | **/ 100** |
