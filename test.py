import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
data = np.random.rand(100, 2)
#生成一个随机数据，样本大小为100, 特征数为2（这里因为要画二维图，所以就将特征设为2，至于三维怎么画？
#后续看有没有机会研究，当然你也可以试着降维到2维画图也行）
estimator = KMeans(n_clusters=3)#构造聚类器，构造一个聚类数为3的聚类器
estimator.fit(data)#聚类
label_pred = estimator.labels_ #获取聚类标签
centroids = estimator.cluster_centers_ #获取聚类中心
inertia = estimator.inertia_ # 获取聚类准则的总和

print(label_pred)
print(data)

mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
#这里'or'代表中的'o'代表画圈，'r'代表颜色为红色，后面的依次类推
color = 0
j = 0
for i in label_pred:
    plt.plot(data[j,0], data[j,1], mark[i], markersize = 5)
    j +=1
plt.show()
