"""
Global CSS Styles for Smart Resume Coach
Premium dark theme with animations, glassmorphism, and micro-interactions
"""
import streamlit as st


def apply_global_styles():
    """Inject production-grade CSS into Streamlit."""
    st.markdown("""
    <style>
        /* =====================================================================
           FONTS
           ===================================================================== */
        @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700&family=DM+Sans:ital,wght@0,400;0,500;0,700;1,400&family=JetBrains+Mono:wght@400;500;600&display=swap');

        :root {
            --bg-primary: #0A0E1A;
            --bg-secondary: #0F1528;
            --surface: #141B2D;
            --surface-hover: #1A2340;
            --accent: #00D9FF;
            --accent-dim: rgba(0, 217, 255, 0.12);
            --accent-glow: rgba(0, 217, 255, 0.25);
            --success: #00E599;
            --success-dim: rgba(0, 229, 153, 0.12);
            --warning: #FFB800;
            --warning-dim: rgba(255, 184, 0, 0.12);
            --danger: #FF4757;
            --danger-dim: rgba(255, 71, 87, 0.12);
            --text-primary: #F1F5F9;
            --text-secondary: #94A3B8;
            --text-muted: #64748B;
            --border: rgba(148, 163, 184, 0.12);
            --border-hover: rgba(148, 163, 184, 0.25);
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
            --radius-xl: 20px;
            --shadow-sm: 0 1px 2px rgba(0,0,0,0.3);
            --shadow-md: 0 4px 12px rgba(0,0,0,0.25);
            --shadow-lg: 0 8px 24px rgba(0,0,0,0.35);
            --shadow-glow: 0 0 20px rgba(0, 217, 255, 0.15);
        }

        /* =====================================================================
           KEYFRAME ANIMATIONS
           ===================================================================== */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(16px); }
            to   { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to   { opacity: 1; }
        }
        @keyframes slideInRight {
            from { opacity: 0; transform: translateX(-12px); }
            to   { opacity: 1; transform: translateX(0); }
        }
        @keyframes sweepRight {
            from { width: 0%; }
        }
        @keyframes pulseGlow {
            0%, 100% { box-shadow: 0 0 8px rgba(0, 217, 255, 0.15); }
            50%      { box-shadow: 0 0 24px rgba(0, 217, 255, 0.3); }
        }
        @keyframes shimmer {
            0%   { background-position: -200% 0; }
            100% { background-position: 200% 0; }
        }
        @keyframes countUp {
            from { opacity: 0; transform: scale(0.8); }
            to   { opacity: 1; transform: scale(1); }
        }
        @keyframes dotPulse {
            0%, 100% { opacity: 0.3; }
            50%      { opacity: 0.6; }
        }

        /* =====================================================================
           GLOBAL RESET & TYPOGRAPHY
           ===================================================================== */
        html, body, [class*="css"] {
            font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            color: var(--text-primary);
            background-color: var(--bg-primary);
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: 'Sora', sans-serif;
            font-weight: 600;
            color: var(--text-primary);
            letter-spacing: -0.02em;
        }

        code, pre, .stCode, .stCodeBlock {
            font-family: 'JetBrains Mono', monospace;
        }

        /* Hide Streamlit chrome */
        #MainMenu, footer, header { visibility: hidden; }
        .stDeployButton { display: none; }

        /* =====================================================================
           LAYOUT
           ===================================================================== */
        .main .block-container {
            padding: 2.5rem 2rem 4rem 2rem;
            max-width: 1200px;
        }

        /* Dot grid background on main area */
        .stApp {
            background:
                radial-gradient(circle at 1px 1px, rgba(148,163,184,0.06) 1px, transparent 0) 0 0 / 32px 32px,
                linear-gradient(180deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
        }

        /* =====================================================================
           SIDEBAR
           ===================================================================== */
        [data-testid="stSidebar"] {
            background: rgba(20, 27, 45, 0.85);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-right: 1px solid var(--border);
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] .stMarkdown h1 {
            font-family: 'Sora', sans-serif !important;
            font-size: 18px !important;
            font-weight: 700 !important;
            color: var(--text-primary) !important;
            letter-spacing: -0.02em;
            margin-bottom: 1.5rem;
        }

        /* Radio buttons as nav items */
        [data-testid="stSidebar"] .stRadio > div {
            gap: 4px;
        }

        [data-testid="stSidebar"] .stRadio > div > label {
            padding: 10px 16px;
            border-radius: var(--radius-sm);
            transition: all 0.15s ease;
            font-size: 14px;
            font-weight: 500;
            color: var(--text-secondary);
            cursor: pointer;
        }

        [data-testid="stSidebar"] .stRadio > div > label:hover {
            background: rgba(255,255,255,0.04);
            color: var(--text-primary);
        }

        [data-testid="stSidebar"] .stRadio > div > label[data-checked="true"],
        [data-testid="stSidebar"] .stRadio > div > label:has(input:checked) {
            background: var(--accent-dim);
            color: var(--accent);
            font-weight: 600;
        }

        /* =====================================================================
           CARDS
           ===================================================================== */
        .glass-card {
            background: rgba(20, 27, 45, 0.75);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 28px;
            transition: all 0.2s ease;
            animation: fadeInUp 0.5s ease both;
        }

        .glass-card:hover {
            border-color: var(--border-hover);
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }

        .metric-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 24px;
            transition: all 0.2s ease;
            animation: fadeInUp 0.4s ease both;
        }

        .metric-card:hover {
            border-color: var(--border-hover);
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }

        /* =====================================================================
           HERO SCORE
           ===================================================================== */
        .score-hero {
            text-align: center;
            padding: 32px 24px;
            animation: fadeInUp 0.5s ease both;
        }

        .score-ring-container {
            position: relative;
            width: 180px;
            height: 180px;
            margin: 0 auto 16px auto;
        }

        .score-ring-container svg {
            transform: rotate(-90deg);
        }

        .score-number {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-family: 'JetBrains Mono', monospace;
            font-size: 48px;
            font-weight: 700;
            animation: countUp 0.6s ease both;
            animation-delay: 0.3s;
        }

        .score-label {
            font-family: 'DM Sans', sans-serif;
            font-size: 13px;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-top: 8px;
        }

        /* =====================================================================
           PROGRESS BARS (custom)
           ===================================================================== */
        .progress-track {
            width: 100%;
            height: 6px;
            background: rgba(255,255,255,0.06);
            border-radius: 3px;
            overflow: hidden;
            margin-top: 10px;
        }

        .progress-fill {
            height: 100%;
            border-radius: 3px;
            animation: sweepRight 0.8s ease both;
            animation-delay: 0.4s;
        }

        /* Streamlit default progress bar */
        .stProgress > div > div > div > div {
            background-color: var(--accent);
            border-radius: 3px;
        }

        /* =====================================================================
           SKILL PILLS
           ===================================================================== */
        .skill-pill {
            display: inline-block;
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 500;
            margin: 3px;
            transition: all 0.2s ease;
            animation: fadeIn 0.3s ease both;
        }

        .skill-matched {
            background: var(--success-dim);
            color: var(--success);
            border: 1px solid rgba(0, 229, 153, 0.25);
        }
        .skill-matched:hover {
            background: rgba(0, 229, 153, 0.2);
            transform: translateY(-1px);
        }

        .skill-missing {
            background: var(--danger-dim);
            color: var(--danger);
            border: 1px solid rgba(255, 71, 87, 0.25);
        }
        .skill-missing:hover {
            background: rgba(255, 71, 87, 0.2);
            transform: translateY(-1px);
        }

        /* =====================================================================
           BUTTONS
           ===================================================================== */
        .stButton > button {
            background: var(--accent);
            color: var(--bg-primary);
            font-family: 'Sora', sans-serif;
            font-weight: 600;
            border: none;
            border-radius: var(--radius-sm);
            padding: 0.65rem 1.5rem;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            transition: all 0.2s ease;
            box-shadow: 0 2px 8px rgba(0, 217, 255, 0.15);
        }

        .stButton > button:hover {
            transform: translateY(-2px) scale(1.02);
            box-shadow: var(--shadow-glow);
            background: var(--accent);
            color: var(--bg-primary);
        }

        .stButton > button:active {
            transform: translateY(0) scale(1);
        }

        /* =====================================================================
           INPUTS
           ===================================================================== */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            background: var(--surface);
            color: var(--text-primary);
            border: 1px solid var(--border);
            border-radius: var(--radius-sm);
            font-size: 14px;
            padding: 12px;
            transition: all 0.2s ease;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 1px var(--accent), var(--shadow-glow);
        }

        /* =====================================================================
           FILE UPLOADER
           ===================================================================== */
        .stFileUploader {
            border-radius: var(--radius-lg);
            border: 2px dashed var(--border);
            background: rgba(20, 27, 45, 0.4);
            padding: 32px;
            transition: all 0.25s ease;
            text-align: center;
        }

        .stFileUploader:hover {
            border-color: var(--accent);
            background: rgba(0, 217, 255, 0.04);
            transform: translateY(-1px);
        }

        /* =====================================================================
           EXPANDERS
           ===================================================================== */
        [data-testid="stExpander"] {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            transition: all 0.2s ease;
        }

        [data-testid="stExpander"]:hover {
            border-color: var(--border-hover);
        }

        /* =====================================================================
           METRICS
           ===================================================================== */
        [data-testid="stMetricValue"] {
            font-family: 'JetBrains Mono', monospace;
            color: var(--accent);
            font-size: 28px;
        }

        [data-testid="stMetricLabel"] {
            font-family: 'DM Sans', sans-serif;
            color: var(--text-secondary);
            text-transform: uppercase;
            font-size: 11px;
            letter-spacing: 1.5px;
        }

        /* =====================================================================
           STATUS BADGES
           ===================================================================== */
        .status-badge {
            padding: 6px 14px;
            border-radius: 20px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            font-weight: 600;
            display: inline-block;
            letter-spacing: 0.5px;
        }

        .status-success {
            background: var(--success-dim);
            color: var(--success);
            border: 1px solid rgba(0, 229, 153, 0.25);
        }
        .status-warning {
            background: var(--warning-dim);
            color: var(--warning);
            border: 1px solid rgba(255, 184, 0, 0.25);
        }
        .status-danger {
            background: var(--danger-dim);
            color: var(--danger);
            border: 1px solid rgba(255, 71, 87, 0.25);
        }

        /* =====================================================================
           DATAFRAMES / TABLES
           ===================================================================== */
        [data-testid="stDataFrame"] {
            background: var(--surface);
            border-radius: var(--radius-md);
        }

        /* =====================================================================
           TABS
           ===================================================================== */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            border-bottom: 1px solid var(--border);
        }

        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border-radius: var(--radius-sm) var(--radius-sm) 0 0;
            color: var(--text-secondary);
            font-family: 'Sora', sans-serif;
            font-size: 14px;
            font-weight: 500;
            padding: 10px 20px;
            transition: all 0.15s ease;
        }

        .stTabs [data-baseweb="tab"]:hover {
            color: var(--text-primary);
            background: rgba(255,255,255,0.03);
        }

        .stTabs [aria-selected="true"] {
            background: var(--accent-dim);
            color: var(--accent);
            font-weight: 600;
        }

        /* =====================================================================
           SEPARATORS
           ===================================================================== */
        hr {
            margin: 2rem 0;
            border: 0;
            border-top: 1px solid var(--border);
        }

        /* =====================================================================
           CUSTOM SCROLLBAR
           ===================================================================== */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb {
            background: rgba(148, 163, 184, 0.2);
            border-radius: 3px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(148, 163, 184, 0.35);
        }

        /* =====================================================================
           PAGE HEADERS
           ===================================================================== */
        .page-header {
            margin-bottom: 32px;
            animation: fadeInUp 0.4s ease both;
        }

        .page-header h1 {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 6px;
            color: var(--text-primary);
        }

        .page-header p {
            font-size: 15px;
            color: var(--text-secondary);
            margin: 0;
        }

        /* Section Headers */
        .section-label {
            font-family: 'DM Sans', sans-serif;
            font-size: 11px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 12px;
            display: block;
        }

    </style>
    """, unsafe_allow_html=True)


def render_score_ring(score_pct: int, color: str, size: int = 180, stroke: int = 10):
    """Generate SVG circular score ring HTML."""
    radius = (size - stroke) / 2
    circumference = 2 * 3.14159 * radius
    offset = circumference - (score_pct / 100) * circumference

    return f"""
    <div class="score-ring-container" style="width:{size}px; height:{size}px;">
        <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
            <circle cx="{size/2}" cy="{size/2}" r="{radius}"
                    fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="{stroke}"/>
            <circle cx="{size/2}" cy="{size/2}" r="{radius}"
                    fill="none" stroke="{color}" stroke-width="{stroke}"
                    stroke-linecap="round"
                    stroke-dasharray="{circumference}"
                    stroke-dashoffset="{offset}"
                    style="transition: stroke-dashoffset 1s ease 0.2s;"/>
        </svg>
        <div class="score-number" style="color: {color};">{score_pct}%</div>
    </div>
    """


def render_progress_bar(value_pct: int, color: str = "var(--accent)", delay: str = "0.4s"):
    """Generate animated progress bar HTML."""
    return f"""
    <div class="progress-track">
        <div class="progress-fill" style="width: {value_pct}%; background: {color}; animation-delay: {delay};"></div>
    </div>
    """


def get_score_color(score: float) -> str:
    """Return appropriate color for a score value (0-1 range)."""
    if score >= 0.75:
        return "var(--success)"
    elif score >= 0.55:
        return "var(--warning)"
    elif score >= 0.35:
        return "var(--accent)"
    else:
        return "var(--danger)"


def get_score_hex(score: float) -> str:
    """Return hex color for a score value (0-1 range)."""
    if score >= 0.75:
        return "#00E599"
    elif score >= 0.55:
        return "#FFB800"
    elif score >= 0.35:
        return "#00D9FF"
    else:
        return "#FF4757"
