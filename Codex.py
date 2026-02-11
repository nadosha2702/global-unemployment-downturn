import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("unemployment analysis.csv")

# Reshape data from wide to long
df_long = df.melt(
    id_vars=["Country Name", "Country Code"],
    var_name="Year",
    value_name="Unemployment Rate"
)

# Convert Year to numeric
df_long["Year"] = pd.to_numeric(df_long["Year"], errors="coerce")

# Check missing values (for transparency)
df_long.isna().sum()

# Compute global average unemployment per year
global_trend = (
    df_long
    .groupby("Year")["Unemployment Rate"]
    .mean()
    .reset_index()
    .sort_values("Year")
)

# Year-to-year change
global_trend["Change"] = global_trend["Unemployment Rate"].diff()

# Plot global trend
plt.figure()
plt.plot(global_trend["Year"], global_trend["Unemployment Rate"])
plt.xlabel("Year")
plt.ylabel("Global Average Unemployment Rate")
plt.title("Global Unemployment Trend (1991–2021)")
plt.show()

plt.figure()
plt.bar(global_trend["Year"], global_trend["Change"])
plt.axhline(0)

for year in [2009, 2020]:
    value = global_trend.loc[global_trend["Year"] == year, "Change"].values
    if len(value) > 0:
        plt.text(year, value[0], str(year), ha='center', va='bottom')

plt.xlabel("Year")
plt.ylabel("Year-to-Year Change in Unemployment Rate")
plt.title("Yearly Change in Global Unemployment Rate")
plt.show()

# Step 5: Compare selected countries
countries = ["United States", "Germany", "India", "Brazil"]

comparison_df = df_long[df_long["Country Name"].isin(countries)]

plt.figure(figsize=(10, 6))

for country in countries:
    country_data = comparison_df[comparison_df["Country Name"] == country]
    plt.plot(
        country_data["Year"],
        country_data["Unemployment Rate"],
        label=country
    )

# Highlight crisis years
plt.axvline(2009, linestyle="--", alpha=0.7)
plt.axvline(2020, linestyle="--", alpha=0.7)

plt.xlabel("Year")
plt.ylabel("Unemployment Rate (%)")
plt.title("Unemployment Trends Across Selected Economies")
plt.legend()
plt.show()
