import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
from matplotlib.patches import Wedge
import seaborn as sns

class WeatherDataVisualizer:
    def __init__(self):
        # 设置图片清晰度
        plt.rcParams['figure.dpi'] = 300
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        self.data = self.generate_data()

    def generate_data(self):
        # 原始数据（前5行）
        data = pd.DataFrame({
            '小时': [7, 6, 5, 4, 3],
            '温度': [28.0, 27.0, 26.9, 26.7, 27.2],
            '风力方向': ['东北风', '东北风', '东北风', '东北风', '东北风'],
            '风级': [3, 4, 3, 3, 3],
            '降水量': [0.0, 0.0, 0.0, 1.7, 0.2],
            '相对湿度': [86, 92, 93, 95, 91],
            '空气质量': [np.nan, 14.0, 13.0, 13.0, 12.0]
        })

        # 模拟扩展为14天数据（假设每天24小时，简化为每天取4个时间点）
        days = 14
        expanded_data = []
        for day in range(1, days + 1):
            for hour in [3, 9, 15, 21]:  # 每天取4个时间点
                try:
                    row = data.sample(1).copy().iloc[0]
                    # 模拟温度随天数变化（每天温度±1℃波动）
                    temp_fluctuation = np.random.normal(0, 1)
                    row['温度'] = round(row['温度'] + temp_fluctuation, 1)
                    # 模拟风力方向随机变化
                    directions = ['东北风', '东南风', '西南风', '西北风', '东风', '南风', '西风', '北风']
                    row['风力方向'] = np.random.choice(directions)
                    # 模拟风级±1级波动
                    row['风级'] = max(1, min(8, row['风级'] + np.random.randint(-1, 2)))
                    # 模拟降水量随机变化（小概率降雨）
                    if np.random.random() < 0.2:
                        row['降水量'] = round(np.random.uniform(0, 5), 1)
                    else:
                        row['降水量'] = 0.0
                    # 模拟相对湿度±3%波动
                    row['相对湿度'] = max(50, min(100, row['相对湿度'] + np.random.randint(-3, 4)))
                    # 添加日期信息
                    row['日期'] = f'第{day}天'
                    row['小时'] = hour
                    expanded_data.append(row)
                except IndexError:
                    print("数据采样时出现索引错误，请检查数据。")

        return pd.DataFrame(expanded_data)

    def plot_temperature_trend(self):
        """绘制14天高低温变化曲线图"""
        try:
            # 按日期分组，计算每天的最高温和最低温
            daily_temp = self.data.groupby('日期')['温度'].agg(['max', 'min']).reset_index()

            plt.figure(figsize=(10, 6))
            plt.plot(daily_temp['日期'], daily_temp['max'], 'o-', label='最高温', color='#ff6b6b', linewidth=2)
            plt.plot(daily_temp['日期'], daily_temp['min'], 's-', label='最低温', color='#4ecdc4', linewidth=2)

            # 添加网格线
            plt.grid(axis='y', linestyle='--', alpha=0.7)

            # 设置标题和标签
            plt.title('14天高低温变化曲线')
            plt.xlabel('日期')
            plt.ylabel('温度 (℃)')
            plt.xticks(rotation=45, ha='right')

            # 添加图例和装饰
            plt.legend()
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"绘制高低温变化曲线图时出现错误: {e}")

    def plot_wind_radar(self):
        """绘制风向风级雷达图（按风向分组计算平均风级）"""
        try:
            # 按风向分组，计算平均风级
            wind_data = self.data.groupby('风力方向')['风级'].mean().sort_values(ascending=False)

            # 雷达图角度设置
            directions = wind_data.index.tolist()
            N = len(directions)
            angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
            angles += angles[:1]  # 闭合图形

            # 风级数据闭合
            values = wind_data.values.tolist()
            values += values[:1]

            # 绘制雷达图
            fig = plt.figure(figsize=(8, 8))
            ax = fig.add_subplot(111, polar=True)
            ax.plot(angles, values, 'o-', linewidth=2, color='#3a5a78')
            ax.fill(angles, values, alpha=0.25, color='#3a5a78')

            # 设置标签
            ax.set_thetagrids(np.degrees(angles[:-1]), directions)
            plt.title('各风向平均风级雷达图')

            # 添加网格线
            ax.grid(True)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"绘制风向风级雷达图时出现错误: {e}")

    def plot_weather_distribution(self):
        """绘制气候分布饼图"""
        try:
            # 定义气候分类标准
            def classify_weather(rainfall):
                if rainfall == 0:
                    return '无雨'
                elif 0 < rainfall <= 1:
                    return '小雨'
                elif 1 < rainfall <= 5:
                    return '中雨'
                else:
                    return '大雨'

            # 分类气候
            self.data['气候类型'] = self.data['降水量'].apply(classify_weather)
            weather_counts = self.data['气候类型'].value_counts()

            # 绘制饼图
            plt.figure(figsize=(8, 8))
            colors = ['#4CAF50', '#FFC107', '#FF9800', '#F44336']  # 绿色-无雨，黄色-小雨，橙色-中雨，红色-大雨

            # 绘制带缺口的饼图（环形图）
            total = weather_counts.sum()
            wedges = []
            start_angle = 0
            for i, (weather, count) in enumerate(weather_counts.items()):
                angle = 360 * (count / total)
                wedge = Wedge((0, 0), 0.8, start_angle, start_angle + angle,
                              facecolor=colors[i], edgecolor='white', linewidth=1,
                              alpha=0.8)
                wedges.append(wedge)
                start_angle += angle

            # 添加到图表
            ax = plt.gca()
            for wedge in wedges:
                ax.add_patch(wedge)

            # 添加标签
            plt.title('14天气候类型分布')
            plt.axis('equal')  # 保证饼图是圆形

            # 添加图例和百分比标签
            patches = [Wedge((0, 0), 0.1, 0, 360, facecolor=c, edgecolor='white') for c in colors]
            plt.legend(patches, weather_counts.index, loc='best')

            # 添加百分比文本
            for i, (weather, count) in enumerate(weather_counts.items()):
                percent = f'{(count / total * 100):.1f}%'
                angle = start_angle - angle / 2  # 计算文本位置角度
                x = 0.5 * math.cos(math.radians(angle))
                y = 0.5 * math.sin(math.radians(angle))
                plt.text(x, y, percent, ha='center', va='center', fontweight='bold')

            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"绘制气候分布饼图时出现错误: {e}")

    def visualize_all(self):
        self.plot_temperature_trend()
        self.plot_wind_radar()
        self.plot_weather_distribution()

if __name__ == "__main__":
    visualizer = WeatherDataVisualizer()
    visualizer.visualize_all()