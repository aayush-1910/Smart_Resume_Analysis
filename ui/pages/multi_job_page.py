"""
Multi-Job Comparison Page
Compare one resume against multiple job descriptions with ranked results.
"""
import streamlit as st
import tempfile
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ui.styles import apply_global_styles, render_progress_bar, get_score_hex


def render_multi_job_page():
    """Render the multi-job comparison page."""

    apply_global_styles()

    # Header
    st.markdown("""
    <div class="page-header">
        <h1>Multi-Job Comparison</h1>
        <p>Rank your resume against multiple positions to find the best fit</p>
    </div>
    """, unsafe_allow_html=True)

    # Resume upload
    st.markdown('<span class="section-label">1. Upload Resume</span>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=['pdf'],
        key="multi_job_resume",
        label_visibility="collapsed"
    )

    if uploaded_file:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 10px; padding: 12px 16px;
                    background: rgba(0,229,153,0.06); border-radius: 10px;
                    border: 1px solid rgba(0,229,153,0.15); margin-top: 8px;
                    animation: fadeInUp 0.3s ease both;">
            <span style="color: #00E599;">&#10003;</span>
            <span style="font-size: 14px; color: #F1F5F9;">{uploaded_file.name}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Job descriptions section
    st.markdown('<span class="section-label">2. Job Descriptions</span>', unsafe_allow_html=True)

    if 'job_count' not in st.session_state:
        st.session_state.job_count = 3

    jobs = []

    for i in range(st.session_state.job_count):
        with st.expander(f"Position {i + 1}", expanded=(i == 0)):
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Job Title", key=f"job_title_{i}", placeholder="e.g. Senior Developer")
            with col2:
                company = st.text_input("Company", key=f"job_company_{i}", placeholder="Optional")

            description = st.text_area("Description", key=f"job_desc_{i}", height=120)

            if title and description:
                jobs.append({
                    'title': title,
                    'company': company or None,
                    'description': description
                })

    # Slot controls
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.job_count < 5:
            if st.button("Add Position", use_container_width=True):
                st.session_state.job_count += 1
                st.rerun()
    with col2:
        if st.session_state.job_count > 3:
            if st.button("Remove Last", use_container_width=True):
                st.session_state.job_count -= 1
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Compare
    if st.button("Compare All Positions", type="primary", use_container_width=True):
        if not uploaded_file:
            st.error("Please upload a resume PDF")
        elif len(jobs) < 2:
            st.error("Please enter at least 2 complete job descriptions")
        else:
            with st.spinner("Analyzing multiple positions..."):
                try:
                    results = process_multi_job_comparison(uploaded_file, jobs)
                    display_comparison_results(results)
                except Exception as e:
                    st.error(f"Error processing: {str(e)}")


def process_multi_job_comparison(uploaded_file, jobs):
    """Process the multi-job comparison."""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        tmp.write(uploaded_file.getbuffer())
        tmp_path = tmp.name

    try:
        from pipeline.screening_pipeline import ScreeningPipeline
        from src.matching.multi_job_matcher import compare_resume_to_jobs

        pipeline = ScreeningPipeline()
        resume_data = pipeline.process_resume(tmp_path)
        results = compare_resume_to_jobs(resume_data, jobs)
        return results
    finally:
        os.unlink(tmp_path)


def display_comparison_results(results):
    """Display ranked comparison results with styled cards."""

    st.markdown("""
    <div class="page-header" style="margin-bottom: 16px;">
        <h3 style="font-size: 20px;">Rankings</h3>
    </div>
    """, unsafe_allow_html=True)

    job_results = results.get('results', [])

    # Rank cards
    for i, r in enumerate(job_results):
        rank = r.get('rank', i + 1)
        score = r.get('overall_score', 0)
        score_pct = int(score * 100)
        color = get_score_hex(score)
        title = r.get('job_title', '')
        company = r.get('job_company', '')
        skill_match = r.get('subscores', {}).get('skill_match', 0)
        skill_pct = int(skill_match * 100)

        # Medal for top 3
        if rank == 1:
            rank_icon = '<span style="font-size: 24px;">&#129351;</span>'
            card_border = "rgba(0,229,153,0.3)"
        elif rank == 2:
            rank_icon = '<span style="font-size: 24px;">&#129352;</span>'
            card_border = "rgba(192,192,192,0.3)"
        elif rank == 3:
            rank_icon = '<span style="font-size: 24px;">&#129353;</span>'
            card_border = "rgba(205,127,50,0.3)"
        else:
            rank_icon = f'<span style="font-family: JetBrains Mono; font-size: 18px; color: #64748B;">#{rank}</span>'
            card_border = "var(--border)"

        bar_html = render_progress_bar(score_pct, color, f"{0.3 + i * 0.15}s")

        st.markdown(f"""
        <div style="background: var(--surface); border: 1px solid {card_border};
                    border-radius: 14px; padding: 20px 24px; margin-bottom: 12px;
                    display: flex; align-items: center; gap: 20px;
                    transition: all 0.2s ease; animation: fadeInUp 0.4s ease both;
                    animation-delay: {i * 0.1}s;"
             onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 24px rgba(0,0,0,0.3)';"
             onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none';">

            <div style="min-width: 48px; text-align: center;">{rank_icon}</div>

            <div style="flex: 1;">
                <div style="font-family: 'Sora'; font-weight: 600; font-size: 16px; color: #F1F5F9;">{title}</div>
                <div style="font-size: 12px; color: #64748B; margin-top: 2px;">{company or ''}</div>
                {bar_html}
            </div>

            <div style="text-align: right; min-width: 80px;">
                <div style="font-family: 'JetBrains Mono'; font-size: 28px; font-weight: 700; color: {color};">{score_pct}%</div>
                <div style="font-size: 11px; color: #64748B;">Skill: {skill_pct}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Detailed breakdown
    st.markdown("---")
    st.markdown("""
    <div class="page-header" style="margin-bottom: 16px;">
        <h3 style="font-size: 20px;">Detailed Breakdown</h3>
    </div>
    """, unsafe_allow_html=True)

    for r in job_results:
        score = r.get('overall_score', 0)
        color = get_score_hex(score)

        with st.expander(f"{r.get('job_title')} - {int(score * 100)}%"):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown('<span class="section-label">Matched Skills</span>', unsafe_allow_html=True)
                matched = r.get('matched_skills', [])
                if matched:
                    pills = ''.join([f'<span class="skill-pill skill-matched">{s}</span>' for s in matched])
                    st.markdown(pills, unsafe_allow_html=True)
                else:
                    st.caption("None found")

            with col2:
                st.markdown('<span class="section-label">Missing Skills</span>', unsafe_allow_html=True)
                missing = r.get('missing_skills', [])
                if missing:
                    pills = ''.join([f'<span class="skill-pill skill-missing">{s.get("skill_name")}</span>' for s in missing[:5]])
                    st.markdown(pills, unsafe_allow_html=True)
                else:
                    st.caption("None")
