import pandas as pd
from preprocess import load_and_clean_data


def run_eda_summaries(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Generates statistical summaries, groupby tables, and pivot tables for FootLens EDA."""
    # 1. Descriptive statistics
    metrics = [
        "Age",
        "FIFA_Rating",
        "Days_Out",
        "Avg_Rating_Before",
        "Avg_Rating_After",
        "Rating_Delta",
        "Team_Perf_Drop_Index",
    ]
    summary_stats = df[metrics].describe().T[["count", "mean", "std", "min", "50%", "max"]]

    # 2. Top 5 high-impact injuries (min 5 cases)
    top_injuries = (
        df.groupby("Injury_Type", as_index=False)
        .agg(
            Cases=("Player_Name", "count"),
            Mean_Days_Out=("Days_Out", "mean"),
            Median_Days_Out=("Days_Out", "median"),
            Team_GD_Drop=("Team_Perf_Drop_Index", "mean"),
            Rating_Delta=("Rating_Delta", "mean"),
        )
        .query("Cases >= 5")
        .sort_values("Team_GD_Drop", ascending=False)
    )

    # 3. Club vulnerability aggregation
    club_summary = (
        df.groupby("Club", as_index=False)
        .agg(
            Total_Injuries=("Player_Name", "count"),
            Mean_Days_Out=("Days_Out", "mean"),
            Win_Rate_Before=("Win_Rate_Before", "mean"),
            Win_Rate_Missed=("Win_Rate_Missed", "mean"),
            Team_GD_Drop=("Team_Perf_Drop_Index", "mean"),
        )
        .sort_values("Total_Injuries", ascending=False)
    )

    # 4. Pivot table: Pre- vs. Post-injury metrics by Position
    position_pivot = pd.pivot_table(
        df,
        index="Position",
        values=[
            "Days_Out",
            "Avg_Rating_Before",
            "Avg_Rating_After",
            "Rating_Delta",
            "Team_Perf_Drop_Index",
        ],
        aggfunc={
            "Days_Out": "median",
            "Avg_Rating_Before": "mean",
            "Avg_Rating_After": "mean",
            "Rating_Delta": "mean",
            "Team_Perf_Drop_Index": "mean",
        },
    )

    # 5. Pivot table: Multi-season injury trends
    season_pivot = pd.pivot_table(
        df,
        index="Season",
        values=["Player_Name", "Days_Out", "Avg_Rating_Before", "Avg_Rating_After", "Team_Perf_Drop_Index"],
        aggfunc={
            "Player_Name": "count",
            "Days_Out": "mean",
            "Avg_Rating_Before": "mean",
            "Avg_Rating_After": "mean",
            "Team_Perf_Drop_Index": "mean",
        },
    ).rename(columns={"Player_Name": "Injury_Count"})

    return {
        "summary_stats": summary_stats,
        "top_injuries": top_injuries,
        "club_summary": club_summary,
        "position_pivot": position_pivot,
        "season_pivot": season_pivot,
    }


if __name__ == "__main__":
    cleaned_df = load_and_clean_data()
    tables = run_eda_summaries(cleaned_df)
    for name, table in tables.items():
        print(f"\n=== {name.upper()} ===")
        print(table.round(2))