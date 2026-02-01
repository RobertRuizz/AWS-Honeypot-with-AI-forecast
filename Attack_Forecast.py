import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta
from statsmodels.tsa.statespace.sarimax import SARIMAX

# === STEP 1: Load and simulate attack data ===
df = pd.read_csv("cleaned_minimal_logs.csv")
if 'alert.category' not in df.columns:
    raise ValueError("Column 'alert.category' not found!")

# Define the time window
start_date = pd.Timestamp("2025-03-01")
end_date = pd.Timestamp("2025-07-31")
days_range = pd.date_range(start=start_date, end=end_date, freq='D')

# Simulate total daily attack volumes between 20k–100k
daily_attack_counts = np.randint(20000, 100000, size=len(days_range))
categories = df['alert.category'].dropna().unique()

# Simulate rows for each day
simulated_rows = []
for date, attack_count in zip(days_range, daily_attack_counts):
    sampled_attacks = np.choice(categories, size=attack_count, replace=True)
    timestamps = [date + timedelta(seconds=np.random.randint(0, 86400)) for _ in range(attack_count)]
    simulated_rows.extend(zip(timestamps, sampled_attacks))

# Create full dataset
sim_df = pd.DataFrame(simulated_rows, columns=['@timestamp', 'alert.category'])
sim_df['date'] = sim_df['@timestamp'].dt.floor('D')

# === STEP 2: Analyze top 5 attacks and forecast the top one ===
attack_counts = sim_df.groupby(['date', 'alert.category']).size().reset_index(name='count')
top_5_attacks = attack_counts['alert.category'].value_counts().nlargest(5).index.tolist()

# Plot all 5 attack trends and forecast the top one
plt.figure(figsize=(16, 7))
colors = ['blue', 'green', 'red', 'orange', 'purple']

for i, attack in enumerate(top_5_attacks):
    df_attack = attack_counts[attack_counts['alert.category'] == attack].set_index('date').sort_index()
    ts_data = df_attack['count'].asfreq('D').fillna(0)

    if i == 0:
        # Forecast only for top attack
        model = SARIMAX(ts_data, order=(1, 1, 1), seasonal_order=(1, 1, 1, 7))
        result = model.fit(disp=False)
        forecast_days = 30
        forecast = result.get_forecast(steps=forecast_days)
        forecast_index = pd.date_range(start=ts_data.index[-1] + pd.Timedelta(days=1), periods=forecast_days, freq='D')
        forecast_series = pd.Series(forecast.predicted_mean, index=forecast_index)
        ts_data = pd.concat([ts_data, forecast_series])
    
    # Limit to March–July
    ts_data = ts_data[(ts_data.index >= start_date) & (ts_data.index <= end_date)]
    plt.plot(ts_data.index, ts_data.values, label=attack, linewidth=2, color=colors[i % len(colors)])

    # Add labels for July only
    for date, val in ts_data.items():
        if date >= pd.Timestamp("2025-07-01") and val > 0 and date.day in [1, 15, 31]:
            plt.text(date, val + 1000, f"{attack}\n{int(val):,}", ha='center', fontsize=8, color=colors[i % len(colors)])

# === STEP 3: Final chart details ===
plt.title("📈 Forecasted Honeypot Attacks (Mar–Jul 2025)", fontsize=16)
plt.xlabel("Date")
plt.ylabel("Attack Count (per Day)")
plt.legend(title="Attack Types")
plt.grid(True)
plt.xticks(rotation=45)
plt.xlim(start_date, end_date)
plt.tight_layout()

plt.show()
