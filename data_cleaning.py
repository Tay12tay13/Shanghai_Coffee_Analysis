# data_cleaning.py
# 清洗原始咖啡店数据，输出清洗后的CSV文件

import pandas as pd
import numpy as np

# 1. 读取原始数据
print("正在读取原始数据...")
df = pd.read_csv("shanghai_coffee_shops_raw.csv", encoding="utf-8-sig")
print(f"原始数据行数: {len(df)}")

# 2. 将字符串 '[]' 替换为 NaN（缺失值）
df = df.replace('[]', np.nan)

# 3. 按 id 去重（保留第一个）
print("去重前:", len(df))
df = df.drop_duplicates(subset=['id'], keep='first')
print("去重后:", len(df))

# 4. 拆分经纬度字段
# location 字段格式为 "经度,纬度"
df[['longitude', 'latitude']] = df['location'].str.split(',', expand=True).astype(float)
# 删除原 location 列
df = df.drop('location', axis=1)

# 5. 过滤异常经纬度（上海大致范围：经度121.0~122.0，纬度31.0~31.5）
df = df[(df['longitude'] > 121.0) & (df['longitude'] < 122.0)]
df = df[(df['latitude'] > 31.0) & (df['latitude'] < 31.5)]
print("过滤异常经纬度后:", len(df))

# 6. 新增品牌分类字段（基于name）
# 定义连锁品牌关键词
chain_brands = {
    '国际连锁': ['星巴克', 'Starbucks', 'Costa', 'COSTA', 'Tims', 'Tim Hortons',
                 'Peet', "Peet's", 'Lavazza', '拉瓦萨', '% Arabica', 'Arabica','Blue Bottle', '蓝瓶', 'illy', '意利',
                 'Dunkin', 'Caribou','Gloria Jeans', 'McCafé', '麦咖啡', 'Caffè Nero'],
    '本土连锁': ['瑞幸', 'Luckin', 'Manner', 'M Stand', 'Seesaw', 'Nowwa', '挪瓦', 'Cubic Coffee', '三立方', '太平洋',
                 'Pacific Coffee', '上岛', 'UCC','代数学家', 'Algebraist', 'Double Win', '库迪', 'Cotti','T97','本来不该有',
                 '爵渴', '拉环咖啡', '干咖人', '比星咖啡', 'BeanStar','银流咖啡', 'Silver Flow','苏醒咖啡', 'Sober']
}

def classify_brand(name):
    if not isinstance(name, str):
        return '独立/精品'
    for brand_type, keywords in chain_brands.items():
        for kw in keywords:
            if kw in name:
                return brand_type
    return '独立/精品'

df['brand_type'] = df['name'].apply(classify_brand)

# 查看分类结果
print("\n品牌类型分布：")
print(df['brand_type'].value_counts())

# 7. 保留对分析有用的字段
useful_cols = [
    'id', 'name', 'address', 'longitude', 'latitude',
    'district', 'brand_type'
]
# 只保留存在的列
useful_cols = [col for col in useful_cols if col in df.columns]
df_clean = df[useful_cols].copy()

# 8. 保存清洗后的数据
output_file = "shanghai_coffee_shops_cleaned.csv"
df_clean.to_csv(output_file, index=False, encoding="utf-8-sig")
print(f"清洗完成！清洗后数据共 {len(df_clean)} 条，已保存为 {output_file}")