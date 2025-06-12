
import streamlit as st
import subprocess
import os
import json
from pathlib import Path
import sys

# ✅ Add scripts/ to import path
sys.path.append(str(Path(__file__).resolve().parent / "scripts"))
from case_to_json import extract_saju_rules

# 페이지 설정
st.set_page_config(page_title="NER 전체 파이프라인", layout="wide")
st.title("🔄 NER 전체 자동화 파이프라인")

# 경로 설정
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)
rule_path = data_dir / "rules_from_saju_cases.json"
train_file = data_dir / "training_data.jsonl"
test_file = data_dir / "test_data.jsonl"

# 1. 규칙 JSON 업로드
uploaded_file = st.file_uploader("📤 규칙 JSON 파일 업로드 (rules_from_saju_cases.json)", type="json")
if uploaded_file is not None:
    with open(rule_path, "wb") as f:
        f.write(uploaded_file.read())
    st.success("✅ 규칙 파일 업로드 완료")

    # 규칙 추출
    rules = extract_saju_rules(rule_path)
    st.info(f"🔍 총 {len(rules)}개의 규칙 추출됨")
    st.json(rules[:5])

    # 학습 데이터 생성
    from random import shuffle
    examples = []
    seen = set()
    for rule in rules:
        if not rule["condition"] or not rule["result"]:
            continue
        text = f"조건: {rule['condition']} → {rule['result']}"
        if text in seen:
            continue
        seen.add(text)
        start_cond = text.find(rule['condition'])
        end_cond = start_cond + len(rule['condition'])
        start_res = text.find(rule['result'])
        end_res = start_res + len(rule['result'])
        entities = [
            [start_cond, end_cond, "조건"],
            [start_res, end_res, "결과"]
        ]
        examples.append({"text": text, "entities": entities})

    shuffle(examples)
    split = int(0.8 * len(examples))
    with open(train_file, "w", encoding="utf-8") as f:
        for item in examples[:split]:
            json.dump(item, f, ensure_ascii=False)
            f.write("\n")
    with open(test_file, "w", encoding="utf-8") as f:
        for item in examples[split:]:
            json.dump(item, f, ensure_ascii=False)
            f.write("\n")

    st.success("📄 학습/테스트 데이터 생성 완료")

# 학습 및 평가 실행 버튼
if train_file.exists() and test_file.exists():
    if st.button("🚀 모델 학습 시작"):
        with st.spinner("학습 중..."):
            result = subprocess.run(["python", "scripts/train.py"], capture_output=True, text=True)
        st.code(result.stdout + result.stderr)

    if st.button("📊 모델 평가 실행"):
        with st.spinner("평가 중..."):
            result = subprocess.run(["python", "scripts/evaluate.py"], capture_output=True, text=True)
        st.code(result.stdout + result.stderr)
else:
    st.warning("📂 학습/평가를 위해 먼저 규칙 파일을 업로드하세요.")
