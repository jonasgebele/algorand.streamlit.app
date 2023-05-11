import pandas as pd

# Load the csv file
df = pd.read_csv("./data/responses_27410001.csv")

# Rename the required columns and delete unnecessary ones
df.rename(columns={'Binance_ALGOUSDT': 'Binance_ALGOUSDT', 'round:': 'round'}, inplace=True)
df = df.drop(df.columns[df.columns.str.contains('round:',case=False)], axis=1)

# Identify the market columns and rename them
cols = df.columns.tolist()
new_cols = []
i = 0
while i < len(cols):
    col = cols[i]
    if "pool_size_X" in col or "pool_size_Y" in col:
        market = new_cols[-1].split("_")[0] + "_" + new_cols[-1].split("_")[1] # Assuming market names are always the first two parts when split by "_"
        if "pool_size_X" in col:
            new_cols.append(f"{market}_[ALGO]")
        else: # "pool_size_Y" in col
            new_cols.append(f"{market}_[USDC]")
        i += 1
    else:
        new_cols.append(col)
        i += 1

# Replace the old columns with the new ones
df.columns = new_cols

# Drop columns that don't have "[" or "]" in their name, except the first three
df = df[['timestamp', 'Binance_ALGOUSDT', 'round'] + [col for col in df.columns[3:] if '[' in col or ']' in col]]

# Save the new DataFrame to a csv file
df.to_csv("./data/responses_27410001_new2.csv", index=False)