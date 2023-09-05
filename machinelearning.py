from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn import svm, metrics

# Pandas is used for data manipulation
import pandas as pd
# Read in data and display first 5 rows
df = pd.read_csv('datadownload/downloaded_files/_compined_df.csv')
# df.fillna(0, inplace=True)

le_Wind_direction = LabelEncoder()
label_Wind_direction = le_Wind_direction.fit_transform(df['Wind direction'])
df.drop("Wind direction", axis=1, inplace=True)
df["Wind direction"] = label_Wind_direction

le_Condition = LabelEncoder()
label_Condition = le_Condition.fit_transform(df['Condition'])
df.drop("Condition", axis=1, inplace=True)
df["Condition"] = label_Condition

print(type(df))
print(df.head(5))

print('The shape of our features is:', df.shape)

# Descriptive statistics for each column
print(df.describe())

import numpy as np
# Labels are the values we want to predict

train_data_df = df.iloc[: , 1:-1]
flood_labels_df = df.loc[: , "Flood"]

print(train_data_df.head(5))
print(flood_labels_df.head(5))

train_data = np.array(train_data_df)
flood_labels = np.array(flood_labels_df)

feature_list = list(df.columns)

from sklearn.model_selection import train_test_split
# Split the data into training and testing sets
train_features, test_features, train_labels, test_labels = train_test_split(train_data, flood_labels, test_size = 0.2, stratify = flood_labels)

print('Training Features Shape:', train_features.shape)
print('Training Labels Shape:', train_labels.shape)
print('Testing Features Shape:', test_features.shape)
print('Testing Labels Shape:', test_labels.shape)

unique, counts = np.unique(flood_labels, return_counts=True)
print(unique)
print(counts)
unique, counts = np.unique(test_labels, return_counts=True)
print(unique)
print(counts)

print("RF --- start")
# Import the model we are using
from sklearn.ensemble import RandomForestClassifier
# Instantiate model with 1000 decision trees
rf = RandomForestClassifier(n_estimators = 4)
# Train the model on training data
rf.fit(train_features, train_labels)

# Use the forest's predict method on the test data
predictions = rf.predict(test_features)
# print(test_features)
# Calculate the absolute errors
errors = abs(predictions - test_labels)
# Print out the mean absolute error (mae)
print('RF Mean Absolute Error:', np.mean(errors), '%.')
print("RF Accuracy:",metrics.accuracy_score(test_labels, predictions))
print("RF Precision:",metrics.precision_score(test_labels, predictions,average='micro'))
print("RF Recall:",metrics.recall_score(test_labels, predictions,average='micro'))
# import pickle
# pickle.dump(rf, open("RandomForestModel.sav", 'wb'))
# loaded_model = pickle.load(open("RandomForestModel.sav", 'rb'))

conf_mat = confusion_matrix(test_labels, predictions)
print(conf_mat)


print("RF --- end")