import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Define the input data
X = np.array([
[530.6701299, 532.0614973, 530.9559229, 531.8806818, 533.8826979, 536.6515152, 541.184953, 546.0746753, 551.2491582, 556.8846154, 562.9672727, 562.2234848, 566.1383399, 560.0330579, 559.4632035, 559.7545455, 527.708134, 486.8333333, 460.2887701, 454.1306818, 427.7757576, 416.3896104, 411.7202797, 409.0833333, 405.2975207, 405.7272727, 405.8181818, 405.7727273, 405.4285714, 405.4545455, 405.1454545, 405.4090909, 405.5151515, 406.2727273, 405.7272727]
]).T

# Define the output data (target variable)
y = np.array(['Tea', 'Tea', 'Tea', 'Tea', 'Tea', 'Coke', 'Coke', 'Coke', 'Coke', 'Coke', 'Boiling', 'Boiling', 'Boiling', 'Boiling', 'Boiling', 'Beer', 'Beer', 'Beer', 'Beer', 'Beer', 'Coffee', 'Coffee', 'Coffee', 'Coffee', 'Coffee', 'Open Air', 'Open Air', 'Open Air', 'Open Air', 'Open Air', 'Room Temp Water', 'Room Temp Water', 'Room Temp Water', 'Room Temp Water', 'Room Temp Water'])

# Split the data into training and validation sets
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Test the model on the validation set
accuracy = model.score(X_valid, y_valid)
print('Validation accuracy:', accuracy)
