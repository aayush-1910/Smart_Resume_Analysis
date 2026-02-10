"""
Streamlit Web Interface for Smart Resume Coach
Premium Dark Theme with Animations
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
    page_title="Smart Resume Coach",
    page_icon="@",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global styles
from ui.styles import apply_global_styles, render_score_ring, render_progress_bar, get_score_hex
apply_global_styles()


def main():
    """Main application with sidebar navigation."""

    with st.sidebar:
        # Logo / Brand
        st.markdown("""
        <div style="padding: 8px 0 24px 0;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="width: 36px; height: 36px; background: rgba(0,217,255,0.12);
                     border-radius: 10px; display: flex; align-items: center; justify-content: center;
                     border: 1px solid rgba(0,217,255,0.2);">
                    <span style="font-size: 18px; color: #00D9FF; font-family: 'JetBrains Mono'; font-weight: 700;">S</span>
                </div>
                <div>
                    <div style="font-family: 'Sora'; font-weight: 700; font-size: 15px; color: #F1F5F9; letter-spacing: -0.02em;">Smart Resume Coach</div>
                    <div style="font-size: 11px; color: #64748B;">AI-Powered Analysis</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<span class="section-label">Navigation</span>', unsafe_allow_html=True)

        page = st.radio(
            "nav",
            ["Resume Analyzer", "Multi-Job Comparison", "Batch Processing"],
            index=0,
            label_visibility="collapsed"
        )

        st.markdown("---")

        # Status box
        st.markdown("""
        <div style="padding: 14px; background: rgba(255,255,255,0.02); border-radius: 10px;
                    border: 1px solid rgba(148,163,184,0.08);">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                <div style="width: 6px; height: 6px; border-radius: 50%; background: #00E599;
                     box-shadow: 0 0 8px rgba(0,229,153,0.4);"></div>
                <span style="font-size: 11px; color: #64748B; text-transform: uppercase; letter-spacing: 1px;">System Online</span>
            </div>
            <div style="font-family: 'JetBrains Mono'; font-size: 12px; color: #94A3B8;">v0.1.0</div>
        </div>
        """, unsafe_allow_html=True)

    # Route
    if page == "Resume Analyzer":
        render_single_job_page()
    elif page == "Multi-Job Comparison":
        render_multi_job_page()
    elif page == "Batch Processing":
        render_batch_processing_page()


def render_single_job_page():
    """Render the single job match page."""

    # Page header
    st.markdown("""
    <div class="page-header">
        <h1>Resume Analyzer</h1>
        <p>Analyze candidate fit against job requirements with AI-powered scoring</p>
    </div>
    """, unsafe_allow_html=True)

    # Input section
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<span class="section-label">1. Upload Resume</span>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Drop your PDF here",
            type=['pdf'],
            key="single_resume",
            label_visibility="collapsed"
        )

        if uploaded_file:
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 10px; padding: 12px 16px;
                        background: rgba(0,229,153,0.06); border-radius: 10px; 
                        border: 1px solid rgba(0,229,153,0.15); margin-top: 8px;
                        animation: fadeInUp 0.3s ease both;">
                <span style="color: #00E599; font-size: 16px;">&#10003;</span>
                <div>
                    <div style="font-size: 14px; color: #F1F5F9; font-weight: 500;">{uploaded_file.name}</div>
                    <div style="font-size: 12px; color: #64748B;">{uploaded_file.size/1024:.1f} KB</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown('<span class="section-label">2. Job Details</span>', unsafe_allow_html=True)
        job_title = st.text_input(
            "Job Title",
            placeholder="e.g. Senior Software Engineer",
            key="single_job_title"
        )
        job_description = st.text_area(
            "Job Description",
            placeholder="Paste the job description here - requirements, responsibilities, qualifications...",
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
        elif len(job_description.strip()) < 30:
            st.error("Job description is too short. Please provide at least 30 characters.")
        else:
            with st.spinner("Analyzing match..."):
                try:
                    # Simulate slight delay for effect
                    time.sleep(0.5)
                    result = process_screening(uploaded_file, job_title, job_description)
                    st.session_state['last_result'] = result
                    st.session_state['last_analyzed_file'] = uploaded_file.name
                except Exception as e:
                    st.error(f"Analysis Failed: {str(e)}")
                    st.session_state.pop('last_result', None)
    
    # Display results if available (persists across reruns)
    if 'last_result' in st.session_state:
        analyzed_name = st.session_state.get('last_analyzed_file', '')
        if analyzed_name:
            st.caption(f"📋 Showing results for: **{analyzed_name}**")
        display_results(st.session_state['last_result'])


def render_multi_job_page():
    """Render the multi-job comparison page."""
    from ui.pages.multi_job_page import render_multi_job_page as mjp
    mjp()


def render_batch_processing_page():
    """Render the batch processing page."""
    from ui.pages.batch_processing_page import render_batch_processing_page as bpp
    bpp()


def process_screening(uploaded_file, job_title: str, job_description: str):
    """Process the screening request with error handling."""
    # Validate file size (5 MB limit)
    if uploaded_file.size > 5 * 1024 * 1024:
        raise ValueError(f"File too large ({uploaded_file.size / (1024*1024):.1f} MB). Maximum is 5 MB.")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        tmp.write(uploaded_file.getbuffer())
        tmp_path = tmp.name
    
    try:
        from pipeline.screening_pipeline import ScreeningPipeline
        
        pipeline = ScreeningPipeline()
        result = pipeline.screen_resume(tmp_path, job_description, job_title or "Job Position")
        return result
    except Exception as e:
        raise RuntimeError(f"Pipeline error: {str(e)}")
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def display_results(result: dict):
    """Display screening results with animated premium UI."""
    match = result.get('match', {})
    resume = result.get('resume', {})

    score = match.get('overall_score', 0)
    skill_score = match.get('subscores', {}).get('skill_match', 0)
    semantic_score = match.get('subscores', {}).get('semantic_similarity', 0)

    score_pct = int(score * 100)
    skill_pct = int(skill_score * 100)
    semantic_pct = int(semantic_score * 100)

    score_color = get_score_hex(score)

    # Status
    if score >= 0.75:
        status_class = "status-success"
        status_text = "STRONG MATCH"
    elif score >= 0.55:
        status_class = "status-warning"
        status_text = "MODERATE MATCH"
    else:
        status_class = "status-danger"
        status_text = "WEAK MATCH"

    st.markdown("---")

    # -------------------------------------------------------------------------
    # HERO SECTION
    # -------------------------------------------------------------------------
    hero_col1, hero_col2 = st.columns([1, 2])

    with hero_col1:
        # SVG Score Ring
        ring_html = render_score_ring(score_pct, score_color)
        hero_html = (
            '<div class="glass-card" style="text-align:center;">'
            + ring_html
            + '<div style="font-size:13px; color:#94A3B8; text-transform:uppercase; letter-spacing:1.5px; margin-top:12px;">Overall Match</div>'
            + f'<div style="margin-top:12px;"><span class="status-badge {status_class}">{status_text}</span></div>'
            + '</div>'
        )
        st.markdown(hero_html, unsafe_allow_html=True)

    with hero_col2:
        # Subscore Cards
        sub_col1, sub_col2 = st.columns(2)

        with sub_col1:
            skill_color = get_score_hex(skill_score)
            bar_html = render_progress_bar(skill_pct, skill_color, "0.5s")
            card1 = (
                '<div class="metric-card">'
                '<span class="section-label">Skill Match</span>'
                f'<div style="font-family:JetBrains Mono,monospace; font-size:36px; font-weight:700; color:{skill_color}; '
                f'margin:8px 0 4px 0;">{skill_pct}%</div>'
                + bar_html
                + '</div>'
            )
            st.markdown(card1, unsafe_allow_html=True)

        with sub_col2:
            sem_color = get_score_hex(semantic_score)
            bar_html2 = render_progress_bar(semantic_pct, sem_color, "0.7s")
            card2 = (
                '<div class="metric-card">'
                '<span class="section-label">Semantic Similarity</span>'
                f'<div style="font-family:JetBrains Mono,monospace; font-size:36px; font-weight:700; color:{sem_color}; '
                f'margin:8px 0 4px 0;">{semantic_pct}%</div>'
                + bar_html2
                + '</div>'
            )
            st.markdown(card2, unsafe_allow_html=True)

        # Candidate Info
        candidate = resume.get('candidate', {})
        cand_name = candidate.get('name', 'Unknown')
        cand_email = candidate.get('email', 'N/A')

        cand_html = (
            '<div style="margin-top:16px; padding:16px 20px; background:rgba(255,255,255,0.02); '
            'border-radius:12px; border:1px solid rgba(148,163,184,0.08); '
            'display:flex; gap:32px; align-items:center;">'
            '<div>'
            '<span class="section-label" style="margin-bottom:4px;">Candidate</span>'
            f'<div style="font-weight:600; font-size:15px; color:#F1F5F9;">{cand_name}</div>'
            '</div>'
            '<div>'
            '<span class="section-label" style="margin-bottom:4px;">Email</span>'
            f'<div style="font-family:JetBrains Mono,monospace; font-size:13px; color:#94A3B8;">{cand_email}</div>'
            '</div>'
            '</div>'
        )
        st.markdown(cand_html, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # SKILLS ANALYSIS
    # -------------------------------------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="page-header" style="margin-bottom: 16px;">
        <h3 style="font-size: 20px;">Skill Analysis</h3>
    </div>
    """, unsafe_allow_html=True)

    skill_col1, skill_col2 = st.columns(2)

    with skill_col1:
        st.markdown('<span class="section-label">Matched Skills</span>', unsafe_allow_html=True)
        matched = match.get('matched_skills', [])
        if matched:
            pills_html = ''.join([
                f'<span class="skill-pill skill-matched" style="animation-delay: {i*0.05}s;">{skill}</span>'
                for i, skill in enumerate(matched)
            ])
            st.markdown(f'<div style="animation: fadeInUp 0.4s ease both;">{pills_html}</div>', unsafe_allow_html=True)
        else:
            st.info("No matching skills found.")

    with skill_col2:
        st.markdown('<span class="section-label">Missing Skills</span>', unsafe_allow_html=True)
        missing = match.get('missing_skills', [])
        if missing:
            pills_html = ''.join([
                f'<span class="skill-pill skill-missing" style="animation-delay: {i*0.05}s;">{s["skill_name"]}</span>'
                for i, s in enumerate(missing[:10])
            ])
            st.markdown(f'<div style="animation: fadeInUp 0.4s ease both; animation-delay: 0.2s;">{pills_html}</div>', unsafe_allow_html=True)
        else:
            st.success("No missing critical or preferred skills!")

    # -------------------------------------------------------------------------
    # ACTION BUTTONS
    # -------------------------------------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="page-header" style="margin-bottom: 16px;">
        <h3 style="font-size: 20px;">Actionable Insights</h3>
    </div>
    """, unsafe_allow_html=True)

    act_col1, act_col2 = st.columns(2)

    with act_col1:
        if st.button("Get Improvement Plan", use_container_width=True, key="btn_improve"):
            st.session_state['show_improvement'] = True
            st.session_state['show_learning'] = False

    with act_col2:
        if st.button("View Learning Resources", use_container_width=True, key="btn_learn"):
            st.session_state['show_learning'] = True
            st.session_state['show_improvement'] = False

    if st.session_state.get('show_improvement', False):
        st.markdown("---")
        try:
            show_improvement_suggestions(resume, match)
        except Exception as e:
            st.error(f"Could not generate improvement plan: {str(e)}")
            st.code(str(e)) # Show details for debugging

    if st.session_state.get('show_learning', False):
        st.markdown("---")
        try:
            show_learning_recommendations(match.get('missing_skills', []))
        except Exception as e:
            st.error(f"Could not load learning resources: {str(e)}")
            st.code(str(e))


def show_improvement_suggestions(resume: dict, match: dict):
    """Display improvement suggestions."""
    try:
        from src.matching.improvement_analyzer import generate_improvement_suggestions
        from ui.components.improvement_suggestions import render_improvement_suggestions
    except ImportError as e:
        st.error(f"Module import error: {e}")
        return

    job_desc = st.session_state.get('single_job_desc', '')
    # Fallback to description from previous analysis if text area is cleared
    if not job_desc and 'job_description' in match:
        job_desc = match['job_description']
        
    job_data = {'description': job_desc}
    
    with st.spinner("Analyzing resume for improvements..."):
        suggestions = generate_improvement_suggestions(resume, job_data, match)
        render_improvement_suggestions(suggestions)


def show_learning_recommendations(missing_skills: list):
    """Display learning recommendations."""
    try:
        from src.recommendations.learning_recommender import generate_learning_recommendations
        from ui.components.learning_recommendations import render_learning_recommendations, render_learning_milestones
    except ImportError as e:
        st.error(f"Module import error: {e}")
        return

    if not missing_skills:
        st.info("No missing skills identified! Great match.")
        return

    with st.spinner("Curating learning resources..."):
        recommendations = generate_learning_recommendations(
            missing_skills=missing_skills,
            max_skills=5,
            difficulty_preference="beginner"
        )
        render_learning_recommendations(recommendations)
        render_learning_milestones(recommendations)


if __name__ == "__main__":
    main()
