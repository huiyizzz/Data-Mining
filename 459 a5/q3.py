import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

filename = 'training.csv'
training_df = pd.read_csv(filename)

k_clusters = [10, 20, 30, 50]
avg_purity = []
for k in k_clusters:
    cluster = KMeans(n_init=10, n_clusters=k, max_iter=100)
    cluster = cluster.fit(training_df.iloc[:, 1:])

    label = cluster.labels_
    clusters = [[] for i in range(k)]
    for i in range(0, len(label)):
        clusters[label[i]] += training_df['class'][i]

    sum_purity = 0
    for i in range(k):
        x = len(clusters[i])
        y = 0
        for class_label in clusters[i]:
            if class_label == 'w':
                y += 1
        sum_purity += max(y, x-y) / x

    avg_purity.append(sum_purity / k)

for i in range(4):
    print('k =', k_clusters[i], end=', ')
    print('Average purity:', avg_purity[i])

plt.figure(1)
plt.plot(k_clusters, avg_purity, '*-', color='firebrick')
plt.xlabel('k')
plt.ylabel('Average Purity')
plt.title('The Plot of Training Data')
plt.show()
