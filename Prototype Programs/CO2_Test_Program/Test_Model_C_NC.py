import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Define the input data
X = np.array([
    [483.3636364, 568.5454545, 501.3636364, 469.8181818, 450.8181818, 405.1818182, 404.2727273, 406.3636364, 404.7272727, 404.8181818, 580.8181818, 472.1818182, 700.4545455, 572, 553.6363636, 1168.636364, 1263.454545, 938.0909091, 900, 849.4545455, 587.1818182, 477.0909091, 443.3636364, 450.7272727, 401, 404.9090909, 406.1818182, 408.1818182, 405.2727273, 407, 404.0909091, 405.0909091, 404, 406.8181818, 405.7272727]
]).T

# Define the output data (target variable)
y = np.array(['NC', 'NC', 'NC', 'NC', 'NC', 'NC', 'NC', 'NC', 'NC', 'NC', 'NC', 'NC', 'NC', 'NC', 'NC', 'NC', 'NC', 'NC', 'NC', 'NC', 'Coffee', 'Coffee', 'Coffee', 'Coffee', 'Coffee', 'NC', 'NC', 'NC', 'NC', 'NC', 'NC', 'NC', 'NC', 'NC', 'NC'])

# Split the data into training and validation sets
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict the output for the whole dataset
y_pred = model.predict(X)

accuracy = model.score(X_valid, y_valid)
print('Validation accuracy:', accuracy)

# Find the unique predicted values and their range
unique_values = np.unique(y_pred)
for value in unique_values:
    print('Bounding data for', value)
    print('Minimum value:', np.min(X[y_pred == value]))
    print('Maximum value:', np.max(X[y_pred == value]))
