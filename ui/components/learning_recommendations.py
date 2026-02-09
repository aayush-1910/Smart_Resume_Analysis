"""
Learning Recommendations Component
Displays personalized learning path for missing skills.
"""
import streamlit as st
from typing import Dict


def render_learning_recommendations(learning_result: Dict):
    """
    Render the learning recommendations component.
    
    Args:
        learning_result: Result from generate_learning_recommendations()
    """
    st.markdown("### Learning Path")
    
    # Overview
    total_skills = learning_result.get('total_skills_to_learn', 0)
    estimated_time = learning_result.get('estimated_total_time', 'Unknown')
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Skills to Master:** {total_skills}")
    with col2:
        st.markdown(f"**Total Est. Time:** {estimated_time}")
    
    st.markdown("---")
    
    # Skill-by-skill breakdown
    skills = learning_result.get('skills', [])
    
    for skill in skills:
        skill_name = skill.get('skill_name', '')
        importance = skill.get('importance', '')
        courses = skill.get('recommended_courses', [])
        
        with st.expander(f"📚 Learn: {skill_name}"):
            if not courses:
                st.write("No specific courses found. Try searching YouTube or Coursera.")
                continue
            
            for course in courses:
                render_course_card(course)


def render_course_card(course: Dict):
    """Render a single course card."""
    title = course.get('title', '')
    provider = course.get('provider', '')
    url = course.get('url', '')
    difficulty = course.get('difficulty', 'beginner')
    duration = course.get('duration', 'self-paced')
    cost = course.get('cost', 'free')
    rating = course.get('rating', 0)
    
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(148, 163, 184, 0.2); border-radius: 12px; padding: 16px; margin-bottom: 12px; transition: transform 0.2s;">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div>
                <h4 style="margin: 0; font-size: 16px; color: #FFFFFF;">{title}</h4>
                <p style="margin: 4px 0 0 0; font-size: 12px; color: #94A3B8;">{provider}</p>
            </div>
            <div style="background: rgba(0, 217, 255, 0.1); color: #00D9FF; font-size: 10px; padding: 2px 8px; border-radius: 12px; font-weight: 600;">
                {difficulty.upper()}
            </div>
        </div>
        
        <div style="margin-top: 12px; display: flex; gap: 16px; font-size: 12px; color: #CBD5E1;">
            <span>⏱ {duration}</span>
            <span>💰 {cost.title()}</span>
            <span>⭐ {rating if rating else 'N/A'}</span>
        </div>
        
        <div style="margin-top: 16px;">
            <a href="{url}" target="_blank" style="display: block; text-align: center; background: rgba(0, 217, 255, 0.1); color: #00D9FF; text-decoration: none; padding: 8px; border-radius: 6px; font-weight: 600; font-size: 13px; border: 1px solid rgba(0, 217, 255, 0.3); transition: all 0.2s;">
                START LEARNING ➔
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_learning_milestones(learning_result: Dict):
    """Render the learning path milestones."""
    milestones = learning_result.get('learning_path_milestones', [])
    
    if not milestones:
        return
    
    st.markdown("### Timeline")
    
    for milestone in milestones:
        month = milestone.get('month', 0)
        focus = milestone.get('focus', '')
        
        st.markdown(f"""
        <div style="border-left: 2px solid #00D9FF; padding-left: 16px; margin-left: 8px; margin-bottom: 24px;">
            <div style="font-size: 12px; color: #00D9FF; font-weight: 600;">MONTH {month}</div>
            <div style="font-size: 16px; color: #FFFFFF; font-weight: 600; margin-top: 4px;">{focus}</div>
        </div>
        """, unsafe_allow_html=True)
