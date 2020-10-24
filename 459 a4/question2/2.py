import pandas as pd
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import KFold

attributes = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W'
    ]
attributes_with_label = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'label'
    ]

filename = 'CMPT459DataSetforStudents.xls'
training_df = pd.read_excel(filename, names=attributes_with_label,
                            header=None, sheet_name='Training Data')

clf = DecisionTreeClassifier()
kf = KFold(n_splits=10, shuffle=False)
precision_sum = 0
recall_sum = 0
for training_index, test_index in kf.split(training_df):
    training_data = training_df.drop(training_index)
    test_data = training_df.drop(test_index)
    clf = clf.fit(training_data[attributes], training_data['label'])
    test_predict = clf.predict(test_data[attributes])

    test_actual = test_data['label']
    precision = metrics.precision_score(test_actual, test_predict)
    recall = metrics.recall_score(test_actual, test_predict)
    accuracy = metrics.accuracy_score(test_actual, test_predict)

    print('precision:', precision)
    print('recall:', recall)
    print('accuracy:', accuracy, '\n')
    precision_sum += precision
    recall_sum += recall

avg_precision = precision_sum / 10
avg_recall = recall_sum / 10

print('Overall average precision:', avg_precision)
print('Overall average recall:', avg_recall)
