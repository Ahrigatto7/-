import streamlit as st
import json

st.set_page_config(page_title="NER 태깅 편집기+", layout="wide")
st.title("✍ 수암명리 NER 편집기 (고급 기능 포함)")

PER_PAGE = 10

def load_data(uploaded_file):
    return [json.loads(line) for line in uploaded_file.readlines()]

def save_session(data):
    st.session_state["data"] = data

uploaded = st.file_uploader("📤 JSONL 학습 데이터 업로드", type="jsonl")
if uploaded:
    save_session(load_data(uploaded))

if "data" in st.session_state:
    data = st.session_state["data"]
    total_pages = (len(data) - 1) // PER_PAGE + 1
    page = st.number_input("📄 페이지 선택", min_value=1, max_value=total_pages, value=1, step=1)
    start_idx = (page - 1) * PER_PAGE
    end_idx = min(start_idx + PER_PAGE, len(data))
    new_data = []

    st.subheader(f"📄 {start_idx + 1} ~ {end_idx} 문장 편집")

    for i in range(start_idx, end_idx):
        item = data[i]
        st.markdown(f"---\n#### 문장 {i+1}")
        st.text(item["text"])
        ents = item["entities"]
        new_ents = []

        for j, ent in enumerate(ents):
            start, end, label = ent
            col1, col2, col3, col4 = st.columns([2, 2, 3, 1])
            new_start = col1.number_input(f"Start {i}_{j}", value=start, key=f"start_{i}_{j}")
            new_end = col2.number_input(f"End {i}_{j}", value=end, key=f"end_{i}_{j}")
            new_label = col3.selectbox(f"Label {i}_{j}", ["TERM", "CONDITION", "OUTCOME"], index=["TERM", "CONDITION", "OUTCOME"].index(label))
            delete_flag = col4.checkbox("삭제", key=f"del_{i}_{j}")
            if not delete_flag:
                new_ents.append([int(new_start), int(new_end), new_label])

        with st.expander("➕ 개체 추가", expanded=False):
            colx, coly, colz = st.columns(3)
            add_start = colx.number_input(f"Add Start {i}", value=0, key=f"add_start_{i}")
            add_end = coly.number_input(f"Add End {i}", value=0, key=f"add_end_{i}")
            add_label = colz.selectbox(f"Add Label {i}", ["TERM", "CONDITION", "OUTCOME"], key=f"add_label_{i}")
            if st.button("➕ 추가", key=f"btn_add_{i}"):
                new_ents.append([int(add_start), int(add_end), add_label])
                st.success("✅ 개체가 추가되었습니다.")

        new_data.append({"text": item["text"], "entities": new_ents})

    if st.button("💾 현재 페이지 저장"):
        for idx in range(start_idx, end_idx):
            data[idx] = new_data[idx - start_idx]
        save_session(data)
        st.success("📌 저장 완료")

    st.markdown("---")
    if st.button("⬇️ 전체 JSONL 다운로드"):
        output = "\n".join([json.dumps(item, ensure_ascii=False) for item in data])
        st.download_button("JSONL 파일 다운로드", output, file_name="edited_all.jsonl", mime="text/json")

else:
    st.info("🛈 먼저 JSONL 학습 파일을 업로드해주세요.")
