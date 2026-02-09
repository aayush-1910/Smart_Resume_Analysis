"""
Batch Processing Page
Process multiple resumes against a single job description.
"""
import streamlit as st
import tempfile
import os
import sys
import pandas as pd
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def render_batch_processing_page():
    """Render the batch processing page."""
    
    # Apply global styles
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from styles import apply_global_styles
    apply_global_styles()
    
    st.markdown('<h1 class="page-title">Batch Processing</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Screen multiple candidates efficiently against one job description.</p>', unsafe_allow_html=True)
    
    # Upload Resumes
    st.markdown("### 1. Upload Resumes")
    uploaded_files = st.file_uploader(
        "Upload PDFs",
        type=['pdf'],
        accept_multiple_files=True,
        key="batch_resumes",
        label_visibility="collapsed"
    )
    
    if uploaded_files:
        st.success(f"{len(uploaded_files)} files loaded ready for processing.")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Job Description
    st.markdown("### 2. Job Description")
    job_description = st.text_area(
        "Paste Job Description",
        placeholder="Requirements and responsibilities...",
        height=150,
        key="batch_job_desc",
        label_visibility="collapsed"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Process Button
    if st.button("START BATCH SCREENING ➔", type="primary", use_container_width=True):
        if not uploaded_files:
            st.error("Please upload resumes")
        elif not job_description:
            st.error("Please provide a job description")
        else:
            job_data = {'description': job_description}
            
            # Progress Container
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            results = []
            
            try:
                from pipeline.screening_pipeline import ScreeningPipeline
                pipeline = ScreeningPipeline()
                
                total = len(uploaded_files)
                
                for i, file in enumerate(uploaded_files):
                    # Save temp
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                        tmp.write(file.getbuffer())
                        tmp_path = tmp.name
                    
                    try:
                        status_text.text(f"Processing {i+1}/{total}: {file.name}...")
                        
                        # Process
                        result = pipeline.screen_resume(tmp_path, job_description)
                        match = result.get('match', {})
                        score = match.get('overall_score', 0)
                        
                        results.append({
                            'Filename': file.name,
                            'Score': score,
                            'Status': 'Completed'
                        })
                        
                        # Update progress
                        progress = (i + 1) / total
                        progress_bar.progress(progress)
                        
                    except Exception as e:
                        results.append({
                            'Filename': file.name,
                            'Score': 0,
                            'Status': f'Error: {str(e)}'
                        })
                    finally:
                        if os.path.exists(tmp_path):
                            os.unlink(tmp_path)
                
                status_text.text("Batch processing complete!")
                display_batch_results(results)
                
            except Exception as e:
                st.error(f"Batch Error: {str(e)}")


def display_batch_results(results):
    """Display batch results in a clean table."""
    st.markdown("### Results Breakdown")
    
    df = pd.DataFrame(results)
    df = df.sort_values('Score', ascending=False)
    
    # Score formatting
    df['Score_Pct'] = df['Score'].apply(lambda x: f"{x:.0%}")
    
    # Custom Table
    st.dataframe(
        df[['Filename', 'Score', 'Status']],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Score": st.column_config.ProgressColumn(
                "Match Score",
                format="%.2f",
                min_value=0,
                max_value=1,
            )
        }
    )
    
    # Export
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "DOWNLOAD CSV REPORT ➔",
        csv,
        "batch_results.csv",
        "text/csv",
        key='download-csv',
        use_container_width=True
    )
