# get_env_data.py
# 为每个咖啡店获取周边环境数据（地铁站、公交站、餐饮店、竞品）

import pandas as pd
import requests
import json
import time
import random

# 配置
YOUR_KEY = "你的高德Key"
RADIUS = 500
TYPES = {
    'subway': '地铁站',
    'bus': '公交站',
    'restaurant': '餐饮',
    'coffee_competitor': '咖啡'
}
RETRY_TIMES = 3           # 请求失败重试次数
RETRY_DELAY = 2           # 重试等待秒数
SLEEP_INTERVAL = 0.5      # 每次请求后固定延时
SAVE_INTERVAL = 50        # 每处理多少条保存一次

def get_around_count(lon, lat, keyword):
    """带重试的周边搜索，返回POI数量"""
    url = f"https://restapi.amap.com/v3/place/around?key={YOUR_KEY}&location={lon},{lat}&keywords={keyword}&radius={RADIUS}&output=json"
    for attempt in range(RETRY_TIMES):
        try:
            resp = requests.get(url, timeout=10)
            data = json.loads(resp.text)
            if data.get("status") == "1":
                return int(data.get("count", 0))
            else:
                error = data.get("info")
                print(f"    API错误: {error}")
                if "LIMIT" in error:
                    # 限流错误，多等一会儿
                    time.sleep(RETRY_DELAY * 2)
                continue
        except Exception as e:
            print(f"    请求异常: {e}")
            time.sleep(RETRY_DELAY)
            continue
    print(f"    失败: 无法获取 {keyword} 数据")
    return 0

# 读取数据
df = pd.read_csv("shanghai_coffee_shops_cleaned.csv", encoding="utf-8-sig")
print(f"共读取 {len(df)} 条记录")

# 初始化新列（如果已有则跳过）
for col in ['subway_count', 'bus_count', 'restaurant_count', 'competitor_count']:
    if col not in df.columns:
        df[col] = 0

# 从上次中断处继续（可选）
# 你可以根据已有文件设定起始索引，例如 start_index = len(pd.read_csv("temp.csv"))
start_index = 0
print(f"从第 {start_index+1} 条开始处理")

# 主循环
for idx in range(start_index, len(df)):
    row = df.loc[idx]
    lon = row['longitude']
    lat = row['latitude']
    print(f"正在处理 {idx+1}/{len(df)}: {row['name']} ({lon},{lat})")

    # 获取各类数据
    subway = get_around_count(lon, lat, TYPES['subway'])
    bus = get_around_count(lon, lat, TYPES['bus'])
    restaurant = get_around_count(lon, lat, TYPES['restaurant'])
    competitor = get_around_count(lon, lat, TYPES['coffee_competitor'])

    df.at[idx, 'subway_count'] = subway
    df.at[idx, 'bus_count'] = bus
    df.at[idx, 'restaurant_count'] = restaurant
    df.at[idx, 'competitor_count'] = competitor

    # 每处理 SAVE_INTERVAL 条保存一次中间文件
    if (idx + 1) % SAVE_INTERVAL == 0:
        temp_file = f"coffee_env_temp_{idx+1}.csv"
        df.to_csv(temp_file, index=False, encoding="utf-8-sig")
        print(f"  已保存临时文件: {temp_file}")

    time.sleep(SLEEP_INTERVAL + random.uniform(0, 0.2))  # 随机延时

# 最终保存
df.to_csv("shanghai_coffee_shops_with_env.csv", index=False, encoding="utf-8-sig")
print("\n全部处理完成！最终文件: shanghai_coffee_shops_with_env.csv")