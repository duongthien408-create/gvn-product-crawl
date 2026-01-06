# CellphoneS Product Crawler

Website crawl thông số kỹ thuật sản phẩm từ CellphoneS.

## Cài đặt

```bash
# Cài dependencies
pip install -r requirements.txt

# Cài Playwright browser
playwright install chromium
```

## Chạy

```bash
python app.py
```

Mở trình duyệt tại: http://127.0.0.1:5000

## Tính năng

- Nhập URL sản phẩm CellphoneS để crawl thông tin
- Lấy đầy đủ thông số kỹ thuật (25+ thông số)
- Lưu sản phẩm vào database SQLite
- Copy thông số / Tải JSON
- Xem lại sản phẩm đã lưu

## API Endpoints

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | /api/crawl | Crawl sản phẩm từ URL |
| GET | /api/products | Danh sách sản phẩm đã lưu |
| GET | /api/products/:sku | Chi tiết sản phẩm |
| DELETE | /api/products/:sku | Xóa sản phẩm |
| GET | /api/history | Lịch sử crawl |

## Cấu trúc thư mục

```
cellphones-web/
├── app.py              # Flask backend
├── requirements.txt    # Dependencies
├── products.db         # SQLite database (auto-created)
└── templates/
    └── index.html      # Frontend với Tailwind CSS
```
