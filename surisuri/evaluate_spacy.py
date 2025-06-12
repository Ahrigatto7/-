import spacy
from pathlib import Path
import json
from spacy.scorer import Scorer
from spacy.training import Example

model_path = Path("suam_ner_model/model-best")
test_path = Path("test_set.jsonl")

if not model_path.exists():
    raise FileNotFoundError("❗ 모델이 존재하지 않습니다.")
if not test_path.exists():
    raise FileNotFoundError("❗ 테스트셋이 존재하지 않습니다.")

nlp = spacy.load(model_path)

examples = []
with open(test_path, encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        doc = nlp.make_doc(data["text"])
        example = Example.from_dict(doc, {"entities": data["entities"]})
        examples.append(example)

scorer = Scorer()
results = scorer.score(examples)

print("📊 평가 결과 (NER)")
print(results["ents_p"], "% precision")
print(results["ents_r"], "% recall")
print(results["ents_f"], "% F1")
