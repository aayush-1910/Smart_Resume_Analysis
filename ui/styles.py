"""
Global CSS Styles for AI Resume Screener
Shared across all pages for consistency
"""
import streamlit as st


def apply_global_styles():
    """Inject global CSS styling into Streamlit pages."""
    st.markdown("""
    <style>
        /* Import Google Fonts */
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

        /* Global Typography */
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
        
        code, pre, .stCode, .stCodeBlock {
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

        /* Cards */
        .metric-card {
            background-color: var(--surface-color);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
            border-color: rgba(0, 217, 255, 0.3);
        }

        /* Headings */
        h1.page-title {
            font-size: 32px;
            margin-bottom: 8px;
            color: var(--text-color);
        }
        
        p.page-subtitle {
            color: var(--subtext-color);
            font-size: 16px;
            margin-bottom: 32px;
        }

        /* File Uploader */
        .stFileUploader {
            border-radius: 16px;
            border: 2px dashed var(--border-color);
            background-color: rgba(20, 27, 45, 0.5);
            padding: 32px;
            transition: all 0.2s ease;
            text-align: center;
        }
        
        .stFileUploader:hover {
            border-color: var(--primary-color);
            transform: translateY(-1px);
        }

        /* Buttons - NO GRADIENTS */
        .stButton > button {
            background: var(--primary-color);
            color: var(--bg-color);
            font-family: 'Sora', sans-serif;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.5rem;
            transition: all 0.2s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-size: 14px;
            box-shadow: 0 2px 8px rgba(0, 217, 255, 0.2);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 4px 12px rgba(0, 217, 255, 0.3);
            background: var(--primary-color);
            color: var(--bg-color);
        }

        /* Inputs */
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
            background-color: var(--surface-color);
            color: var(--text-color);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 14px;
            padding: 12px;
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
            font-size: 28px;
        }
        
        [data-testid="stMetricLabel"] {
            font-family: 'DM Sans', sans-serif;
            color: var(--subtext-color);
            text-transform: uppercase;
            font-size: 12px;
            letter-spacing: 1px;
        }

        /* Expanders */
        [data-testid="stExpander"] {
            background-color: var(--surface-color);
            border: 1px solid var(--border-color);
            border-radius: 8px;
        }

        /* Status Badges */
        .status-badge {
            padding: 6px 14px;
            border-radius: 20px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            font-weight: 600;
            display: inline-block;
        }
        
        .status-success { background: rgba(0, 229, 153, 0.15); color: var(--success-color); border: 1px solid rgba(0, 229, 153, 0.3); }
        .status-warning { background: rgba(255, 184, 0, 0.15); color: var(--warning-color); border: 1px solid rgba(255, 184, 0, 0.3); }
        .status-danger { background: rgba(255, 71, 87, 0.15); color: var(--danger-color); border: 1px solid rgba(255, 71, 87, 0.3); }

        /* Skill Pills */
        .skill-pill {
            display: inline-block;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 500;
            margin: 4px;
            transition: all 0.2s ease;
        }
        
        .skill-matched {
            background: rgba(0, 229, 153, 0.15);
            color: var(--success-color);
            border: 1px solid rgba(0, 229, 153, 0.3);
        }
        
        .skill-matched:hover {
            background: rgba(0, 229, 153, 0.25);
        }
        
        .skill-missing {
            background: rgba(255, 71, 87, 0.15);
            color: var(--danger-color);
            border: 1px solid rgba(255, 71, 87, 0.3);
        }
        
        .skill-missing:hover {
            background: rgba(255, 71, 87, 0.25);
        }

        /* Progress Bars */
        .stProgress > div > div > div > div {
            background-color: var(--primary-color);
        }

        /* Separator */
        hr { 
            margin: 2rem 0; 
            border: 0; 
            border-top: 1px solid var(--border-color); 
        }

        /* Dataframes */
        [data-testid="stDataFrame"] {
            background-color: var(--surface-color);
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }

        .stTabs [data-baseweb="tab"] {
            background-color: transparent;
            border-radius: 8px;
            color: var(--subtext-color);
            font-family: 'Sora', sans-serif;
        }

        .stTabs [aria-selected="true"] {
            background-color: rgba(0, 217, 255, 0.1);
            color: var(--primary-color);
        }
        
    </style>
    """, unsafe_allow_html=True)
