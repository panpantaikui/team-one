import requests
from bs4 import BeautifulSoup
import csv
import json


def getHTMLtext(url):
    """请求获取网页内容，包含异常处理"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        print("成功访问网页")
        return r.text
    except Exception as e:
        print(f"访问错误: {e}")
        return ""


def get_content(html):
    """解析7天预报页面，获取当天24小时数据和未来7天数据"""
    final_day = []  # 当天24小时数据
    final_7days = []  # 未来7天数据
    if not html:
        return final_day, final_7days

    try:
        bs = BeautifulSoup(html, "html.parser")
        body = bs.body

        # --------------------- 解析当天24小时数据 ---------------------
        data2 = body.find_all('div', {'class': 'left-div'})
        if len(data2) < 3:
            print("未找到left-div标签")
            return final_day, final_7days

        script_tag = data2[2].find('script')
        if not script_tag:
            print("未找到script标签")
            return final_day, final_7days

        script_text = script_tag.string
        if '=' not in script_text:
            print("脚本中未找到JSON数据标识")
            return final_day, final_7days

        # 提取JSON数据
        json_data = script_text[script_text.index('=') + 1:-2].strip()
        if not json_data:
            print("JSON数据为空")
            return final_day, final_7days

        jd = json.loads(json_data)
        dayone = jd.get('od', {}).get('od2', [])

        count = 0
        for item in dayone:
            if count > 23:
                break
            temp = [
                item.get('od21', '未知'),
                item.get('od22', '未知'),
                item.get('od24', '未知'),
                item.get('od25', '未知'),
                item.get('od26', '未知'),
                item.get('od27', '未知'),
                item.get('od28', '未知')
            ]
            final_day.append(temp)
            count += 1

        # --------------------- 解析未来7天数据 ---------------------
        data = body.find('div', {'id': '7d'})
        if not data:
            print("未找到id=7d的div标签")
            return final_day, final_7days

        ul = data.find('ul')
        if not ul:
            print("未找到ul标签")
            return final_day, final_7days

        li_list = ul.find_all('li')
        if not li_list:
            print("未找到li标签")
            return final_day, final_7days

        i = 0
        for day in li_list:
            if i <= 0 or i >= 8:
                i += 1
                continue

            temp = []
            try:
                # 提取日期
                h1_tag = day.find('h1')
                date = h1_tag.string.split(' ')[0] if h1_tag else "未知日期"

                # 提取天气
                p_tags = day.find_all('p')
                weather = p_tags[0].string if p_tags and len(p_tags) > 0 else "未知天气"

                # 提取最低气温
                tem_low = "未知"
                if len(p_tags) > 1:
                    i_tag = p_tags[1].find('i')
                    tem_low = i_tag.string[:-1] if i_tag else "未知"

                # 提取最高气温
                tem_high = "无"
                if len(p_tags) > 1 and p_tags[1].find('span'):
                    span_tag = p_tags[1].find('span')
                    tem_high = span_tag.string[:-1] if span_tag else "无"

                # 提取风向
                wind_dirs = []
                if len(p_tags) > 2:
                    span_tags = p_tags[2].find_all('span')
                    wind_dirs = [span.get('title', '未知') for span in span_tags]

                # 提取风级
                wind_level = 0
                if len(p_tags) > 2:
                    i_tag = p_tags[2].find('i')
                    wind_text = i_tag.string if i_tag else "0级"
                    if '级' in wind_text:
                        wind_level = int(wind_text[wind_text.index('级') - 1])

                temp.extend([date, weather, tem_low, tem_high] + wind_dirs + [wind_level])
                final_7days.append(temp)
            except Exception as e:
                print(f"第{i}天数据解析错误: {e}")
            i += 1

    except Exception as e:
        print(f"7天预报解析整体错误: {e}")

    return final_day, final_7days


def get_content2(html):
    """解析15天预报页面，获取第8-14天数据"""
    final_8_14days = []
    if not html:
        return final_8_14days

    try:
        bs = BeautifulSoup(html, "html.parser")
        body = bs.body
        data = body.find('div', {'id': '15d'})
        if not data:
            print("未找到id=15d的div标签")
            return final_8_14days

        ul = data.find('ul')
        if not ul:
            print("未找到ul标签")
            return final_8_14days

        li_list = ul.find_all('li')
        if not li_list:
            print("未找到li标签")
            return final_8_14days

        i = 0
        for day in li_list:
            if i >= 8:
                break

            temp = []
            try:
                # 提取日期
                time_span = day.find('span', {'class': 'time'})
                date = time_span.string if time_span else "未知日期"
                date = re.search(r'\((.*?)\)', date).group(1) if '(' in date else date

                # 提取天气
                wea_span = day.find('span', {'class': 'wea'})
                weather = wea_span.string if wea_span else "未知天气"

                # 提取温度
                tem_span = day.find('span', {'class': 'tem'})
                tem_text = tem_span.text if tem_span else "未知/未知"
                if '/' in tem_text:
                    tem_low, tem_high = [t.strip()[:-1] for t in tem_text.split('/')]
                else:
                    tem_low, tem_high = tem_text.strip()[:-1], "未知"

                # 提取风向
                wind_span = day.find('span', {'class': 'wind'})
                wind_text = wind_span.string if wind_span else "无风向"
                wind_dirs = wind_text.split('转') if '转' in wind_text else [wind_text, wind_text]

                # 提取风级
                wind1_span = day.find('span', {'class': 'wind1'})
                wind_scale = wind1_span.string if wind1_span else "0级"
                wind_level = int(wind_scale[wind_scale.index('级') - 1]) if '级' in wind_scale else 0

                temp.extend([date, weather, tem_low, tem_high] + wind_dirs + [wind_level])
                final_8_14days.append(temp)
            except Exception as e:
                print(f"第{i + 1}天数据解析错误: {e}")
            i += 1

    except Exception as e:
        print(f"15天预报解析整体错误: {e}")

    return final_8_14days


def write_to_csv(file_name, data, day_type=14):
    """保存数据到CSV文件，day_type=14为14天数据，=1为当天数据"""
    if not data:
        print("数据为空，无法保存")
        return

    try:
        with open(file_name, 'w', encoding='utf-8-sig', newline='') as f:
            if day_type == 14:
                header = ['日期', '天气', '最低气温', '最高气温', '风向1', '风向2', '风级']
            else:
                header = ['小时', '温度', '风力方向', '风级', '降水量', '相对湿度', '空气质量']
            csv_writer = csv.writer(f)
            csv_writer.writerow(header)
            csv_writer.writerows(data)
        print(f"数据已保存至 {file_name}")
    except Exception as e:
        print(f"CSV写入错误: {e}")


def main():
    """主函数：执行数据获取、合并及保存流程"""
    print("开始获取天气数据...")
    # 珠海天气预报URL
    url_7days = 'http://www.weather.com.cn/weather/101280701.shtml'  # 7天预报
    url_15days = 'http://www.weather.com.cn/weather15d/101280701.shtml'  # 15天预报

    # 获取网页内容
    html_7days = getHTMLtext(url_7days)
    html_15days = getHTMLtext(url_15days)

    if not html_7days or not html_15days:
        print("网页获取失败，程序终止")
        return

    # 解析数据
    day_data, seven_days_data = get_content(html_7days)
    eight_fourteen_data = get_content2(html_15days)

    # 合并14天数据
    fourteen_days_data = seven_days_data + eight_fourteen_data

    # 保存数据
    write_to_csv('D:\PyCharm\pythonProject\实训weather_today.csv', day_data, day_type=1)
    write_to_csv('D:\PyCharm\pythonProject\实训weather_today.csv', fourteen_days_data, day_type=14)

    print("数据获取与保存完成")


if __name__ == '__main__':
    main()