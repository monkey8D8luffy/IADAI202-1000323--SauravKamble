import numpy as np
import pandas as pd

BIG_SIX_CLUBS = {
    "Man City",
    "Liverpool",
    "Arsenal",
    "Chelsea",
    "Man United",
    "Tottenham",
}


def _categorize_injury(injury_name: str) -> str:
    """Classifies raw injury descriptions into biomechanical sports-science groups."""
    s = str(injury_name).lower()
    if any(
        k in s
        for k in [
            "hamstring",
            "calf",
            "groin",
            "thigh",
            "muscle",
            "quadriceps",
            "adductor",
            "hip flexor",
        ]
    ):
        return "Soft-Tissue / Muscular"
    if any(
        k in s
        for k in [
            "knee",
            "ankle",
            "ligament",
            "meniscus",
            "cruciate",
            "shoulder",
            "hip",
            "achilles",
            "tendon",
        ]
    ):
        return "Joint / Ligament / Tendon"
    if any(
        k in s
        for k in [
            "head",
            "concussion",
            "knock",
            "fracture",
            "broken",
            "toe",
            "foot",
            "back",
            "rib",
            "hand",
            "wrist",
            "jaw",
        ]
    ):
        return "Contact / Structural Trauma"
    if any(k in s for k in ["corona", "ill", "virus", "fitness", "fatigue", "infection"]):
        return "Illness / Conditioning"
    return "Other / Unspecified"


def load_and_clean_data(filepath: str = "data/player_injuries_impact.xlsx") -> pd.DataFrame:
    """
    Loads raw FootLens injury data, resolves string/date anomalies,
    and engineers advanced sports-science & tactical performance KPIs.
    """
    if filepath.endswith(".csv"):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath, sheet_name="player_injuries_impact")

    # 1. Standardize column names
    df = df.rename(
        columns={
            "Name": "Player_Name",
            "Team Name": "Club",
            "FIFA rating": "FIFA_Rating",
            "Date of Injury": "Injury_Date",
            "Date of return": "Return_Date_Raw",
        }
    )

    # 2. Clean text categories
    df["Injury_Type"] = df["Injury"].astype(str).str.strip().str.title()
    df["Position"] = df["Position"].astype(str).str.strip().str.title()
    df["Club"] = df["Club"].astype(str).str.strip()
    df["Injury_Category"] = df["Injury_Type"].apply(_categorize_injury)

    # 3. Clean & parse dates (fixing 'Present' and year typos)
    df["Injury_Date"] = pd.to_datetime(df["Injury_Date"], errors="coerce")
    df["Is_Ongoing_Injury"] = df["Return_Date_Raw"].astype(str).str.strip().eq("Present")

    return_str = (
        df["Return_Date_Raw"]
        .astype(str)
        .str.strip()
        .replace({"Present": np.nan, "Mar 7, 0202": "Mar 7, 2021"})
    )
    df["Return_Date"] = pd.to_datetime(return_str, errors="coerce")

    neg_duration_mask = df["Return_Date"] < df["Injury_Date"]
    df.loc[neg_duration_mask, "Return_Date"] = (
        df.loc[neg_duration_mask, "Return_Date"] + pd.DateOffset(years=1)
    )

    df["Days_Out"] = (df["Return_Date"] - df["Injury_Date"]).dt.days
    df["Injury_Month"] = df["Injury_Date"].dt.month_name()
    df["Injury_Month_Num"] = df["Injury_Date"].dt.month

    # 4. Chronological player sorting for Relapse / Re-injury Detection
    df = df.sort_values(["Player_Name", "Injury_Date"]).reset_index(drop=True)
    df["Prev_Return_Date"] = df.groupby("Player_Name")["Return_Date"].shift(1)
    df["Prev_Injury_Type"] = df.groupby("Player_Name")["Injury_Type"].shift(1)
    df["Days_Since_Last_Return"] = (df["Injury_Date"] - df["Prev_Return_Date"]).dt.days
    df["Is_Relapse_60d"] = (df["Days_Since_Last_Return"] >= 0) & (
        df["Days_Since_Last_Return"] <= 60
    )

    # 5. Clean match player ratings & extract Return-to-Play protocol
    before_r_cols = [f"Match{i}_before_injury_Player_rating" for i in range(1, 4)]
    after_r_cols = [f"Match{i}_after_injury_Player_rating" for i in range(1, 4)]

    for col in before_r_cols + after_r_cols:
        cleaned_rating = (
            df[col]
            .astype(str)
            .str.replace(r"\(S\)", "", regex=True)
            .str.replace(r"\.\.+", ".", regex=True)
            .str.strip()
        )
        df[f"{col}_num"] = pd.to_numeric(cleaned_rating, errors="coerce")

    df["Post_Injury_Sub_Apps"] = df[after_r_cols].apply(
        lambda row: sum("(S)" in str(val) for val in row), axis=1
    )

    m1_after_raw = df["Match1_after_injury_Player_rating"].astype(str).str.strip()
    df["Return_Protocol"] = np.where(
        m1_after_raw.str.contains(r"\(S\)", regex=True),
        "Gradual Sub Reintegration (S)",
        np.where(
            m1_after_raw.isin(["N.A.", "nan", "None", ""]),
            "No Post-Return Data",
            "Immediate Full Start",
        ),
    )
    df["Next_Spell_Relapse_60d"] = (
        df.groupby("Player_Name")["Is_Relapse_60d"].shift(-1).fillna(False)
    )

    # 6. Clean Goal Difference (GD) columns
    before_gd_cols = [f"Match{i}_before_injury_GD" for i in range(1, 4)]
    missed_gd_cols = [f"Match{i}_missed_match_GD" for i in range(1, 4)]
    after_gd_cols = [f"Match{i}_after_injury_GD" for i in range(1, 4)]

    for col in before_gd_cols + missed_gd_cols + after_gd_cols:
        df[f"{col}_num"] = pd.to_numeric(df[col], errors="coerce")

    df["Avg_Rating_Before"] = df[[f"{c}_num" for c in before_r_cols]].mean(axis=1)
    df["Avg_Rating_After"] = df[[f"{c}_num" for c in after_r_cols]].mean(axis=1)
    df["Rating_Delta"] = df["Avg_Rating_After"] - df["Avg_Rating_Before"]

    df["Avg_GD_Before"] = df[[f"{c}_num" for c in before_gd_cols]].mean(axis=1)
    df["Avg_GD_Missed"] = df[[f"{c}_num" for c in missed_gd_cols]].mean(axis=1)
    df["Avg_GD_After"] = df[[f"{c}_num" for c in after_gd_cols]].mean(axis=1)
    df["Team_Perf_Drop_Index"] = df["Avg_GD_Before"] - df["Avg_GD_Missed"]

    # 7. Win Rates & Points Per Game (PPG: Win=3, Draw=1, Lose=0)
    before_res_cols = [f"Match{i}_before_injury_Result" for i in range(1, 4)]
    missed_res_cols = [f"Match{i}_missed_match_Result" for i in range(1, 4)]
    after_res_cols = [f"Match{i}_after_injury_Result" for i in range(1, 4)]

    def _calc_win_rate(row: pd.Series, cols: list[str]) -> float:
        valid = [
            str(row[c]).strip().lower()
            for c in cols
            if str(row[c]).strip() not in {"N.A.", "nan", "None", ""}
        ]
        return (sum(v == "win" for v in valid) / len(valid) * 100.0) if valid else np.nan

    def _calc_ppg(row: pd.Series, cols: list[str]) -> float:
        pts = []
        for c in cols:
            v = str(row[c]).strip().lower()
            if v == "win":
                pts.append(3.0)
            elif v == "draw":
                pts.append(1.0)
            elif v == "lose":
                pts.append(0.0)
        return float(np.mean(pts)) if pts else np.nan

    df["Win_Rate_Before"] = df.apply(lambda r: _calc_win_rate(r, before_res_cols), axis=1)
    df["Win_Rate_Missed"] = df.apply(lambda r: _calc_win_rate(r, missed_res_cols), axis=1)
    df["Win_Rate_After"] = df.apply(lambda r: _calc_win_rate(r, after_res_cols), axis=1)
    df["Win_Rate_Drop"] = df["Win_Rate_Before"] - df["Win_Rate_Missed"]

    df["PPG_Before"] = df.apply(lambda r: _calc_ppg(r, before_res_cols), axis=1)
    df["PPG_Missed"] = df.apply(lambda r: _calc_ppg(r, missed_res_cols), axis=1)
    df["PPG_After"] = df.apply(lambda r: _calc_ppg(r, after_res_cols), axis=1)
    df["PPG_Drop"] = df["PPG_Before"] - df["PPG_Missed"]

    # 8. Opposition Difficulty Adjustment (% of matches vs Big-6 clubs)
    before_opp_cols = [f"Match{i}_before_injury_Opposition" for i in range(1, 4)]
    missed_opp_cols = [f"Match{i}_missed_match_Opposition" for i in range(1, 4)]

    def _calc_big6_share(row: pd.Series, cols: list[str]) -> float:
        valid = [
            str(row[c]).strip()
            for c in cols
            if str(row[c]).strip() not in {"N.A.", "nan", "None", ""}
        ]
        return (sum(v in BIG_SIX_CLUBS for v in valid) / len(valid) * 100.0) if valid else np.nan

    df["Big6_Share_Before"] = df.apply(lambda r: _calc_big6_share(r, before_opp_cols), axis=1)
    df["Big6_Share_Missed"] = df.apply(lambda r: _calc_big6_share(r, missed_opp_cols), axis=1)
    df["Fixture_Difficulty_Shift"] = df["Big6_Share_Missed"] - df["Big6_Share_Before"]

    # 9. Squad Role Tier based on FIFA Rating
    df["Squad_Tier"] = pd.cut(
        df["FIFA_Rating"],
        bins=[0, 76, 81, 100],
        labels=["Squad Depth (<77)", "First-Team Regular (77–81)", "Star Player (82+)"],
    )

    return df