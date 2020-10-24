import pandas as pd

attributes = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W'
    ]
attributes_with_label = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'label'
    ]


def range_mean_variance(dataset):
    for attribute in attributes:
        attribute_min = dataset[attribute].min()
        attribute_max = dataset[attribute].max()
        attribute_range = [attribute_min, attribute_max]
        attribute_mean = dataset[attribute].mean()
        attribute_var = dataset[attribute].var()
        print('Attribute', attribute, end=': \n')
        print('range:', attribute_range, end=', ')
        print('mean:', attribute_mean, end=', ')
        print('variance:', attribute_var)
    print()


filename = 'CMPT459DataSetforStudents.xls'
training_df = pd.read_excel(filename, names=attributes_with_label,
                            header=None, sheet_name='Training Data')
test_df = pd.read_excel(filename, names=attributes, header=None,
                        sheet_name='Test data')
print('For training data set:')
range_mean_variance(training_df)
print('For test data set:')
range_mean_variance(test_df)

label_count = [0, 0]
for row in training_df['label']:
    if row == 0:
        label_count[0] += 1
    else:
        label_count[1] += 1
print('The total number of class label 0:', label_count[0])
print('The total number of class label 1:', label_count[1])
