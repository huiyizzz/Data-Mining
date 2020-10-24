import pandas as pd
import matplotlib.pyplot as plt
from _kmeans import KMeans

filename = 'training.csv'
training_df = pd.read_csv(filename)

cluster = KMeans(n_init=1, n_clusters=10, max_iter=100, verbose=True)
cluster = cluster.fit(training_df.iloc[:, 1:])
SSE_list = cluster.SSE
iteration = list(range(0, len(SSE_list)))

plt.figure(1)
plt.plot(iteration, SSE_list, '-', color='firebrick')
plt.xlabel('Iteration')
plt.ylabel('Sum of Squared Errors')
plt.title('The Plot of Training Data')
plt.show()
