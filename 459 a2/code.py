import csv
import pandas as pd
import copy

dimension = ['Allocation Subcategory', 'City', 'College',
             'Gift Allocation', 'Major', 'State']
output = []
total = ['*', '*', '*', '*', '*', '*']
combination = [[total], [], [], [], [], [], []]
recorded_amount = []
count = 0

f = open('result.txt', 'w')
f.close()


def dimen(item):
    count = 0
    for dim in item:
        if dim == '*':
            count += 1
    count = 6 - count

    return count


def convertToCSV(file_name):
    xls = pd.read_excel(file_name)
    xls.to_csv('data.csv', index=0)
    csv = pd.read_csv('data.csv')
    csv.drop(['Gift Date', 'Prospect ID'], axis=1, inplace=True)
    csv = csv[['Allocation Subcategory', 'City', 'College',
               'Gift Allocation', 'Major', 'State', 'Gift Amount']]
    csv.to_csv('data.csv', index=0)


def load_data(file_name):
    data_output = []
    with open(file_name, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            data_output.append(row)

    return data_output


def isChild(a, b):
    flag = True
    for i in range(0, 6):
        if b[i] == '*':
            continue
        if b[i] != a[i]:
            flag = False
            break

    return flag


def get_amount(input_item, data_set):
    amount = 0.0
    for data in data_set:
        if isChild(data, input_item[:6]):
            amount = amount + float(data[6])

    return amount


def get_data_by_input(data_set_item, a):
    output_data = []
    if isChild(data_set_item, a):
        for i in range(0, 6):
            temp = copy.deepcopy(a)
            if a[i] == data_set_item[i]:
                continue
            if a[i] == '*':
                temp[i] = data_set_item[i]
                output_data.append(temp)

    return output_data


def accessAmount(item):
    for record in recorded_amount:
        if item == record[:6]:
            return float(record[6])
    new = copy.deepcopy(item)
    amount = get_amount(item, data_set)
    new.append(str(amount))
    recorded_amount.append(new)
    return amount


def get_next_data_layer(data_set, input_data, dim):
    final_level_output = copy.deepcopy(input_data)
    if dim == 1:

        for b in range(len(data_set)):
            layer_data = get_data_by_input(data_set[b][:6], total)
            for c in range(len(layer_data)):
                if layer_data[c] not in final_level_output:
                    final_level_output.append(layer_data[c])
                    combination[1].append(layer_data[c])
    else:
        for a in range(len(input_data)):
            if dimen(input_data[a]) == dim - 1:
                for b in range(len(data_set)):
                    layer_data = get_data_by_input(data_set[b][:6],
                                                   input_data[a])
                    for c in range(len(layer_data)):
                        if layer_data[c] not in final_level_output:
                            final_level_output.append(layer_data[c])
                            combination[dim].append(layer_data[c])
    return final_level_output


def buc(data_set, input_list, dim):
    if dim <= len(dimension):
        dim = dim + 1
        level_output = get_next_data_layer(data_set, input_list, dim)
        return buc(data_set, level_output, dim)
    else:
        return input_list


convertToCSV('advancement_donations_and_giving_demo.xls')
data_set = load_data('data.csv')

print("Computing...")

buc_output = buc(data_set, [], 0)

for data in data_set:
    for dim in range(7):
        for index in range(len(combination[dim])):
            temp = combination[dim][index]
            if isChild(data[:6], temp):
                if len(temp) == 6:
                    temp.append(data[6])
                else:
                    amount = float(temp[6]) + float(data[6])
                    temp[6] = str(amount)

for dim in range(6):
    for parent in combination[dim]:
        for child in combination[dim+1]:
            if isChild(child, parent):
                if float(parent[6]) >= 3*float(child[6]):
                    pair = []
                    pair.append(parent)
                    pair.append(child)
                    output.append(pair)

print("Computing Finished")
print("The total number of pairs that t.SUM()>=3*t'.SUM() is", len(output))

print("Writing to file...")
with open('result.txt', 'a+') as f:
        for pair in output:
            f.write('(('+str(','.join(pair[0][:6]))+'),')
            f.write('('+str(','.join(pair[1][:6]))+'))'+'\n')
print("Done")
