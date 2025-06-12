import streamlit as st
import json

st.set_page_config(page_title="NER 태깅 편집기", layout="wide")
st.title("✍ 수암명리 NER 편집기")

uploaded = st.file_uploader("JSONL 학습 파일 업로드", type="jsonl")
if uploaded:
    data = [json.loads(line) for line in uploaded.readlines()]
    st.session_state["data"] = data

if "data" in st.session_state:
    data = st.session_state["data"]
    edited_data = []

    for i, item in enumerate(data[:10]):
        st.markdown(f"---\n#### 문장 {i+1}")
        st.text(item["text"])
        ents = item["entities"]
        new_ents = []

        for j, ent in enumerate(ents):
            start, end, label = ent
            st.write(f"🔹 `{item['text'][start:end]}` ({label})")
            col1, col2, col3 = st.columns(3)
            new_start = col1.number_input(f"Start {j}", value=start, key=f"start_{i}_{j}")
            new_end = col2.number_input(f"End {j}", value=end, key=f"end_{i}_{j}")
            new_label = col3.selectbox(f"Label {j}", options=["TERM", "CONDITION", "OUTCOME"], index=["TERM", "CONDITION", "OUTCOME"].index(label), key=f"label_{i}_{j}")
            new_ents.append([int(new_start), int(new_end), new_label])

        edited_data.append({"text": item["text"], "entities": new_ents})

    st.markdown("---")
    if st.button("💾 JSONL 파일로 저장"):
        output = "\n".join([json.dumps(item, ensure_ascii=False) for item in edited_data])
        st.download_button("⬇️ 수정된 JSONL 다운로드", output, file_name="edited_training_data.jsonl", mime="text/json")
