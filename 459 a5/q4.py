import pandas as pd
import matplotlib.pyplot as plt
from _kmeans import KMeans

training_filename = 'training.csv'
test_filename = 'testing.csv'
training_df = pd.read_csv(training_filename)
test_df = pd.read_csv(test_filename)

k_clusters = list(range(10, 31))
SSD_list = []
for k in k_clusters:
    cluster = KMeans(n_init=10, n_clusters=k)
    cluster = cluster.fit(training_df.iloc[:, 1:])
    SSD = cluster.predict(test_df.iloc[:, 1:])[1]
    SSD_list.append(SSD)
    print('k =', k, end=', ')
    print('SSD:', SSD)

k = k_clusters[SSD_list.index(min(SSD_list))]
print('The best value of k is', k)

plt.figure(1)
plt.plot(k_clusters, SSD_list, '*-', color='firebrick')
plt.xlabel('k')
plt.ylabel('Sum of Squared Distances')
plt.title('The Plot of Testing Data')
plt.xticks(range(10, 31))
plt.show()
