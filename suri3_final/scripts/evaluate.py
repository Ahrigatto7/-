import spacy
from pathlib import Path
import json

# 모델과 테스트셋 불러오기
model_path = Path("models/ner_model/model-best")
nlp = spacy.load(model_path)
test_path = Path("data/test_data.jsonl")

# 정확도 측정
with test_path.open(encoding="utf-8") as f:
    lines = [json.loads(line) for line in f.readlines()]

total, correct = 0, 0
for item in lines:
    doc = nlp(item["text"])
    pred_ents = {(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents}
    true_ents = {tuple(e) for e in item["entities"]}
    total += len(true_ents)
    correct += len(pred_ents & true_ents)

precision = correct / (len(pred_ents) + 1e-5)
recall = correct / (total + 1e-5)
f1 = 2 * precision * recall / (precision + recall + 1e-5)

print(f"🔍 평가 결과 — Precision: {precision:.2f}, Recall: {recall:.2f}, F1: {f1:.2f}")
