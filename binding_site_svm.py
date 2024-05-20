import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score

# Prepare your lists
list1 = [[1, 2], [2, 3], [3, 4], [4, 5]]  # Class 0
list2 = [[5, 6], [6, 7], [7, 8], [8, 9]]  # Class 1

# Combine the lists and create labels
X = np.array(list1 + list2)
y = np.array([0] * len(list1) + [1] * len(list2))

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train the SVM model
clf = SVC(kernel='linear')  # You can use 'linear', 'poly', 'rbf', 'sigmoid', etc.
clf.fit(X_train, y_train)

# Make predictions
y_pred = clf.predict(X_test)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
