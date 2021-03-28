import math
import random
import sys

import matplotlib.pyplot as plt

# 城市坐标范围
M = 1
# 城市数量
n = 10
# 初始化城市坐标
city_x = [0.4 ,0.2439,0.1707,0.2293,0.5171,0.8732,0.6878,0.8488,0.6683,0.6195]
city_y = [0.4439 , 0.1463,0.2293,0.7610,0.9414,0.6536,0.5219,0.3609,0.2536,0.2634]
# 初始化距离矩阵
distance_Citys = [[0 for col in range(10)] for row in range(10)]
# 初始温度，结束温度
t_init = 168.14
t_final = 1e-2
# 温度衰减系数
a = 0.98
# 迭代次数
markovlen = 1000


# 初始化距离矩阵
def initDistanceMatrix():
    for i in range(n):
        for j in range(n):
            x = pow(city_x[i] - city_x[j], 2)
            y = pow(city_y[i] - city_y[j], 2)
            distance_Citys[i][j] = pow(x + y, 0.5)
            #if distance_Citys[i][j] <= 1e-6:
            #   distance_Citys[i][j] = sys.maxsize


# 计算路径距离
def getDistance(path):
    res = 0
    for i in range(n - 1):
        res += distance_Citys[path[i]][path[i + 1]]
    res += distance_Citys[path[n - 1]][path[0]]
    return res


# 在现有路径上采用2变换法，返回新的路径
def getNewPath(cur_path):
    path = cur_path.copy()
    u = random.randint(0, n - 1)
    v = random.randint(1, n)
    path[u, v + 1] = path[v, u - 1, -1]
    return path


def drawPath(best_path):
    x = [0 for col in range(n + 1)]
    y = [0 for col in range(n + 1)]

    for i in range(n):
        x[i] = city_x[best_path[i]]
        y[i] = city_y[best_path[i]]
    x[n] = x[0]
    y[n] = y[0]

    print("最佳路线为：")
    for i, city in enumerate(list(zip(x, y))):
        print(city, end=', ')
        if i % 10 == 9:
            print()

    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.plot(x, y, marker='o', mec='r', mfc='w', label='path')
    plt.legend()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("SA_TSP")
    plt.show()


def SA_TSP():
    # 获取初始距离矩阵
    initDistanceMatrix()
    # 得到初始解
    cur_path = random.sample(range(0, n), n)
    cur_dis = getDistance(cur_path)
    best_path = cur_path
    best_dis = cur_dis
    t = t_init

    while t < t_final:
        for point in range(markovlen):
            new_path = getNewPath(cur_path)
            new_dis = getDistance(new_path)
            delt = new_dis - cur_dis
            if delt <= 0:  # 表示得到优解
                cur_path = new_path
                cur_dis = new_dis
                if best_dis > cur_dis:
                    best_dis = cur_dis
                    best_path = cur_path
            else:  # 得到较差解
                p = math.exp(-delt / t)
                if random.random() < p:  # 接受差解
                    cur_path = new_path
                    cur_dis = new_dis
        t *= a  # 退火
    print("城市数量：{}, 城市坐标范围：{}, 结果距离为：{:.2f}".format(n, M, best_dis))

    drawPath(best_path)


if __name__ == '__main__':
    SA_TSP()