"""RESUME IQ Streamlit application."""

from __future__ import annotations

import json

import streamlit as st

from ml_features import calculate_tfidf_similarity
from resume_insights import build_resume_insights, gap_recommendation
from resume_parser import parse_resume


st.set_page_config(page_title="RESUME IQ | Career Analysis", page_icon="RI", layout="wide")


def inject_styles() -> None:
    st.markdown("""
    <style>
    :root { --ink:#121212; --panel:#1b1b1a; --paper:#f6f1e8; --muted:#aaa39a; --accent:#f28c28; }
    .stApp { background:var(--ink); color:var(--paper); } [data-testid="stHeader"] { background:rgba(18,18,18,.92); }
    .block-container { max-width:1180px; padding-top:2.25rem; padding-bottom:3rem; } h1,h2,h3,p,label { color:var(--paper)!important; }
    .eyebrow,.section-label { color:var(--accent); font-size:.76rem; font-weight:800; letter-spacing:.14em; text-transform:uppercase; }
    .hero { font-size:clamp(2.3rem,5vw,4.7rem); line-height:.98; letter-spacing:-.06em; font-weight:800; margin:.45rem 0; }
    .subtle { color:var(--muted)!important; font-size:1.05rem; max-width:650px; }
    .flow { display:flex; flex-wrap:wrap; gap:.55rem; align-items:center; color:var(--muted); font-size:.8rem; font-weight:700; letter-spacing:.04em; }
    .flow span { border:1px solid #393734; padding:.48rem .65rem; border-radius:999px; } .flow b { color:var(--accent); }
    .section-label { margin-top:2rem; } .card { background:var(--panel); border:1px solid #302f2c; border-radius:14px; padding:1.15rem 1.2rem; min-height:118px; }
    .card-title { color:var(--muted); font-size:.75rem; font-weight:800; letter-spacing:.1em; text-transform:uppercase; }
    .card-value { color:var(--paper); font-size:1.6rem; font-weight:750; line-height:1.25; margin:.2rem 0; overflow-wrap:anywhere; }
    .card-note { color:var(--muted); font-size:.85rem; } .skill { display:inline-block; padding:.32rem .58rem; margin:.16rem .16rem .16rem 0; border-radius:999px; background:#282724; color:#f7d7b3; border:1px solid #464139; font-size:.83rem; }
    .footer { color:var(--muted); font-size:.8rem; text-align:center; padding:2.5rem 0 0; }
    .stButton > button { background:var(--accent); border:0; color:#15110c; font-weight:800; border-radius:8px; padding:.66rem 1rem; }
    .stTextArea textarea, [data-testid="stFileUploader"] { background:#1b1b1a!important; color:var(--paper)!important; }
    </style>""", unsafe_allow_html=True)


def chips(items: list[str], empty: str) -> None:
    if items:
        st.markdown("".join(f'<span class="skill">{item}</span>' for item in items), unsafe_allow_html=True)
    else:
        st.caption(empty)


def card(title: str, value: str, note: str) -> None:
    st.markdown(f'<div class="card"><div class="card-title">{title}</div><div class="card-value">{value}</div><div class="card-note">{note}</div></div>', unsafe_allow_html=True)


def render_results(filename: str, insights: dict, keyword_score: float, ai_results: dict | None) -> None:
    match = insights["job_match"]
    coverage = f"{match['coverage']}%" if match and match["coverage"] is not None else "—"
    st.markdown('<div class="section-label">Analysis report</div>', unsafe_allow_html=True)
    st.subheader("Resume overview")
    columns = st.columns(4)
    with columns[0]: card("Resume", filename, "Parsed successfully")
    with columns[1]: card("Skills detected", str(len(insights["skills"])), "Rule-based catalog match")
    with columns[2]: card("Job coverage", coverage, "Explicit skill overlap")
    with columns[3]: card("Keyword similarity", f"{keyword_score:.0f}%" if match else "—", "TF-IDF, not an ATS score")
    left, right = st.columns([1.18, .82], gap="large")
    with left:
        st.markdown('<div class="section-label">Skills detected</div>', unsafe_allow_html=True)
        if not insights["skill_categories"]:
            st.info("No skills from the supported catalog were detected. This does not mean your resume has no skills.")
        for category, skills in insights["skill_categories"].items():
            st.markdown(f"**{category}**")
            chips(skills, "")
        st.markdown('<div class="section-label">Resume strengths</div>', unsafe_allow_html=True)
        for item in insights["strengths"] or ["No section or catalog signal was detected; review the uploaded file text."]:
            st.success(item)
        st.markdown('<div class="section-label">Areas to improve</div>', unsafe_allow_html=True)
        for item in insights["improvements"] or ["No basic structure gaps were flagged by the rule-based check."]:
            st.warning(item)
    with right:
        st.markdown('<div class="section-label">Job match</div>', unsafe_allow_html=True)
        if not match:
            st.info("Add a job description to compare explicit skills against the role.")
        elif not match["required_skills_detected"]:
            st.info("No skills from the supported catalog were found in the job description. This is not a judgment of fit.")
        else:
            st.markdown("**You have**")
            chips(match["matching_skills"], "No explicit catalogued overlaps found.")
            st.markdown("**Job requires / skill gaps**")
            chips(match["missing_skills"], "No gaps were found in the supported catalog.")
            st.caption("Coverage measures only explicit skills from the built-in catalog. It is not an official ATS score.")
        st.markdown('<div class="section-label">Improvement plan</div>', unsafe_allow_html=True)
        for skill in (match["missing_skills"] if match else [])[:5]:
            st.write(f"**{skill}** — {gap_recommendation(skill)}")
        if not match or not match["missing_skills"]:
            st.write("Use role-specific language from the job description where it truthfully reflects your experience.")
    st.markdown('<div class="section-label">Gemini career review</div>', unsafe_allow_html=True)
    if ai_results:
        evaluation, coaching = ai_results.get("evaluation", {}), ai_results.get("coaching", {})
        ai_left, ai_right = st.columns(2)
        with ai_left:
            st.markdown("**Gemini suggestions**")
            for item in evaluation.get("ats_suggestions", []) + evaluation.get("improved_bullet_points", []): st.write(f"• {item}")
        with ai_right:
            st.markdown("**Next steps from Gemini**")
            for item in coaching.get("learning_path", []) + coaching.get("mock_interview_questions", []): st.write(f"• {item}")
        with st.expander("View Gemini agent data"): st.json(ai_results)
    else:
        st.info("Gemini review was not run. The report above is deterministic parsing and skill matching, not generated AI feedback.")
    report = {"deterministic_analysis": insights, "tfidf_keyword_similarity": keyword_score, "gemini_analysis": ai_results}
    st.download_button("Download analysis report", json.dumps(report, indent=2), "resume_iq_report.json", "application/json", use_container_width=True)


def main() -> None:
    inject_styles()
    st.markdown('<div class="eyebrow">RESUME IQ · Vulli Koushik</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="hero">A clearer next step<br>for your career.</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtle">AI-Powered Resume & Career Analysis Platform. Parse your resume, compare it to a role, and turn explicit gaps into a practical plan.</p>', unsafe_allow_html=True)
    st.markdown('<div class="flow"><span>UPLOAD RESUME</span><b>→</b><span>ANALYZE</span><b>→</b><span>EXTRACT SKILLS</span><b>→</b><span>COMPARE WITH JOB</span><b>→</b><span>BUILD PLAN</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Start an analysis</div>', unsafe_allow_html=True)
    upload_col, jd_col = st.columns([.9, 1.1], gap="large")
    with upload_col:
        uploaded_file = st.file_uploader("Resume file", type=["pdf", "docx"], help="PDF and DOCX are supported. The file is processed in this session.")
        st.caption("Supported formats: PDF, DOCX")
    with jd_col:
        job_description = st.text_area("Job description (optional)", placeholder="Paste a role description to compare explicit skills and keywords.", height=174)
    run_ai = st.checkbox("Add Gemini-powered career review", value=False, help="Requires a configured Gemini API key. Rule-based analysis remains separate.")
    if st.button("Analyze resume", type="primary", use_container_width=True):
        if not uploaded_file:
            st.error("Upload a PDF or DOCX resume to continue.")
            return
        try:
            resume_text = parse_resume(uploaded_file, uploaded_file.name)
        except ValueError as error:
            st.error(f"We could not read this file: {error}")
            return
        if not resume_text.strip():
            st.error("No readable text was found. Try an exported text-based PDF or DOCX.")
            return
        insights = build_resume_insights(resume_text, job_description)
        keyword_score = calculate_tfidf_similarity(resume_text, job_description) if job_description.strip() else 0.0
        ai_results = None
        if run_ai:
            try:
                # Keep Gemini and its RAG initialization out of the standard local analysis path.
                from agents.orchestrator import Orchestrator
                from gemini_client import configure_gemini

                configure_gemini()
                status = st.empty()
                with st.spinner("Gemini agents are reviewing the resume..."):
                    ai_results = Orchestrator().analyze(resume_text, job_description, progress_callback=status.info)
                status.success("Gemini review complete.")
            except (ValueError, RuntimeError) as error:
                st.warning(f"Gemini review could not run: {error}. Your deterministic analysis is still available below.")
        render_results(uploaded_file.name, insights, keyword_score, ai_results)
    st.markdown('<div class="footer">RESUME IQ · AI-Powered Resume & Career Analysis Platform<br>Built & redesigned by Vulli Koushik</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
