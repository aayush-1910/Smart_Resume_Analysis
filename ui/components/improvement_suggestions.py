"""
Improvement Suggestions Component
Displays actionable resume improvement suggestions with animated UI.
"""
import streamlit as st
from typing import Dict

from ui.styles import render_score_ring


def render_improvement_suggestions(suggestions_result: Dict):
    """Render the improvement suggestions component."""

    st.markdown("""
    <div class="page-header" style="margin-bottom: 16px;">
        <h3 style="font-size: 20px;">Resume Audit</h3>
    </div>
    """, unsafe_allow_html=True)

    # Quality score
    quality_score = suggestions_result.get('overall_resume_quality_score', 50)

    if quality_score >= 80:
        score_color = "#00E599"
        msg = "Excellent Quality"
        desc = "Your resume is well-structured and ATS-compatible."
    elif quality_score >= 60:
        score_color = "#FFB800"
        msg = "Good Foundation"
        desc = "Some areas could be improved for better results."
    else:
        score_color = "#FF4757"
        msg = "Needs Improvement"
        desc = "Several areas need attention for competitive applications."

    col1, col2 = st.columns([1, 3])

    with col1:
        # SVG score ring
        ring_html = render_score_ring(quality_score, score_color, size=120, stroke=8)
        st.markdown(f"""
        <div style="text-align: center; animation: fadeInUp 0.4s ease both;">
            {ring_html}
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="padding: 16px 0; animation: fadeInUp 0.4s ease both; animation-delay: 0.1s;">
            <h4 style="margin: 0 0 4px 0; color: #F1F5F9; font-size: 18px;">{msg}</h4>
            <p style="color: #94A3B8; font-size: 14px; margin: 0;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Suggestions and strengths
    suggestions = suggestions_result.get('suggestions', [])
    positive_points = suggestions_result.get('positive_points', [])

    if not suggestions and not positive_points:
        st.success("No specific improvements found. Looks good!")
        return

    tab1, tab2 = st.tabs(["Improvements", "Strengths"])

    with tab1:
        high = [s for s in suggestions if s.get('priority') == 'high']
        medium = [s for s in suggestions if s.get('priority') == 'medium']
        low = [s for s in suggestions if s.get('priority') == 'low']

        if high:
            st.markdown('<span class="section-label">High Priority</span>', unsafe_allow_html=True)
            for s in high:
                render_suggestion_item(s, "high")

        if medium:
            st.markdown('<span class="section-label">Medium Priority</span>', unsafe_allow_html=True)
            for s in medium:
                render_suggestion_item(s, "medium")

        if low:
            st.markdown('<span class="section-label">Low Priority</span>', unsafe_allow_html=True)
            for s in low:
                render_suggestion_item(s, "low")

    with tab2:
        for i, point in enumerate(positive_points):
            st.markdown(f"""
            <div style="display: flex; gap: 12px; align-items: start; margin-bottom: 10px;
                        background: rgba(0, 229, 153, 0.04); padding: 12px 16px; border-radius: 10px;
                        border: 1px solid rgba(0, 229, 153, 0.1);
                        animation: fadeInUp 0.3s ease both; animation-delay: {i * 0.05}s;">
                <span style="color: #00E599; font-size: 14px; margin-top: 1px;">&#10003;</span>
                <span style="color: #E2E8F0; font-size: 14px; line-height: 1.5;">{point}</span>
            </div>
            """, unsafe_allow_html=True)


def render_suggestion_item(suggestion: Dict, priority: str):
    """Render a single suggestion accordion item."""
    title = suggestion.get('title', '')
    description = suggestion.get('description', '')
    action_items = suggestion.get('action_items', [])
    impact = suggestion.get('impact', '')

    if priority == 'high':
        border_color = "rgba(255, 71, 87, 0.2)"
        dot_color = "#FF4757"
    elif priority == 'medium':
        border_color = "rgba(255, 184, 0, 0.2)"
        dot_color = "#FFB800"
    else:
        border_color = "rgba(0, 217, 255, 0.2)"
        dot_color = "#00D9FF"

    with st.expander(f"{title}"):
        st.markdown(f"""
        <div style="border-left: 3px solid {dot_color}; padding-left: 14px; margin-bottom: 12px;">
            <p style='color: #94A3B8; font-size: 14px; line-height: 1.6; margin: 0;'>{description}</p>
        </div>
        """, unsafe_allow_html=True)

        if action_items:
            st.markdown('<span class="section-label">Action Items</span>', unsafe_allow_html=True)
            for item in action_items:
                st.markdown(f"""
                <div style="display: flex; gap: 8px; align-items: start; margin-bottom: 6px;">
                    <span style="color: #64748B; font-size: 10px; margin-top: 5px;">&#9679;</span>
                    <span style="color: #CBD5E1; font-size: 14px;">{item}</span>
                </div>
                """, unsafe_allow_html=True)

        if impact:
            st.markdown(f"""
            <div style="margin-top: 14px; padding: 10px 14px; background: rgba(255,255,255,0.02);
                        border-radius: 8px; font-size: 13px; border: 1px solid {border_color};">
                <span style="color: #64748B; text-transform: uppercase; font-size: 10px; letter-spacing: 1px;">Impact</span>
                <div style="color: #CBD5E1; margin-top: 4px;">{impact}</div>
            </div>
            """, unsafe_allow_html=True)
