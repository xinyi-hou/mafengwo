import numpy as np

if __name__ == '__main__':
    #数据格式转换
    fr = open("./data/辽宁省.txt", 'r', encoding='UTF-8')
    frw = open("./data/liaoning.txt", 'w')

    line = fr.readlines()
    for L in line:
        string = L.strip("\n").split(",")
        a = np.float64(string[0])
        b = np.float64(string[4])
        c = np.float64(string[5])

        str = '%f,%f,%f\n' % (a, b, c)
        print(str)
        frw.write(str)
    frw.close()
    fr.close()