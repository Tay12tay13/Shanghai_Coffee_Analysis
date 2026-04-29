# exploratory_analysis.py
# 探索性分析，只有基础信息，主要看样本分布、品牌构成、地理位置等
# 数据文件：shanghai_coffee_shops_cleaned.csv

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 设置中文显示（Windows 使用 SimHei，Mac 可用 Heiti TC 等）
plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows
# plt.rcParams['font.sans-serif'] = ['Heiti TC']  # Mac 可尝试
plt.rcParams['axes.unicode_minus'] = False

#1. 读取数据
df = pd.read_csv("shanghai_coffee_shops_cleaned.csv", encoding="utf-8-sig")
print(f"成功读取数据，共 {len(df)} 条记录\n")

# 2. 各区样本分布
district_counts = df['district'].value_counts().sort_values(ascending=False)
print("各区咖啡店数量（样本分布，受API限制不代表实际总量）：")
print(district_counts)

plt.figure(figsize=(12, 6))
sns.barplot(x=district_counts.index, y=district_counts.values, order=district_counts.index)
plt.title("上海各区咖啡店样本分布（受API返回上限影响，不代表实际总量）")
plt.xlabel("行政区")
plt.ylabel("咖啡店数量（样本）")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("district_distribution.png", dpi=150)
plt.show()

#3. 品牌类型分布
brand_counts = df['brand_type'].value_counts()
print("\n品牌类型分布：")
print(brand_counts)

# 饼图
plt.figure(figsize=(8, 8))
plt.pie(brand_counts, labels=brand_counts.index, autopct='%1.1f%%', startangle=90)
plt.title("咖啡店品牌类型分布")
plt.tight_layout()
plt.savefig("brand_distribution_pie.png", dpi=150)
plt.show()

# 柱状图
plt.figure(figsize=(8, 5))
sns.barplot(x=brand_counts.index, y=brand_counts.values)
plt.title("咖啡店品牌类型分布")
plt.xlabel("品牌类型")
plt.ylabel("数量")
plt.tight_layout()
plt.savefig("brand_distribution_bar.png", dpi=150)
plt.show()

#4. 经纬度描述统计
print("\n经纬度描述统计：")
print(df[['longitude', 'latitude']].describe())

#5. 品牌类型在各区的分布
# 交叉表：各区 × 品牌类型
cross_tab = pd.crosstab(df['district'], df['brand_type'])
print("\n各区品牌类型分布（样本数）：")
print(cross_tab)

# 画堆叠柱状图（前10个区）
top_districts = district_counts.head(10).index
cross_tab_top = cross_tab.loc[top_districts]
cross_tab_top.plot(kind='bar', stacked=True, figsize=(12, 6))
plt.title("各区咖啡店品牌类型构成（样本）")
plt.xlabel("行政区")
plt.ylabel("数量")
plt.legend(title="品牌类型")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("district_brand_composition.png", dpi=150)
plt.show()

print("\n探索性分析完成！")