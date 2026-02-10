"""
Learning Recommendations Component
Displays personalized learning path with animated timeline and course cards.
"""
import streamlit as st
from typing import Dict


def render_learning_recommendations(learning_result: Dict):
    """Render the learning recommendations component."""

    st.markdown("""
    <div class="page-header" style="margin-bottom: 16px;">
        <h3 style="font-size: 20px;">Learning Path</h3>
    </div>
    """, unsafe_allow_html=True)

    # Overview stats
    total_skills = learning_result.get('total_skills_to_learn', 0)
    estimated_time = learning_result.get('estimated_total_time', 'Unknown')

    st.markdown(f"""
    <div style="display: flex; gap: 24px; margin-bottom: 24px; animation: fadeInUp 0.4s ease both;">
        <div class="metric-card" style="flex: 1; text-align: center; padding: 20px;">
            <div style="font-family: 'JetBrains Mono'; font-size: 32px; font-weight: 700; color: #00D9FF;">{total_skills}</div>
            <div style="font-size: 11px; color: #64748B; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px;">Skills to Master</div>
        </div>
        <div class="metric-card" style="flex: 1; text-align: center; padding: 20px;">
            <div style="font-family: 'JetBrains Mono'; font-size: 32px; font-weight: 700; color: #A78BFA;">{estimated_time}</div>
            <div style="font-size: 11px; color: #64748B; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px;">Estimated Time</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Skill-by-skill breakdown
    skills = learning_result.get('skills', [])

    for skill in skills:
        skill_name = skill.get('skill_name', '')
        courses = skill.get('recommended_courses', [])

        with st.expander(f"Learn: {skill_name}"):
            if not courses:
                st.caption("No specific courses found. Try searching YouTube or Coursera.")
                continue

            for i, course in enumerate(courses):
                render_course_card(course, i)


def render_course_card(course: Dict, index: int = 0):
    """Render a single course card with animations."""
    title = course.get('title', '')
    provider = course.get('provider', '')
    url = course.get('url', '#')
    difficulty = course.get('difficulty', 'beginner')
    duration = course.get('duration', 'self-paced')
    cost = course.get('cost', 'free')
    rating = course.get('rating', 0)

    # Difficulty badge color
    if difficulty.lower() == 'advanced':
        diff_color = "#FF4757"
        diff_bg = "rgba(255,71,87,0.1)"
    elif difficulty.lower() == 'intermediate':
        diff_color = "#FFB800"
        diff_bg = "rgba(255,184,0,0.1)"
    else:
        diff_color = "#00E599"
        diff_bg = "rgba(0,229,153,0.1)"

    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border);
                border-radius: 12px; padding: 18px 20px; margin-bottom: 10px;
                transition: all 0.2s ease; animation: fadeInUp 0.3s ease both;
                animation-delay: {index * 0.08}s;"
         onmouseover="this.style.borderColor='rgba(148,163,184,0.25)'; this.style.transform='translateY(-1px)'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.2)';"
         onmouseout="this.style.borderColor='var(--border)'; this.style.transform='translateY(0)'; this.style.boxShadow='none';">

        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div style="flex: 1;">
                <div style="font-family: 'Sora'; font-weight: 600; font-size: 15px; color: #F1F5F9;">{title}</div>
                <div style="font-size: 12px; color: #64748B; margin-top: 3px;">{provider}</div>
            </div>
            <div style="background: {diff_bg}; color: {diff_color}; font-size: 10px;
                        padding: 3px 10px; border-radius: 12px; font-weight: 600;
                        letter-spacing: 0.5px; text-transform: uppercase; white-space: nowrap;">
                {difficulty}
            </div>
        </div>

        <div style="margin-top: 14px; display: flex; gap: 20px; font-size: 12px; color: #94A3B8;">
            <span>{duration}</span>
            <span>{cost.title()}</span>
            <span>Rating: {rating if rating else 'N/A'}</span>
        </div>

        <a href="{url}" target="_blank" style="display: block; text-align: center;
           margin-top: 14px; background: rgba(0,217,255,0.08); color: #00D9FF;
           text-decoration: none; padding: 10px; border-radius: 8px;
           font-weight: 600; font-size: 13px; font-family: 'Sora';
           border: 1px solid rgba(0,217,255,0.15);
           transition: all 0.2s ease;"
           onmouseover="this.style.background='rgba(0,217,255,0.15)'; this.style.borderColor='rgba(0,217,255,0.3)';"
           onmouseout="this.style.background='rgba(0,217,255,0.08)'; this.style.borderColor='rgba(0,217,255,0.15)';">
            Start Learning
        </a>
    </div>
    """, unsafe_allow_html=True)


def render_learning_milestones(learning_result: Dict):
    """Render the learning path milestones as a connected timeline."""
    milestones = learning_result.get('learning_path_milestones', [])

    if not milestones:
        return

    st.markdown("""
    <div class="page-header" style="margin-top: 24px; margin-bottom: 16px;">
        <h3 style="font-size: 20px;">Timeline</h3>
    </div>
    """, unsafe_allow_html=True)

    for i, milestone in enumerate(milestones):
        month = milestone.get('month', 0)
        focus = milestone.get('focus', '')
        is_last = i == len(milestones) - 1

        st.markdown(f"""
        <div style="display: flex; gap: 16px; animation: fadeInUp 0.3s ease both; animation-delay: {i * 0.1}s;">
            <div style="display: flex; flex-direction: column; align-items: center; min-width: 24px;">
                <div style="width: 12px; height: 12px; border-radius: 50%; background: #00D9FF;
                     box-shadow: 0 0 10px rgba(0,217,255,0.3); flex-shrink: 0;"></div>
                {'<div style="width: 2px; flex: 1; background: rgba(0,217,255,0.15); margin: 4px 0;"></div>' if not is_last else ''}
            </div>
            <div style="padding-bottom: {'24px' if not is_last else '0'};">
                <div style="font-family: 'JetBrains Mono'; font-size: 11px; color: #00D9FF;
                     font-weight: 600; letter-spacing: 1px;">MONTH {month}</div>
                <div style="font-size: 15px; color: #F1F5F9; font-weight: 500; margin-top: 4px;">{focus}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
