# environment_analysis.py
# 环境数据分析（分组对比 + 地理分布 + 统计描述）
# 数据文件：shanghai_coffee_shops_env.csv

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 读取包含环境字段的数据
df = pd.read_csv("shanghai_coffee_shops_env.csv", encoding="utf-8-sig")
print(f"成功读取数据，共 {len(df)} 条记录")
print("包含的环境字段：", [c for c in df.columns if 'count' in c or 'subway' in c])

# 2. 整体描述统计
print("\n【整体周边环境描述】")
print(df[['subway_count', 'bus_count', 'restaurant_count', 'competitor_count']].describe())

# 3. 按品牌类型分组对比（均值）
grouped = df.groupby('brand_type')[['subway_count', 'bus_count', 'restaurant_count', 'competitor_count']].mean()
print("\n【不同品牌类型周边环境均值】")
print(grouped)

# 4. 柱状图：分组对比
grouped.plot(kind='bar', figsize=(10, 6))
plt.title("不同品牌类型咖啡店周边环境均值对比")
plt.ylabel("平均数量")
plt.xlabel("品牌类型")
plt.legend(title="环境指标")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("brand_env_comparison.png", dpi=150)
plt.show()

# 5. 箱线图：分布差异
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
for ax, col in zip(axes.flat, ['subway_count', 'bus_count', 'restaurant_count', 'competitor_count']):
    sns.boxplot(x='brand_type', y=col, data=df, ax=ax)
    ax.set_title(col)
    ax.set_xlabel("")
plt.tight_layout()
plt.savefig("boxplots_env.png", dpi=150)
plt.show()

# 6. 地理分布（按品牌类型着色）
plt.figure(figsize=(12, 10))
colors = {'国际连锁': 'red', '本土连锁': 'blue', '独立/精品': 'green'}
for brand, color in colors.items():
    subset = df[df['brand_type'] == brand]
    plt.scatter(subset['longitude'], subset['latitude'], s=1, alpha=0.5, c=color, label=brand)
plt.title("上海咖啡店地理分布（按品牌类型）")
plt.xlabel("经度")
plt.ylabel("纬度")
plt.legend()
plt.tight_layout()
plt.savefig("geo_by_brand_env.png", dpi=150)
plt.show()

print("\n环境分析完成！生成的图表：brand_env_comparison.png, boxplots_env.png, geo_by_brand_env.png")