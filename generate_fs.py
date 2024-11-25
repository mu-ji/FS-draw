import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import pygame
import numpy as np
import time
from matplotlib.animation import FuncAnimation


# 打开并读取文件
with open('trajectory.txt', 'r', encoding='utf-8') as file:
    content = file.read()
    print(type(content))

content = content.split('\n')

trajectory_length = len(content)-1

trajectory_x = np.zeros(trajectory_length)
trajectory_y = np.zeros(trajectory_length)


for i in range(trajectory_length):
    x = int(content[i].split(' ')[0][:-1])
    y = int(content[i].split(' ')[1])
    trajectory_x[i] = x
    trajectory_y[i] = y

#data['x'] = data['x'] - (data['x'].max() + data['x'].min()) / 2
#data['x'] = data['x'] / data['x'].max()
#data['y'] = -data['y'] + (data['y'].max() + data['y'].min()) / 2
#data['y'] = data['y'] / data['y'].max()

#generate a smooth curve
#theta = np.linspace(0, 2 * np.pi, trajectory_length)

# 计算单位圆的 x 和 y 坐标
#trajectory_x = np.cos(theta)
#trajectory_y = np.sin(theta)


trajectory_x = trajectory_x - (trajectory_x.max() + trajectory_x.min())/2
trajectory_x = trajectory_x/trajectory_x.max()
trajectory_y = trajectory_y - (trajectory_y.max() + trajectory_y.min())/2
trajectory_y = -trajectory_y/trajectory_y.max()

plt.plot(trajectory_x, trajectory_y)
plt.show()

t = np.linspace(0, 2*np.pi, trajectory_length)

def f_(t, trajectory_x, trajectory_y):
    return trajectory_x[t] + trajectory_y[t]*1j

def simu_interate(t, n):
    sum = 0
    for t_index in range(trajectory_length):
        sum += f_(t_index, trajectory_x, trajectory_y)*np.exp(n*1j*t[t_index]) * (2*np.pi/trajectory_length)
    return sum/(2*np.pi)

positive_coeff_list = []
nagtive_coeff_list = []
num_circle = 50

for i in range(1, num_circle):
    positive_coeff_list.append(simu_interate(t, i))        #cal c1 to cn

for i in range(1, num_circle):
    nagtive_coeff_list.append(simu_interate(t, -i))

#for times in range(len(num_circle)):
c0 = simu_interate(t, 0)

t_index = 0

start_point = c0
end_point = start_point
for coeff_index in range(num_circle-1):
    end_point += positive_coeff_list[coeff_index]*np.exp(-1j*t[t_index]*(coeff_index+1))
    end_point += nagtive_coeff_list[coeff_index]*np.exp(1j*t[t_index]*(coeff_index+1))

    start_point = end_point


plt.scatter(end_point.real, end_point.imag, marker = '*', s = 100)
plt.plot(trajectory_x, trajectory_y)
plt.show()



# 创建图形和坐标轴
fig, ax = plt.subplots()

trajectory_endpoint_x_list = []
trajectory_endpoint_y_list = []
# 更新函数
def update(frame):
    # 清除当前的图形
    ax.clear()
    t_index = frame
    print(t_index)
    ax.plot(trajectory_x, trajectory_y, linestyle = '--', label = 'Pattern drawn by FS')
    start_point = c0
    end_point = start_point
    for coeff_index in range(num_circle-1):
        end_point = start_point + positive_coeff_list[coeff_index]*np.exp(-1j*t[t_index]*(coeff_index+1))
        ax.plot([start_point.real, end_point.real], [start_point.imag, end_point.imag])
        start_point = end_point

        end_point = start_point + nagtive_coeff_list[coeff_index]*np.exp(1j*t[t_index]*(coeff_index+1))
        ax.plot([start_point.real, end_point.real], [start_point.imag, end_point.imag])
        start_point = end_point

    trajectory_endpoint_x_list.append(end_point.real)
    trajectory_endpoint_y_list.append(end_point.imag)
    ax.plot(trajectory_endpoint_x_list, trajectory_endpoint_y_list, label='Original pattern')
    ax.set_ylim(-1.5, 1.5)  # 重新设置 y 轴范围
    ax.set_xlim(-1.5, 1.5)      # 重新设置 x 轴范围
    ax.set_title('Visualization with n={}'.format(num_circle))
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    plt.legend()

    if t_index == trajectory_length-1:
        plt.savefig('n={}.png'.format(num_circle))

# 创建动画
ani = FuncAnimation(fig, update, frames=np.arange(0, trajectory_length), blit=False, interval=1)

# 显示动画
plt.show()