import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import  DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Load the preprocessed data
df = pd.read_csv("preprocessed_data.csv")

# Separate featues (X) and target variable (y)
# We will drop the original 'Label' and the 'Label_encoded'from the features
# so the model doesn't cheat
X = df.drop(columns=['Label', 'Label_encoded'])
y = df['Label_encoded']

# Split the data into a training set and a testing set
# We'll use 80% of the data for training and 20% for testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the Decision Tree Classifier
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Make predictions on the test data
y_pred = model.predict(X_test)

# Evaluate the model's accuracy
accuracy = accuracy_score(y_test, y_pred)

print("Decision Tree Model Trained Successfully!")
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save the trained model to a file
import joblib
joblib.dump(model, 'decision_tree_model.pkl')