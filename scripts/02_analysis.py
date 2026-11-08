"""Step 2: Clean, analyze, and chart the data."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

df = pd.read_csv(DATA / "cambodia_raw.csv")

# Ensure year is treated as an integer
df["year"] = df["year"].astype(int)

# Save a cleaned copy (sorted, no fully empty rows)
clean = df.dropna(how="all", subset=[c for c in df.columns if c != "year"])
clean.to_csv(DATA / "cambodia_clean.csv", index=False)

# 1. Descriptive statistics
print("=== Descriptive statistics ===")
print(df.describe().round(2))

# 2. Average GDP growth by period
df["period"] = pd.cut(df["year"], bins=[1994, 2004, 2014, 2024],
                      labels=["1995-2004", "2005-2014", "2015-2024"])
print("\n=== GDP growth by period ===")
print(df.groupby("period", observed=True)["gdp_growth"].agg(["mean", "std"]).round(2))

# 3. Correlation
cols = ["gdp_growth", "inflation", "gdp_per_capita", "primary_enrollment"]
print("\n=== Correlation matrix ===")
print(df[cols].corr().round(2))

# 4. Simple regression: GDP per capita trend over time
reg = df.dropna(subset=["gdp_per_capita"])
X = sm.add_constant(reg["year"])
model = sm.OLS(reg["gdp_per_capita"], X).fit()
print("\n=== Regression: GDP per capita ~ year ===")
print(model.summary())

# 5. Chart 1: GDP growth with shocks marked
plt.figure(figsize=(9, 5))
plt.plot(df["year"], df["gdp_growth"], marker="o")
plt.axvline(2009, color="red", linestyle="--", label="Global financial crisis")
plt.axvline(2020, color="orange", linestyle="--", label="COVID-19")
plt.title("Cambodia GDP Growth, 1995-2024")
plt.xlabel("Year")
plt.ylabel("GDP growth (annual %)")
plt.legend()
plt.tight_layout()
plt.savefig(FIG / "gdp_growth.png", dpi=150)
plt.close()

# 6. Chart 2: GDP per capita with regression line
plt.figure(figsize=(9, 5))
plt.plot(reg["year"], reg["gdp_per_capita"], marker="o", label="Actual")
plt.plot(reg["year"], model.predict(X), linestyle="--", label="Linear trend")
plt.title("Cambodia GDP per Capita (current US$)")
plt.xlabel("Year")
plt.ylabel("US$")
plt.legend()
plt.tight_layout()
plt.savefig(FIG / "gdp_per_capita.png", dpi=150)
plt.close()

# 7. Chart 3: Inflation
plt.figure(figsize=(9, 5))
plt.bar(df["year"], df["inflation"])
plt.title("Cambodia Inflation (consumer prices, annual %)")
plt.xlabel("Year")
plt.ylabel("%")
plt.tight_layout()
plt.savefig(FIG / "inflation.png", dpi=150)
plt.close()

print("\nCharts saved in the figures/ folder.")