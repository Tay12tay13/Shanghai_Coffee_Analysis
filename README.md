# 上海咖啡店选址与品牌类型关系分析

## 项目简介
利用高德地图 API 获取上海 2718 家咖啡店数据，分析国际连锁、本土连锁、独立/精品三类咖啡店在周边环境（地铁站、公交站、餐饮店、竞品数量）上的差异，并可视化地理分布。

## 文件说明
- `shanghai_coffee_shops_env.csv`：最终数据集，包含每家咖啡店的坐标、品牌类型、周边 500 米内地铁站/公交站/餐饮店/竞品数量。
- `shanghai_coffee_shops_cleaned.csv`：清洗后的基础数据（不含环境字段），用于探索性分析。
- `exploratory_analysis.py`：探索性分析脚本，基于 `shanghai_coffee_shops_cleaned.csv`，生成样本分布、品牌构成、各区品牌堆叠图等（不生成地理散点图，避免与环境分析脚本重复）。
- `env_analysis.py`：环境数据分析脚本，基于 `shanghai_coffee_shops_env.csv`，生成环境指标描述统计、品牌环境对比柱状图、箱线图及地理分布图。
- `generate_map.py`：生成交互式地图（HTML），需安装 folium。
- `get_shops_data.py`：数据采集脚本（需高德 API Key），抓取咖啡店基础信息。
- `get_env_data.py`：数据采集脚本（需高德 API Key），为每家咖啡店获取周边环境数据。
- `*.png`：分析结果图表（由两个分析脚本生成在对应文件夹中）。
- `coffee_map_final.html`：可交互地图（用浏览器打开）。
- `shanghai_districts.geojson`：上海市行政区边界（用于地图底图）。

## 核心结论
- 独立/精品咖啡店周边餐饮店和竞品数量最多，依靠聚集效应。
- 国际连锁交通便利性略优，覆盖最广。
- 本土连锁周边环境指标均略低，偏向办公场景。

## 运行环境
- Python 3.8+
- 依赖库：pandas, matplotlib, seaborn, folium, requests

安装依赖：
```bash
pip install pandas matplotlib seaborn folium requests