import streamlit as st
import spacy
from pathlib import Path
import pandas as pd
import random

st.set_page_config(page_title="수암명리 NER 분석", layout="wide")
st.title("🧠 수암명리 문장 분석기 (개체 인식 + 하이라이트 시각화)")

model_path = Path("suam_ner_model/model-best")
if not model_path.exists():
    st.error("❗ 학습된 모델이 없습니다. 먼저 train_spacy.py를 실행해주세요.")
    st.stop()

nlp = spacy.load(model_path)

text = st.text_area("📥 분석할 문장을 입력하세요", 
                    "자식성이 허투하면 성별이 바뀐다. 정인이 약하면 입양을 고려한다.", height=150)

if st.button("🔍 개체 분석"):
    doc = nlp(text)
    ents = [(ent.text, ent.label_, ent.start_char, ent.end_char) for ent in doc.ents]

    if ents:
        st.success(f"✅ 총 {len(ents)}개의 개체가 추출되었습니다.")
        df = pd.DataFrame(ents, columns=["텍스트", "레이블", "시작 위치", "끝 위치"])
        st.dataframe(df)

        # 시각화용 HTML
        color_map = {"TERM": "#ffcccc", "CONDITION": "#ccf2ff", "OUTCOME": "#d2f8d2"}
        highlighted = ""
        last_end = 0
        for ent in doc.ents:
            color = color_map.get(ent.label_, "#eeeeee")
            highlighted += text[last_end:ent.start_char]
            highlighted += f"<span style='background-color:{color};padding:2px 4px;border-radius:4px'>{ent.text}</span>"
            last_end = ent.end_char
        highlighted += text[last_end:]

        st.markdown("### 🔎 하이라이트 보기", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size: 16px; line-height: 2;'>{highlighted}</div>", unsafe_allow_html=True)
    else:
        st.warning("📭 추출된 개체가 없습니다.")
