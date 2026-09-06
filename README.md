## B1
- Trước khi chạy eval (inference) phải chạy export mode để export mode về mode inference:

```
cd third_party/PaddleOCR
python tools/export_model.py \
  -c configs/rec/PP-OCRv5/PP-OCRv5_server_rec.yml \
  -o \
  Global.pretrained_model=../../model/PP-OCR-v5/model_B1.pdparams \
  Global.save_inference_dir=../../model/PP-OCR-v5/model_B1_infer
```

- Lệnh chạy eval:

```bash
python source/eval/eval_mthv2.py \
  --dataset-root dataset/processed/MTHv2 \
  --manifest test.tsv \
  --model-name PP-OCRv5_server_rec \
  --model-dir model/PP-OCR-v5/model_B1_infer \
  --experiment B1 \
  --weights-label model_B1 \
  --output-dir outputs/B1 \
  --device gpu:0 \
  --batch-size 8
```

## B2

```bash
cd third_party/PaddleOCR

python tools/export_model.py \
  -c configs/rec/PP-OCRv5/PP-OCRv5_server_rec.yml \
  -o \
  Global.pretrained_model=../../model/PP-OCR-v5/model_B2.pdparams \
  Global.save_inference_dir=../../model/PP-OCR-v5/model_B2_infer \
  Global.character_dict_path=../../source/ppocrv5_mthv2_expanded.txt
  ```

```bash
  python source/eval/eval_mthv2.py \
  --dataset-root dataset/processed/MTHv2 \
  --manifest test.tsv \
  --model-name PP-OCRv5_server_rec \
  --model-dir model/PP-OCR-v5/model_B2_infer \
  --experiment B2 \
  --weights-label model_B2 \
  --output-dir outputs/B2 \
  --device gpu:0 \
  --batch-size 8
  ```


  ### B3

  ```bash
cd third_party/PaddleOCR

python tools/export_model.py \
  -c configs/rec/PP-OCRv5/PP-OCRv5_server_rec.yml \
  -o \
  Global.pretrained_model=../../model/PP-OCR-v5/model_B3.pdparams \
  Global.save_inference_dir=../../model/PP-OCR-v5/model_B3_infer \
  Global.character_dict_path=../../source/ppocrv5_mthv2_expanded.txt
  ```

  ```
  cd ../..
  python source/eval/eval_mthv2.py \
  --dataset-root dataset/processed/MTHv2 \
  --manifest test.tsv \
  --model-name PP-OCRv5_server_rec \
  --model-dir model/PP-OCR-v5/model_B3_infer \
  --experiment B3 \
  --weights-label model_B3 \
  --output-dir outputs/B3 \
  --device gpu:0 \
  --batch-size 8
  ```
## PP-OCR-v6-medium

```
cd third_party/PaddleOCR

python tools/export_model.py \
  -c configs/rec/PP-OCRv6/PP-OCRv6_medium_rec.yml \
  -o \
  Global.pretrained_model=../../model/PP-OCR-v6/model.pdparams \
  Global.save_inference_dir=../../model/PP-OCR-v6/model_infer
```

```
cd ../..
python source/eval/eval_mthv2.py \
  --dataset-root dataset/processed/MTHv2 \
  --manifest test.tsv \
  --model-name PP-OCRv6_medium_rec \
  --model-dir model/PP-OCR-v6/model_infer \
  --experiment PP-OCRv6_medium_B1 \
  --weights-label model \
  --output-dir outputs/PP-OCRv6_medium_B1 \
  --device gpu:0 \
  --batch-size 8
  ```

  ## Vấn đề:

  ppocrv5_mthv2_expanded.txt ở đâu ra??

- Trước tiên phải lấy từ điển đó:

```bash
python source/prepare_dataset/prepare_mthv2_vocab.py \
  --base-dict third_party/PaddleOCR/ppocr/utils/dict/ppocrv5_dict.txt \
  --train-tsv dataset/processed/MTHv2/train.tsv \
  --output-dict source/ppocrv5_mthv2_expanded.txt
```