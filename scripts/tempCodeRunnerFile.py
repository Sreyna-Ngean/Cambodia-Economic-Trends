"""Step 1: Download Cambodia indicators from the World Bank and save as CSV."""
from pathlib import Path
import wbgapi as wb

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

indicators = {
    "NY.GDP.MKTP.KD.ZG": "gdp_growth",        # GDP growth (annual %)
    "FP.CPI.TOTL.ZG": "inflation",            # Inflation, consumer prices (annual %)
    "NY.GDP.PCAP.CD": "gdp_per_capita",       # GDP per capita (current US$)
    "SE.PRM.ENRR": "primary_enrollment",      # School enrollment, primary (% gross)
    "SP.POP.TOTL": "population",              # Total population
}

# Fetch data and transpose so years are rows and indicators are columns
df = wb.data.DataFrame(list(indicators.keys()), "KHM", time=range(1995, 2025), numericTimeKeys=True)
df = df.T
df.index.name = "year"
df = df.reset_index()

# Clean year column (remove 'YR' if any linger, convert to int)
df["year"] = df["year"].astype(str).str.replace("YR", "").astype(int)

# Rename indicator columns and sort by year
df = df.rename(columns=indicators)
df = df.sort_values("year")

out = DATA / "cambodia_raw.csv"
df.to_csv(out, index=False)

print(f"Saved {len(df)} rows to {out}")
print(df.head())
print("\nMissing values per column:")
print(df.isna().sum())