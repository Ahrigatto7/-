import spacy
from spacy.cli.train import train
from pathlib import Path

# 설정
output_dir = Path("suam_ner_model")
config_path = Path("config.cfg")
train_data_path = Path("suam_ner_manual_review.jsonl")  # 수동 검토본 사용

# 기본 config 파일 생성
if not config_path.exists():
    from spacy.cli.init_config import init_config
    init_config(overwrite=True, lang="xx", pipeline=["ner"], output_file=config_path)

# 학습 실행
train(
    config_path=config_path,
    output_path=output_dir,
    overrides={
        "paths.train": str(train_data_path),
        "paths.dev": str(train_data_path),
        "training.max_steps": 300,
        "training.eval_frequency": 50
    }
)

print(f"✅ 모델 학습 완료: {output_dir}")
