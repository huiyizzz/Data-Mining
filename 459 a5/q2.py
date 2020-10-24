import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

filename = 'training.csv'
training_df = pd.read_csv(filename)

k_clusters = [2, 5, 10, 20]
min_SSE = []
for k in k_clusters:
    cluster = KMeans(n_init=10, n_clusters=k, max_iter=100)
    cluster = cluster.fit(training_df.iloc[:, 1:])
    min_SSE.append(cluster.inertia_)

for i in range(4):
    print('k =', k_clusters[i], end=', ')
    print('Minimum SSE:', min_SSE[i])

plt.figure(1)
plt.plot(k_clusters, min_SSE, '*-', color='firebrick')
plt.xlabel('k')
plt.ylabel('Minimum Sum of Squared Errors')
plt.title('The Plot of Training Data')
plt.show()
