import streamlit as st
import pandas as pd
import glob
import more_itertools
import tabulate

st.set_page_config(layout="wide")

li = []
all_files = glob.glob("data/*.csv")
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    df["Season"] = filename.split("/")[-1].split(".")[0]
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)
frame = frame.rename({"Squad": "Team"}, axis=1)

st.title("Premier League since Ferguson retired")

st.header("2014-2021")
st.table(frame[frame["Season"].isin([str(i) for i in range(2014,2022)])].groupby(["Team"]).agg(
    Rk=("Rk","mean"),
    W=("W","mean"),
    D=("D","mean"),
    L= ("L","mean"),
    GF=("GF","mean"),
    GA= ("GA","mean"),
    Pts= ("Pts","mean"),
    TotalPts= ("Pts","sum"),
).sort_values("TotalPts", ascending=False).head(n=6).style.format("{:.2f}"))

for years in more_itertools.windowed(range(2014,2022),n=3, step=1):
    st.header(f"{years[0]}-{years[-1]}")
    df = frame[frame["Season"].isin([str(y) for y in years])].groupby(["Team"]).agg(
        # Rk=("Rk","mean"),
        W=("W","mean"),
        D=("D","mean"),
        L= ("L","mean"),
        GF=("GF","mean"),
        GA= ("GA","mean"),
        Pts= ("Pts","mean"),
        TotalPts= ("Pts","sum"),
    ).sort_values("Pts", ascending=False).head(n=6)

    st.table(df.style.format("{:.2f}"))
