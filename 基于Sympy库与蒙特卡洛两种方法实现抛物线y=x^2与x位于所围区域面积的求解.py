import sympy as sp
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # 使用 TkAgg 后端

# 方法1 --> 使用 Sympy 库计算精确面积
x = sp.Symbol('x')  # 定义变量x
y = x**2  # 创建函数
ans_s = sp.integrate(y, (x, 0, 1))  # 计算面积--调用积分函数
print("%s函数与x从0到1所围区间的精确面积是%s" % (str(y), str(ans_s)))

# 美化坐标轴
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['bottom'].set_position(('data', 0))
ax.spines['left'].set_position(('data', 0))
x = np.arange(-3.5, 3.5, 0.1)
y = x**2
plt.plot(x, y)
# 将0到1范围下的区域标注
plt.fill_between(x, y, color="skyblue", where=np.logical_and(x >= 0, x <= 1))
plt.show()


# 方法2 --> 蒙特卡洛方法
n = 1  # 采样点数初始化
k = 0  # 落入曲线指定范围下的点数初始化
j = 0  # 循环计数器初始化
ans = 0  # 估算面积值
ans_new = 0  # 平均后的估算面积值
y_num = []  # 存储每次计算的估算面积
n_values = []  # 用于记录每次计算时的n值
max_trials = 10000  # 最大循环次数限制
final_num = 0
final = 0
while j < max_trials:
    k = 0  # 初始化
    for _ in range(n):
        # 随机生成点的坐标
        x_val, y_val = random.uniform(0, 1), random.uniform(0, 1)
        # 判断点是否落在曲线下方,若成立则计数器加1
        if y_val <= x_val**2:
            k += 1
    ans = k / n  # 计算当前估算面积

    y_num.append(ans)  # 记录当前估算值
    n_values.append(n)  # 记录当前采样点数

    # 每 10 次计算平滑一次结果
    if len(y_num) >= 10:
        ans_new = np.mean(y_num[-10:])  # 取最近 10 次的均值

    # 判断估算值是否收敛到精确值附近
    if abs(ans_new - ans_s) <= 0.05:
        final = ans_new  # 保存最终的估算值
        final_num = n   # 保存最终使用的采样点数
        break
    else:
        n += 50  # 每次循环增加采样点数
        j += 1  # 循环计数器加 1

    if j == max_trials:
        print("达到了最大试验次数，仍未收敛")
        break

print(f"最少样本点为 {final_num}，估算的面积为 {final:.5f}")

plt.figure(figsize=(10, 6))
plt.plot(n_values, y_num)
plt.axhline(float(ans_s), color="red", linestyle="--",
            label="Exact Value (Sympy)")
plt.title("Monte Carlo Method: Evaluate Area")
plt.xlabel("n")
plt.ylabel("S_Evaluate")
plt.show()
