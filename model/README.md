# Trained Models

Thư mục này chứa thông tin về các model checkpoint đã được huấn luyện trong project.

Do kích thước các file model lớn, các checkpoint không được lưu trực tiếp trên GitHub. Thay vào đó, toàn bộ model đã huấn luyện được cung cấp thông qua Google Drive.

---

## Download trained models

Google Drive:
- All trained models: https://drive.google.com/drive/folders/1MZ_eTeJAoWCfApyLk2QGxNN14B2vT4QO?usp=sharing

---

## Expected directory structure

Sau khi tải model về, đặt các checkpoint vào đúng cấu trúc sau:

```text
model/
├── README.md
├── PP-OCR-v5/
│   ├── model_B1.pdparams
│   ├── model_B2.pdparams
│   └── model_B3.pdparams
└── PP-OCR-v6/
    └── model.pdparams