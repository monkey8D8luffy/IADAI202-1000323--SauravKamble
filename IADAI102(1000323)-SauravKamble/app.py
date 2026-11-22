import calendar
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

from src.ai_analyst import ask_groq_analyst
from src.preprocess import load_and_clean_data

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & LOGISTICS-STYLE OBSIDIAN RED/BLUE THEME (CLEAN, NO EMOJIS)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="FootLens Pro | Sports Science & Performance Intelligence",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom High-End Apple visionOS / Obsidian Glassmorphism Styling - AMOLED Black, White Neon & Purple Glow
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

    :root {
        --amoled: #000000;
        --surface: #040508;
        --surface-glass: rgba(5, 6, 11, 0.92);
        --tx: #ffffff;
        --mute: #cbd5e1;
        --white-neon: #ffffff;
        --white-neon-glow: rgba(255, 255, 255, 0.40);
        --purple-neon: #c084fc;
        --purple-bright: #d8b4fe;
        --purple-glow: rgba(168, 85, 247, 0.35);
        --purple-deep: #7e22ce;
        --purple-border: rgba(168, 85, 247, 0.20);
    }

    /* Pure AMOLED Black Canvas with Subtle Focused Glow */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #000000 !important;
    }
    .stApp {
        background:
            radial-gradient(35vw 25vh at 5% 0%, rgba(255, 255, 255, 0.04), transparent 70%),
            radial-gradient(35vw 30vh at 95% 0%, rgba(168, 85, 247, 0.08), transparent 70%),
            #000000 !important;
        background-attachment: fixed !important;
        color: var(--tx) !important;
        font-family: 'Manrope', system-ui, -apple-system, sans-serif !important;
        -webkit-font-smoothing: antialiased;
    }

    /* Fill viewport width naturally without cramped layout */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2.5rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }

    /* Clean Streamlined Brand Header with Crisp Refined Glow */
    .brand-bar {
        margin-bottom: 0.9rem;
        display: flex;
        flex-direction: column;
        gap: 3px;
    }
    .brand-title {
        font-size: 26px;
        font-weight: 800;
        letter-spacing: -0.025em;
        color: #ffffff;
        margin: 0;
        line-height: 1.2;
    }
    .gradient-accent {
        color: #c084fc;
        text-shadow: 0 0 12px rgba(192, 132, 252, 0.50);
    }
    .brand-sub {
        font-size: 13px;
        color: #94a3b8;
        margin: 0;
        font-weight: 500;
    }

    /* KPI Row Grid - AMOLED Black with Crisp Laser Edges & Refined Glow */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 0.75rem;
        margin-bottom: 1.1rem;
        width: 100%;
    }
    @media (max-width: 1280px) {
        .kpi-grid { grid-template-columns: repeat(3, 1fr); }
    }
    @media (max-width: 768px) {
        .kpi-grid { grid-template-columns: repeat(2, 1fr); }
    }
    .kpi-card {
        padding: 0.9rem 1.1rem;
        border-radius: 14px;
        position: relative;
        overflow: hidden;
        background: radial-gradient(100% 60% at 0% 0%, rgba(255, 255, 255, 0.03), transparent 55%),
                    rgba(6, 7, 12, 0.92);
        border: 1px solid rgba(168, 85, 247, 0.18);
        border-top: 1px solid rgba(255, 255, 255, 0.55);
        backdrop-filter: blur(24px);
        box-shadow: 0 6px 20px -6px #000000, 0 0 10px -2px rgba(168, 85, 247, 0.12);
        transition: transform 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: rgba(192, 132, 252, 0.40);
        box-shadow: 0 10px 26px -6px #000000, 0 0 16px rgba(168, 85, 247, 0.25);
    }
    .kpi-accent-bar {
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, #ffffff 0%, #c084fc 50%, #9333ea 100%);
        box-shadow: 0 0 6px rgba(192, 132, 252, 0.40);
    }
    .kpi-label {
        font-size: 10.5px;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: #94a3b8;
        margin-bottom: 0.25rem;
    }
    .kpi-val {
        font-size: 24px;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #ffffff;
        font-variant-numeric: tabular-nums;
        line-height: 1.15;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.8), 0 0 8px rgba(192, 132, 252, 0.25);
    }
    .kpi-badge {
        display: inline-block;
        margin-top: 0.35rem;
        font-size: 10.5px;
        font-weight: 700;
        padding: 2.5px 8px;
        border-radius: 99px;
        font-variant-numeric: tabular-nums;
        letter-spacing: 0.02em;
    }
    .kpi-badge.white {
        background: rgba(255, 255, 255, 0.08);
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.35);
        box-shadow: 0 0 6px rgba(255, 255, 255, 0.15);
    }
    .kpi-badge.purple {
        background: rgba(168, 85, 247, 0.12);
        color: #e9d5ff;
        border: 1px solid rgba(168, 85, 247, 0.35);
        box-shadow: 0 0 6px rgba(168, 85, 247, 0.20);
    }
    .kpi-badge.violet {
        background: rgba(126, 34, 206, 0.14);
        color: #d8b4fe;
        border: 1px solid rgba(192, 132, 252, 0.35);
        box-shadow: 0 0 6px rgba(147, 51, 234, 0.20);
    }

    /* AMOLED Black Liquid White & Purple Neon Pill Tab Dock */
    div[role="tablist"] {
        display: inline-flex !important;
        align-items: center !important;
        gap: 4px !important;
        padding: 4px 5px !important;
        border-radius: 9999px !important;
        background: radial-gradient(120% 80% at 50% 0%, rgba(255, 255, 255, 0.04) 0%, transparent 100%),
                    rgba(6, 7, 12, 0.94) !important;
        -webkit-backdrop-filter: blur(36px) saturate(200%) !important;
        backdrop-filter: blur(36px) saturate(200%) !important;
        border: 1px solid rgba(168, 85, 247, 0.20) !important;
        border-top: 1px solid rgba(255, 255, 255, 0.45) !important;
        box-shadow: 0 8px 24px -8px #000000,
                    0 0 10px -2px rgba(168, 85, 247, 0.15),
                    inset 0 1px 0 rgba(255, 255, 255, 0.20) !important;
        margin: 0.3rem 0 1.25rem 0 !important;
        width: fit-content !important;
        max-width: 100% !important;
        overflow-x: auto !important;
        scrollbar-width: none !important;
    }
    div[role="tablist"]::-webkit-scrollbar {
        display: none !important;
    }
    div[role="tab"] {
        border-radius: 9999px !important;
        padding: 7px 18px !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        letter-spacing: -0.01em !important;
        border: 1px solid transparent !important;
        background: transparent !important;
        cursor: pointer !important;
        white-space: nowrap !important;
        position: relative !important;
        user-select: none !important;
        transition: color 0.22s ease, background 0.3s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.3s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.22s ease !important;
    }
    div[role="tab"]:hover {
        color: #ffffff !important;
        background: rgba(255, 255, 255, 0.06) !important;
    }
    div[role="tab"]:active {
        transform: scale(0.97) !important;
        transition: transform 0.08s ease !important;
    }
    /* Liquid Morph Active Tab Pill (Refined White Neon Border with Subtle Purple Glow) */
    div[role="tab"][aria-selected="true"] {
        color: #ffffff !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.90) 0%, rgba(126, 34, 206, 0.90) 100%) !important;
        background-size: 200% 200% !important;
        animation: whitePurpleFlow 4s ease infinite alternate !important;
        backdrop-filter: blur(24px) saturate(180%) !important;
        border: 1px solid rgba(192, 132, 252, 0.45) !important;
        border-top: 1.5px solid #ffffff !important;
        border-bottom: 1px solid rgba(126, 34, 206, 0.40) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5),
                    0 0 14px rgba(168, 85, 247, 0.40),
                    inset 0 1px 1px rgba(255, 255, 255, 0.50) !important;
        filter: none !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.6) !important;
    }
    @keyframes whitePurpleFlow {
        0% {
            background-position: 0% 50%;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5),
                        0 0 14px rgba(168, 85, 247, 0.40),
                        inset 0 1px 1px rgba(255, 255, 255, 0.50);
        }
        100% {
            background-position: 100% 50%;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5),
                        0 0 14px rgba(192, 132, 252, 0.40),
                        inset 0 1px 1px rgba(255, 255, 255, 0.50);
        }
    }
    .react-aria-SelectionIndicator, div[data-baseweb="tab-highlight"], div[data-baseweb="tab-border"] {
        display: none !important;
    }

    /* Second Tab Bar ("Select Impact Metric") - AMOLED Black Liquid Neon Pill Dock */
    div[data-testid="stButtonGroup"],
    div.stButtonGroup,
    div[data-testid="stSegmentedControl"],
    div[data-testid="stPills"] {
        margin-bottom: 0.95rem !important;
    }
    div[data-testid="stButtonGroup"] > label,
    div.stButtonGroup > label,
    div[data-testid="stSegmentedControl"] > label,
    div[data-testid="stPills"] > label {
        display: block !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
        color: #94a3b8 !important;
        margin-bottom: 0.45rem !important;
    }
    div[data-testid="stButtonGroup"] > div,
    div.stButtonGroup > div,
    div[data-testid="stButtonGroup"] .react-aria-ToggleButtonGroup,
    div[data-testid="stSegmentedControl"] > div,
    div[data-testid="stPills"] > div {
        display: inline-flex !important;
        flex-wrap: wrap !important;
        align-items: center !important;
        gap: 4px !important;
        padding: 4px 5px !important;
        border-radius: 9999px !important;
        background: radial-gradient(120% 80% at 50% 0%, rgba(255, 255, 255, 0.04) 0%, transparent 100%),
                    rgba(6, 7, 12, 0.92) !important;
        -webkit-backdrop-filter: blur(36px) saturate(200%) !important;
        backdrop-filter: blur(36px) saturate(200%) !important;
        border: 1px solid rgba(168, 85, 247, 0.20) !important;
        border-top: 1px solid rgba(255, 255, 255, 0.45) !important;
        border-bottom: 1px solid rgba(126, 34, 206, 0.25) !important;
        box-shadow: 0 8px 24px -8px #000000,
                    0 0 10px -2px rgba(168, 85, 247, 0.15),
                    inset 0 1px 0 rgba(255, 255, 255, 0.20) !important;
        width: fit-content !important;
        max-width: 100% !important;
    }
    /* Graceful Adaptation for Smaller Columns / Mobile / Narrow Orientation */
    @media (max-width: 820px) {
        div[data-testid="stButtonGroup"] > div,
        div.stButtonGroup > div,
        div[data-testid="stButtonGroup"] .react-aria-ToggleButtonGroup,
        div[data-testid="stSegmentedControl"] > div,
        div[data-testid="stPills"] > div {
            border-radius: 18px !important;
        }
    }
    div[data-testid="stButtonGroup"] button,
    div.stButtonGroup button,
    div[data-testid="stSegmentedControl"] button,
    div[data-testid="stPills"] button {
        border-radius: 9999px !important;
        padding: 6px 16px !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 12.5px !important;
        letter-spacing: -0.01em !important;
        border: 1px solid transparent !important;
        background: transparent !important;
        cursor: pointer !important;
        white-space: nowrap !important;
        transition: color 0.22s ease, background 0.3s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.3s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.22s ease !important;
        margin: 0 !important;
        box-shadow: none !important;
        user-select: none !important;
    }
    div[data-testid="stButtonGroup"] button:hover,
    div.stButtonGroup button:hover,
    div[data-testid="stSegmentedControl"] button:hover,
    div[data-testid="stPills"] button:hover {
        color: #ffffff !important;
        background: rgba(255, 255, 255, 0.06) !important;
    }
    div[data-testid="stButtonGroup"] button:active,
    div.stButtonGroup button:active,
    div[data-testid="stSegmentedControl"] button:active,
    div[data-testid="stPills"] button:active {
        transform: scale(0.97) !important;
        transition: transform 0.08s ease !important;
    }
    /* Liquid Morph Active Pill in Second Tab Bar - Refined Focused Glow */
    div[data-testid="stButtonGroup"] button[data-selected="true"],
    div[data-testid="stButtonGroup"] button[aria-checked="true"],
    div[data-testid="stButtonGroup"] button[aria-pressed="true"],
    div[data-testid="stButtonGroup"] button[data-state="on"],
    div.stButtonGroup button[data-selected="true"],
    div.stButtonGroup button[aria-checked="true"],
    div[data-testid="stSegmentedControl"] button[aria-checked="true"],
    div[data-testid="stSegmentedControl"] button[data-state="on"],
    div[data-testid="stPills"] button[aria-checked="true"],
    div[data-testid="stPills"] button[data-state="on"] {
        color: #ffffff !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.90) 0%, rgba(126, 34, 206, 0.90) 100%) !important;
        background-size: 200% 200% !important;
        animation: whitePurpleFlow 4s ease infinite alternate !important;
        backdrop-filter: blur(24px) saturate(180%) !important;
        border: 1px solid rgba(192, 132, 252, 0.45) !important;
        border-top: 1.5px solid #ffffff !important;
        border-bottom: 1px solid rgba(126, 34, 206, 0.40) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5),
                    0 0 14px rgba(168, 85, 247, 0.40),
                    inset 0 1px 1px rgba(255, 255, 255, 0.50) !important;
        filter: none !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.6) !important;
    }

    /* Universal Nuclear Defense: Completely eliminate radio check circles and convert any st.radio to Liquid Pill Dock */
    div[data-testid="stRadio"] [data-baseweb="radio"] > div:first-child,
    div[data-testid="stRadio"] div[data-testid="stRadioCircle"],
    div[data-testid="stRadio"] div[data-testid="stRadioCircleCheck"],
    div[data-testid="stRadio"] input[type="radio"],
    div[data-testid="stRadio"] svg,
    div[data-baseweb="radio"] > div:first-child,
    div[data-baseweb="radio"] svg {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        opacity: 0 !important;
        position: absolute !important;
        pointer-events: none !important;
    }
    div[data-testid="stRadio"] > div[role="radiogroup"],
    div[data-testid="stRadio"] div[data-baseweb="radio-group"] {
        display: inline-flex !important;
        flex-wrap: wrap !important;
        align-items: center !important;
        gap: 4px !important;
        padding: 4px 5px !important;
        border-radius: 9999px !important;
        background: radial-gradient(120% 80% at 50% 0%, rgba(255, 255, 255, 0.04) 0%, transparent 100%),
                    rgba(6, 7, 12, 0.92) !important;
        backdrop-filter: blur(36px) saturate(200%) !important;
        border: 1px solid rgba(168, 85, 247, 0.20) !important;
        border-top: 1px solid rgba(255, 255, 255, 0.45) !important;
        border-bottom: 1px solid rgba(126, 34, 206, 0.25) !important;
        box-shadow: 0 8px 24px -8px #000000,
                    0 0 10px -2px rgba(168, 85, 247, 0.15),
                    inset 0 1px 0 rgba(255, 255, 255, 0.20) !important;
        width: fit-content !important;
        max-width: 100% !important;
    }
    div[data-testid="stRadio"] [data-baseweb="radio"] {
        border-radius: 9999px !important;
        padding: 6px 16px !important;
        margin: 0 !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 12.5px !important;
        letter-spacing: -0.01em !important;
        border: 1px solid transparent !important;
        background: transparent !important;
        cursor: pointer !important;
        white-space: nowrap !important;
        transition: color 0.22s ease, background 0.3s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.3s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.22s ease !important;
    }
    div[data-testid="stRadio"] [data-baseweb="radio"]:hover {
        color: #ffffff !important;
        background: rgba(255, 255, 255, 0.06) !important;
    }
    div[data-testid="stRadio"] [data-baseweb="radio"]:has(input:checked) {
        color: #ffffff !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.90) 0%, rgba(126, 34, 206, 0.90) 100%) !important;
        background-size: 200% 200% !important;
        animation: whitePurpleFlow 4s ease infinite alternate !important;
        border: 1px solid rgba(192, 132, 252, 0.45) !important;
        border-top: 1.5px solid #ffffff !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5),
                    0 0 14px rgba(168, 85, 247, 0.40),
                    inset 0 1px 1px rgba(255, 255, 255, 0.50) !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.6) !important;
    }

    /* AMOLED Black Glass Cards for Plotly Charts & Containers */
    .glass-card {
        padding: 1.15rem 1.35rem;
        border-radius: 18px;
        background: radial-gradient(130% 70% at 0% 0%, rgba(255, 255, 255, 0.04), transparent 55%),
                    rgba(4, 5, 9, 0.92);
        border: 1px solid rgba(168, 85, 247, 0.22);
        border-top: 1px solid rgba(255, 255, 255, 0.75);
        border-left: 1px solid rgba(192, 132, 252, 0.40);
        backdrop-filter: blur(24px) saturate(160%);
        box-shadow: 0 14px 40px -10px #000000, 0 0 24px -6px rgba(168, 85, 247, 0.18);
        margin-bottom: 0.85rem;
    }

    /* Insight Banner with White Neon Edge & Refined Purple Glow */
    .insight-banner {
        background: rgba(8, 7, 14, 0.85) !important;
        border: 1px solid rgba(168, 85, 247, 0.20) !important;
        border-left: 3.5px solid #ffffff !important;
        border-radius: 12px !important;
        padding: 12px 18px !important;
        margin-bottom: 1.1rem !important;
        font-size: 0.93rem !important;
        line-height: 1.6 !important;
        color: #f1f5f9 !important;
        box-shadow: 0 4px 16px -4px #000000, 0 0 10px -2px rgba(168, 85, 247, 0.12) !important;
    }

    /* AMOLED Black Frosted Liquid Glass Sidebar with Clean Edge */
    [data-testid="stSidebar"] {
        background: radial-gradient(110% 55% at 0% 0%, rgba(168, 85, 247, 0.08) 0%, transparent 70%),
                    #000000 !important;
        -webkit-backdrop-filter: blur(36px) saturate(190%) !important;
        backdrop-filter: blur(36px) saturate(190%) !important;
        border-right: 1px solid rgba(168, 85, 247, 0.20) !important;
        box-shadow: 6px 0 24px -8px rgba(0, 0, 0, 0.9) !important;
    }
    [data-testid="stSidebarContent"] {
        padding: 1.25rem 1.15rem 2rem 1.15rem !important;
    }

    /* Sidebar Header & Status Card */
    .sidebar-header-card {
        padding: 0.95rem 1.1rem;
        border-radius: 16px;
        background: radial-gradient(120% 80% at 0% 0%, rgba(255, 255, 255, 0.04), transparent 60%),
                    rgba(6, 7, 12, 0.92);
        border: 1px solid rgba(168, 85, 247, 0.20);
        border-top: 1px solid rgba(255, 255, 255, 0.55);
        backdrop-filter: blur(24px);
        margin-bottom: 0.95rem;
        box-shadow: 0 6px 18px -4px #000000, 0 0 10px -2px rgba(168, 85, 247, 0.15);
    }
    .sidebar-header-title {
        font-size: 15px;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #ffffff;
        margin-bottom: 2px;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.8), 0 0 8px rgba(192, 132, 252, 0.30);
    }
    .sidebar-header-sub {
        font-size: 11px;
        color: #94a3b8;
        font-weight: 500;
        line-height: 1.35;
        margin-bottom: 0.65rem;
    }
    .sidebar-status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 3.5px 10px;
        border-radius: 9999px;
        font-size: 10.5px;
        font-weight: 600;
        background: rgba(168, 85, 247, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.40);
        color: #ffffff;
        box-shadow: 0 0 6px rgba(168, 85, 247, 0.20);
    }
    .sidebar-status-pill.active {
        background: rgba(147, 51, 234, 0.20);
        border-color: rgba(255, 255, 255, 0.70);
        color: #ffffff;
        box-shadow: 0 0 8px rgba(168, 85, 247, 0.30);
    }
    .sidebar-status-pill .status-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #ffffff;
        box-shadow: 0 0 6px #ffffff, 0 0 10px #a855f7;
    }
    .sidebar-status-pill.active .status-dot {
        background: #ffffff;
        box-shadow: 0 0 6px #ffffff, 0 0 12px #c084fc;
    }
    .sidebar-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(168, 85, 247, 0.25), transparent);
        margin: 1.1rem 0 0.85rem 0;
    }
    div[data-testid="stSidebar"] label {
        font-size: 11px !important;
        font-weight: 700 !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
        color: #94a3b8 !important;
        margin-bottom: 0.35rem !important;
    }

    /* MultiSelect AMOLED Glass Input Container */
    div[data-testid="stMultiSelect"] [data-testid="stMultiSelectTagsContainer"],
    div[data-testid="stMultiSelect"] [data-baseweb="select"] > div,
    div[data-baseweb="select"] > div {
        background: radial-gradient(120% 80% at 50% 0%, rgba(255, 255, 255, 0.03) 0%, transparent 100%),
                    rgba(6, 7, 12, 0.90) !important;
        border: 1px solid rgba(168, 85, 247, 0.20) !important;
        border-top: 1px solid rgba(255, 255, 255, 0.45) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(24px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
        box-shadow: 0 4px 16px -4px #000000,
                    inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
        min-height: 42px !important;
    }
    div[data-testid="stMultiSelect"] [data-baseweb="select"] > div:hover,
    div[data-baseweb="select"] > div:hover {
        border-color: rgba(192, 132, 252, 0.45) !important;
        border-top-color: #ffffff !important;
        box-shadow: 0 4px 14px -4px #000000, 0 0 10px rgba(168, 85, 247, 0.20) !important;
    }
    div[data-testid="stMultiSelect"] [data-baseweb="select"] > div:focus-within,
    div[data-baseweb="select"] > div:focus-within {
        border-color: #ffffff !important;
        box-shadow: 0 0 0 2px rgba(168, 85, 247, 0.25),
                    0 0 16px rgba(168, 85, 247, 0.35),
                    inset 0 1px 0 #ffffff !important;
    }

    /* MultiSelect Frosted White Neon & Purple Pill Tags */
    div[data-testid="stMultiSelect"] span[data-tag],
    div[data-testid="stMultiSelectTagsContainer"] span[data-tag],
    div[data-testid="stMultiSelect"] span[data-baseweb="tag"],
    div[data-testid="stMultiSelect"] div[data-baseweb="tag"],
    span[data-baseweb="tag"] {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.35) 0%, rgba(126, 34, 206, 0.25) 100%) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        border: 1px solid rgba(255, 255, 255, 0.40) !important;
        border-top: 1px solid #ffffff !important;
        border-bottom: 1px solid rgba(192, 132, 252, 0.45) !important;
        border-radius: 9999px !important;
        padding: 3px 10px !important;
        margin: 2px 3px 2px 0 !important;
        box-shadow: 0 0 6px rgba(168, 85, 247, 0.20),
                    inset 0 1px 1.5px rgba(255, 255, 255, 0.60) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 11.5px !important;
        letter-spacing: -0.01em !important;
        display: inline-flex !important;
        align-items: center !important;
        gap: 4px !important;
    }
    div[data-testid="stMultiSelect"] span[data-tag] svg,
    div[data-testid="stMultiSelect"] span[data-baseweb="tag"] svg,
    span[data-baseweb="tag"] svg {
        fill: #ffffff !important;
        opacity: 0.9 !important;
        transition: all 0.15s ease !important;
    }
    div[data-testid="stMultiSelect"] span[data-tag] svg:hover,
    div[data-testid="stMultiSelect"] span[data-baseweb="tag"] svg:hover,
    span[data-baseweb="tag"] svg:hover {
        fill: #c084fc !important;
        opacity: 1 !important;
        transform: scale(1.2) !important;
    }

    /* MultiSelect Dropdown Menu Popover */
    div[data-baseweb="popover"],
    ul[role="listbox"] {
        background: radial-gradient(120% 80% at 50% 0%, rgba(255, 255, 255, 0.04) 0%, transparent 100%),
                    rgba(6, 7, 12, 0.96) !important;
        backdrop-filter: blur(40px) saturate(220%) !important;
        -webkit-backdrop-filter: blur(40px) saturate(220%) !important;
        border: 1px solid rgba(168, 85, 247, 0.22) !important;
        border-top: 1px solid rgba(255, 255, 255, 0.60) !important;
        border-radius: 16px !important;
        box-shadow: 0 16px 45px -10px #000000,
                    0 0 16px rgba(168, 85, 247, 0.18),
                    inset 0 1px 0 rgba(255, 255, 255, 0.25) !important;
        padding: 6px !important;
    }
    li[role="option"] {
        border-radius: 10px !important;
        color: #cbd5e1 !important;
        font-size: 12.5px !important;
        font-weight: 500 !important;
        padding: 8px 12px !important;
        margin: 2px 0 !important;
        transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    li[role="option"]:hover,
    li[role="option"][aria-selected="true"] {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(168, 85, 247, 0.25) 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        box-shadow: 0 0 10px rgba(168, 85, 247, 0.20) !important;
        transform: translateX(2px) !important;
    }

    /* Reset All Filters Button */
    div[data-testid="stSidebar"] div.stButton > button {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.10) 0%, rgba(168, 85, 247, 0.18) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.45) !important;
        border-top: 1.5px solid #ffffff !important;
        border-radius: 9999px !important;
        color: #ffffff !important;
        font-size: 11.5px !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em !important;
        padding: 6px 14px !important;
        margin-bottom: 0.75rem !important;
        box-shadow: 0 0 10px rgba(168, 85, 247, 0.25),
                    inset 0 1px 1px #ffffff !important;
        backdrop-filter: blur(20px) !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    div[data-testid="stSidebar"] div.stButton > button:hover {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.20) 0%, rgba(168, 85, 247, 0.35) 100%) !important;
        border-color: #ffffff !important;
        color: #ffffff !important;
        box-shadow: 0 0 16px rgba(168, 85, 247, 0.40) !important;
        transform: translateY(-1px) !important;
    }

    /* General Action Buttons - AMOLED Black with White/Purple Specular Accents */
    div.stButton > button, div.stDownloadButton > button {
        background: rgba(6, 7, 12, 0.88) !important;
        border: 1px solid rgba(168, 85, 247, 0.20) !important;
        border-top: 1px solid rgba(255, 255, 255, 0.50) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        box-shadow: 0 4px 16px -4px #000000, 0 0 8px rgba(168, 85, 247, 0.12) !important;
        transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }
    div.stButton > button:hover, div.stDownloadButton > button:hover {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(168, 85, 247, 0.25)) !important;
        border-color: #ffffff !important;
        box-shadow: 0 0 16px rgba(168, 85, 247, 0.35) !important;
        transform: translateY(-1px) !important;
        color: #ffffff !important;
    }

    /* White Neon Slider Thumb with Refined Purple Glow */
    div[data-testid="stSlider"] div[role="slider"] {
        background: #ffffff !important;
        border: 2px solid #a855f7 !important;
        box-shadow: 0 0 6px #ffffff, 0 0 12px rgba(168, 85, 247, 0.45) !important;
    }
    div[data-testid="stSlider"] [data-baseweb="slider"] div[style*="background-color"] {
        background-color: #a855f7 !important;
        box-shadow: 0 0 6px rgba(168, 85, 247, 0.35) !important;
    }

    /* Expanders */
    div[data-testid="stExpander"] {
        background: radial-gradient(130% 70% at 0% 0%, rgba(255, 255, 255, 0.03) 0%, transparent 60%),
                    rgba(6, 7, 12, 0.88) !important;
        border: 1px solid rgba(168, 85, 247, 0.18) !important;
        border-top: 1px solid rgba(255, 255, 255, 0.50) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(24px) !important;
        margin-top: 1rem !important;
        box-shadow: 0 6px 20px -6px #000000, 0 0 10px -3px rgba(168, 85, 247, 0.12) !important;
    }

    /* AI Section Hero Card - AMOLED Black with Refined Laser Accents */
    .ai-hero-card {
        padding: 1.15rem 1.35rem;
        border-radius: 18px;
        background: radial-gradient(120% 80% at 0% 0%, rgba(255, 255, 255, 0.06) 0%, transparent 60%),
                    radial-gradient(120% 80% at 100% 100%, rgba(168, 85, 247, 0.10) 0%, transparent 60%),
                    rgba(6, 7, 12, 0.94);
        border: 1px solid rgba(168, 85, 247, 0.20);
        border-top: 1px solid rgba(255, 255, 255, 0.65);
        border-left: 3.5px solid #a855f7;
        backdrop-filter: blur(28px) saturate(180%);
        -webkit-backdrop-filter: blur(28px) saturate(180%);
        box-shadow: 0 10px 30px -8px #000000, 0 0 12px -3px rgba(168, 85, 247, 0.18);
        margin-bottom: 1.1rem;
    }
    .ai-hero-title {
        font-size: 20px;
        font-weight: 800;
        letter-spacing: -0.025em;
        color: #ffffff;
        margin: 0 0 4px 0;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.8), 0 0 8px rgba(192, 132, 252, 0.30);
    }
    .ai-hero-sub {
        font-size: 12.5px;
        color: #94a3b8;
        margin: 0;
        font-weight: 500;
        line-height: 1.45;
    }
    .ai-engine-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 10.5px;
        font-weight: 700;
        background: rgba(168, 85, 247, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.40);
        color: #ffffff;
        box-shadow: 0 0 6px rgba(168, 85, 247, 0.20);
        white-space: nowrap;
    }
    .ai-pulse-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #ffffff;
        box-shadow: 0 0 6px #ffffff, 0 0 10px #a855f7;
        animation: aiPulse 2s ease-in-out infinite;
    }
    @keyframes aiPulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.35; transform: scale(0.85); }
    }

    /* AI Chat Message Bubbles - AMOLED Black with Refined Glow */
    div[data-testid="stChatMessage"] {
        background: radial-gradient(130% 70% at 0% 0%, rgba(255, 255, 255, 0.03) 0%, transparent 60%),
                    rgba(6, 7, 12, 0.94) !important;
        border: 1px solid rgba(255, 255, 255, 0.10) !important;
        border-top: 1px solid rgba(255, 255, 255, 0.25) !important;
        border-radius: 16px !important;
        padding: 1rem 1.2rem !important;
        margin-bottom: 0.85rem !important;
        backdrop-filter: blur(24px) saturate(170%) !important;
        -webkit-backdrop-filter: blur(24px) saturate(170%) !important;
        box-shadow: 0 6px 20px -6px #000000 !important;
        color: #f8fafc !important;
        line-height: 1.6 !important;
    }
    /* Assistant Message Accent */
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
        border-left: 3px solid #a855f7 !important;
        border-color: rgba(168, 85, 247, 0.25) !important;
        box-shadow: 0 6px 20px -6px #000000, 0 0 12px -3px rgba(168, 85, 247, 0.20) !important;
        background: radial-gradient(100% 60% at 0% 0%, rgba(168, 85, 247, 0.06) 0%, transparent 50%),
                    rgba(6, 7, 12, 0.94) !important;
    }
    /* User Message Accent */
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        border-left: 3px solid #ffffff !important;
        border-color: rgba(255, 255, 255, 0.25) !important;
        box-shadow: 0 6px 20px -6px #000000, 0 0 10px -3px rgba(255, 255, 255, 0.15) !important;
        background: radial-gradient(100% 60% at 100% 0%, rgba(255, 255, 255, 0.05) 0%, transparent 50%),
                    rgba(6, 7, 12, 0.94) !important;
    }
    /* Sleek Translucent Avatars (No Cartoon Emoji) */
    div[data-testid="stChatMessageAvatarAssistant"] {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.35), rgba(126, 34, 206, 0.30)) !important;
        border: 1px solid rgba(255, 255, 255, 0.45) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        box-shadow: 0 0 10px rgba(168, 85, 247, 0.25) !important;
    }
    div[data-testid="stChatMessageAvatarAssistant"] svg,
    div[data-testid="stChatMessageAvatarAssistant"] span {
        filter: grayscale(1) brightness(2) !important;
    }
    div[data-testid="stChatMessageAvatarUser"] {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.20), rgba(192, 132, 252, 0.20)) !important;
        border: 1px solid rgba(255, 255, 255, 0.50) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.25) !important;
    }

    /* AMOLED Black Liquid Glass Chat Input Bar */
    div[data-testid="stChatInput"] {
        background: radial-gradient(120% 80% at 50% 0%, rgba(255, 255, 255, 0.04) 0%, transparent 100%),
                    rgba(6, 7, 12, 0.95) !important;
        border: 1px solid rgba(168, 85, 247, 0.20) !important;
        border-top: 1px solid rgba(255, 255, 255, 0.55) !important;
        border-radius: 18px !important;
        backdrop-filter: blur(36px) saturate(200%) !important;
        -webkit-backdrop-filter: blur(36px) saturate(200%) !important;
        box-shadow: 0 10px 30px -8px #000000,
                    0 0 12px rgba(168, 85, 247, 0.15),
                    inset 0 1px 0 rgba(255, 255, 255, 0.25) !important;
        padding: 4px 6px !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    div[data-testid="stChatInput"]:focus-within {
        border-color: #ffffff !important;
        box-shadow: 0 0 0 2px rgba(168, 85, 247, 0.30),
                    0 0 20px rgba(168, 85, 247, 0.35),
                    inset 0 1px 0 #ffffff !important;
    }
    div[data-testid="stChatInputTextArea"] {
        color: #ffffff !important;
        font-family: 'Manrope', system-ui, sans-serif !important;
        font-size: 13.5px !important;
    }
    div[data-testid="stChatInputSubmitButton"] button {
        background: linear-gradient(135deg, #ffffff, #a855f7) !important;
        border: 1px solid #ffffff !important;
        border-radius: 12px !important;
        box-shadow: 0 0 12px rgba(168, 85, 247, 0.45) !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stChatInputSubmitButton"] button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 0 18px rgba(168, 85, 247, 0.65), 0 0 8px #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# PLOTLY CHART THEME ENGINE (AMOLED BLACK & NEON GLOW ENGINE)
# -----------------------------------------------------------------------------
def polish_chart(fig, height=420):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Manrope, system-ui, sans-serif", color="#cbd5e1", size=11),
        xaxis=dict(
            gridcolor="rgba(168, 85, 247, 0.12)",
            zerolinecolor="rgba(255, 255, 255, 0.30)",
            tickfont=dict(color="#cbd5e1", size=10),
            title_font=dict(color="#ffffff", size=11, family="Manrope, sans-serif"),
        ),
        yaxis=dict(
            gridcolor="rgba(168, 85, 247, 0.12)",
            zerolinecolor="rgba(255, 255, 255, 0.30)",
            tickfont=dict(color="#cbd5e1", size=10),
            title_font=dict(color="#ffffff", size=11, family="Manrope, sans-serif"),
        ),
        height=height,
        margin=dict(l=25, r=20, t=35, b=25),
    )
    return fig


# -----------------------------------------------------------------------------
# CACHED DATA LOADER
# -----------------------------------------------------------------------------
@st.cache_data
def get_cleaned_data() -> pd.DataFrame:
    candidate_paths = [
        "data/player_injuries_impact.xlsx",
        "data/player_injuries_impact.csv",
        "player_injuries_impact.xlsx",
        "player_injuries_impact.csv",
    ]
    for path in candidate_paths:
        if Path(path).exists():
            return load_and_clean_data(path)
    raise FileNotFoundError(
        "Dataset not found. Place 'player_injuries_impact.xlsx' inside the 'data/' folder."
    )


df = get_cleaned_data()
GROQ_MODEL = "openai/gpt-oss-20b"

# -----------------------------------------------------------------------------
# SIDEBAR CONTROLS (LIQUID GLASS INTELLIGENCE DOCK - CLEAN & ACCESSIBLE)
# -----------------------------------------------------------------------------
# Check if any filter is active
active_filter_labels = []
if st.session_state.get("f_seasons"):
    active_filter_labels.append(f"{len(st.session_state['f_seasons'])} Seasons")
if st.session_state.get("f_clubs"):
    active_filter_labels.append(f"{len(st.session_state['f_clubs'])} Clubs")
if st.session_state.get("f_positions"):
    active_filter_labels.append(f"{len(st.session_state['f_positions'])} Positions")
if st.session_state.get("f_categories"):
    active_filter_labels.append(f"{len(st.session_state['f_categories'])} Categories")
if st.session_state.get("f_tiers"):
    active_filter_labels.append(f"{len(st.session_state['f_tiers'])} Tiers")

is_filtered = len(active_filter_labels) > 0
status_text = f"Filtered: {', '.join(active_filter_labels)}" if is_filtered else "Showing All 656 Spells (20 Clubs)"
status_class = "sidebar-status-pill active" if is_filtered else "sidebar-status-pill"

st.sidebar.markdown(
    f"""
    <div class="sidebar-header-card">
        <div class="sidebar-header-title">FootLens Controls</div>
        <div class="sidebar-header-sub">Premier League Performance Suite (2019/20–2023/24)</div>
        <div class="{status_class}">
            <span class="status-dot"></span>
            {status_text}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if is_filtered:
    if st.sidebar.button("Reset All Filters", use_container_width=True):
        for k in ["f_seasons", "f_clubs", "f_positions", "f_categories", "f_tiers"]:
            st.session_state[k] = []
        st.rerun()

all_seasons = sorted(df["Season"].dropna().unique())
selected_seasons = st.sidebar.multiselect(
    "Seasons",
    all_seasons,
    default=[],
    placeholder="All 5 Seasons (2019/20–2023/24)",
    key="f_seasons",
)

all_clubs = sorted(df["Club"].dropna().unique())
selected_clubs = st.sidebar.multiselect(
    "Clubs",
    all_clubs,
    default=[],
    placeholder="All 20 Premier League Clubs",
    key="f_clubs",
)

all_positions = sorted(df["Position"].dropna().unique())
selected_positions = st.sidebar.multiselect(
    "Positions",
    all_positions,
    default=[],
    placeholder="All 10 Positions",
    key="f_positions",
)

all_categories = sorted(df["Injury_Category"].dropna().unique())
selected_categories = st.sidebar.multiselect(
    "Biomechanical Category",
    all_categories,
    default=[],
    placeholder="All Injury Categories",
    key="f_categories",
)

all_tiers = ["Star Player (82+)", "First-Team Regular (77–81)", "Squad Depth (<77)"]
selected_tiers = st.sidebar.multiselect(
    "Squad Role Tier (FIFA)",
    all_tiers,
    default=[],
    placeholder="All Squad Role Tiers",
    key="f_tiers",
)

st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
st.sidebar.markdown(
    '<div style="font-size: 11px; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase; color: #9ba3ae; margin-bottom: 0.45rem;">Statistical Thresholds</div>',
    unsafe_allow_html=True,
)
min_injury_cases = st.sidebar.slider("Min. Cases for Injury Ranking", 1, 15, 5, key="f_min_cases")
min_comeback_spells = st.sidebar.slider("Min. Spells for Leaderboard", 1, 5, 2, key="f_min_spells")

# Intelligent multi-filter logic: if empty, includes ALL records!
active_seasons = selected_seasons if selected_seasons else all_seasons
active_clubs = selected_clubs if selected_clubs else all_clubs
active_positions = selected_positions if selected_positions else all_positions
active_categories = selected_categories if selected_categories else all_categories
active_tiers = selected_tiers if selected_tiers else all_tiers

filtered_df = df[
    df["Season"].isin(active_seasons)
    & df["Club"].isin(active_clubs)
    & df["Position"].isin(active_positions)
    & df["Injury_Category"].isin(active_categories)
    & df["Squad_Tier"].astype(str).isin(active_tiers)
].copy()

if filtered_df.empty:
    st.warning("No records match your filter combination. Click below or clear filters in the sidebar.")
    if st.button("Reset All Filters to Default"):
        for k in ["f_seasons", "f_clubs", "f_positions", "f_categories", "f_tiers"]:
            if k in st.session_state:
                st.session_state[k] = []
        st.rerun()
    st.stop()

# -----------------------------------------------------------------------------
# BRAND HEADER (CLEAN PRO TYPOGRAPHY - NO TAGS, NO EMOJIS)
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="brand-bar">
        <h1 class="brand-title">FootLens <span class="gradient-accent">Pro Intelligence</span></h1>
        <p class="brand-sub">
            Sports science telemetry & squad impact analytics for Technical Directors, Heads of Performance & Analysts
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

total_spells = len(filtered_df)
unique_players = filtered_df["Player_Name"].nunique()
median_days = filtered_df["Days_Out"].median()
mean_gd_drop = filtered_df["Team_Perf_Drop_Index"].mean()
ppg_before = filtered_df["PPG_Before"].mean()
ppg_missed = filtered_df["PPG_Missed"].mean()
relapse_rate = filtered_df["Is_Relapse_60d"].mean() * 100
mean_rating_delta = filtered_df["Rating_Delta"].mean()

# 6 AMOLED Black Glass KPI Cards with Laser Neon Accents & Detailing
st.markdown(
    f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-accent-bar"></div>
            <div class="kpi-label">Total Injury Spells</div>
            <div class="kpi-val">{total_spells:,}</div>
            <div class="kpi-badge white">{unique_players} unique players</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-accent-bar"></div>
            <div class="kpi-label">Median Absence</div>
            <div class="kpi-val">{median_days:.0f} <span style="font-size: 14px; color: #cbd5e1; font-weight: 500;">days</span></div>
            <div class="kpi-badge purple">Mean: {filtered_df['Days_Out'].mean():.1f} d</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-accent-bar"></div>
            <div class="kpi-label">Team GD Drop Index</div>
            <div class="kpi-val">{mean_gd_drop:+.2f}</div>
            <div class="kpi-badge violet">Goals/match lost</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-accent-bar"></div>
            <div class="kpi-label">Points Per Game (Out)</div>
            <div class="kpi-val">{ppg_missed:.2f} <span style="font-size: 14px; color: #cbd5e1; font-weight: 500;">PPG</span></div>
            <div class="kpi-badge purple">{ppg_missed - ppg_before:+.2f} vs pre-injury</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-accent-bar"></div>
            <div class="kpi-label">60-Day Relapse Rate</div>
            <div class="kpi-val">{relapse_rate:.1f}%</div>
            <div class="kpi-badge violet">{int(filtered_df['Is_Relapse_60d'].sum())} repeat spells</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-accent-bar"></div>
            <div class="kpi-label">Post-Return Form</div>
            <div class="kpi-val">{mean_rating_delta:+.2f}</div>
            <div class="kpi-badge white">{filtered_df['Avg_Rating_Before'].mean():.2f} → {filtered_df['Avg_Rating_After'].mean():.2f}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 5-TAB ANALYTICAL WORKSPACE (APPLE VISIONOS LIQUID PILL DOCK - NO EMOJIS)
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Club & Tactical Impact",
        "Sports Science & Relapse Lab",
        "Congestion & Positional Matrix",
        "Player Scouting & Comeback Lab",
        "AI Data Analyst Chat",
    ]
)

# =============================================================================
# TAB 1: CLUB & TACTICAL IMPACT
# =============================================================================
with tab1:
    st.markdown(
        '<div class="insight-banner"><b>Tactical Takeaway:</b> Structural injuries (Knee Surgery, Muscle Tears) '
        "inflict the heaviest Goal Difference collapse (+1.42 GD drop), while thinner squads like <b>Brentford</b> and <b>Burnley</b> "
        "suffer steep table point losses even when opposition difficulty remains constant.</div>",
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("1. Top 10 Injuries by Team Performance Drop")
        
        # Apple visionOS Liquid Pill Dock (The "Second Tab Bar", Zero check circles, fully responsive in all orientations)
        if hasattr(st, "pills"):
            metric_choice = st.pills(
                "Select Impact Metric",
                options=["Team GD Drop Index", "Points Per Game Lost", "Win Rate Drop"],
                default="Team GD Drop Index",
            )
        elif hasattr(st, "segmented_control"):
            metric_choice = st.segmented_control(
                "Select Impact Metric",
                options=["Team GD Drop Index", "Points Per Game Lost", "Win Rate Drop"],
                default="Team GD Drop Index",
            )
        else:
            metric_choice = st.radio(
                "Select Impact Metric",
                options=["Team GD Drop Index", "Points Per Game Lost", "Win Rate Drop"],
                horizontal=True,
            )
        if not metric_choice:
            metric_choice = "Team GD Drop Index"

        inj_impact = (
            filtered_df.groupby("Injury_Type", as_index=False)
            .agg(
                Cases=("Player_Name", "count"),
                Avg_Days_Out=("Days_Out", "mean"),
                Avg_GD_Drop=("Team_Perf_Drop_Index", "mean"),
                Avg_PPG_Drop=("PPG_Drop", "mean"),
                Avg_Win_Drop=("Win_Rate_Drop", "mean"),
                Relapse_Pct=("Is_Relapse_60d", lambda s: s.mean() * 100),
            )
            .query("Cases >= @min_injury_cases")
        )

        if "GD Drop" in metric_choice:
            sort_col, x_lab, fmt = "Avg_GD_Drop", "Team GD Drop Index", "{:+.2f}"
        elif "PPG" in metric_choice or "Points" in metric_choice:
            sort_col, x_lab, fmt = "Avg_PPG_Drop", "Points Per Game Lost (PPG)", "{:+.2f}"
        else:
            sort_col, x_lab, fmt = "Avg_Win_Drop", "Win Rate Drop (%)", "{:+.1f}%"

        top10_inj = inj_impact.sort_values(sort_col, ascending=False).head(10)

        # White Neon to Purple Glow gradient bar styling
        fig_bar = px.bar(
            top10_inj,
            x=sort_col,
            y="Injury_Type",
            orientation="h",
            color=sort_col,
            color_continuous_scale=[[0, "#4c1d95"], [0.35, "#7e22ce"], [0.70, "#c084fc"], [1.0, "#ffffff"]],
            text=top10_inj[sort_col].map(lambda v: fmt.format(v)),
            hover_data={
                "Cases": True,
                "Avg_Days_Out": ":.1f",
                "Avg_GD_Drop": ":+.2f",
                "Avg_PPG_Drop": ":+.2f",
                "Relapse_Pct": ":.1f",
            },
            labels={sort_col: x_lab, "Injury_Type": "Injury", "Avg_Days_Out": "Avg Days Out"},
        )
        fig_bar.update_traces(textposition="outside", cliponaxis=False)
        fig_bar.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
        polish_chart(fig_bar, height=430)
        st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        st.subheader("2. Club Resilience: Points Per Game (Before vs. Absent)")
        st.caption("Compares club PPG in the 3 games prior to injury vs. the 3 games missed.")

        club_ppg = (
            filtered_df.groupby("Club", as_index=False)
            .agg(
                Spells=("Player_Name", "count"),
                PPG_Before=("PPG_Before", "mean"),
                PPG_Missed=("PPG_Missed", "mean"),
                PPG_After=("PPG_After", "mean"),
                GD_Drop=("Team_Perf_Drop_Index", "mean"),
                Big6_Shift=("Fixture_Difficulty_Shift", "mean"),
            )
            .sort_values("PPG_Before", ascending=True)
        )

        fig_club = go.Figure()
        fig_club.add_trace(
            go.Bar(
                y=club_ppg["Club"],
                x=club_ppg["PPG_Before"],
                name="Pre-Injury PPG",
                orientation="h",
                marker_color="#ffffff",
                text=club_ppg["PPG_Before"].map(lambda v: f"{v:.2f}"),
                textposition="auto",
            )
        )
        fig_club.add_trace(
            go.Bar(
                y=club_ppg["Club"],
                x=club_ppg["PPG_Missed"],
                name="During Absence PPG",
                orientation="h",
                marker_color="#a855f7",
                text=club_ppg["PPG_Missed"].map(lambda v: f"{v:.2f}"),
                textposition="auto",
            )
        )
        fig_club.update_layout(
            barmode="group",
            xaxis_title="Points Per Game (Max = 3.00)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
        )
        polish_chart(fig_club, height=500)
        st.plotly_chart(fig_club, use_container_width=True)

    st.subheader("3. Opposition-Adjusted Squad Dependency Matrix")
    st.caption(
        "Separates true squad dependency from tough fixture runs: 'Big-6 Fixture Shift (%)' shows whether a club "
        "faced more Top-6 opponents while players were out."
    )
    club_table = (
        filtered_df.groupby("Club", as_index=False)
        .agg(
            Total_Spells=("Player_Name", "count"),
            Avg_Days_Out=("Days_Out", "mean"),
            PPG_Before=("PPG_Before", "mean"),
            PPG_Missed=("PPG_Missed", "mean"),
            PPG_Shift=("PPG_Drop", lambda s: -s.mean()),
            Team_GD_Drop=("Team_Perf_Drop_Index", "mean"),
            Big6_Shift_Pct=("Fixture_Difficulty_Shift", "mean"),
            Relapse_60d_Pct=("Is_Relapse_60d", lambda s: s.mean() * 100),
        )
        .sort_values("Team_GD_Drop", ascending=False)
    )
    st.dataframe(
        club_table.style.format(
            {
                "Avg_Days_Out": "{:.1f}",
                "PPG_Before": "{:.2f}",
                "PPG_Missed": "{:.2f}",
                "PPG_Shift": "{:+.2f}",
                "Team_GD_Drop": "{:+.2f}",
                "Big6_Shift_Pct": "{:+.1f}%",
                "Relapse_60d_Pct": "{:.1f}%",
            }
        ).background_gradient(subset=["Team_GD_Drop"], cmap="Purples"),
        use_container_width=True,
    )

# =============================================================================
# TAB 2: SPORTS SCIENCE & RELAPSE LAB
# =============================================================================
with tab2:
    st.markdown(
        '<div class="insight-banner"><b>Sports Science Insight:</b> Soft-tissue / muscular injuries carry the highest '
        "60-day relapse rate (28.0%). Players eased back via <b>Gradual Sub Reintegration (S)</b> show a <b>26.5% relative risk reduction</b> "
        "in secondary injury vs. immediate starting XI deployment.</div>",
        unsafe_allow_html=True,
    )

    s1, s2 = st.columns(2)

    with s1:
        st.subheader("4. Return-to-Play Protocol: Sub Reintegration vs. Full Start")
        st.caption("Measures 60-day re-injury risk following Match +1 starting vs. substitute reintegration.")

        proto_df = (
            filtered_df[filtered_df["Return_Protocol"] != "No Post-Return Data"]
            .groupby("Return_Protocol", as_index=False)
            .agg(
                Cases=("Player_Name", "count"),
                Next_Relapse_Rate=("Next_Spell_Relapse_60d", lambda s: s.mean() * 100),
                Avg_Rating_After=("Avg_Rating_After", "mean"),
                Avg_Rating_Delta=("Rating_Delta", "mean"),
            )
        )

        fig_proto = px.bar(
            proto_df,
            x="Return_Protocol",
            y="Next_Relapse_Rate",
            color="Return_Protocol",
            color_discrete_map={
                "Gradual Sub Reintegration (S)": "#ffffff",
                "Immediate Full Start": "#a855f7",
            },
            text=proto_df["Next_Relapse_Rate"].map(lambda v: f"{v:.1f}%"),
            hover_data={"Cases": True, "Avg_Rating_After": ":.2f", "Avg_Rating_Delta": ":+.2f"},
            labels={
                "Return_Protocol": "First Match Back Protocol",
                "Next_Relapse_Rate": "Subsequent 60-Day Relapse Rate (%)",
            },
        )
        fig_proto.update_traces(textposition="outside")
        fig_proto.update_layout(showlegend=False, yaxis_range=[0, 38])
        polish_chart(fig_proto, height=410)
        st.plotly_chart(fig_proto, use_container_width=True)

    with s2:
        st.subheader("5. Biomechanical Injury Burden & Relapse Risk")
        st.caption("Compares average recovery days and 60-day relapse rate across medical injury classes.")

        bio_df = (
            filtered_df.groupby("Injury_Category", as_index=False)
            .agg(
                Total_Cases=("Player_Name", "count"),
                Avg_Days_Out=("Days_Out", "mean"),
                Relapse_Rate_60d=("Is_Relapse_60d", lambda s: s.mean() * 100),
                Team_GD_Drop=("Team_Perf_Drop_Index", "mean"),
            )
            .sort_values("Total_Cases", ascending=False)
        )

        fig_bio = px.scatter(
            bio_df,
            x="Avg_Days_Out",
            y="Relapse_Rate_60d",
            size="Total_Cases",
            color="Injury_Category",
            color_discrete_sequence=["#ffffff", "#c084fc", "#a855f7", "#e9d5ff", "#7e22ce"],
            text="Injury_Category",
            size_max=45,
            labels={
                "Avg_Days_Out": "Mean Recovery Duration (Days)",
                "Relapse_Rate_60d": "60-Day Relapse Rate (%)",
            },
        )
        fig_bio.update_traces(textposition="top center")
        fig_bio.update_layout(showlegend=False)
        polish_chart(fig_bio, height=410)
        st.plotly_chart(fig_bio, use_container_width=True)

    s3, s4 = st.columns([1.15, 0.85])

    with s3:
        st.subheader("6. Player Age vs. Team Performance Drop Index")
        st.caption("Bubble size = Days Out. Highlights veteran leadership loss vs. youth recovery variance.")
        scatter_df = filtered_df.dropna(subset=["Age", "Team_Perf_Drop_Index", "Days_Out"]).copy()
        fig_scatter = px.scatter(
            scatter_df,
            x="Age",
            y="Team_Perf_Drop_Index",
            color="Injury_Category",
            color_discrete_sequence=["#ffffff", "#c084fc", "#a855f7", "#e9d5ff", "#7e22ce"],
            size="Days_Out",
            size_max=26,
            opacity=0.85,
            hover_name="Player_Name",
            hover_data={
                "Club": True,
                "Injury_Type": True,
                "FIFA_Rating": True,
                "Days_Out": ":.0f",
                "Team_Perf_Drop_Index": ":+.2f",
            },
            labels={
                "Age": "Player Age (Years)",
                "Team_Perf_Drop_Index": "Team GD Drop Index",
            },
        )
        fig_scatter.add_hline(y=0, line_dash="dot", line_color="rgba(168, 85, 247, 0.45)")
        polish_chart(fig_scatter, height=420)
        st.plotly_chart(fig_scatter, use_container_width=True)

    with s4:
        st.subheader("7. High-Risk 60-Day Relapse Watchlist")
        st.caption("Players injured again within 60 days of medical clearance.")
        relapses = (
            filtered_df[filtered_df["Is_Relapse_60d"]]
            .sort_values("Days_Since_Last_Return")[
                [
                    "Player_Name",
                    "Club",
                    "Days_Since_Last_Return",
                    "Prev_Injury_Type",
                    "Injury_Type",
                    "Season",
                ]
            ]
            .rename(
                columns={
                    "Days_Since_Last_Return": "Days_Clear",
                    "Prev_Injury_Type": "Prior_Injury",
                    "Injury_Type": "Relapse_Injury",
                }
            )
        )
        st.dataframe(relapses, use_container_width=True, height=385, hide_index=True)

# =============================================================================
# TAB 3: CONGESTION & POSITIONAL MATRIX
# =============================================================================
with tab3:
    m1, m2 = st.columns([1.2, 0.8])

    with m1:
        st.subheader("8. Fixture Congestion Heatmap (Months vs. Clubs)")
        st.caption("Pinpoints winter fixture congestion clusters (Dec–Feb) and early-season soft-tissue spikes.")
        month_order = list(calendar.month_name)[1:]
        heatmap_pivot = (
            filtered_df.pivot_table(
                index="Club",
                columns="Injury_Month",
                values="Player_Name",
                aggfunc="count",
                fill_value=0,
            )
            .reindex(columns=month_order, fill_value=0)
        )
        # AMOLED black to deep purple to white neon glow heatmap
        fig_heat = px.imshow(
            heatmap_pivot,
            text_auto=True,
            aspect="auto",
            color_continuous_scale=[[0, "#000000"], [0.30, "#2e1065"], [0.65, "#7e22ce"], [0.85, "#c084fc"], [1.0, "#ffffff"]],
            labels={"x": "Calendar Month", "y": "Club", "color": "Injuries"},
        )
        polish_chart(fig_heat, height=440)
        st.plotly_chart(fig_heat, use_container_width=True)

    with m2:
        st.subheader("9. Positional Depth Vulnerability")
        st.caption("Which positions hurt team Goal Difference most when injured?")
        pos_df = (
            filtered_df.groupby("Position", as_index=False)
            .agg(
                Cases=("Player_Name", "count"),
                Median_Days=("Days_Out", "median"),
                Team_GD_Drop=("Team_Perf_Drop_Index", "mean"),
            )
            .sort_values("Team_GD_Drop", ascending=True)
        )
        fig_pos = px.bar(
            pos_df,
            x="Team_GD_Drop",
            y="Position",
            orientation="h",
            color="Team_GD_Drop",
            color_continuous_scale=[[0, "#4c1d95"], [0.5, "#a855f7"], [1.0, "#ffffff"]],
            text=pos_df["Team_GD_Drop"].map(lambda v: f"{v:+.2f}"),
            labels={"Team_GD_Drop": "Team GD Drop Index", "Median_Days": "Median Days"},
        )
        fig_pos.update_traces(textposition="outside", cliponaxis=False)
        fig_pos.update_layout(coloraxis_showscale=False)
        polish_chart(fig_pos, height=440)
        st.plotly_chart(fig_pos, use_container_width=True)

    st.subheader("10. Multi-Season Injury Volume vs. Severity Trend (2019/20 – 2023/24)")
    season_df = (
        filtered_df.groupby("Season", as_index=False)
        .agg(
            Injury_Count=("Player_Name", "count"),
            Mean_Days_Out=("Days_Out", "mean"),
            Mean_GD_Drop=("Team_Perf_Drop_Index", "mean"),
        )
        .sort_values("Season")
    )
    fig_season = make_subplots(specs=[[{"secondary_y": True}]])
    fig_season.add_trace(
        go.Bar(
            x=season_df["Season"],
            y=season_df["Injury_Count"],
            name="Total Injury Spells",
            marker_color="#a855f7",
            opacity=0.85,
        ),
        secondary_y=False,
    )
    fig_season.add_trace(
        go.Scatter(
            x=season_df["Season"],
            y=season_df["Mean_Days_Out"],
            name="Mean Recovery Duration (Days)",
            mode="lines+markers+text",
            text=season_df["Mean_Days_Out"].map(lambda v: f"{v:.1f}d"),
            textposition="top center",
            line=dict(color="#ffffff", width=3.5),
            marker=dict(size=9, color="#ffffff", line=dict(color="#c084fc", width=2)),
        ),
        secondary_y=True,
    )
    fig_season.update_yaxes(title_text="Total Injury Spells", secondary_y=False)
    fig_season.update_yaxes(title_text="Mean Days Out", secondary_y=True)
    fig_season.update_layout(legend=dict(orientation="h", y=1.12))
    polish_chart(fig_season, height=380)
    st.plotly_chart(fig_season, use_container_width=True)

# =============================================================================
# TAB 4: PLAYER SCOUTING & COMEBACK LAB
# =============================================================================
with tab4:
    st.subheader("11. Individual Player Rating Trajectory & Full 9-Match Team GD Arc")
    player_options = sorted(filtered_df["Player_Name"].dropna().unique())
    default_idx = player_options.index("Richarlison") if "Richarlison" in player_options else 0
    selected_player = st.selectbox("Select Player Profile", options=player_options, index=default_idx)

    p_df = filtered_df[filtered_df["Player_Name"] == selected_player]
    p_meta = p_df.iloc[0]

    pm1, pm2, pm3, pm4 = st.columns(4)
    pm1.metric("Club & Position", f"{p_meta['Club']}", f"{p_meta['Position']}")
    pm2.metric("Age & FIFA Rating", f"{int(p_meta['Age'])} yrs", f"FIFA {int(p_meta['FIFA_Rating'])}")
    pm3.metric("Recorded Spells", f"{len(p_df)}", f"{p_df['Days_Out'].sum():.0f} total days out")
    pm4.metric(
        "Player Rating Delta",
        f"{p_df['Rating_Delta'].mean():+.2f}",
        f"Team GD Drop: {p_df['Team_Perf_Drop_Index'].mean():+.2f}",
    )

    p_col1, p_col2 = st.columns(2)

    with p_col1:
        rating_stages = [
            ("Match -3", "Match3_before_injury_Player_rating_num"),
            ("Match -2", "Match2_before_injury_Player_rating_num"),
            ("Match -1", "Match1_before_injury_Player_rating_num"),
            ("Match +1", "Match1_after_injury_Player_rating_num"),
            ("Match +2", "Match2_after_injury_Player_rating_num"),
            ("Match +3", "Match3_after_injury_Player_rating_num"),
        ]
        r_labels = [s[0] for s in rating_stages]
        p_r_vals = [p_df[s[1]].mean() for s in rating_stages]
        sq_r_vals = [filtered_df[s[1]].mean() for s in rating_stages]

        fig_p_line = go.Figure()
        fig_p_line.add_trace(
            go.Scatter(
                x=r_labels,
                y=p_r_vals,
                mode="lines+markers+text",
                name=f"{selected_player}",
                line=dict(width=3.5, color="#ffffff"),
                marker=dict(size=9, color="#ffffff", line=dict(color="#c084fc", width=2)),
                text=[f"{v:.2f}" if pd.notna(v) else "" for v in p_r_vals],
                textposition="top center",
            )
        )
        fig_p_line.add_trace(
            go.Scatter(
                x=r_labels,
                y=sq_r_vals,
                mode="lines+markers",
                name="Squad Benchmark",
                line=dict(width=2, dash="dot", color="#c084fc"),
            )
        )
        fig_p_line.add_vline(x=2.5, line_dash="dash", line_color="#a855f7", annotation_text="Injury")
        fig_p_line.update_layout(
            title="Match Rating Trajectory (Before vs. After)",
            yaxis=dict(title="Match Rating", range=[4.5, 9.0]),
            legend=dict(orientation="h", y=1.12),
        )
        polish_chart(fig_p_line, height=390)
        st.plotly_chart(fig_p_line, use_container_width=True)

    with p_col2:
        gd_stages = [
            ("M-3", "Match3_before_injury_GD_num"),
            ("M-2", "Match2_before_injury_GD_num"),
            ("M-1", "Match1_before_injury_GD_num"),
            ("Out 1", "Match1_missed_match_GD_num"),
            ("Out 2", "Match2_missed_match_GD_num"),
            ("Out 3", "Match3_missed_match_GD_num"),
            ("M+1", "Match1_after_injury_GD_num"),
            ("M+2", "Match2_after_injury_GD_num"),
            ("M+3", "Match3_after_injury_GD_num"),
        ]
        gd_labels = [g[0] for g in gd_stages]
        gd_vals = [p_df[g[1]].mean() for g in gd_stages]
        bar_colors = ["#ffffff"] * 3 + ["#a855f7"] * 3 + ["#c084fc"] * 3

        fig_gd_arc = go.Figure(
            go.Bar(
                x=gd_labels,
                y=gd_vals,
                marker_color=bar_colors,
                text=[f"{v:+.1f}" if pd.notna(v) else "" for v in gd_vals],
                textposition="outside",
            )
        )
        fig_gd_arc.add_hline(y=0, line_color="rgba(168, 85, 247, 0.40)")
        fig_gd_arc.update_layout(
            title=f"{p_meta['Club']} Goal Difference Arc (Pre → Absent → Return)",
            yaxis_title="Avg Team Goal Difference",
        )
        polish_chart(fig_gd_arc, height=390)
        st.plotly_chart(fig_gd_arc, use_container_width=True)

    st.subheader("12. Comeback Players Leaderboard (Ranked by Rating Improvement)")
    leaderboard = (
        filtered_df.groupby(["Player_Name", "Club", "Position", "FIFA_Rating"], as_index=False)
        .agg(
            Injury_Spells=("Injury_Type", "count"),
            Total_Days_Out=("Days_Out", "sum"),
            Avg_Rating_Before=("Avg_Rating_Before", "mean"),
            Avg_Rating_After=("Avg_Rating_After", "mean"),
            Rating_Improvement=("Rating_Delta", "mean"),
            Sub_Reintegrations=("Post_Injury_Sub_Apps", "sum"),
            Team_GD_Drop_When_Out=("Team_Perf_Drop_Index", "mean"),
            Team_PPG_Drop_When_Out=("PPG_Drop", "mean"),
        )
        .query("Injury_Spells >= @min_comeback_spells")
        .dropna(subset=["Rating_Improvement"])
        .sort_values("Rating_Improvement", ascending=False)
        .reset_index(drop=True)
    )
    leaderboard.index = leaderboard.index + 1

    st.dataframe(
        leaderboard.style.format(
            {
                "Total_Days_Out": "{:.0f}",
                "Avg_Rating_Before": "{:.2f}",
                "Avg_Rating_After": "{:.2f}",
                "Rating_Improvement": "{:+.2f}",
                "Team_GD_Drop_When_Out": "{:+.2f}",
                "Team_PPG_Drop_When_Out": "{:+.2f}",
            }
        ).background_gradient(subset=["Rating_Improvement"], cmap="Purples"),
        use_container_width=True,
        height=390,
    )

    st.download_button(
        label="Download Full Comeback & Impact Leaderboard (CSV)",
        data=leaderboard.to_csv(index_label="Rank").encode("utf-8"),
        file_name="footlens_pro_comeback_leaderboard.csv",
        mime="text/csv",
    )

# =============================================================================
# TAB 5: GROQ AI DATA ANALYST CHAT (CLEAN, NO EMOJIS)
# =============================================================================
with tab5:
    st.markdown(
        """
        <div class="ai-hero-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
                <div>
                    <h2 class="ai-hero-title">FootLens AI Performance Analyst</h2>
                    <p class="ai-hero-sub">Sports science & tactical reasoning engine grounded in 656 Premier League match telemetry records.</p>
                </div>
                <div class="ai-engine-badge">
                    <span class="ai-pulse-dot"></span>
                    <span>Neural Analyst Active · Live Telemetry Context</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div style="font-size: 11px; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase; color: #9ba3ae; margin: 0.6rem 0 0.5rem 0;">Suggested Analytical Inquiries</div>',
        unsafe_allow_html=True,
    )

    q_cols = st.columns(4)
    preset_prompt = None
    if q_cols[0].button("Most Damaging Injuries", use_container_width=True, help="Analyze which injuries cause the greatest Goal Difference drop"):
        preset_prompt = "Which injuries cause the biggest team performance drop and why?"
    if q_cols[1].button("Brentford vs Man United", use_container_width=True, help="Compare club resilience between high and low depth squads"):
        preset_prompt = "Compare Brentford and Man United in terms of injury volume vs actual team PPG and GD drop."
    if q_cols[2].button("Richarlison vs Pogba", use_container_width=True, help="Compare comeback trajectories and rating recovery"):
        preset_prompt = "Compare Richarlison and Paul Pogba's injury history and post-recovery rating changes."
    if q_cols[3].button("Relapse Prevention Guide", use_container_width=True, help="Evidence-based return protocols for medical teams"):
        preset_prompt = "Based on the dataset, what practical changes should sports scientists make to reduce 60-day relapses?"

    initial_welcome = (
        "**FootLens AI Performance Engine is online.**\n\n"
        "I am grounded in your verified Premier League dataset (**656 injury spells across 224 players and 20 clubs**). "
        "Ask me to analyze squad dependencies, compare player comeback trajectories, evaluate fixture congestion impacts, "
        "or recommend sports science return-to-play protocols.\n\n"
        "*Select an inquiry chip above or enter any tactical, player, or injury question below.*"
    )

    if "footlens_chat" not in st.session_state:
        st.session_state.footlens_chat = [
            {
                "role": "assistant",
                "content": initial_welcome,
            }
        ]

    # Dedicated message stream container (Always placed ABOVE the chat input box)
    chat_box = st.container()

    with chat_box:
        for msg in st.session_state.footlens_chat:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Chat input bar (Strictly positioned BELOW all messages)
    user_query = st.chat_input("Ask about any player, club, injury, or recovery trend...")
    active_prompt = preset_prompt or user_query

    if active_prompt:
        st.session_state.footlens_chat.append({"role": "user", "content": active_prompt})
        
        # Render the new exchange INSIDE chat_box so it appears ABOVE the input bar
        with chat_box:
            with st.chat_message("user"):
                st.markdown(active_prompt)

            with st.chat_message("assistant"):
                with st.spinner("Synthesizing telemetry data & generating sports science insights..."):
                    reply = ask_groq_analyst(
                        st.session_state.footlens_chat[1:],
                        filtered_df,
                        model=GROQ_MODEL,
                    )
                st.markdown(reply)

        st.session_state.footlens_chat.append({"role": "assistant", "content": reply})
        st.rerun()

    if len(st.session_state.footlens_chat) > 1:
        c_left, c_right = st.columns([6, 1])
        with c_right:
            if st.button("Clear Chat", use_container_width=True):
                st.session_state.footlens_chat = [
                    {
                        "role": "assistant",
                        "content": initial_welcome,
                    }
                ]
                st.rerun()

# -----------------------------------------------------------------------------
# EXECUTIVE RESEARCH QUESTIONS & SPORTS SCIENCE RECOMMENDATIONS (NO EMOJIS)
# -----------------------------------------------------------------------------
with st.expander("Research Findings & Sports Science Protocols"):
    st.markdown(
        """
        ### Research Findings
        1. **Which injuries cause the steepest team collapse?**  
           **Knee Surgery** (+1.42 GD drop, 138.9 days out) and **Fitness setbacks** (+1.29 GD drop) inflict the sharpest Goal Difference losses, while **Soft-Tissue / Muscular injuries** account for 41% of all spells and carry the highest 60-day relapse rate (**28.0%**).
        2. **How do club Points Per Game (PPG) and Win Rates shift during player absence?**  
           League-wide win rate drops from **40.7% → 38.8%**, with thinner squads suffering severe table-point losses (**Brentford**: 33.3% → 22.1% win rate, +0.62 GD drop; **Burnley**: 31.9% → 24.3%, +0.53 GD drop).
        3. **Does gradual substitute reintegration reduce re-injury risk?**  
           Yes—players eased back via substitute appearances `(S)` on Match +1 recorded a **20.0% 60-day relapse rate**, compared to **27.2%** for players thrown immediately into the starting XI (**26.5% relative risk reduction**).
        4. **When do injury clusters peak?**  
           Injury volume spikes during winter fixture congestion (**December–February**) and early-season intensity (**August–October**).
        5. **How does player age impact recovery and team results?**  
           Age has near-zero linear correlation with days out ($r = -0.006$), but **veteran players (32+)** trigger the steepest team GD drop (**+0.25** vs. **-0.01** for U23s) due to tactical leadership loss.
        """
    )
