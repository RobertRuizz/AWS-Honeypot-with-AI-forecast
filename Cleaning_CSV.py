import pandas as pd

input_file = "cleaned_HoneypotDataLogs.csv"
output_file = "cleaned_minimal_logs.csv"
columns_to_keep = ['@timestamp', 'alert.category']

# Step 1: Load in chunks
chunks = pd.read_csv(
    input_file,
    usecols=lambda col: col in columns_to_keep,
    chunksize=5000,
    on_bad_lines='skip',
    engine='python'
)

# Step 2: Write to new file
with open(output_file, 'w', encoding='utf-8') as f:
    first = True
    total_rows = 0
    for chunk in chunks:
        # Drop only if BOTH are missing
        chunk = chunk.dropna(subset=['@timestamp', 'alert.category'], how='all')
        if not chunk.empty:
            if first:
                chunk.to_csv(f, index=False)
                first = False
            else:
                chunk.to_csv(f, index=False, header=False)
            total_rows += len(chunk)

print(f"✅ Finished. Total rows written: {total_rows}")
print(f"📄 Output saved to: {output_file}")
