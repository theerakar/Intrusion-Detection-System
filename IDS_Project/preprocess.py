import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load the combined data
df = pd.read_csv("all_traffic_data.csv")

# Identify and fix any column names with spaces
df.columns = df.columns.str.strip()

# Some columns can contain 'inf' values, which are not handled by ML modules
# We replace them with NaN and then drop those rows.
df.replace([float('inf')], pd.NA, inplace=True)
df.dropna(inplace=True)

# Convert the 'Label' column (our target variable) from text to numbers.
# We'll map 'BENIGN' to 0 and all other labels (attacks) to 1.
# That makes it a binary classification problem ( normal vs attack )
label_encoder = LabelEncoder()
df["Label_encoded"] = label_encoder.fit_transform(df['Label'])

# Display the unique attack types and their new encode values
print("Unique attack types and their corresponding integer labels:")
for i, label in enumerate(label_encoder.classes_):
    print(f"Label: {label} -> Encoded as: {i}")

# Show the first 5 rows with the new encoded label
print("\nFirst 5 rows of the preprocessed data with the new encoded label:")
print(df[['Label', 'Label_encoded']].head())

# Save the preprocessed data to a new CSV file
df.to_csv("preprocessed_data.csv", index=False)