"""
Improvement Suggestions Component
Displays actionable resume improvement suggestions.
"""
import streamlit as st
from typing import Dict


def render_improvement_suggestions(suggestions_result: Dict):
    """
    Render the improvement suggestions component.
    
    Args:
        suggestions_result: Result from generate_improvement_suggestions()
    """
    st.markdown("### Resume Audit")
    
    # Quality score
    quality_score = suggestions_result.get('overall_resume_quality_score', 50)
    
    # Determine color based on score
    if quality_score >= 80:
        score_color = "#00E599" # Success
        msg = "Excellent Quality"
    elif quality_score >= 60:
        score_color = "#FFB800" # Warning
        msg = "Good Foundation"
    else:
        score_color = "#FF4757" # Danger
        msg = "Needs Improvement"
        
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.03); border-radius: 12px; padding: 16px; text-align: center; border: 1px solid rgba(148, 163, 184, 0.2);">
            <div style="font-family: 'JetBrains Mono'; font-size: 36px; font-weight: 700; color: {score_color};">{quality_score}</div>
            <div style="font-size: 12px; color: #94A3B8; margin-top: 4px;">QUALITY SCORE</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div style="padding: 12px;">
            <h4 style="margin: 0; color: #FFFFFF;">{msg}</h4>
            <p style="color: #94A3B8; font-size: 14px; margin-top: 4px;">Based on structure, content, and ATS compatibility checks.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    # Suggestions grouped by priority
    suggestions = suggestions_result.get('suggestions', [])
    positive_points = suggestions_result.get('positive_points', [])
    
    if not suggestions and not positive_points:
        st.success("No specific improvements found. Looks good!")
        return

    # Tabs for organization
    tab1, tab2 = st.tabs(["🔴 Improvements", "🟢 Strengths"])
    
    with tab1:
        # Group by priority
        high = [s for s in suggestions if s.get('priority') == 'high']
        medium = [s for s in suggestions if s.get('priority') == 'medium']
        low = [s for s in suggestions if s.get('priority') == 'low']
        
        if high:
            st.caption("HIGH PRIORITY")
            for s in high:
                render_accordion_item(s, "high")
                
        if medium:
            st.caption("MEDIUM PRIORITY")
            for s in medium:
                render_accordion_item(s, "medium")
                
        if low:
            st.caption("LOW PRIORITY")
            for s in low:
                render_accordion_item(s, "low")
                
    with tab2:
        for point in positive_points:
            st.markdown(f"""
            <div style="display: flex; gap: 12px; align-items: start; margin-bottom: 12px; background: rgba(0, 229, 153, 0.05); padding: 12px; border-radius: 8px;">
                <span style="color: #00E599;">✓</span>
                <span style="color: #E2E8F0; font-size: 14px;">{point}</span>
            </div>
            """, unsafe_allow_html=True)


def render_accordion_item(suggestion: Dict, priority: str):
    """Render a single suggestion accordion."""
    title = suggestion.get('title', '')
    description = suggestion.get('description', '')
    action_items = suggestion.get('action_items', [])
    impact = suggestion.get('impact', '')
    
    # Icons and colors
    if priority == 'high':
        icon = "🔴"
        border_color = "rgba(255, 71, 87, 0.3)"
    elif priority == 'medium':
        icon = "🟡"
        border_color = "rgba(255, 184, 0, 0.3)"
    else:
        icon = "🔵"
        border_color = "rgba(59, 130, 246, 0.3)"
        
    with st.expander(f"{icon} {title}"):
        st.markdown(f"<p style='color: #94A3B8; font-size: 14px;'>{description}</p>", unsafe_allow_html=True)
        
        if action_items:
            st.markdown("**Action Items:**")
            for item in action_items:
                st.markdown(f"- {item}")
        
        if impact:
            st.markdown(f"""
            <div style="margin-top: 12px; padding: 8px 12px; background: rgba(255,255,255,0.05); border-radius: 6px; font-size: 12px; border: 1px solid {border_color};">
                <strong>Impact:</strong> {impact}
            </div>
            """, unsafe_allow_html=True)
