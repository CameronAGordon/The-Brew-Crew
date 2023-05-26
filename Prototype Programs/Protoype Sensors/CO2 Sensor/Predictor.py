import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Load the trained model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Load the CSV file containing liquid measurements
data = pd.read_csv('Beer_3.csv')

# Get the last 10 measurements from the second column as a NumPy array
X = data.iloc[-10:, 1].values.reshape(-1, 1)

# Make predictions on the data
y_pred = model.predict(X)

# Print the predicted liquid for each measurement
for liquid in y_pred:
    print(liquid)
