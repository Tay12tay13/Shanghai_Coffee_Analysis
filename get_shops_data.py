import requests
import json
import time
import pandas as pd

# 配置
YOUR_KEY = "你的高德Key"
KEYWORD = "咖啡"
OFFSET = 25  # 每页25条（最大）

# 上海所有区/县的adcode（行政区划代码）
districts = [
    {"name": "黄浦区", "adcode": "310101"},
    {"name": "徐汇区", "adcode": "310104"},
    {"name": "长宁区", "adcode": "310105"},
    {"name": "静安区", "adcode": "310106"},
    {"name": "普陀区", "adcode": "310107"},
    {"name": "虹口区", "adcode": "310109"},
    {"name": "杨浦区", "adcode": "310110"},
    {"name": "闵行区", "adcode": "310112"},
    {"name": "宝山区", "adcode": "310113"},
    {"name": "嘉定区", "adcode": "310114"},
    {"name": "浦东新区", "adcode": "310115"},
    {"name": "金山区", "adcode": "310116"},
    {"name": "松江区", "adcode": "310117"},
    {"name": "青浦区", "adcode": "310118"},
    {"name": "奉贤区", "adcode": "310120"},
    {"name": "崇明区", "adcode": "310151"},
]

# 存储所有店铺
all_shops = []

# 遍历每个区
for district in districts:
    print(f"\n正在获取 {district['name']} 的咖啡店数据...")

    # 对每个区循环翻页
    for page in range(1, 20):  # 最多翻20页（每页25条=500条，够用了）
        url = f"https://restapi.amap.com/v3/place/text?keywords={KEYWORD}&city={district['adcode']}&offset={OFFSET}&page={page}&key={YOUR_KEY}"

        try:
            resp = requests.get(url)
            data = json.loads(resp.text)

            if data.get("status") != "1":
                print(f"  {district['name']} 请求失败: {data.get('info')}")
                break

            pois = data.get("pois", [])
            if not pois:
                print(f"  {district['name']} 第{page}页无数据，已获取完")
                break

            # 添加区名到每条数据中（便于后续分析）
            for poi in pois:
                poi["district"] = district["name"]

            all_shops.extend(pois)
            print(f"  {district['name']} 第{page}页: {len(pois)}条，累计{len(all_shops)}条")

            time.sleep(0.2)  # 礼貌性等待

        except Exception as e:
            print(f"  {district['name']} 发生异常: {e}")
            break

print(f"\n总共获取到 {len(all_shops)} 条咖啡店数据")

# 保存为CSV
if all_shops:
    df = pd.DataFrame(all_shops)
    df.to_csv("shanghai_coffee_shops_raw.csv", index=False, encoding="utf-8-sig")
    print("数据已保存为 shanghai_coffee_shops_raw.csv")
else:
    print("未获取到任何数据")