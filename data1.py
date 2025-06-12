import matplotlib.pyplot as plt
import numpy as np

# 示例数据 - 请替换为当天的实际温度和湿度数据
# 温度数据（单位：°C）
temperature = [22, 23, 24, 25, 26, 27, 28, 29, 30, 29, 28, 27]
# 湿度数据（单位：%）
humidity = [60, 58, 55, 52, 50, 48, 45, 42, 40, 43, 46, 49]

# 设置图片清晰度
plt.rcParams['figure.dpi'] = 300

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']

# 创建画布
plt.figure(figsize=(10, 6))

# 绘制散点图
scatter = plt.scatter(temperature, humidity, s=100, c='skyblue', edgecolor='k', alpha=0.7)

# 添加标题和坐标轴标签
plt.title('当天温湿度相关性分析散点图')
plt.xlabel('温度 (°C)')
plt.ylabel('湿度 (%)')

# 设置x轴刻度
plt.xticks(np.arange(min(temperature), max(temperature) + 1, 1))

# 添加网格线
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 去掉左右上三边的边框
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['left'].set_visible(False)

# 添加数据点标注（可选）
for i, (temp, hum) in enumerate(zip(temperature, humidity)):
    plt.annotate(f'({temp}, {hum})', (temp, hum), xytext=(5, 5),
                 textcoords='offset points')

# 显示图形
plt.show()

# 示例数据 - 请替换为当天的实际风向和风级数据
# 风向数据（用角度表示，0°为北风，90°为东风，180°为南风，270°为西风）
wind_directions = [0, 45, 90, 135, 180, 225, 270, 315]
# 风级数据（0-12级）
wind_speeds = [2, 3, 4, 3, 2, 1, 2, 3]

# 设置图片清晰度
plt.rcParams['figure.dpi'] = 300

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']

# 将风向角度转换为弧度（雷达图需要弧度）
angles = np.deg2rad(wind_directions)

# 闭合雷达图（使起点和终点相连）
angles = np.concatenate((angles, [angles[0]]))
wind_speeds = np.concatenate((wind_speeds, [wind_speeds[0]]))

# 定义风向标签
wind_labels = ['北', '东北', '东', '东南', '南', '西南', '西', '西北', '北']

# 创建画布
plt.figure(figsize=(10, 8))

# 创建极坐标子图
ax = plt.subplot(111, polar=True)

# 绘制雷达图
ax.plot(angles, wind_speeds, 'o-', linewidth=2, color='navy')
ax.fill(angles, wind_speeds, alpha=0.25, color='navy')


# 添加标题
plt.title('当天风向风级雷达图')

# 设置风级刻度
ax.set_ylim(0, max(wind_speeds) + 1)
ax.set_yticks(range(0, max(wind_speeds) + 2))
ax.set_yticklabels([f'{i}级' for i in range(0, max(wind_speeds) + 2)])

# 添加网格线
ax.grid(True)

# 显示图形
plt.show()