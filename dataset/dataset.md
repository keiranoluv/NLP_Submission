# MTHv2 Dataset

Dự án này sử dụng bộ dữ liệu **MTHv2 (Multiple Tripitaka in Han v2)** cho bài toán nhận dạng văn bản Hán cổ.

MTHv2 gồm ba tập con chính:

* **MTH1000**
* **MTH1200**
* **TKH**

Bộ dữ liệu cung cấp ảnh tài liệu lịch sử cùng với các loại nhãn như:

* Nhãn theo dòng văn bản
* Nhãn theo ký tự
* Nhãn đường biên/bố cục tài liệu

## Nguồn dữ liệu

- Repository chính thức: https://github.com/HCIILAB/MTHv2_Datasets_Release

- Có thể download trực tiếp tại link: https://drive.google.com/file/d/1JOFWYmiM2Ljcn1qJII2yHSGNA_0eouaj/view

## Chuẩn bị dữ liệu

Trong đồ án này, nhóm sử dụng official train/test split của MTHv2.

Tập train chính thức tiếp tục được chia thành:

* **Train:** 90%
* **Validation:** 10%
* **Test:** giữ nguyên official test set

Validation set được tạo cố định với `seed=2026` để đảm bảo khả năng tái lập kết quả.

Các vùng text-line được crop từ ảnh gốc dựa trên polygon annotation và chuyển thành các mẫu dùng cho bài toán OCR Recognition.

```bash
python scripts/data/prepare_mthv2.py \
  --root ~/dataset/TKHMTH2200 \
  --train-split ~/data/train.txt \
  --test-split ~/data/test.txt \
  --output ~/final_project/data/processed/MTHv2 \
  --val-ratio 0.10 \
  --seed 2026 \
  --overwrite
```

Sau khi xử lý, dữ liệu được lưu dưới dạng các ảnh text-line cùng với các file manifest:

```text
data/processed/MTHv2/
├── images/
├── train.tsv
├── val.tsv
├── test.tsv
├── splits.json
├── skipped.json
└── train_characters.txt
```
