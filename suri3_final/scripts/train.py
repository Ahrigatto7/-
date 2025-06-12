import spacy
from spacy.cli.train import train
from pathlib import Path
from spacy.cli.data_convert import convert

# 경로 설정
config_path = Path("config/base_config.cfg")
output_path = Path("models/ner_model")
data_path = Path("data/training_data.jsonl")

# JSONL → spaCy 형식으로 변환
convert(str(data_path), "data", "json", n_splits=1)

# 학습 실행
train(config_path, output_path=output_path)
print(f"✅ 모델 학습 완료 → 저장 위치: {output_path}")
