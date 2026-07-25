import sys

import pandas as pd
print('arguments', sys.argv)

month = int(sys.argv[1])

df = pd.DataFrame({"Day": [1, 2], "Num_Passengers": [3, 4]})
df["Month"] = month
print(df.head())

df.to_parquet

print(f"Hello pipeline, month={month}") 