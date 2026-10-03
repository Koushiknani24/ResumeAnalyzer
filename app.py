import streamlit as st
import json
from resume_parser import parse_resume
from ml_features import calculate_tfidf_similarity, generate_competition_plot
from agents.orchestrator import Orchestrator

st.set_page_config(
    page_title="AI Resume Analyzer (Agentic Edition)",
    page_icon="📄",
    layout="wide"
)

# Custom CSS for premium look
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px;
        color: #888;
        font-size: 16px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        color: #4A90E2 !important;
        border-bottom: 2px solid #4A90E2 !important;
    }
    .metric-card {
        background: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.title("📄 AI Resume Analyzer (Agentic & RAG Edition)")
st.markdown("Powered by a multi-agent workflow and Retrieval-Augmented Generation (RAG).")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Resume")
    uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

with col2:
    st.subheader("2. Job Description")
    job_description = st.text_area("Paste the job description here", height=200)

if st.button("🚀 Launch Agentic Analysis", type="primary", use_container_width=True):
    if not uploaded_file:
        st.error("Please upload a resume to proceed.")
        st.stop()
    if not job_description.strip():
        st.error("Please paste a job description to proceed.")
        st.stop()
        
    try:
        resume_text = parse_resume(uploaded_file, uploaded_file.name)
    except Exception as e:
        st.error(f"Error parsing resume: {e}")
        st.stop()
        
    if not resume_text.strip():
        st.error("The uploaded resume appears to be empty.")
        st.stop()

    # Calculate baseline score
    tfidf_score = calculate_tfidf_similarity(resume_text, job_description)

    st.markdown("---")
    
    # Status container for agent feedback
    status_text = st.empty()
    
    def update_status(msg):
        status_text.info(msg)

    orchestrator = Orchestrator()
    
    try:
        with st.spinner("Agents are analyzing your profile..."):
            results = orchestrator.analyze(resume_text, job_description, progress_callback=update_status)
            
        status_text.success("✨ Analysis Complete!")
    except Exception as e:
        st.error(f"An error occurred during agent analysis: {e}")
        st.stop()
        
    extracted = results.get("extraction", {})
    evaluated = results.get("evaluation", {})
    coaching = results.get("coaching", {})

    with st.expander("⚙️ View Backend Processing Logs (Developer Mode)"):
        st.markdown("**Extractor Agent JSON Output:**")
        st.json(extracted)
        st.markdown("**Evaluator Agent JSON Output:**")
        st.json(evaluated)
        st.markdown("**Coach Agent JSON Output:**")
        st.json(coaching)

    # Create Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🧠 Agent Analysis", "🎓 Career Coach"])
    
    with tab1:
        st.header("Executive Summary")
        score = evaluated.get("match_score", 0)
        
        mcol1, mcol2, mcol3 = st.columns([1, 1, 2])
        with mcol1:
            st.metric(label="Agent Match Score", value=f"{score}%")
        with mcol2:
            st.metric(label="Baseline Keyword Score", value=f"{tfidf_score}%")
        with mcol3:
            st.progress(score / 100.0, text="Overall Fit")
            
        comp_fig = generate_competition_plot(score)
        st.pyplot(comp_fig)
        
    with tab2:
        st.header("Deep Dive Analysis")
        
        stcol1, stcol2 = st.columns(2)
        with stcol1:
            st.subheader("Extracted Profile (Extractor Agent)")
            st.json(extracted)
            
        with stcol2:
            st.subheader("Missing Skills")
            missing = evaluated.get("missing_skills", [])
            for m in missing:
                st.error(f"- {m}")
                
            st.subheader("Weak Points")
            weak = evaluated.get("weak_points", [])
            for w in weak:
                st.warning(f"- {w}")
                
        st.markdown("---")
        st.subheader("ATS Suggestions & Rewrites (Evaluator Agent)")
        
        rag_context = evaluated.get("rag_context_used", [])
        if rag_context:
            with st.expander("📚 View RAG Citations Used for Suggestions"):
                st.info("The Evaluator Agent pulled these industry standards from the knowledge base to guide its suggestions:")
                for item in rag_context:
                    st.write(f"**{item['content']}** (Similarity: {item['similarity_score']:.2f})")
                    if 'example' in item:
                        st.caption(f"Example: {item['example']}")
                        
        sug_col1, sug_col2 = st.columns(2)
        with sug_col1:
            st.markdown("**Structural Suggestions:**")
            for sug in evaluated.get("ats_suggestions", []):
                st.success(f"✓ {sug}")
        with sug_col2:
            st.markdown("**Bullet Point Rewrites:**")
            for bp in evaluated.get("improved_bullet_points", []):
                st.info(f"✨ {bp}")

    with tab3:
        st.header("Interview Prep (Coach Agent)")
        st.markdown("The Coach Agent has reviewed your weaknesses and generated a custom prep plan.")
        
        st.subheader("🔥 Mock Interview Challenge")
        st.caption("Answer these aloud to prepare for the toughest questions.")
        for i, q in enumerate(coaching.get("mock_interview_questions", [])):
            st.warning(f"**Q{i+1}:** {q}")
            
        st.markdown("---")
        st.subheader("📈 Actionable Learning Path")
        st.caption("How to close your skill gaps before the interview.")
        for step in coaching.get("learning_path", []):
            st.success(f"✅ {step}")
            
    # Final export
    st.download_button(
        label="Download Full Agent Report",
        data=json.dumps(results, indent=2),
        file_name="agentic_resume_analysis.json",
        mime="application/json"
    )
