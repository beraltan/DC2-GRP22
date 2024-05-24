import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('/Users/banana/Documents/GitHub/DC2-GRP22/embedded_data.csv')

# Filter the DataFrame to get the first three rows where 'Borough' is 'Barnet'
barnet_rows = df[df['Borough'] == 'Barnet']

# Check if the 'Borough_embedding' values are the same
all_embeddings_equal = barnet_rows['Borough_embedding'].nunique() == 1

print("The first three rows with 'Barnet' in the 'Borough' column are:")
print(barnet_rows)

if all_embeddings_equal:
    print("The 'Borough_embedding' values are the same for these rows.")
else:
    print("The 'Borough_embedding' values are not the same for these rows.")
