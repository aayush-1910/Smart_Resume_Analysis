"""
Multi-Job Comparison Page
Compare one resume against multiple job descriptions.
"""
import streamlit as st
import tempfile
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def render_multi_job_page():
    """Render the multi-job comparison page."""
    
    # Apply global styles
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from styles import apply_global_styles
    apply_global_styles()
    
    st.markdown('<h1 class="page-title">Multi-Job Comparison</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Rank your resume against multiple positions to find the best fit.</p>', unsafe_allow_html=True)
    
    # Resume upload section
    st.markdown("### 1. Upload Resume")
    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=['pdf'],
        key="multi_job_resume",
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        st.success(f"File loaded: {uploaded_file.name}")
    
    st.markdown("---")
    
    # Job descriptions section
    st.markdown("### 2. Job Descriptions")
    
    # Initialize job list in session state
    if 'job_count' not in st.session_state:
        st.session_state.job_count = 3
    
    jobs = []
    
    for i in range(st.session_state.job_count):
        with st.expander(f"Job Position {i + 1}", expanded=(i == 0)):
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
    
    # Add/remove job buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.job_count < 5:
            if st.button("ADD JOB SLOT +", use_container_width=True):
                st.session_state.job_count += 1
                st.rerun()
    with col2:
        if st.session_state.job_count > 3:
            if st.button("REMOVE LAST SLOT -", use_container_width=True):
                st.session_state.job_count -= 1
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Compare button
    if st.button("COMPARE JOBS ➔", type="primary", use_container_width=True):
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
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        tmp.write(uploaded_file.getbuffer())
        tmp_path = tmp.name
    
    try:
        from pipeline.screening_pipeline import ScreeningPipeline
        from src.matching.multi_job_matcher import compare_resume_to_jobs
        
        # Process resume first
        pipeline = ScreeningPipeline()
        resume_data = pipeline.process_resume(tmp_path)
        
        # Compare against all jobs
        results = compare_resume_to_jobs(resume_data, jobs)
        return results
    finally:
        os.unlink(tmp_path)


def display_comparison_results(results):
    """Display the comparison results."""
    st.markdown("### Ranking")
    
    job_results = results.get('results', [])
    
    # Create table data
    table_data = []
    for r in job_results:
        rank = r.get('rank', '-')
        
        # Medal Icons
        if rank == 1:
            rank_display = "🥇"
        elif rank == 2:
            rank_display = "🥈"
        elif rank == 3:
            rank_display = "🥉"
        else:
            rank_display = f"#{rank}"
            
        table_data.append({
            'Rank': rank_display,
            'Job Title': r.get('job_title', ''),
            'Company': r.get('job_company', '-') or '-',
            'Score': f"{r.get('overall_score', 0):.0%}",
            'Skill Match': f"{r.get('subscores', {}).get('skill_match', 0):.0%}",
        })
    
    import pandas as pd
    df = pd.DataFrame(table_data)
    
    # Custom styled table
    st.dataframe(
        df, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Score": st.column_config.ProgressColumn(
                "Match Score",
                help="Overall match percentage",
                format="%s",
                min_value=0,
                max_value=1,
            ),
        }
    )
    
    st.markdown("---")
    st.markdown("### Detailed Breakdown")
    
    for r in job_results:
        score = r.get('overall_score', 0)
        color = "#00E599" if score >= 0.7 else "#FFB800" if score >= 0.5 else "#FF4757"
        
        with st.expander(f"{r.get('job_title')} - {score:.0%}"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Matched Skills**")
                for s in r.get('matched_skills', []):
                    st.markdown(f"- {s}")
            with col2:
                st.markdown("**Missing Skills**")
                for s in r.get('missing_skills', [])[:5]:
                    st.markdown(f"- {s.get('skill_name')}")
