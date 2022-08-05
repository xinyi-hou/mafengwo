import random
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt
from  matplotlib.colors import rgb2hex

#选择初始均值向量
def selectInitMeanVec(Data,k):
    # range() 创建整数列表 range(10) [0,1,...,9]  range(1,11) [1,2,...,10]
    # random.sample 从range(m)中随机获取3个元素，作为一个数组返回
    # 随机选取0~m-1 中的三个整数，作为初始的三个聚类中心
    indexInitMeanVec = random.sample(range(m),k)
    initMeanVec = Data[indexInitMeanVec,:]
    return initMeanVec

#计算距离并归入簇中
def calcDistance(Data,k,MeanVec):
    Dist = np.zeros((k,1)) # [[0.],[0.],...,[0.]]  中间k个[0.] 临时变量，用来存储其他节点距离k个聚类中心的距离
    Label = np.zeros((m,1)) # 样本共m个，记录每个样本所属的聚类中心
    for i in range(m):
        for j in range(k):
            a = Data[i,:]-MeanVec[j,:]
            Dist[j] = np.sqrt(sum(a**2))
        Label[i] = np.argmin(Dist) # np.argmin 最小值在数组中的索引，记录每个样本所属的聚类中心索引
    return Label

#更新均值向量
def updateMeanVec(Data,Label,k,oldMeanVec):
    newMeanVec = np.zeros((k,n)) # n数据的列数 新的中心向量
    numSamples = np.zeros((k,1),dtype = int) # 记录每个类的样本数
    for i in range(k):
        num = 0
        D = np.zeros((k,0))
        for j in range(m):
            if Label[j] == i:
                D = np.append(D,Data[j,:])
                num += 1
        numSamples[i] = num
        # 对D中的数据重新排列为(a*b)的格式，满足a*b=D矩阵的行列乘积，默认从D中的行开始重新排列
        # 如果D是整型矩阵，则a、b其中一个可以为-1，按照另一个的大小自动计算
        D = np.reshape(D,(-1,n))
        # axis=0，计算每一列的均值
        newMeanVec[i,:] = np.mean(D,axis=0)
        #如果本次更新后某一簇中无样本，取上一次均值向量为本次均值向量
        if num == 0:
            newMeanVec[i,:] = oldMeanVec[i,:]
    return newMeanVec,numSamples

if __name__ == '__main__':

    # np.loadtxt 读取文件 并以矩阵形式输出
    data = np.loadtxt("./data/liaoning.txt",delimiter=',')[:,[2,1]] # 所有行中第4列和第3列的数据 经度、纬度
    Data = preprocessing.scale(data)
    k = 20
    global m,n
    m,n = Data.shape
    initMeanVec = selectInitMeanVec(Data,k) # 随机选取初始的k个向量，作为初始聚类中心
    oldMeanVec = initMeanVec.copy()
    Label = calcDistance(Data,k,initMeanVec) # 计算每个样本所属的聚类中心
    for i in range(20):
        newMeanVec,numSamples = updateMeanVec(Data,Label,k,oldMeanVec) # 新的聚类中心向量 每个类的样本数
        oldMeanVec = newMeanVec.copy()
        Label = calcDistance(Data,k,newMeanVec)
        print('---第%d轮迭代完成'%(i+1))
    # print(Label)
    # print(numSamples)

    # colors = ['or', 'ob', 'og', 'oc', 'oy', 'om', 'ok', 'sr', 'sb', 'sg']
    for temp in range(5):
        colors = tuple([(np.random.random(), np.random.random(), np.random.random()) for i in range(k)])
        colors = [rgb2hex(x) for x in colors]  # from  matplotlib.colors import  rgb2hex
        print(colors)
        # 这里'or'代表中的'o'代表画圈，'r'代表颜色为红色，后面的依次类推
        i = 0
        for item in Label:
            plt.plot(data[i, 0], data[i, 1], color=colors[int(item[0])], marker='o', markersize=2)
            # plt.plot(data[i, 0], data[i, 1], color="black", marker='o', markersize=2)
            i += 1
        plt.show()


