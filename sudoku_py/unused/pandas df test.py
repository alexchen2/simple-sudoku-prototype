import pandas as pd
import numpy as np

test = [[(i+j) for i in range(1, 10)] for j in range(9)]
test2 = [[{i for i in range(1, 10)} for j in range(9)] for j in range(9)]

df = pd.DataFrame(test)
df2 = pd.DataFrame(test2)

print(df)

for col in df.iterrows():        # Gives three elem. tuple (row#, row as pd.series (col = indices), type metadata)
    for tiles in col[1].items(): # Gives tuple pairs (col#, value)
        print(f"({col[0]}, {tiles[0]}):", tiles[1])

print(df2)

test2 = df.to_numpy()
for i in test2:
    for j in i:
        print(j)



