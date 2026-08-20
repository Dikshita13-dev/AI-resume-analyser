import streamlit as st
import json
import re
import os
from groq import Groq
import pdfplumber
import docx

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

def extract_text_from_pdf(file) -> str:
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def extract_text_from_docx(file) -> str:
    doc = docx.Document(file)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

def extract_text(uploaded_file) -> str:
    name = uploaded_file.name.lower()
    if name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif name.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    elif name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8", errors="ignore")
    else:
        st.error("Unsupported file type. Please upload a PDF, DOCX, or TXT file.")
        return ""

def analyze_resume(api_key: str, resume_text: str, jd_text: str) -> dict:
    client = Groq(api_key=api_key)

    system_prompt = (
        "You are an expert technical recruiter and resume screener. "
        "You compare a candidate's resume against a job description and "
        "respond ONLY with valid JSON, no markdown fences, no preamble. "
        "The JSON schema must be exactly:\n"
        "{\n"
        '  "match_score": <integer 0-100>,\n'
        '  "matched_skills": [<strings>],\n'
        '  "missing_skills": [<strings>],\n'
        '  "strengths": [<strings>],\n'
        '  "gaps": [<strings>],\n'
        '  "summary": "<2-3 sentence overall verdict>",\n'
        '  "suggestions": [<strings, concrete resume improvement tips>]\n'
        "}"
    )

    user_prompt = (
        f"JOB DESCRIPTION:\n{jd_text}\n\n"
        f"RESUME:\n{resume_text}\n\n"
        "Analyze the fit and return the JSON described in the system prompt."
    )

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=1500,
    )

    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"^```(json)?|```$", "", raw, flags=re.MULTILINE).strip()
    return json.loads(raw)

st.title("📄 AI Resume Analyzer")
st.caption("Upload a resume and a job description — get an instant AI-powered match score.")

# Key comes from the environment, not from a text box or hardcoded string
api_key = os.environ.get("GROQ_API_KEY", "")

with st.sidebar:
    st.error("No GROQ_API_KEY found in environment. Set it before launching the app.")
    st.divider()
    st.markdown(
        "**How it works**\n"
        "1. Upload a resume (PDF/DOCX/TXT)\n"
        "2. Paste the job description\n"
        "3. Click Analyze\n"
        "4. Get a match score + skill gap breakdown"
    )

col1, col2 = st.columns(2)

with col1:
    st.subheader("Resume")
    resume_file = st.file_uploader("Upload resume", type=["pdf", "docx", "txt"])

with col2:
    st.subheader("Job Description")
    jd_text = st.text_area("Paste the job description here", height=300)

analyze_clicked = st.button("🔍 Analyze Match", type="primary", use_container_width=True)

if analyze_clicked:
    if not api_key:
        st.error("No API key found. Set GROQ_API_KEY before launching the app.")
    elif not resume_file:
        st.error("Please upload a resume.")
    elif not jd_text.strip():
        st.error("Please paste a job description.")
    else:
        with st.spinner("Extracting resume text..."):
            resume_text = extract_text(resume_file)

        if not resume_text:
            st.error("Couldn't extract text from that resume. Try a different file.")
        else:
            with st.spinner("Analyzing with AI..."):
                try:
                    result = analyze_resume(api_key, resume_text, jd_text)
                except Exception as e:
                    st.error(f"Something went wrong calling the AI: {e}")
                    result = None

            if result:
                score = result.get("match_score", 0)
                st.divider()
                st.subheader("Results")

                score_col, summary_col = st.columns([1, 3])
                with score_col:
                    st.metric("Match Score", f"{score}/100")
                    st.progress(min(max(score, 0), 100) / 100)
                with summary_col:
                    st.write(result.get("summary", ""))

                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**✅ Matched Skills**")
                    for s in result.get("matched_skills", []):
                        st.markdown(f"- {s}")
                    st.markdown("**💪 Strengths**")
                    for s in result.get("strengths", []):
                        st.markdown(f"- {s}")

                with c2:
                    st.markdown("**❌ Missing Skills**")
                    for s in result.get("missing_skills", []):
                        st.markdown(f"- {s}")
                    st.markdown("**⚠️ Gaps**")
                    for s in result.get("gaps", []):
                        st.markdown(f"- {s}")

                st.markdown("**📝 Suggestions to Improve Your Resume**")
                for s in result.get("suggestions", []):
                    st.markdown(f"- {s}")
