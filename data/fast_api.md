
# title: "Tối ưu hóa Kiến trúc RAG với LangGraph và Vector Database"


# Tối ưu hóa Hệ thống Retrieval-Augmented Generation (RAG)

## 1. Giới thiệu tổng quan
Tài liệu này trình bày các kỹ thuật nâng cao để cải thiện độ chính xác của hệ thống RAG, tập trung vào việc quản lý luồng dữ liệu (State Management) thông qua **LangGraph** và tối ưu hóa truy vấn trên **ChromaDB**.

## 2. Kiến trúc Hệ thống (System Architecture)

### 2.1. Thành phần chính
* **Embedding Model:** Sử dụng các mô hình có khả năng xử lý ngữ cảnh dài (như `text-embedding-3-small`).
* **Vector Database:** **ChromaDB** được cấu hình với metadata filtering để tăng tốc độ truy xuất.
* **Orchestrator:** **LangGraph** điều phối các node kiểm tra chất lượng câu trả lời (Self-Correction).

### 2.2. Quy trình xử lý (Pipeline)
1.  **Ingestion:** Chuyển đổi tài liệu PDF sang định dạng Markdown để giữ cấu trúc Header.
2.  **Chunking:** Sử dụng `RecursiveCharacterTextSplitter` với kích thước chunk 512 và overlap 50.
3.  **Retrieval:** Thực hiện tìm kiếm tương đồng (Similarity Search) kết hợp với bộ lọc Metadata.

## 3. Kỹ thuật Nâng cao (Advanced Techniques)

### 3.1. Metadata Filtering trong ChromaDB
Để tránh hiện tượng "trôi ngữ cảnh", chúng ta áp dụng bộ lọc trực tiếp vào truy vấn:

```python
results = collection.query(
    query_texts=["Làm thế nào để tối ưu RAG?"],
    where={"category": "Technical Research"},
    n_results=5
)