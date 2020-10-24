import pandas as pd
from sklearn import metrics
from sklearn.neural_network import MLPClassifier

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
test_df = pd.read_excel(filename, names=attributes, header=None,
                        sheet_name='Test data')

training_label_0 = training_df[training_df['label'] == 0]
training_label_1 = training_df[training_df['label'] == 1]

fisher_score = {}
for attribute in attributes:
    mean = training_df[attribute].mean()
    mean_label_0 = training_label_0[attribute].mean()
    mean_label_1 = training_label_1[attribute].mean()
    var_label_0 = training_label_0[attribute].var()
    var_label_1 = training_label_1[attribute].var()

    numerator = len(training_label_0) * pow(mean_label_0-mean, 2)
    numerator += len(training_label_1) * pow(mean_label_1-mean, 2)
    denominator = len(training_label_0) * pow(var_label_0, 2)
    denominator += len(training_label_1) * pow(var_label_1, 2)

    fisher_score[attribute] = numerator / denominator

score_list = sorted(fisher_score.items(), key=lambda x: x[1], reverse=True)
new_order = [attribute[0] for attribute in score_list]

select_feature = new_order[0:6]
clf = MLPClassifier(max_iter=500)
clf = clf.fit(training_df[select_feature], training_df['label'])
test_predict = clf.predict(test_df[select_feature])

f = open('output4.txt', 'w')
with open('output4.txt', 'a+') as f:
    for label in test_predict[0:4999]:
        f.write(str(label) + '\n')
    f.write(str(test_predict[4999]))
print("Done")


