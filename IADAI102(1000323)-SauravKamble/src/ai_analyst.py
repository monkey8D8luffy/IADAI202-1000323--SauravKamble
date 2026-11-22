import os
from dotenv import load_dotenv
from groq import Groq
import pandas as pd
import streamlit as st

load_dotenv()


def _get_groq_api_key() -> str:
    """Reads GROQ_API_KEY from .env / environment locally, or st.secrets on Streamlit Cloud."""
    env_key = os.getenv("GROQ_API_KEY", "").strip()
    if env_key:
        return env_key
    try:
        return str(st.secrets.get("GROQ_API_KEY", "")).strip()
    except Exception:
        return ""


def build_data_context(df: pd.DataFrame, question: str) -> str:
    """Creates a compact, exact statistical digest + any player/club rows mentioned in the prompt."""
    top_injuries = (
        df.groupby("Injury_Type")
        .agg(cases=("Player_Name", "count"), days=("Days_Out", "mean"), gd_drop=("Team_Perf_Drop_Index", "mean"))
        .query("cases >= 3")
        .sort_values("gd_drop", ascending=False)
        .head(8)
    )
    inj_lines = "\n".join(
        f"  - {idx}: {int(r.cases)} cases, {r.days:.1f} avg days out, {r.gd_drop:+.2f} GD drop"
        for idx, r in top_injuries.iterrows()
    )

    club_stats = (
        df.groupby("Club")
        .agg(
            spells=("Player_Name", "count"),
            ppg_before=("PPG_Before", "mean"),
            ppg_missed=("PPG_Missed", "mean"),
            gd_drop=("Team_Perf_Drop_Index", "mean"),
            relapse=("Is_Relapse_60d", lambda s: s.mean() * 100),
        )
        .sort_values("gd_drop", ascending=False)
    )
    club_lines = "\n".join(
        f"  - {idx}: {int(r.spells)} spells | PPG {r.ppg_before:.2f} -> {r.ppg_missed:.2f} | GD drop {r.gd_drop:+.2f} | 60d relapse {r.relapse:.1f}%"
        for idx, r in club_stats.iterrows()
    )

    comebacks = (
        df.groupby(["Player_Name", "Club"])
        .agg(spells=("Injury_Type", "count"), delta=("Rating_Delta", "mean"), after=("Avg_Rating_After", "mean"))
        .query("spells >= 2")
        .dropna()
        .sort_values("delta", ascending=False)
        .head(6)
    )
    cb_lines = "\n".join(
        f"  - {idx[0]} ({idx[1]}): {r.delta:+.2f} rating delta (post-return avg {r.after:.2f} across {int(r.spells)} spells)"
        for idx, r in comebacks.iterrows()
    )

    q_lower = question.lower()
    specific_records = ""
    for player in df["Player_Name"].dropna().unique():
        if player.lower() in q_lower:
            sub = df[df["Player_Name"] == player][
                [
                    "Season",
                    "Club",
                    "Position",
                    "Age",
                    "FIFA_Rating",
                    "Injury_Type",
                    "Days_Out",
                    "Avg_Rating_Before",
                    "Avg_Rating_After",
                    "Rating_Delta",
                    "Team_Perf_Drop_Index",
                    "Is_Relapse_60d",
                ]
            ]
            specific_records += f"\n\nEXACT INJURY LOGS FOR {player.upper()}:\n{sub.to_string(index=False)}"

    for club in df["Club"].dropna().unique():
        if club.lower() in q_lower:
            top_p = (
                df[df["Club"] == club]
                .groupby("Player_Name")
                .agg(
                    spells=("Injury_Type", "count"),
                    days=("Days_Out", "sum"),
                    gd_drop=("Team_Perf_Drop_Index", "mean"),
                    rating_delta=("Rating_Delta", "mean"),
                )
                .sort_values("gd_drop", ascending=False)
                .head(8)
            )
            specific_records += f"\n\nTOP AFFECTED PLAYERS AT {club.upper()}:\n{top_p.round(2).to_string()}"

    return f"""
ACTIVE FILTERED DATASET SNAPSHOT:
- Total Injury Spells: {len(df)} across {df['Player_Name'].nunique()} unique players
- Clubs: {', '.join(sorted(df['Club'].unique()))}
- Seasons: {', '.join(sorted(df['Season'].unique()))}
- Median Days Out: {df['Days_Out'].median():.1f} days (Mean: {df['Days_Out'].mean():.1f} days)
- Team GD Drop Index (Mean): {df['Team_Perf_Drop_Index'].mean():+.2f} goals/match
- Team PPG Shift: {df['PPG_Before'].mean():.2f} -> {df['PPG_Missed'].mean():.2f} PPG during absence
- 60-Day Relapse Rate: {df['Is_Relapse_60d'].mean() * 100:.1f}% ({int(df['Is_Relapse_60d'].sum())} repeat spells)
- Avg Player Match Rating: {df['Avg_Rating_Before'].mean():.2f} before -> {df['Avg_Rating_After'].mean():.2f} after (Delta: {df['Rating_Delta'].mean():+.2f})

TOP HIGH-IMPACT INJURIES (min 3 cases):
{inj_lines}

CLUB RESILIENCE BREAKDOWN:
{club_lines}

TOP COMEBACK PLAYERS (min 2 spells):
{cb_lines}
{specific_records}
""".strip()


def ask_groq_analyst(
    messages: list[dict],
    df: pd.DataFrame,
    model: str = "openai/gpt-oss-20b",
) -> str:
    """Sends conversation + live filtered dataset context to Groq with intent-aware prompting."""
    resolved_key = _get_groq_api_key()
    if not resolved_key:
        return "⚠️ `GROQ_API_KEY` not found. Add it to your local `.env` file or Streamlit Cloud Secrets."

    latest_question = messages[-1]["content"]
    data_context = build_data_context(df, latest_question)

    system_prompt = f"""You are **FootLens AI**, an elite Premier League Sports Science & Tactical Data Analyst embedded inside an interactive Streamlit dashboard.

### CORE BEHAVIOR RULES
1. **Match User Intent:**
   - If the user sends a casual greeting or small talk (e.g., "hi", "hello", "thanks"), respond warmly in 1–2 sentences and suggest 2 specific analytical questions they can ask based on the active dataset. Do NOT dump statistics unprompted.
   - If the user asks an analytical, player, club, injury, or tactical question, answer directly with structured bullet points and bold key numbers.
2. **Strict Grounding (Zero Hallucination):**
   - Base ALL numerical claims strictly on the **VERIFIED DATASET SNAPSHOT** below.
   - If a player, club, or metric is not present in the active filtered snapshot, explicitly state that it is outside the current filter selection and suggest adjusting the sidebar filters. Never invent or estimate missing stats.
3. **Metric Sign Conventions (Read Carefully):**
   - `Team GD Drop Index` = $\\text{{Avg GD}}_{{\\text{{Before}}}} - \\text{{Avg GD}}_{{\\text{{Missed}}}}$. A **positive** number (e.g., `+1.42`) means the team's Goal Difference **worsened** during the player's absence. A **negative** number means the team performed better without them.
   - `Rating Delta` = $\\text{{Avg Rating}}_{{\\text{{After}}}} - \\text{{Avg Rating}}_{{\\text{{Before}}}}$. A **positive** number (e.g., `+0.98`) means the player **improved** post-recovery.
   - `60-Day Relapse Rate` = percentage of injuries occurring within 60 days of a previous medical clearance.
4. **Actionable Sports-Science Framing:**
   - For analytical questions, conclude with **1 concise, evidence-backed recommendation** tailored to a Technical Director, Head of Sports Science, or Manager (e.g., substitute reintegration `(S)`, squad rotation during Dec–Feb congestion, or soft-tissue load management).

### VERIFIED DATASET SNAPSHOT (LIVE FILTERED VIEW)
{data_context}"""

    api_messages = [{"role": "system", "content": system_prompt}] + [
        {"role": m["role"], "content": m["content"]} for m in messages[-6:]
    ]

    client = Groq(api_key=resolved_key)
    completion = client.chat.completions.create(
        model=model,
        messages=api_messages,
        temperature=0.25,
        max_tokens=900,
    )
    return completion.choices[0].message.content