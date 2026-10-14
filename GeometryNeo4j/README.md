# GeometryNeo4j

Project nhỏ mô hình hóa **Tứ giác trong hình học phẳng bằng Neo4j**.

## Chức năng

- Lưu kiến thức hình học dưới dạng Knowledge Graph.
- Hiển thị tên gọi, tính chất, nhận biết, chu vi, diện tích.
- Truy vấn các hình được suy ra từ một hình.
- Tìm đường suy luận giữa hai hình.
- Tìm kiếm kiến thức theo từ khóa.
- Có giao diện Streamlit để demo.
- Có thể mở Neo4j Browser để xem trực tiếp graph.

## Mô hình graph

Mỗi node có:

```text
tenGoi
tinhChat
nhanBiet
chuVi
dienTich
```

Quan hệ:

```text
(:TuGiac)-[:THEM_TINH_CHAT {tinhChatThem: "..."}]->(:TuGiac)
```

Ví dụ:

```text
Hình thang
    --[Có thêm một cặp cạnh đối song song]-->
Hình bình hành
```

## Yêu cầu

- Python 3.10+
- Neo4j Desktop/Neo4j Server hoặc Neo4j Aura
- Neo4j đang chạy và có database `neo4j`

## Cài đặt

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Cài thư viện:

```bash
pip install -r requirements.txt
```

Tạo `.env` từ `.env.example` và sửa password Neo4j.

## Khởi tạo dữ liệu

```bash
python init_db.py
```

Lệnh này xóa dữ liệu có label `TuGiac` rồi tạo lại graph.

## Chạy ứng dụng

```bash
streamlit run app.py
```

Mở:

```text
http://localhost:8501
```

## Neo4j Browser

Mở:

```text
http://localhost:7474
```

Chạy:

```cypher
MATCH (n:TuGiac)
OPTIONAL MATCH (n)-[r:THEM_TINH_CHAT]->(m:TuGiac)
RETURN n, r, m;
```

Hoặc:

```cypher
MATCH p=(a:TuGiac)-[:THEM_TINH_CHAT*]->(b:TuGiac)
RETURN p;
```

## Thuyết trình ngắn

> Hệ thống sử dụng Neo4j để biểu diễn kiến thức hình học dưới dạng Knowledge Graph. Mỗi hình là một node, các thuộc tính lưu thông tin về tính chất, nhận biết, chu vi và diện tích. Quan hệ THEM_TINH_CHAT biểu diễn việc bổ sung một tính chất để từ hình ban đầu suy ra một hình đặc biệt hơn. Ứng dụng Python sử dụng Neo4j Driver để truy vấn dữ liệu và Streamlit để xây dựng giao diện demo.

## Cấu trúc

```text
GeometryNeo4j/
├── app.py
├── init_db.py
├── neo4j_connection.py
├── geometry_service.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── cypher/
    ├── create_data.cypher
    └── queries.cypher
```
