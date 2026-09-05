## Đánh giá mô hình

Mô hình được đánh giá trên **official test set** của MTHv2 sau bước preprocessing.

Tập test gồm:

```text
800 pages
25262 text-line images
```

Script đánh giá sử dụng:

```text
source/evaluate_paddleocr_b0.py
```

Script thực hiện các bước:

* Đọc `test.tsv`.
* Load từng ảnh text-line từ tập test.
* Thực hiện inference bằng mô hình PaddleOCR Recognition.
* Chuẩn hóa Unicode theo chuẩn `NFC` cho cả ground truth và prediction.
* Tính Levenshtein edit distance cho từng mẫu.
* Tính các metric:

  * Character Error Rate (CER)
  * Exact-match accuracy
  * Mean model confidence
  * Inference throughput
* Lưu toàn bộ prediction và metric ra file.

### Đánh giá baseline PP-OCRv5

Baseline sử dụng model pretrained chính thức:

```bash
python source/evaluate_paddleocr_b0.py \
  --dataset-root dataset/processed/MTHv2 \
  --manifest test.tsv \
  --output-dir outputs/B0_MTHv2 \
  --model-name PP-OCRv5_server_rec \
  --device gpu:0 \
  --batch-size 8
```

Khi không truyền `--model-dir`, PaddleOCR sẽ sử dụng model pretrained tương ứng với `--model-name`.

### Đánh giá model đã fine-tune

Đối với model đã fine-tune và export sang inference model:

```bash
python source/evaluate_paddleocr_b0.py \
  --dataset-root dataset/processed/MTHv2 \
  --manifest test.tsv \
  --model-name PP-OCRv5_server_rec \
  --model-dir model/best_model_infer \
  --experiment B1 \
  --weights-label best_model \
  --output-dir outputs/B1_best_model \
  --device gpu:0 \
  --batch-size 8
```

Trong đó:

* `--dataset-root`: thư mục dataset đã preprocess.
* `--manifest`: tập dữ liệu cần đánh giá.
* `--model-name`: tên kiến trúc/model PaddleOCR.
* `--model-dir`: đường dẫn tới inference model đã export.
* `--experiment`: tên experiment.
* `--weights-label`: nhãn của checkpoint/model.
* `--output-dir`: thư mục lưu kết quả.
* `--device`: thiết bị inference.
* `--batch-size`: batch size khi inference.

### Metric

#### Character Error Rate

CER được tính trên toàn bộ corpus:

```text
CER = Tổng Levenshtein edit distance
      -----------------------------
      Tổng số ký tự ground truth
```

Trong đó edit distance gồm ba loại lỗi:

* insertion
* deletion
* substitution

CER càng thấp thì mô hình càng tốt.

Lưu ý rằng script tính **corpus-level CER**, không phải trung bình `sample_cer` của từng dòng.

#### Exact-match accuracy

Một text-line chỉ được tính là đúng khi prediction khớp hoàn toàn với ground truth:

```text
Exact-match accuracy =
    Số dòng prediction == ground truth
    -----------------------------------
             Tổng số dòng
```

### Output

Sau khi chạy evaluation:

```text
outputs/<experiment>/
├── predictions.tsv
└── metrics.json
```

`predictions.tsv` chứa kết quả theo từng text-line:

```text
image_path
page_id
line_number
ground_truth
prediction
confidence
edit_distance
gt_length
pred_length
sample_cer
exact_match
```

`metrics.json` chứa kết quả tổng hợp như:

```text
num_samples
num_ground_truth_characters
total_edit_distance
cer
exact_match_accuracy
mean_model_confidence
elapsed_seconds
lines_per_second
milliseconds_per_line
```

Thứ tự của `predictions.tsv` được giữ nguyên theo thứ tự của `test.tsv`; kết quả không được sort theo CER.
