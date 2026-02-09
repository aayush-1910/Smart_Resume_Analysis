"""
Streamlit Web Interface for AI Resume Screener v0.2
Refined Professional Design - Dark Theme (Option A)
"""
import streamlit as st
import tempfile
import os
import time
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# GLOBAL STYLING & ASSETS
# -----------------------------------------------------------------------------

st.markdown("""
<style>
    /* Import Google Fonts: Sora (Headings), DM Sans (Body), JetBrains Mono (Code/Data) */
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=DM+Sans:wght@400;500;700&family=JetBrains+Mono:wght@500;600&display=swap');

    :root {
        --bg-color: #0A0E1A;
        --surface-color: #141B2D;
        --primary-color: #00D9FF;
        --success-color: #00E599;
        --warning-color: #FFB800;
        --danger-color: #FF4757;
        --text-color: #FFFFFF;
        --subtext-color: #94A3B8;
        --border-color: rgba(148, 163, 184, 0.2);
    }

    /* Global Reset & Typography */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        color: var(--text-color);
        background-color: var(--bg-color);
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Sora', sans-serif;
        font-weight: 600;
        color: var(--text-color);
        letter-spacing: -0.02em;
    }
    
    code, pre, .stCode, .stCodeBlock, .score-display {
        font-family: 'JetBrains Mono', monospace;
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main Container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
        max-width: 1200px;
    }

    /* -------------------------------------------------------------------------
       COMPONENTS
       ------------------------------------------------------------------------- */
       
    /* Cards */
    .metric-card {
        background-color: var(--surface-color);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        border-color: rgba(0, 217, 255, 0.3);
    }

    /* Headings */
    h1.page-title {
        font-size: 32px;
        margin-bottom: 8px;
        background: linear-gradient(90deg, #FFFFFF, #94A3B8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    p.page-subtitle {
        color: var(--subtext-color);
        font-size: 16px;
        margin-bottom: 32px;
    }

    /* Custom File Uploader Styling */
    .stFileUploader {
        border-radius: 12px;
        border: 2px dashed var(--border-color);
        background-color: rgba(20, 27, 45, 0.5);
        padding: 20px;
        transition: border-color 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: var(--primary-color);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00D9FF 0%, #00B4D8 100%);
        color: #0A0E1A;
        font-family: 'Sora', sans-serif;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        transition: all 0.2s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 14px;
        box-shadow: 0 4px 12px rgba(0, 217, 255, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 217, 255, 0.3);
        color: #0A0E1A;
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Inputs */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: var(--surface-color);
        color: var(--text-color);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 14px;
    }
    
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 1px var(--primary-color);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: var(--surface-color);
        border-right: 1px solid var(--border-color);
    }
    
    [data-testid="stSidebar"] h1 {
        font-family: 'Sora', sans-serif !important;
        font-size: 20px !important;
        color: var(--primary-color) !important;
        margin-bottom: 2rem;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace;
        color: var(--primary-color);
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'DM Sans', sans-serif;
        color: var(--subtext-color);
        text-transform: uppercase;
        font-size: 12px;
        letter-spacing: 1px;
    }
    
    /* Status Colors */
    .status-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
    }
    
    .status-success { background: rgba(0, 229, 153, 0.15); color: var(--success-color); border: 1px solid rgba(0, 229, 153, 0.3); }
    .status-warning { background: rgba(255, 184, 0, 0.15); color: var(--warning-color); border: 1px solid rgba(255, 184, 0, 0.3); }
    .status-danger { background: rgba(255, 71, 87, 0.15); color: var(--danger-color); border: 1px solid rgba(255, 71, 87, 0.3); }
    
    /* Separator */
    hr { margin: 2rem 0; border: 0; border-top: 1px solid var(--border-color); }
    
</style>
""", unsafe_allow_html=True)


def main():
    """Main Streamlit application with navigation."""
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("# AI Resume Screener")
        
        page = st.radio(
            "NAVIGATION",
            ["Single Job Match", "Multi-Job Comparison", "Batch Processing"],
            index=0,
            label_visibility="visible"
        )
        
        st.markdown("---")
        
        st.markdown("""
        <div style="padding: 1rem; background: rgba(255,255,255,0.03); border-radius: 8px;">
            <p style="font-size: 12px; color: #94A3B8; margin: 0;">CURRENT VERSION</p>
            <p style="font-family: 'JetBrains Mono'; color: #00D9FF; font-size: 14px; margin: 0;">v0.2.0-beta</p>
        </div>
        """, unsafe_allow_html=True)

    # Route to selected page
    if page == "Single Job Match":
        render_single_job_page()
    elif page == "Multi-Job Comparison":
        render_multi_job_page()
    elif page == "Batch Processing":
        render_batch_processing_page()


def render_single_job_page():
    """Render the single job match page."""
    
    # Header
    st.markdown('<h1 class="page-title">Resume Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Analyze candidate fit against job requirements with AI-powered scoring.</p>', unsafe_allow_html=True)
    
    # Input Section
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("### 1. Upload Resume")
        uploaded_file = st.file_uploader(
            "Drop your PDF here",
            type=['pdf'],
            key="single_resume",
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            st.success(f"File loaded: {uploaded_file.name} ({uploaded_file.size/1024:.1f} KB)")
    
    with col2:
        st.markdown("### 2. Job Description")
        job_title = st.text_input(
            "Job Title",
            placeholder="e.g. Senior Software Engineer",
            key="single_job_title"
        )
        job_description = st.text_area(
            "Paste Job Description",
            placeholder="Key responsibilities, required skills...",
            height=200,
            key="single_job_desc",
            label_visibility="collapsed"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Analyze Button
    if st.button("RUN ANALYSIS ➔", type="primary", use_container_width=True, key="single_analyze"):
        if not uploaded_file:
            st.error("Please upload a resume first.")
        elif not job_description:
            st.error("Please provide a job description.")
        else:
            with st.spinner("Analyzing match..."):
                try:
                    # Simulate slight delay for effect
                    time.sleep(0.5)
                    result = process_screening(uploaded_file, job_title, job_description)
                    st.session_state['last_result'] = result
                    display_results(result)
                except Exception as e:
                    st.error(f"Analysis Failed: {str(e)}")


def render_multi_job_page():
    """Render the multi-job comparison page."""
    from ui.pages.multi_job_page import render_multi_job_page as mjp
    mjp()


def render_batch_processing_page():
    """Render the batch processing page."""
    from ui.pages.batch_processing_page import render_batch_processing_page as bpp
    bpp()


def process_screening(uploaded_file, job_title: str, job_description: str):
    """Process the screening request."""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        tmp.write(uploaded_file.getbuffer())
        tmp_path = tmp.name
    
    try:
        from pipeline.screening_pipeline import ScreeningPipeline
        
        pipeline = ScreeningPipeline()
        result = pipeline.screen_resume(tmp_path, job_description, job_title or "Job Position")
        return result
    finally:
        os.unlink(tmp_path)


def display_results(result: dict):
    """Display screening results with modernized UI."""
    match = result.get('match', {})
    resume = result.get('resume', {})
    
    score = match.get('overall_score', 0)
    recommendation = match.get('recommendation', 'unknown')
    skill_score = match.get('subscores', {}).get('skill_match', 0)
    semantic_score = match.get('subscores', {}).get('semantic_similarity', 0)
    
    # Determine Status Color & Text via CSS Class
    if score >= 0.75:
        status_class = "status-success"
        status_text = "STRONG MATCH"
        score_color = "#00E599"
    elif score >= 0.55:
        status_class = "status-warning"
        status_text = "MODERATE MATCH"
        score_color = "#FFB800"
    else:
        status_class = "status-danger"
        status_text = "WEAK MATCH"
        score_color = "#FF4757"
        
    st.markdown("---")
    
    # -------------------------------------------------------------------------
    # HERO SECTION
    # -------------------------------------------------------------------------
    hero_col1, hero_col2 = st.columns([1, 2])
    
    with hero_col1:
        st.markdown(f"""
        <div class="metric-card" style="text-align: center;">
            <p style="color: #94A3B8; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0;">Overall Match</p>
            <div style="font-family: 'JetBrains Mono'; font-size: 72px; font-weight: 700; color: {score_color}; line-height: 1.2;">
                {int(score * 100)}%
            </div>
            <span class="status-badge {status_class}">{status_text}</span>
        </div>
        """, unsafe_allow_html=True)
        
    with hero_col2:
        # Subscores Grid
        sub_col1, sub_col2 = st.columns(2)
        with sub_col1:
            st.markdown(f"""
            <div class="metric-card">
                <p style="color: #94A3B8; font-size: 12px; text-transform: uppercase;">Skill Match</p>
                <div style="font-family: 'JetBrains Mono'; font-size: 32px; font-weight: 600; color: #FFFFFF;">
                    {int(skill_score * 100)}%
                </div>
                <div style="width: 100%; background: #1E293B; height: 6px; border-radius: 3px; margin-top: 8px;">
                    <div style="width: {int(skill_score * 100)}%; background: #00D9FF; height: 100%; border-radius: 3px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with sub_col2:
            st.markdown(f"""
            <div class="metric-card">
                <p style="color: #94A3B8; font-size: 12px; text-transform: uppercase;">Semantic Similarity</p>
                <div style="font-family: 'JetBrains Mono'; font-size: 32px; font-weight: 600; color: #FFFFFF;">
                    {int(semantic_score * 100)}%
                </div>
                <div style="width: 100%; background: #1E293B; height: 6px; border-radius: 3px; margin-top: 8px;">
                    <div style="width: {int(semantic_score * 100)}%; background: #A78BFA; height: 100%; border-radius: 3px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Candidate Info Mini-Card
        candidate = resume.get('candidate', {})
        st.markdown(f"""
        <div style="margin-top: 1rem; padding: 1rem; background: rgba(255,255,255,0.03); border-radius: 8px; display: flex; gap: 2rem; align-items: center;">
            <div>
                <span style="color: #94A3B8; font-size: 12px;">CANDIDATE</span><br>
                <strong style="color: #fff;">{candidate.get('name', 'Unknown')}</strong>
            </div>
            <div>
                <span style="color: #94A3B8; font-size: 12px;">EMAIL</span><br>
                <span style="color: #fff; font-family: 'JetBrains Mono'; font-size: 13px;">{candidate.get('email', 'N/A')}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # SKILLS ANALYSIS
    # -------------------------------------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Skill Analysis")
    
    skill_col1, skill_col2 = st.columns(2)
    
    with skill_col1:
        st.caption("MATCHED SKILLS")
        matched = match.get('matched_skills', [])
        if matched:
            # Custom Pill Styling
            skills_html = ' '.join([
                f'<span style="background: rgba(0, 229, 153, 0.15); color: #00E599; padding: 4px 12px; border-radius: 16px; font-size: 13px; font-weight: 500; display: inline-block; margin-bottom: 8px; border: 1px solid rgba(0, 229, 153, 0.3);">{skill}</span>' 
                for skill in matched
            ])
            st.markdown(skills_html, unsafe_allow_html=True)
        else:
            st.info("No matching skills found.")
            
    with skill_col2:
        st.caption("MISSING SKILLS (RECOMMENDED)")
        missing = match.get('missing_skills', [])
        if missing:
            # Custom Pill Styling
            skills_html = ' '.join([
                f'<span style="background: rgba(255, 71, 87, 0.15); color: #FF4757; padding: 4px 12px; border-radius: 16px; font-size: 13px; font-weight: 500; display: inline-block; margin-bottom: 8px; border: 1px solid rgba(255, 71, 87, 0.3);">{s["skill_name"]}</span>' 
                for s in missing[:10]
            ])
            st.markdown(skills_html, unsafe_allow_html=True)
        else:
            st.success("No missing Critical or Preferred skills!")

    # -------------------------------------------------------------------------
    # ACTIONS
    # -------------------------------------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Actionable Insights")
    
    act_col1, act_col2 = st.columns(2)
    
    with act_col1:
        if st.button("GET IMPROVEMENT PLAN ➔", use_container_width=True, key="btn_improve"):
            st.session_state['show_improvement'] = True
            st.session_state['show_learning'] = False
            
    with act_col2:
        if st.button("VIEW LEARNING RESOURCES ➔", use_container_width=True, key="btn_learn"):
            st.session_state['show_learning'] = True
            st.session_state['show_improvement'] = False
    
    # Display improvement suggestions if toggled
    if st.session_state.get('show_improvement', False):
        st.markdown("---")
        show_improvement_suggestions(resume, match)
    
    # Display learning recommendations if toggled
    if st.session_state.get('show_learning', False):
        st.markdown("---")
        show_learning_recommendations(match.get('missing_skills', []))


def show_improvement_suggestions(resume: dict, match: dict):
    """Display improvement suggestions."""
    from src.matching.improvement_analyzer import generate_improvement_suggestions
    from ui.components.improvement_suggestions import render_improvement_suggestions
    
    job_data = {'description': st.session_state.get('single_job_desc', '')}
    suggestions = generate_improvement_suggestions(resume, job_data, match)
    render_improvement_suggestions(suggestions)


def show_learning_recommendations(missing_skills: list):
    """Display learning recommendations."""
    from src.recommendations.learning_recommender import generate_learning_recommendations
    from ui.components.learning_recommendations import render_learning_recommendations, render_learning_milestones
    
    if not missing_skills:
        st.info("No missing skills identified.")
        return
    
    recommendations = generate_learning_recommendations(
        missing_skills=missing_skills,
        max_skills=5,
        difficulty_preference="beginner"
    )
    render_learning_recommendations(recommendations)
    render_learning_milestones(recommendations)


if __name__ == "__main__":
    main()
