#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Model for Real-Time Social Network Data Mining For Predicting The Path For A Disaster

# This Model is tested on Alabama Tornado (October 2014) tweets 

import numpy as np
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score


# X contains position of tweet and time  

X = X[['lat', 'lon', 'time']]
X = StandardScaler().fit_transform(X)


# Density-Based Spatial Clustering of Applications with Noise (DBSCAN) Clustering of locations to further filter the data points to reduce noise from data points

# On experimentation, it was found that the best number of clusters to obtain is 3 where the cluster with minimum number of samples can be removed.
#This was obtained by keeping the min_samples value as 160 and eps = 2.8.


db = DBSCAN(eps=2.8, min_samples=160).fit(X) 
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# lat_X_train contains all latitudes other than those classified as noise by DBSCAN
# lon_X_train contains all longitudes other than those classified as noise by DBSCAN


lat_X_train = []
long_X_train = []



for i in labels:
    if i != -1:
        df = df[['lat','lon']]
        
        

#core_sample_indices_ : array, shape = [n_core_samples]

#    Indices of core samples.
#components_ : array, shape = [n_core_samples, n_features]

#    Copy of each core sample found by training.
#labels_ : array, shape = [n_samples]

#   Cluster labels for each point in the dataset given to fit(). Noisy samples are given the label -1.






# Number of clusters in labels, ignoring noise if present.

n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print('Estimated number of clusters: %d' % n_clusters_)
print('Estimated number of noise points: %d' % n_noise_)
print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
print("Adjusted Rand Index: %0.3f"
      % metrics.adjusted_rand_score(labels_true, labels))
print("Adjusted Mutual Information: %0.3f"
      % metrics.adjusted_mutual_info_score(labels_true, labels))
print("Silhouette Coefficient: %0.3f"
      % metrics.silhouette_score(X, labels))

# It was experimented with linear regression and non-linear regression with degrees two, three and four. 
#Higher degrees were also tried but they did not change the curve significantly. 
# It was found that Linear Regression gives the best result.
#The points were also assigned weights depending upon its frequency. But that did not bring much changes and therefore, the results were found without weights.

X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.2)

# Create linear regression object
regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(X_train, y_train)

# Make predictions using the testing set
y_pred = regr.predict(X_test)


# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean squared error
print("Mean squared error: %.2f"
      % mean_squared_error(y_test, y_pred))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % r2_score(y_test, y_pred))

# Coefficients with 95% confidence bounds
# for latitude
# p1 lower = 2.646       p2 lower =-1.68e+05 
# p1 exact = 3.323       p2 exact =-1.39e+05
# p1 upper = 3.999       p2 upper =-1.11e+05
# sse = 1.86e+04     R-square = 0.04176    Adjusted R-square = 0.04131       RMSE = 2.953


# for longitude
# p1 lower = 0.009029       p2 lower =-88.2
# p1 exact = 0.1594         p2 exact =-88.05
# p1 upper = 0.3099         p2 upper =--87.9
# sse = 2.66ee+04     R-square = 0.002028   Adjusted R-square = 0.001558       RMSE = 3.538

# where p1 and p2 are the coefficients for the linear polynomial equation



# list contain location of disaster as predicted by model at particular time
res = [lon_y_pred,lat_y_pre]


# In[ ]:




