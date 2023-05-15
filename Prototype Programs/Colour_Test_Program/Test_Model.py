import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Define the input data
X = np.array([
[54.414, 54.55652174, 55.45833333, 54.06272727, 54.794, 62.00187, 68.0408, 60, 59.86166667, 60.105, 66.92052632, 65.838125, 62.37466667, 60, 60.37055556, 63.0795122, 68.85181818, 68.94952381, 63.14571429, 69.16129032]
]).T

# Define the output data (target variable)
y = np.array(['NC', 'NC', 'NC', 'NC', 'NC', 'NC', 'NC', 'NC', 'NC', 'NC', 'Coffee', 'Coffee', 'Coffee', 'Coffee', 'Coffee', 'NC', 'NC', 'NC', 'NC', 'NC'])

# Encode categorical labels to numerical labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Split the data into training and validation sets
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X)

# Test the model on the validation set
accuracy = model.score(X_valid, y_valid)
print('Validation accuracy:', accuracy)

unique_values = np.unique(y_pred)
for value in unique_values:
    print('Bounding data for', label_encoder.inverse_transform([value])[0])
    print('Minimum value:', np.min(X[y_pred == value]))
    print('Maximum value:', np.max(X[y_pred == value]))

