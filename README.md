# NLP Submission - Nhận dạng văn bản Hán cổ với PaddleOCR

Repository này chứa mã nguồn, hướng dẫn chuẩn bị dữ liệu, huấn luyện và đánh giá các mô hình PaddleOCR trên bộ dữ liệu **MTHv2**.

Mục tiêu của repository là giúp người đọc có thể tự tái lập quy trình:

```text
Tải dataset
→ Tiền xử lý dữ liệu
→ Huấn luyện / tải checkpoint
→ Export model inference
→ Chạy evaluation
→ Kiểm tra kết quả
```

---

## 1. Cấu trúc repository

```text
NLP_Submission/
├── dataset/
│   └── README.md
├── model/
│   └── README.md
├── outputs/
│   ├── B1/
│   ├── B2/
│   ├── B3/
│   └── PP-OCRv6_medium_B1/
├── source/
│   ├── eval/
│   │   └── eval_mthv2.py
│   ├── prepare_dataset/
│   │   ├── prepare_mthv2.py
│   │   └── prepare_mthv2_vocab.py
│   ├── train/
│   │   ├── PP-OCR-v5_B1.ipynb
│   │   ├── PP-OCR-v5_B2.ipynb
│   │   ├── PP-OCR-v5_B3.ipynb
│   │   └── PP-OCR-v6.ipynb
│   └── ppocrv5_mthv2_expanded.txt
└── third_party/
    └── PaddleOCR/
```

---

## 2. Clone repository

Clone repository cùng PaddleOCR submodule:

```bash
git clone --recursive https://github.com/keiranoluv/NLP_Submission.git
cd NLP_Submission
```

Nếu đã clone repository nhưng chưa có submodule:

```bash
git submodule update --init --recursive
```

---

## 3. Cài đặt môi trường

Khuyến nghị sử dụng Conda với Python 3.12:

```bash
conda create -n paddleocr python=3.12 -y
conda activate paddleocr
```

Cài đặt PaddlePaddle GPU phù hợp với môi trường CUDA 12.6:

```bash
python -m pip install paddlepaddle-gpu==3.3.0 \
  -i https://www.paddlepaddle.org.cn/packages/stable/cu126/
```

Sau đó cài đặt các dependency còn lại của project:

```bash
pip install -r requirements.txt
```

Nên sử dụng đúng phiên bản PaddlePaddle, PaddleOCR và PaddleX đã dùng trong quá trình thực nghiệm để đảm bảo kết quả có thể tái lập.

---

## 4. Dataset

Project sử dụng bộ dữ liệu **MTHv2 (Multiple Tripitaka in Han v2)**.

Thông tin chi tiết và link tải dataset được ghi tại:

```text
dataset/README.md
```

Sau khi tải raw dataset, cấu trúc mong đợi:

```text
dataset/raw_dataset/
├── TKHMTH2200/
│   ├── MTH1000/
│   ├── MTH1200/
│   └── TKH/
├── train.txt
└── test.txt
```

### Tiền xử lý dữ liệu

Chạy:

```bash
python source/prepare_dataset/prepare_mthv2.py   --root dataset/raw_dataset/TKHMTH2200   --train-split dataset/raw_dataset/train.txt   --test-split dataset/raw_dataset/test.txt   --output dataset/processed/MTHv2   --val-ratio 0.10   --seed 2026   --overwrite
```

Dữ liệu sau khi xử lý:

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

Có thể tải trực tiếp bản dataset đã preprocessing từ link được cung cấp trong `dataset/README.md` nếu chỉ muốn reproduce bước evaluation.

---

## 5. Custom vocabulary

Experiment **B2** và **B3** sử dụng vocabulary mở rộng cho MTHv2.

File đã tạo sẵn:

```text
source/ppocrv5_mthv2_expanded.txt
```

Có thể tạo lại bằng:

```bash
python source/prepare_dataset/prepare_mthv2_vocab.py   --base-dict third_party/PaddleOCR/ppocr/utils/dict/ppocrv5_dict.txt   --train-tsv dataset/processed/MTHv2/train.tsv   --output-dict source/ppocrv5_mthv2_expanded.txt
```

---

## 6. Training

Quá trình huấn luyện các model trong project được thực hiện trên **Kaggle Notebook** với GPU.

Các notebook tương ứng với từng experiment:

| Experiment         | Model                                        | Kaggle Notebook                                                                                                    |
| ------------------ | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| B1                 | PP-OCRv5 Server                              | [PaddleOCR-Fine-Tuning - B1](https://www.kaggle.com/code/zephyrvn/paddleocr-fine-tuning?scriptVersionId=340862365) |
| B2                 | PP-OCRv5 Server + Expanded Vocabulary        | [PaddleOCR-Fine-Tuning - B2](https://www.kaggle.com/code/zephyrvn/paddleocr-fine-tuning?scriptVersionId=341074260) |
| B3                 | PP-OCRv5 Server + Rare-character Fine-tuning | [PaddleOCR-Fine-Tuning - B3](https://www.kaggle.com/code/zephyrvn/paddleocr-fine-tuning?scriptVersionId=341204845) |
| PP-OCRv6 Medium B1 | PP-OCRv6 Medium                              | [PaddleOCR-Fine-Tuning-PPOCR-v6](https://www.kaggle.com/code/zephyrvn/paddleocr-fine-tuning-ppocr-v6)              |

Bản notebook tương ứng cũng được lưu trong repository tại:

```text
source/train/
├── PP-OCR-v5_B1.ipynb
├── PP-OCR-v5_B2.ipynb
├── PP-OCR-v5_B3.ipynb
└── PP-OCR-v6.ipynb
```

Các notebook trong repository được cung cấp để tham khảo và hỗ trợ việc tái lập quy trình huấn luyện. Các kết quả model được sử dụng trong báo cáo được tạo từ các Kaggle Notebook ở trên.

Checkpoint sau khi huấn luyện không được lưu trực tiếp trên GitHub do kích thước lớn. Link tải checkpoint và cấu trúc thư mục model được mô tả tại:

```text
model/README.md
```

Cấu trúc mong đợi:

```text
model/
├── PP-OCR-v5/
│   ├── model_B1.pdparams
│   ├── model_B2.pdparams
│   └── model_B3.pdparams
└── PP-OCR-v6/
    └── model.pdparams
```


---

## 7. Export model để inference

### B1

```bash
cd third_party/PaddleOCR

python tools/export_model.py   -c configs/rec/PP-OCRv5/PP-OCRv5_server_rec.yml   -o   Global.pretrained_model=../../model/PP-OCR-v5/model_B1.pdparams   Global.save_inference_dir=../../model/PP-OCR-v5/model_B1_infer

cd ../..
```

### B2

```bash
cd third_party/PaddleOCR

python tools/export_model.py   -c configs/rec/PP-OCRv5/PP-OCRv5_server_rec.yml   -o   Global.pretrained_model=../../model/PP-OCR-v5/model_B2.pdparams   Global.save_inference_dir=../../model/PP-OCR-v5/model_B2_infer   Global.character_dict_path=../../source/ppocrv5_mthv2_expanded.txt

cd ../..
```

### B3

```bash
cd third_party/PaddleOCR

python tools/export_model.py   -c configs/rec/PP-OCRv5/PP-OCRv5_server_rec.yml   -o   Global.pretrained_model=../../model/PP-OCR-v5/model_B3.pdparams   Global.save_inference_dir=../../model/PP-OCR-v5/model_B3_infer   Global.character_dict_path=../../source/ppocrv5_mthv2_expanded.txt

cd ../..
```

### PP-OCRv6 Medium

```bash
cd third_party/PaddleOCR

python tools/export_model.py   -c configs/rec/PP-OCRv6/PP-OCRv6_medium_rec.yml   -o   Global.pretrained_model=../../model/PP-OCR-v6/model.pdparams   Global.save_inference_dir=../../model/PP-OCR-v6/model_infer

cd ../..
```

---

## 8. Evaluation

Script evaluation:

```text
source/eval/eval_mthv2.py
```

### B1

```bash
python source/eval/eval_mthv2.py   --dataset-root dataset/processed/MTHv2   --manifest test.tsv   --model-name PP-OCRv5_server_rec   --model-dir model/PP-OCR-v5/model_B1_infer   --experiment B1   --weights-label model_B1   --output-dir outputs/B1   --device gpu:0   --batch-size 8
```

### B2

```bash
python source/eval/eval_mthv2.py   --dataset-root dataset/processed/MTHv2   --manifest test.tsv   --model-name PP-OCRv5_server_rec   --model-dir model/PP-OCR-v5/model_B2_infer   --experiment B2   --weights-label model_B2   --output-dir outputs/B2   --device gpu:0   --batch-size 8
```

### B3

```bash
python source/eval/eval_mthv2.py   --dataset-root dataset/processed/MTHv2   --manifest test.tsv   --model-name PP-OCRv5_server_rec   --model-dir model/PP-OCR-v5/model_B3_infer   --experiment B3   --weights-label model_B3   --output-dir outputs/B3   --device gpu:0   --batch-size 8
```

### PP-OCRv6 Medium

```bash
python source/eval/eval_mthv2.py   --dataset-root dataset/processed/MTHv2   --manifest test.tsv   --model-name PP-OCRv6_medium_rec   --model-dir model/PP-OCR-v6/model_infer   --experiment PP-OCRv6_medium_B1   --weights-label model   --output-dir outputs/PP-OCRv6_medium_B1   --device gpu:0   --batch-size 8
```

Nếu không có GPU, có thể đổi:

```text
--device gpu:0
```

thành:

```text
--device cpu
```

---

## 9. Kết quả

Sau khi evaluation, mỗi experiment sinh ra:

```text
outputs/<experiment>/
├── predictions.tsv
└── metrics.json
```

Trong đó:

- `predictions.tsv`: prediction của từng ảnh.
- `metrics.json`: CER, exact-match accuracy, confidence và thời gian inference.

Các kết quả đã chạy của nhóm được lưu sẵn trong thư mục:

```text
outputs/
```

### Tổng hợp kết quả thực nghiệm

| Experiment         | Model                                        |       CER | Exact Match Accuracy | Mean Confidence |
| ------------------ | -------------------------------------------- | --------: | -------------------: | --------------: |
| B1                 | PP-OCRv5 Server                              |     3.25% |               75.98% |          98.21% |
| B2                 | PP-OCRv5 Server + Expanded Vocabulary        |     2.39% |               82.46% |          97.66% |
| B3                 | PP-OCRv5 Server + Rare-character Fine-tuning | **2.19%** |           **83.85%** |          97.35% |
| PP-OCRv6 Medium B1 | PP-OCRv6 Medium                              |     3.51% |               74.22% |          97.73% |

Tất cả các experiment được đánh giá trên cùng tập test gồm **25,262 text-line images** và **263,342 ground-truth characters**.


---

## 10. Quy trình reproduce nhanh

Nếu chỉ muốn kiểm tra lại kết quả cuối cùng:

```text
1. Clone repository + submodule
2. Cài environment
3. Tải dataset đã preprocessing
4. Tải trained checkpoints
5. Export checkpoint sang inference model
6. Chạy eval_mthv2.py
7. So sánh metrics với outputs/
```

Nếu muốn reproduce toàn bộ pipeline từ đầu:

```text
Raw MTHv2
→ prepare_mthv2.py
→ train model
→ export_model.py
→ eval_mthv2.py
→ metrics.json
```

---

## 11. Third-party

Project sử dụng PaddleOCR tại:

```text
third_party/PaddleOCR/
```

PaddleOCR được quản lý dưới dạng Git submodule.

---

## 12. Báo cáo

Báo cáo đồ án được nộp riêng cùng repository này.
