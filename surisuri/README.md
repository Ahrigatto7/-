# 수암명리 NER 통합 앱

이 프로젝트는 수암명리학 기반 문서에서 개체(용어, 조건, 결과 등)를 자동 추출하고, 규칙을 연결하는 AI 기반 분석 도구입니다.

## 🧠 주요 기능
- 📥 문서 업로드 및 문장 자동 추출
- 🔍 spaCy 기반 개체명 인식(NER)
- 🧠 KoNLPy 형태소 기반 NER
- ✍ 자동 태깅 검토 및 JSONL 학습셋 편집
- 📦 ZIP 다운로드

## 🚀 실행 방법 (로컬)

```bash
pip install -r requirements.txt
streamlit run app_integrated.py
```

## 🌐 배포 (Streamlit Cloud)
1. 본 코드를 GitHub에 업로드
2. [https://streamlit.io/cloud](https://streamlit.io/cloud) 에서 배포 시작
3. 파일 구조 예시:
```
📦 프로젝트 루트
├── app_integrated.py
├── requirements.txt
├── rules.csv / concepts.csv
├── suam_ner_model/
├── test_set.jsonl
```

## 📌 모델
- 모델은 `suam_ner_model/model-best` 위치에 있어야 합니다.
- 학습은 `train_spacy_updated.py` 사용
