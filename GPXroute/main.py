import math
import random
import folium
from datetime import datetime, timedelta


# ================== 高德地图 API Key ==================
# 如果你不想每次输入，可以在这里填写你的 Key
GAODE_KEY = ""


# ================== 坐标转换核心 (WGS‑84 ↔ GCJ‑02) ==================
def wgs84_to_gcj02(lng, lat):
    """WGS‑84 → GCJ‑02（境外原样返回）"""
    if out_of_china(lng, lat):
        return lng, lat

    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * math.pi
    magic = math.sin(radlat)
    magic = 1 - 0.00669342162296594323 * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((6378137.0 * (1 - 0.00669342162296594323)) / (magic * sqrtmagic) * math.pi)
    dlng = (dlng * 180.0) / (6378137.0 / sqrtmagic * math.cos(radlat) * math.pi)
    return lng + dlng, lat + dlat


def gcj02_to_wgs84(lng, lat):
    """GCJ‑02 → WGS‑84（迭代逼近，误差 < 0.01m）"""
    if out_of_china(lng, lat):
        return lng, lat
    wgs_lng, wgs_lat = lng, lat
    for _ in range(3):
        gcj_lng, gcj_lat = wgs84_to_gcj02(wgs_lng, wgs_lat)
        wgs_lng += lng - gcj_lng
        wgs_lat += lat - gcj_lat
    return wgs_lng, wgs_lat


def _transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(abs(lng))
    ret += (20.0 * math.sin(6.0 * lng * math.pi) + 20.0 * math.sin(2.0 * lng * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * math.pi) + 40.0 * math.sin(lat / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * math.pi) + 320 * math.sin(lat * math.pi / 30.0)) * 2.0 / 3.0
    return ret


def _transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(abs(lng))
    ret += (20.0 * math.sin(6.0 * lng * math.pi) + 20.0 * math.sin(2.0 * lng * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * math.pi) + 40.0 * math.sin(lng / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * math.pi) + 300.0 * math.sin(lng / 30.0 * math.pi)) * 2.0 / 3.0
    return ret


def out_of_china(lng, lat):
    return not (72.004 <= lng <= 137.8347 and 0.8293 <= lat <= 55.8271)


# ================== 辅助输入 ==================
def get_input(prompt, default):
    value = input(f"{prompt} (默认 {default}): ").strip()
    return type(default)(value) if value else default


def generate_professional_track():
    print("=" * 50)
    print("  GPXroute - 智能操场轨迹生成器")
    print("  规则: 输出到手机必须选 WGS‑84！")
    print("=" * 50)

    # --- 起始点 ---
    start_lat = get_input("\n起始纬度 (Lat)", 30.3070)
    start_lon = get_input("起始经度 (Lon)", 120.0775)

    # --- 输入坐标系 ---
    print("\n你的坐标来源是？")
    print("  1 – WGS‑84（真实GPS、OSM、谷歌地球、境外谷歌地图）")
    print("  2 – GCJ‑02（国内谷歌地图、高德地图、国行iPhone直接获取）")
    src_is_gcj = input("输入选项 (1/2, 默认 1): ").strip() == '2'

    # --- 预览底图 ---
    print("\n预览地图选哪个？")
    print("  1 – OpenStreetMap (WGS‑84)")
    print("  2 – 高德地图 (GCJ‑02)")
    use_gaode = input("输入选项 (1/2, 默认 1): ").strip() == '2'

    # --- 输出 GPX 坐标系 ---
    print("\n※ 重要：模拟位置到手机（Xcode/安卓）必须用 WGS‑84！")
    print("  1 – WGS‑84（通用，推荐用于手机模拟）")
    print("  2 – GCJ‑02（仅用于某些特殊需要，直接手机偏移）")
    gpx_crs = input("输入选项 (1/2, 默认 1): ").strip()
    gpx_is_gcj = (gpx_crs == '2')

    # --- 坐标预处理：统一转换到预览底图使用的坐标系 ---
    # 预览底图坐标系：use_gaode 为 True 则需要 GCJ‑02，否则 WGS‑84
    if src_is_gcj and not use_gaode:
        # 输入 GCJ‑02 → 预览 OSM → 需转为 WGS‑84
        print("\n[转换] GCJ‑02 转 WGS‑84（适配 OSM 底图）")
        start_lon, start_lat = gcj02_to_wgs84(start_lon, start_lat)
    elif not src_is_gcj and use_gaode:
        # 输入 WGS‑84 → 预览高德 → 需转为 GCJ‑02
        print("\n[转换] WGS‑84 转 GCJ‑02（适配高德底图）")
        start_lon, start_lat = wgs84_to_gcj02(start_lon, start_lat)
    else:
        print("\n[无需转换] 输入坐标系与预览底图一致")

    # --- 其他参数 ---
    target_dist = get_input("\n目标长度 (米)", 3000.0)
    target_speed = get_input("目标配速 (m/s)", 2.8)
    heading_deg = get_input("操场旋转角度 (正东为0, 逆时针)", 100)
    offset_x = get_input("起始点水平平移 (米, 东正西负)", 0.0)
    offset_y = get_input("起始点垂直平移 (米, 北正南负)", 0.0)

    # --- 跑道建模 ---
    R_EARTH = 6378137
    straight_len = 80.0
    radius = 36.0
    lap_length = 2 * straight_len + 2 * math.pi * radius
    total_seconds = int(target_dist / target_speed)
    heading_rad = math.radians(heading_deg)

    path_coords = []          # 预览使用的坐标 (当前底图坐标系)
    gpx_raw = []              # 暂存 (预览坐标系下的点，稍后可能转换)
    start_time = datetime.now()

    for s in range(total_seconds + 1):
        dist_in_lap = (target_speed * s) % lap_length

        # 跑道几何形状
        if dist_in_lap < straight_len:
            raw_dx, raw_dy = dist_in_lap, 0
        elif dist_in_lap < straight_len + math.pi * radius:
            theta = (dist_in_lap - straight_len) / radius
            raw_dx = straight_len + radius * math.sin(theta)
            raw_dy = radius - radius * math.cos(theta)
        elif dist_in_lap < 2 * straight_len + math.pi * radius:
            raw_dx = straight_len - (dist_in_lap - straight_len - math.pi * radius)
            raw_dy = 2 * radius
        else:
            theta = (dist_in_lap - 2 * straight_len - math.pi * radius) / radius
            raw_dx = -radius * math.sin(theta)
            raw_dy = radius + radius * math.cos(theta)

        # GPS漂移
        raw_dx += random.uniform(-0.2, 0.2)
        raw_dy += random.uniform(-0.2, 0.2)

        # 旋转 + 平移
        final_dx = raw_dx * math.cos(heading_rad) - raw_dy * math.sin(heading_rad) + offset_x
        final_dy = raw_dx * math.sin(heading_rad) + raw_dy * math.cos(heading_rad) + offset_y

        # 投影到经纬度
        delta_lat = (final_dy / R_EARTH) * (180 / math.pi)
        delta_lon = (final_dx / (R_EARTH * math.cos(math.pi * start_lat / 180))) * (180 / math.pi)

        lat = start_lat + delta_lat
        lon = start_lon + delta_lon

        path_coords.append([lat, lon])
        t_str = (start_time + timedelta(seconds=s)).strftime('%Y-%m-%dT%H:%M:%SZ')
        gpx_raw.append((lat, lon, t_str))

    # --- 输出 GPX 坐标系转换 ---
    # 当前 gpx_raw 的点是预览底图的坐标系（与 use_gaode 一致）
    # 要输出 gpx_is_gcj 坐标系
    if use_gaode == gpx_is_gcj:
        gpx_final = gpx_raw   # 相同，无需转换
    elif use_gaode and not gpx_is_gcj:
        # 预览 GCJ‑02 → 输出 WGS‑84
        print("\n[GPX 转换] GCJ‑02 → WGS‑84（便于手机模拟）")
        gpx_final = [(gcj02_to_wgs84(lon, lat)[0], gcj02_to_wgs84(lon, lat)[1], t) for lat, lon, t in gpx_raw]
    else:  # 预览 WGS‑84 → 输出 GCJ‑02
        print("\n[GPX 转换] WGS‑84 → GCJ‑02")
        gpx_final = [(wgs84_to_gcj02(lon, lat)[0], wgs84_to_gcj02(lon, lat)[1], t) for lat, lon, t in gpx_raw]

    # --- 起点信息 ---
    first_lat, first_lon = gpx_final[0][0], gpx_final[0][1]
    print("-" * 40)
    print(f"GPX 文件起点: {first_lat:.8f}, {first_lon:.8f}")
    print(f"GPX 坐标系 : {'GCJ‑02' if gpx_is_gcj else 'WGS‑84 (手机推荐)'}")
    print("-" * 40)

    # --- 生成预览 HTML ---
    if use_gaode:
        key = GAODE_KEY if GAODE_KEY else input("请输入高德 Key: ").strip()
        if not key:
            print("无 Key，回退到 OSM 预览")
            use_gaode = False
        else:
            tile_url = f'https://webrd0{{s}}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={{x}}&y={{y}}&z={{z}}&key={key}'
            m = folium.Map(location=path_coords[0], zoom_start=18, tiles=None)
            folium.raster_layers.TileLayer(
                tiles=tile_url, attr='高德', subdomains='0123', name='高德'
            ).add_to(m)
    if not use_gaode:
        m = folium.Map(location=path_coords[0], zoom_start=18, tiles='OpenStreetMap')

    folium.PolyLine(path_coords, color="blue", weight=4, opacity=0.7).add_to(m)
    folium.Marker(path_coords[0], popup="Start", icon=folium.Icon(color='green')).add_to(m)
    m.save("preview.html")

    # --- 保存 GPX ---
    gpx_lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<gpx version="1.1" creator="Xcode">']
    for lat, lon, t_str in gpx_final:
        gpx_lines.append(f'  <wpt lat="{lat:.8f}" lon="{lon:.8f}"><time>{t_str}</time></wpt>')
    gpx_lines.append('</gpx>')

    with open("route.gpx", "w", encoding="utf-8") as f:
        f.write("\n".join(gpx_lines))

    print("\n✅ 生成完成！\n   GPX 文件: route.gpx\n   预览网页: preview.html")
    if gpx_is_gcj:
        print("⚠️  警告：GPX 是 GCJ‑02，直接导入手机可能偏移数百米。\n   建议重新生成并选择 WGS‑84 输出。")


if __name__ == "__main__":
    generate_professional_track()
    