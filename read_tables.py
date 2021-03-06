import pandas as pd
import glob
import more_itertools
import tabulate

li = []
all_files = glob.glob("*.csv")
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    df["Season"] = filename.split(".")[0]
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)
frame = frame.rename({"Squad": "Team"}, axis=1)

print("2014-2021")
print(frame[frame["Season"].isin([str(i) for i in range(2014,2022)])].groupby(["Team"]).agg(
    Rk=("Rk","mean"),
    W=("W","mean"),
    D=("D","mean"),
    L= ("L","mean"),
    GF=("GF","mean"),
    GA= ("GA","mean"),
    Pts= ("Pts","mean"),
    TotalPts= ("Pts","sum"),
).sort_values("TotalPts", ascending=False).head(n=10))

for years in more_itertools.windowed(range(2014,2022),n=3, step=1):
    print("")
    print(f"{years[0]}-{years[-1]}")
    df = frame[frame["Season"].isin([str(y) for y in years])].groupby(["Team"]).agg(
        # Rk=("Rk","mean"),
        W=("W","mean"),
        D=("D","mean"),
        L= ("L","mean"),
        GF=("GF","mean"),
        GA= ("GA","mean"),
        Pts= ("Pts","mean"),
    ).sort_values("Pts", ascending=False).head(n=6)
    print(tabulate.tabulate(df, headers='keys'))
print("")
