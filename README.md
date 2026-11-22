# ⚽ FootLens Pro Intelligence

### Premier League Player Injuries, Squad Vulnerability & Sports Science Analytics Platform

**Live Web Application:** <https://iadai202-1000323--sauravkamble-3zobe2liue3eyop8nsekiy.streamlit.app/>

**GitHub Repository:** <https://github.com/monkey8D8luffy/IADAI202-1000323--SauravKamble>

## 📋 Academic & Assessment Metadata

| Field | Details | 
| ----- | ----- | 
| **Student Name** | Saurav Kamble | 
| **Candidate Registration Number** | 1000323 | 
| **CRS Name** | Artificial Intelligence | 
| **Course Name** | Mathematics for AI-II | 
| **Assessment Title** | Summative Assessment — Developing User-Centered Dashboards to Solve Real-World Problems | 
| **Scenario** | Scenario 1: FootLens Analytics — Player Injuries and Team Performance Dashboard | 
| **School Name** | Ryan Global School | 
| **Evaluator Access Granted** | `ai.assignments@wacpinternational.org` | 

## 📌 1. Project Overview & Domain Context

In elite professional football, player availability directly governs tactical continuity, match outcomes, and final league standings. Traditional medical logs often track injuries in isolation from match-by-match team performance, leaving **Technical Directors**, **Heads of Sports Science**, and **Performance Analysts** without clear answers on how specific absences erode Points Per Game (PPG) or whether returning starters are rushed back prematurely.

**FootLens Pro Intelligence** bridges medical telemetry and match performance across **five English Premier League seasons (`2019/20`–`2023/24`)**, analyzing **656 injury spells**, **224 unique players**, **12 playing positions**, and **8 clubs** (*Arsenal, Aston Villa, Brentford, Burnley, Everton, Manchester United, Newcastle United,* and *Tottenham Hotspur*).

### Core Capabilities

* **Executive Telemetry & Multi-Faceted Filtering:** Real-time filtering across Seasons, Clubs, Positions, Biomechanical Categories, and FIFA Squad Role Tiers with 6 live KPI metric cards.

* **Opposition-Adjusted Squad Impact:** Evaluates Goal Difference (GD) Drop Index, Points Per Game (PPG) shifts, Win Rate changes, and Big-6 fixture difficulty shifts during player absences.

* **Sports Science & Relapse Lab:** Quantifies 60-day re-injury relapse rates and demonstrates the protective impact of gradual substitute reintegration `(S)` versus immediate starting XI deployment.

* **Player Scouting & Comeback Lab:** Tracks individual player match ratings across a 6-match window (`Match -3` to `Match +3`) alongside the full 9-match club Goal Difference arc (`Pre → Absent → Return`).

* **Grounded AI Data Analyst Chat:** Conversational analyst powered by Groq (`openai/gpt-oss-20b`) injected with live filtered aggregations and exact player/club injury logs.

## 🖼️ 2. Dashboard Screenshots

### 1. Executive KPI Strip & Tab 1 — Club & Tactical Impact
*Displays the 6 live KPI cards (`656` spells, `25`-day median absence, `+0.10` Team GD Drop Index, `1.40` PPG during absence, `22.3%` 60-day relapse rate, `-0.01` post-return form), Top 10 High-Impact Injuries, and Club PPG Resilience.*

(<img width="1280" height="735" alt="Screenshot 2026-11-22 140131" src="https://github.com/user-attachments/assets/f48084e7-8972-420b-8272-9be9904f71ac" />
)

---

### 2. Tab 2 — Sports Science & Relapse Lab
*Compares Return-to-Play protocols (`20.0%` 60-day relapse rate with Gradual Sub Reintegration `(S)` vs. `27.2%` with Immediate Full Start) alongside Biomechanical Injury Burden across medical categories.*

(<img width="1280" height="734" alt="Screenshot 2026-11-22 140204" src="https://github.com/user-attachments/assets/de8ef81d-83b1-47d5-bca3-a942f1de1b42" />
)

---

### 3. Tab 3 — Congestion & Positional Matrix
*Maps injury frequency clusters across calendar months and clubs (`December–February` winter fixture congestion), positional Goal Difference vulnerability, and multi-season injury volume vs. severity trends.*

(<img width="1280" height="735" alt="Screenshot 2026-11-22 140235" src="https://github.com/user-attachments/assets/779a5a14-2738-40c8-9c08-ffe731307960" />
)

---

### 4. Tab 4 — Player Scouting & Comeback Lab
*Tracks individual match-rating trajectories (`Match -3` to `Match +3`) for Richarlison against the squad benchmark, visualizes Everton's 9-match Goal Difference arc, and ranks top comeback performers.*

(<img width="1280" height="734" alt="Screenshot 2026-11-22 140615" src="https://github.com/user-attachments/assets/25945a36-2c3b-415b-9a4e-c138cfb308ef" />
)

---

### 5. Tab 5 — Grounded AI Data Analyst Chat (`openai/gpt-oss-20b`)
*Demonstrates live natural-language Q&A comparing Brentford (`34` spells, `+0.62` GD drop) and Manchester United (`101` spells, `+0.08` GD drop) grounded strictly in filtered dataset telemetry.*

(<img width="1280" height="732" alt="Screenshot 2026-11-22 140312" src="https://github.com/user-attachments/assets/9d6be90d-89de-418e-acc5-a6cd485cb05b" />
)

## 🔍 3. Research Questions & Verified Statistical Findings

Seven domain-specific research questions guided the statistical modeling and visual design:

### RQ1 — Which injury types cause the sharpest drop in team performance?

While **Hamstring Injuries** (95 cases), **Knee Injuries** (57 cases), and **Ankle Injuries** (52 cases) occur most frequently, structural surgeries and conditioning setbacks inflict the steepest team Goal Difference collapses (minimum 5 cases):

| Rank | Injury Type | Cases | Mean Days Out | Median Days Out | Team GD Before | Team GD Missed | Team GD Drop Index | Rating Delta | 
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | 
| **1** | **Knee Surgery** | 7 | 138.9 | 98.0 | +0.81 | \-0.38 | **+1.42** | +0.09 | 
| **2** | **Fitness Setback** | 6 | 49.7 | 24.0 | +0.08 | \-1.25 | **+1.29** | +0.04 | 
| **3** | **Muscle Injury** | 27 | 38.5 | 24.0 | +0.64 | \-0.12 | **+0.77** | \-0.07 | 
| **4** | **Groin Injury** | 25 | 23.2 | 19.0 | +0.23 | \-0.35 | **+0.58** | \-0.10 | 
| **5** | **Head Injury** | 9 | 18.0 | 7.0 | +0.07 | \-0.35 | **+0.43** | +0.18 | 

### RQ2 — How do club win rates and Goal Differences shift during player absence?

League-wide win rate declines from **40.7% → 38.8%** when players are sidelined. Deep rosters (**Manchester United**, **Newcastle United**) absorb high injury volume with minimal GD erosion, whereas thinner squads (**Brentford**, **Burnley**) suffer severe table-point losses:

| Club | Total Injuries | Mean Days Out | Win Rate (Before) | Win Rate (Missed) | Team GD Drop Index | 
| ----- | ----- | ----- | ----- | ----- | ----- | 
| **Newcastle United** | 120 | 45.3 | 34.8% | 34.2% | **+0.05** | 
| **Everton FC** | 103 | 48.3 | 37.2% | 33.2% | **+0.07** | 
| **Manchester United** | 101 | 37.3 | 44.6% | 50.0% | **+0.08** | 
| **Arsenal FC** | 84 | 44.9 | 49.4% | 48.6% | **-0.07** | 
| **Tottenham Hotspur** | 82 | 34.1 | 49.8% | 47.2% | **-0.14** | 
| **Burnley FC** | 71 | 45.2 | 31.9% | 24.3% | **+0.53** | 
| **Aston Villa** | 61 | 44.3 | 41.8% | 40.4% | **+0.03** | 
| **Brentford FC** | 34 | 90.8 | 33.3% | 22.1% | **+0.62** | 

### RQ3 — How do individual players perform after recovery?

League-wide rating change averages $-0.01$ ($\text{SD} = 0.66$), masking sharp individual divergence across players with $\ge 2$ injury spells:

* **Top 5 Comeback Rebounds (`Rating_Delta > 0`):** **Morgan Schneiderlin** (`+1.33`: $6.05 \rightarrow 7.07$), **Harvey Barnes** (`+1.02`: $5.98 \rightarrow 7.00$), **Richarlison** (`+0.98`: $6.53 \rightarrow 7.51$), **Jadon Sancho** (`+0.83`: $5.88 \rightarrow 6.80$), and **Paul Pogba** (`+0.82`: $6.39 \rightarrow 7.26$ across 6 spells).

* **Top 5 Post-Injury Declines (`Rating_Delta < 0`):** **Nathan Collins** (`-1.57`: $7.02 \rightarrow 5.77$), **Nathan Patterson** (`-1.20`: $6.02 \rightarrow 5.53$), **Alexandre Lacazette** (`-1.16`: $6.71 \rightarrow 6.02$), **Jacob Ramsey** (`-0.93`: $6.63 \rightarrow 6.24$), and **Tom Davies** (`-0.80`: $6.51 \rightarrow 5.98$).

### RQ4 — Are there seasonal injury clusters across months and clubs?

Yes—grouping injury onset dates by calendar month and club reveals recurring peaks during **winter fixture congestion (`December–February`)** and **early-season intensity (`August–October`)**.

### RQ5 — Does player age correlate with recovery duration or team impact?

Linear correlation between player age and recovery duration is negligible (**Pearson** $r = -0.006$), with U23 players (`18–23`, mean `47.4` days) and veterans (`32+`, mean `46.6` days) spending nearly identical time sidelined. However, **veteran absences (`32+`)** inflict the largest team GD penalty (**`+0.25`** vs. **`-0.01`** for U23s), reflecting on-pitch tactical leadership loss.

### RQ6 — Does gradual substitute reintegration `(S)` reduce 60-day relapse rates?

Across 515 spells with complete post-return match records, players eased back via **Gradual Sub Reintegration `(S)`** on `Match +1` ($n = 140$) recorded a **20.0% 60-day relapse rate**, compared to **27.2%** for players thrown immediately into the starting XI ($n = 375$)—a **26.5% relative reduction in re-injury risk**.

### RQ7 — How does positional depth affect team Goal Difference during absences?

**Goalkeeper** absences trigger the steepest single-position drop (**`+0.94`** Team GD Drop Index) due to low positional redundancy, whereas **Attacking Midfielders** recover fastest (`19.0` median days out).

## 🧹 4. Data Preprocessing & Mathematical Formulations (`src/preprocess.py`)

### Raw Data Anomalies Resolved

1. **Substitute Tag Extraction (`(S)`):** Extracted substitute appearances from post-injury ratings (e.g., `6(S)`, `6.1(S)`) into `Post_Injury_Sub_Apps` and classified first-match-back deployment into `Return_Protocol` before stripping `(S)` to recover numeric ratings.

2. **String Nulls & Decimal Typo Sanitization:** Converted `"N.A."` strings across **855 rating cells** and **1,309 goal-difference cells** to `NaN` and corrected malformed double decimals (`'5..8'` $\rightarrow$ `5.8`).

3. **Ongoing Active Injuries (`"Present"`):** Flagged three active `2023/24` cases (*Jacob Ramsey, Boubacar Kamara, Jordan Beyer*) in `Is_Ongoing_Injury` and parsed their return dates as `NaT`.

4. **Year-Entry Date Typos:** Fixed `Mar 7, 0202` $\rightarrow$ `Mar 7, 2021` (Matty Cash) and shifted two 1-year-early return date entries (*Tanguy Ndombele*, *Matej Vydra*) forward by `+1` year, ensuring strictly positive recovery durations (`2` to `682` days).

5. **Categorical Standardization & Biomechanical Mapping:** Consolidated case-duplicate injury strings (e.g., `Hamstring injury` \[72\] + `hamstring injury` \[23\] = **95 `Hamstring Injury` cases**) and mapped all injuries into five biomechanical classes: *Soft-Tissue / Muscular*, *Joint / Ligament / Tendon*, *Contact / Structural Trauma*, *Illness / Conditioning*, and *Other / Unspecified*.

### Engineered Metrics & Equations

* **Individual Rating Delta:**
  $$
  \text{Rating\_Delta} = \overline{\text{Rating}}_{\text{After}(M+1..M+3)} - \overline{\text{Rating}}_{\text{Before}(M-3..M-1)}
  $$

* **Team Performance Drop Index:**
  $$
  \text{Team\_Perf\_Drop\_Index} = \overline{\text{GD}}_{\text{Before}(M-3..M-1)} - \overline{\text{GD}}_{\text{Missed}(\text{Out }1..3)}
  $$

* **Points Per Game (PPG) Shift ($\text{Win} = 3, \text{Draw} = 1, \text{Lose} = 0$):**
  $$
  \text{PPG\_Drop} = \text{PPG}_{\text{Before}} - \text{PPG}_{\text{Missed}}
  $$

* **60-Day Relapse Flag:**
  $$
  \text{Is\_Relapse\_60d} = \mathbb{I}\left(0 \le \text{Injury\_Date}_n - \text{Return\_Date}_{n-1} \le 60\right)
  $$

* **Opposition Difficulty Shift (Big-6 Share):**
  $$
  \text{Fixture\_Difficulty\_Shift} = \%\text{Big6}_{\text{Missed}} - \%\text{Big6}_{\text{Before}}
  $$

## 🏗️ 5. System Architecture & Repository Structure

The codebase separates data engineering, statistical EDA, AI reasoning, and UI presentation into clean, modular Python files:

```text
IADAI202-1000323--SauravKamble/
├── assets/
│   ├── 01_tactical_impact.jpg           # Tab 1: Executive KPIs & Club Tactical Impact
│   ├── 02_sports_science_lab.jpg        # Tab 2: Sports Science & Relapse Lab
│   ├── 03_congestion_matrix.jpg         # Tab 3: Congestion & Positional Matrix
│   ├── 04_player_scouting_comeback.jpg  # Tab 4: Player Scouting & Comeback Lab
│   └── 05_ai_analyst_chat.jpg           # Tab 5: Grounded AI Data Analyst Chat
├── data/
│   └── player_injuries_impact.xlsx      # Raw Premier League injury & match telemetry (656 rows, 42 cols)
├── src/
│   ├── preprocess.py                    # Data sanitization, date/rating fixes & feature engineering
│   ├── eda.py                           # Descriptive statistics, groupby() & pivot_table() summaries
│   └── ai_analyst.py                    # Grounded Groq LLM context builder & anti-hallucination engine
├── app.py                               # Main Streamlit 5-tab interactive dashboard
├── requirements.txt                     # Pinned Python dependencies for Streamlit Cloud
├── .gitignore                           # Excludes .env, local secrets, and Python cache files
└── README.md                            # Complete technical & analytical documentation
```

### AI Analyst Integration (`src/ai_analyst.py`)

* **Model:** Groq `openai/gpt-oss-20b` (`temperature = 0.25`) for low-latency, deterministic analytical reasoning.

* **Dynamic Context Grounding:** On every user query, `build_data_context()` computes real-time aggregations from the active sidebar-filtered DataFrame and automatically appends exact injury logs if a specific player or club name is detected in the prompt.

* **Key Management:** Uses `python-dotenv` to read `GROQ_API_KEY` from a local `.env` file during development and falls back seamlessly to `st.secrets["GROQ_API_KEY"]` in Streamlit Community Cloud.

## 🚀 6. Local Installation & Cloud Deployment

### Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/monkey8D8luffy/IADAI202-1000323--SauravKamble.git
   cd IADAI202-1000323--SauravKamble
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your local Groq API key:**
   Create a `.env` file in the project root:
   ```env
   GROQ_API_KEY=gsk_your_groq_api_key_here
   ```

4. **Launch the Streamlit application:**
   ```bash
   streamlit run app.py
   ```

### Deploy on Streamlit Community Cloud

1. Push the repository to GitHub (`.env` is ignored via `.gitignore` so credentials remain private).

2. Navigate to [share.streamlit.io](https://share.streamlit.io), select the repository, branch (`main`), and main entry point (`app.py`).

3. Open **App Settings → Secrets** and configure:
   ```toml
   GROQ_API_KEY = "gsk_your_groq_api_key_here"
   ```

4. Click **Deploy** to publish the live interactive dashboard.

## 🛠️ 7. Dependencies (`requirements.txt`)

* `streamlit>=1.38.0` — Interactive web application framework and state management

* `pandas>=2.2.0` & `numpy>=1.26.0` — Data cleaning, chronological relapse detection, and statistical aggregations

* `plotly>=5.22.0` — Interactive bar charts, heatmaps, multi-axis trend lines, and bubble scatter plots

* `openpyxl>=3.1.2` — Excel `.xlsx` dataset ingestion engine

* `matplotlib>=3.8.0` — Colormap rendering for Pandas `Styler.background_gradient()` leaderboards

* `groq>=0.15.0` & `python-dotenv>=1.0.0` — Grounded AI Data Analyst integration and secure environment variable loading
