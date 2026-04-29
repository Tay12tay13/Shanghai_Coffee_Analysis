import folium
from folium.plugins import HeatMap
from folium.features import DivIcon
import pandas as pd
import os

# 读取数据
df = pd.read_csv("shanghai_coffee_shops_env.csv", encoding="utf-8-sig")

# 创建底图
m = folium.Map(location=[31.2304, 121.4737], zoom_start=11, control_scale=True)

# ================= 1. 行政区边界（GeoJSON） =================
# 如果文件存在则加载，并添加边界线（虚线）
geojson_path = "shanghai_districts.geojson"
if os.path.exists(geojson_path):
    import json
    with open(geojson_path, 'r', encoding='utf-8') as f:
        district_geojson = json.load(f)
    folium.GeoJson(
        district_geojson,
        name="行政区边界",
        style_function=lambda feature: {
            'fillColor': 'none',
            'color': 'black',
            'weight': 1.5,
            'dashArray': '5, 5'
        },
        tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['区名：'], localize=True)
    ).add_to(m)
else:
    print("警告：未找到 shanghai_districts.geojson，边界线将不显示。")

# ================= 2. 行政区文字标签（预定义中心坐标） =================
# 上海各区大致中心坐标（来源于公开数据，用于文字标注）
district_centers = {
    "黄浦区": [31.2314, 121.4846],
    "徐汇区": [31.1950, 121.4379],
    "长宁区": [31.2182, 121.4246],
    "静安区": [31.2289, 121.4552],
    "普陀区": [31.2496, 121.3961],
    "虹口区": [31.2688, 121.4914],
    "杨浦区": [31.2605, 121.5260],
    "闵行区": [31.1123, 121.3817],
    "宝山区": [31.4055, 121.4891],
    "嘉定区": [31.3747, 121.2665],
    "浦东新区": [31.2215, 121.5444],
    "金山区": [30.7419, 121.3413],
    "松江区": [31.0324, 121.2277],
    "青浦区": [31.1501, 121.1242],
    "奉贤区": [30.9186, 121.4742],
    "崇明区": [31.6265, 121.3977]
}

for district, coords in district_centers.items():
    folium.map.Marker(
        coords,
        icon=DivIcon(
            icon_size=(80, 20),
            icon_anchor=(40, 10),
            html=f'<div style="font-size: 12px; font-weight: bold; color: #333; background: rgba(255,255,255,0.7); padding: 2px 6px; border-radius: 4px; border: 1px solid #888;">{district}</div>',
        )
    ).add_to(m)

# ================= 3. 热力图图层 =================
heat_data = df[['latitude', 'longitude']].values.tolist()
heat_fg = folium.FeatureGroup(name='热力图（咖啡店密度）', show=False)
HeatMap(heat_data, radius=15, blur=10, min_opacity=0.5).add_to(heat_fg)
heat_fg.add_to(m)

# ================= 4. 分品牌点图层（圆点半径=1） =================
brands = {
    '国际连锁': {'color': 'red', 'icon': 'circle'},
    '本土连锁': {'color': 'blue', 'icon': 'circle'},
    '独立/精品': {'color': 'green', 'icon': 'circle'}
}

for brand in brands:
    fg = folium.FeatureGroup(name=brand, show=True)
    subset = df[df['brand_type'] == brand]
    for _, row in subset.iterrows():
        popup_text = f"""
        <b>{row['name']}</b><br>
        品牌: {brand}<br>
        地铁站: {row['subway_count']}<br>
        公交站: {row['bus_count']}<br>
        餐饮店: {row['restaurant_count']}<br>
        竞品咖啡: {row['competitor_count']}
        """
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=0.5,                # 圆点大小
            color=brands[brand]['color'],
            fill=True,
            fill_color=brands[brand]['color'],
            fill_opacity=0.5,
            popup=popup_text
        ).add_to(fg)
    fg.add_to(m)

# ================= 5. 图层控制 =================
folium.LayerControl().add_to(m)

# ================= 6. 图例 =================
legend_html = '''
<div style="position: fixed; bottom: 30px; right: 30px; z-index: 1000; background-color: white; padding: 8px 12px; border: 2px solid grey; border-radius: 5px; font-size: 14px;">
    <strong>图例</strong><br>
    <i style="background: red; width: 12px; height: 12px; display: inline-block; border-radius: 50%;"></i> 国际连锁<br>
    <i style="background: blue; width: 12px; height: 12px; display: inline-block; border-radius: 50%;"></i> 本土连锁<br>
    <i style="background: green; width: 12px; height: 12px; display: inline-block; border-radius: 50%;"></i> 独立/精品<br>
    <i style="background: orange; width: 12px; height: 12px; display: inline-block; background: orange;"></i> 热力图（密度）<br>
    <i style="border: 1px solid black; width: 12px; height: 12px; display: inline-block;"></i> 行政区边界<br>
    <i style="color: #333; font-weight: bold;">🗺️ 区名标签</i>
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# 保存
m.save("coffee_map_final.html")
print("✅ 最终地图已生成：coffee_map.html")