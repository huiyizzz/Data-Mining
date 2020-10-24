import pandas as pd

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
print(score_list)
