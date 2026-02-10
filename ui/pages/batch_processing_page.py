"""
Batch Processing Page
Process multiple resumes against a single job description with live progress.
"""
import streamlit as st
import tempfile
import os
import sys
import pandas as pd
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ui.styles import apply_global_styles, get_score_hex


def render_batch_processing_page():
    """Render the batch processing page."""

    apply_global_styles()

    # Header
    st.markdown("""
    <div class="page-header">
        <h1>Batch Processing</h1>
        <p>Screen multiple candidates efficiently against one job description</p>
    </div>
    """, unsafe_allow_html=True)

    # Upload Resumes
    st.markdown('<span class="section-label">1. Upload Resumes</span>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Upload PDFs",
        type=['pdf'],
        accept_multiple_files=True,
        key="batch_resumes",
        label_visibility="collapsed"
    )

    if uploaded_files:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 10px; padding: 12px 16px;
                    background: rgba(0,217,255,0.06); border-radius: 10px;
                    border: 1px solid rgba(0,217,255,0.15); margin-top: 8px;
                    animation: fadeInUp 0.3s ease both;">
            <span style="font-family: 'JetBrains Mono'; font-size: 20px; font-weight: 700; color: #00D9FF;">{len(uploaded_files)}</span>
            <span style="font-size: 14px; color: #94A3B8;">files ready for processing</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Job Description
    st.markdown('<span class="section-label">2. Job Description</span>', unsafe_allow_html=True)
    job_description = st.text_area(
        "Paste Job Description",
        placeholder="Requirements and responsibilities...",
        height=150,
        key="batch_job_desc",
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Process Button
    if st.button("Start Batch Screening", type="primary", use_container_width=True):
        if not uploaded_files:
            st.error("Please upload resumes")
        elif not job_description:
            st.error("Please provide a job description")
        else:
            job_data = {'description': job_description}

            # Progress
            progress_bar = st.progress(0)
            status_container = st.empty()

            results = []

            try:
                from pipeline.screening_pipeline import ScreeningPipeline
                pipeline = ScreeningPipeline()

                total = len(uploaded_files)

                for i, file in enumerate(uploaded_files):
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                        tmp.write(file.getbuffer())
                        tmp_path = tmp.name

                    try:
                        # Status update
                        status_container.markdown(f"""
                        <div style="display: flex; align-items: center; gap: 12px; padding: 12px 16px;
                                    background: var(--surface); border-radius: 10px; border: 1px solid var(--border);
                                    margin-bottom: 8px;">
                            <div style="width: 8px; height: 8px; border-radius: 50%; background: #00D9FF;
                                        animation: dotPulse 1s ease infinite;"></div>
                            <span style="font-size: 14px; color: #94A3B8;">Processing {i+1}/{total}:</span>
                            <span style="font-size: 14px; color: #F1F5F9; font-weight: 500;">{file.name}</span>
                        </div>
                        """, unsafe_allow_html=True)

                        result = pipeline.screen_resume(tmp_path, job_description)
                        match = result.get('match', {})
                        score = match.get('overall_score', 0)

                        results.append({
                            'Filename': file.name,
                            'Score': score,
                            'Status': 'Completed'
                        })

                        progress_bar.progress((i + 1) / total)

                    except Exception as e:
                        results.append({
                            'Filename': file.name,
                            'Score': 0,
                            'Status': f'Error: {str(e)}'
                        })
                    finally:
                        if os.path.exists(tmp_path):
                            os.unlink(tmp_path)

                # Done
                status_container.markdown("""
                <div style="display: flex; align-items: center; gap: 10px; padding: 12px 16px;
                            background: rgba(0,229,153,0.06); border-radius: 10px;
                            border: 1px solid rgba(0,229,153,0.15);">
                    <span style="color: #00E599;">&#10003;</span>
                    <span style="font-size: 14px; color: #00E599; font-weight: 500;">Batch processing complete</span>
                </div>
                """, unsafe_allow_html=True)

                display_batch_results(results)

            except Exception as e:
                st.error(f"Batch error: {str(e)}")


def display_batch_results(results):
    """Display batch results with styled cards."""

    st.markdown("""
    <div class="page-header" style="margin-top: 24px; margin-bottom: 16px;">
        <h3 style="font-size: 20px;">Results</h3>
    </div>
    """, unsafe_allow_html=True)

    # Sort by score
    results_sorted = sorted(results, key=lambda x: x['Score'], reverse=True)

    # Result cards
    for i, r in enumerate(results_sorted):
        score = r['Score']
        score_pct = int(score * 100)
        color = get_score_hex(score)
        filename = r['Filename']
        status = r['Status']

        is_error = status != 'Completed'

        st.markdown(f"""
        <div style="background: var(--surface); border: 1px solid {'rgba(255,71,87,0.2)' if is_error else 'var(--border)'};
                    border-radius: 12px; padding: 16px 20px; margin-bottom: 8px;
                    display: flex; align-items: center; justify-content: space-between;
                    animation: fadeInUp 0.3s ease both; animation-delay: {i * 0.05}s;
                    transition: all 0.15s ease;"
             onmouseover="this.style.borderColor='rgba(148,163,184,0.25)'; this.style.transform='translateY(-1px)';"
             onmouseout="this.style.borderColor='{'rgba(255,71,87,0.2)' if is_error else 'var(--border)'}'; this.style.transform='translateY(0)';">

            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="font-family: 'JetBrains Mono'; font-size: 13px; color: #64748B; min-width: 24px;">#{i+1}</div>
                <div>
                    <div style="font-size: 14px; font-weight: 500; color: #F1F5F9;">{filename}</div>
                    <div style="font-size: 11px; color: {'#FF4757' if is_error else '#64748B'}; margin-top: 2px;">{status}</div>
                </div>
            </div>

            <div style="font-family: 'JetBrains Mono'; font-size: 22px; font-weight: 700; color: {color};">
                {score_pct}%
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Export
    df = pd.DataFrame(results_sorted)
    csv = df.to_csv(index=False).encode('utf-8')

    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button(
        "Download CSV Report",
        csv,
        "batch_results.csv",
        "text/csv",
        key='download-csv',
        use_container_width=True
    )
