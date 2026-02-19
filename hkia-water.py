import pandas as pd

df = pd.read_csv("hkia_youtube_data.csv")
print(df.head())
print(df.info())

df_sorted = df.sort_values(by='views', ascending=False)

df_sorted.to_csv("hkia_youtube_sorted.csv", index=False)

print("Sorted CSV, ready for Power BI!")