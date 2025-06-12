import streamlit as st
import pandas as pd
from datetime import datetime
import os
import io
import fitz  # PyMuPDF
import docx

st.set_page_config(page_title="Documents Analyze", layout="wide")

st.title("📥 Documents Analyze")
st.markdown(":green[지식 기반 자동 해석 도구]입니다. 규칙과 개념 데이터를 업로드하고 조건을 입력하거나 문서를 분석합니다.")

# Upload document files (PDF, TXT, DOCX)
st.subheader("📎 문서 업로드 및 미리보기")
uploaded_files = st.file_uploader("PDF / TXT / Word 파일 업로드", type=["pdf", "txt", "docx"], accept_multiple_files=True)

def extract_text_from_pdf(file):
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
        return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = "
".join([para.text for para in doc.paragraphs])
    return text

if uploaded_files:
    for uploaded_file in uploaded_files:
        st.markdown(f"### 📄 파일: `{uploaded_file.name}`")
        file_ext = uploaded_file.name.split('.')[-1].lower()
        content = ""
        try:
            if file_ext == "pdf":
                content = extract_text_from_pdf(uploaded_file)
            elif file_ext == "txt":
                content = uploaded_file.read().decode("utf-8")
            elif file_ext == "docx":
                content = extract_text_from_docx(uploaded_file)
            else:
                st.warning("지원하지 않는 파일 형식입니다.")
            if content:
                st.text_area("📜 미리보기", content[:3000], height=300)
        except Exception as e:
            st.error(f"❌ 파일 처리 중 오류 발생: {e}")

# Upload rules and concepts CSVs
log_file = "results.csv"
if os.path.exists(log_file):
    result_log = pd.read_csv(log_file)
else:
    result_log = pd.DataFrame(columns=["timestamp", "day", "branch", "element", "result"])

concept_file = st.file_uploader("🧠 개념 CSV 업로드", type="csv")
rule_file = st.file_uploader("📋 규칙 CSV 업로드", type="csv")

if concept_file:
    concepts_df = pd.read_csv(concept_file)
    st.subheader("📘 개념 테이블")
    filter_type = st.selectbox("유형 필터", options=["전체"] + sorted(concepts_df["type"].unique()))
    if filter_type == "전체":
        st.dataframe(concepts_df)
    else:
        st.dataframe(concepts_df[concepts_df["type"] == filter_type])

if rule_file:
    rules_df = pd.read_csv(rule_file)
    st.subheader("📗 규칙 테이블")
    filter_topic = st.selectbox("주제 필터", options=["전체"] + sorted(rules_df["topic"].dropna().unique()))
    if filter_topic == "전체":
        st.dataframe(rules_df)
    else:
        st.dataframe(rules_df[rules_df["topic"] == filter_topic])

    st.markdown("---")
    st.subheader("🔍 자동 해석 실행")

    with st.form("input_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            day = st.text_input("일간 (예: 갑戌)", key="day")
        with col2:
            branch = st.text_input("시지 (예: 寅)", key="branch")
        with col3:
            element = st.text_input("자식성 (예: 丁)", key="element")
        submitted = st.form_submit_button("🧠 해석 실행")

    if submitted:
        if not all([day, branch, element]):
            st.warning("⚠️ 모든 입력값을 채워주세요.")
        else:
            matched = rules_df[
                rules_df["condition"].astype(str).str.contains(day, na=False) |
                rules_df["condition"].astype(str).str.contains(branch, na=False) |
                rules_df["condition"].astype(str).str.contains(element, na=False)
            ]

            summary = ""
            if not matched.empty:
                invalids = matched[matched["topic"] == "invalidation"]
                overrides = matched[matched["topic"] == "override"]
                base = matched[~matched["topic"].isin(["invalidation", "override"])]

                if not invalids.empty:
                    st.error("🚫 자식 없음 판정 (무효화 규칙 적용)")
                    st.dataframe(invalids[["rule_id", "condition", "outcome"]])
                    summary = f"무효화 적용: {invalids['rule_id'].iloc[0]}"
                elif not overrides.empty:
                    st.warning("🔁 성별 전환 또는 우선 판정")
                    st.dataframe(overrides[["rule_id", "condition", "outcome"]])
                    summary = f"성별 전환: {overrides['rule_id'].iloc[0]}"
                elif not base.empty:
                    st.success("✅ 일반 해석 규칙 적용")
                    st.dataframe(base[["rule_id", "condition", "outcome"]])
                    summary = f"일반 적용: {base['rule_id'].iloc[0]}"
                else:
                    st.info("🔍 해당 조건에 적용되는 규칙이 없습니다.")
                    summary = "해당 없음"
            else:
                st.info("🔍 해당 조건에 적용되는 규칙이 없습니다.")
                summary = "해당 없음"

            # Save result
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result_log.loc[len(result_log)] = [timestamp, day, branch, element, summary]
            result_log.to_csv(log_file, index=False)
            st.success(f"📌 결과 저장 완료 ({log_file})")

    st.markdown("---")
    st.subheader("📊 이전 해석 기록")
    st.dataframe(result_log)

# -------------------------------
# 📌 개념 / 규칙 추출 함수 예시 (간단한 키워드 기반 추출)
# -------------------------------

st.markdown("---")
st.subheader("🧠 문서에서 개념 및 규칙 자동 추출 (실험적 기능)")

def extract_concepts_rules(text):
    lines = text.split("\n")
    concepts, rules = [], []
    for line in lines:
        if "개념:" in line:
            parts = line.split("개념:")
            if len(parts) > 1:
                concepts.append(parts[1].strip())
        elif "규칙:" in line or "rule" in line.lower():
            parts = line.split("규칙:")
            if len(parts) > 1:
                rules.append(parts[1].strip())
    return concepts, rules

for uploaded_file in uploaded_files:
    file_ext = uploaded_file.name.split('.')[-1].lower()
    text = ""
    try:
        if file_ext == "pdf":
            text = extract_text_from_pdf(uploaded_file)
        elif file_ext == "txt":
            text = uploaded_file.read().decode("utf-8")
        elif file_ext == "docx":
            text = extract_text_from_docx(uploaded_file)

        if text:
            concepts, rules = extract_concepts_rules(text)
            if concepts:
                st.success(f"🔍 추출된 개념 {len(concepts)}개")
                st.write(concepts)
            if rules:
                st.info(f"📋 추출된 규칙 {len(rules)}개")
                st.write(rules)
            if not concepts and not rules:
                st.warning("⚠️ 규칙 또는 개념으로 추정되는 항목을 찾을 수 없습니다.")
    except Exception as e:
        st.error(f"❌ 추출 중 오류 발생: {e}")
