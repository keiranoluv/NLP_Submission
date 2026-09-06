# MTHv2 Dataset

Dự án sử dụng bộ dữ liệu **MTHv2 (Multiple Tripitaka in Han v2)** cho bài toán nhận dạng văn bản Hán cổ.

MTHv2 gồm ba tập con chính:

* **MTH1000**
* **MTH1200**
* **TKH**

Bộ dữ liệu cung cấp ảnh tài liệu lịch sử cùng nhiều loại annotation, bao gồm:

* Nhãn theo dòng văn bản
* Nhãn theo ký tự
* Nhãn đường biên và bố cục tài liệu

## Nguồn dữ liệu

* Repository chính thức:
  https://github.com/HCIILAB/MTHv2_Datasets_Release

* Link tải dataset:
  https://drive.google.com/file/d/1JOFWYmiM2Ljcn1qJII2yHSGNA_0eouaj/view

Sau khi tải về, cấu trúc dữ liệu raw được sử dụng trong project như sau:

```text
dataset/
└── raw_dataset/
    ├── TKHMTH2200/
    │   ├── MTH1000/
    │   ├── MTH1200/
    │   └── TKH/
    ├── train.txt
    └── test.txt
```

## Tại sao cần chuẩn bị lại dữ liệu?

Dữ liệu MTHv2 gốc được tổ chức ở **mức trang tài liệu**, trong khi mô hình OCR Recognition được sử dụng trong đồ án nhận đầu vào là **một dòng văn bản**.

Vì vậy, không thể sử dụng trực tiếp ảnh trang trong raw dataset để huấn luyện mô hình recognition.

Script `source/prepare_mthv2.py` thực hiện các bước:

* Đọc official `train.txt` và `test.txt` của MTHv2.
* Xác định từng trang thuộc `MTH1000`, `MTH1200` hoặc `TKH`.
* Sử dụng polygon annotation trong `label_textline` để crop từng dòng văn bản.
* Hiệu chỉnh phối cảnh cho từng vùng text-line.
* Xoay các crop theo chiều đọc thống nhất khi cần thiết.
* Loại bỏ các crop lỗi hoặc có kích thước quá nhỏ.
* Sinh các file manifest phục vụ training và evaluation.

Nói ngắn gọn, bước preprocessing chuyển dữ liệu từ:

```text
Page-level document images
        ↓
Text-line OCR samples
```

để phù hợp với bài toán **OCR Recognition**.

## Chia tập Train / Validation / Test

Project sử dụng official train/test split của MTHv2.

Official training set gồm **2399 trang** và được chia tiếp thành:

* **Train:** 90%
* **Validation:** 10%
* **Test:** giữ nguyên official test set

Validation set được tạo với:

```text
seed = 2026
```

nhằm đảm bảo việc chia dữ liệu có thể được tái lập chính xác.

## Chuẩn bị dữ liệu

Từ thư mục gốc của project, chạy:

```bash
python source/prepare_dataset/prepare_mthv2.py \
  --root dataset/raw_dataset/TKHMTH2200 \
  --train-split dataset/raw_dataset/train.txt \
  --test-split dataset/raw_dataset/test.txt \
  --output dataset/processed/MTHv2 \
  --val-ratio 0.10 \
  --seed 2026 \
  --overwrite
```

Kết quả preprocessing:

```text
Official train pages: 2399
Official test pages : 800

train: 2159 pages, 72563 text-line images
val  :  240 pages,  7753 text-line images
test :  800 pages, 25262 text-line images

Skipped crops    : 1
Train characters : 6063
```

Phân bố theo từng tập con:

| Split      | Pages | Text-line crops | MTH1000 | MTH1200 | TKH |
| ---------- | ----: | --------------: | ------: | ------: | --: |
| Train      |  2159 |           72563 |     712 |     791 | 656 |
| Validation |   240 |            7753 |      65 |      81 |  94 |
| Test       |   800 |           25262 |     223 |     328 | 249 |

## Dữ liệu sau preprocessing

Sau khi xử lý, dữ liệu được lưu tại:

```text
dataset/processed/MTHv2/
├── images/
│   ├── train/
│   ├── val/
│   └── test/
├── train.tsv
├── val.tsv
├── test.tsv
├── splits.json
├── skipped.json
└── train_characters.txt
```

Trong đó:

* `images/`: các ảnh text-line đã được crop từ ảnh trang gốc.
* `train.tsv`, `val.tsv`, `test.tsv`: manifest chứa đường dẫn ảnh và ground-truth tương ứng.
* `splits.json`: thông tin các trang thuộc từng split.
* `skipped.json`: các mẫu bị bỏ qua trong quá trình preprocessing.
* `train_characters.txt`: tập ký tự xuất hiện trong training set.
