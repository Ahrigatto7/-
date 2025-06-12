import streamlit as st
import pandas as pd

st.set_page_config(page_title="자동 해석", layout="wide")

st.title("📥 수암명리 자동 해석 시스템 (Python Streamlit 버전)")

# CSV 업로드
concept_file = st.file_uploader("🧠 개념 CSV 업로드", type="csv", key="concepts")
rule_file = st.file_uploader("📋 규칙 CSV 업로드", type="csv", key="rules")

if concept_file:
    concepts_df = pd.read_csv(concept_file)
    st.subheader("개념 테이블")
    concept_filter = st.selectbox("유형 필터", options=["전체"] + sorted(concepts_df["type"].unique()))
    if concept_filter != "전체":
        st.dataframe(concepts_df[concepts_df["type"] == concept_filter])
    else:
        st.dataframe(concepts_df)

if rule_file:
    rules_df = pd.read_csv(rule_file)
    st.subheader("규칙 테이블")
    topic_filter = st.selectbox("주제 필터", options=["전체"] + sorted(rules_df["topic"].dropna().unique()))
    if topic_filter != "전체":
        st.dataframe(rules_df[rules_df["topic"] == topic_filter])
    else:
        st.dataframe(rules_df)

    st.markdown("---")
    st.subheader("🔍 자동 해석 입력")

    col1, col2, col3 = st.columns(3)
    with col1:
        day = st.text_input("일간 (예: 갑戌)")
    with col2:
        branch = st.text_input("시지 (예: 寅)")
    with col3:
        element = st.text_input("자식성 (예: 丁)")

    if st.button("🔎 해석 실행"):
        if day and branch and element:
            input_str = f"{day} {branch} {element}"
            matched = rules_df[
                rules_df["condition"].astype(str).str.contains(day, na=False) |
                rules_df["condition"].astype(str).str.contains(branch, na=False) |
                rules_df["condition"].astype(str).str.contains(element, na=False)
            ]

            invalids = matched[matched["topic"] == "invalidation"]
            overrides = matched[matched["topic"] == "override"]
            base = matched[~matched["topic"].isin(["invalidation", "override"])]

            if not invalids.empty:
                st.error("🚫 자식 없음 판정 (무효화 규칙 적용):")
                st.dataframe(invalids[["rule_id", "condition", "outcome"]])
            elif not overrides.empty:
                st.warning("🔁 성별 전환 또는 우선 판정:")
                st.dataframe(overrides[["rule_id", "condition", "outcome"]])
            elif not base.empty:
                st.success("✅ 일반 해석 규칙 적용:")
                st.dataframe(base[["rule_id", "condition", "outcome"]])
            else:
                st.info("🔍 해당 조건에 적용되는 규칙이 없습니다.")
        else:
            st.warning("⚠️ 모든 입력값을 채워주세요.")
