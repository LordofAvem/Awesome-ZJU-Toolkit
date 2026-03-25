import math
import random
import folium
from datetime import datetime, timedelta


def get_input(prompt, default):
    """辅助函数：处理用户输入，回车则使用默认值"""
    value = input(f"{prompt} (默认 {default}): ").strip()
    return type(default)(value) if value else default


def generate_professional_track():
    print("------ GPXroute ------")

    # 获取基础参数 (支持回车默认)
    start_lat = get_input("起始纬度 (Lat)", 30.3070)
    start_lon = get_input("起始经度 (Lon)", 120.0775)
    target_dist = get_input("目标长度 (米)", 3000.0)
    target_speed = get_input("目标配速 (m/s)", 2.8)
    heading_deg = get_input("操场旋转角度 (正东为0, 逆时针)", 100)
    offset_x = get_input("起始点水平平移 (米, 东正西负)", 0.0)
    offset_y = get_input("起始点垂直平移 (米, 北正南负)", 0.0)

    # 物理常量与模型参数
    R_EARTH = 6378137
    # 标准400米跑道参数
    straight_len = 80.0
    radius = 36.0
    lap_length = 2 * straight_len + 2 * math.pi * radius

    # 计算总耗时
    total_seconds = int(target_dist / target_speed)
    heading_rad = math.radians(heading_deg)

    path_coords = []
    gpx_points = []
    start_time = datetime.now()

    print(f"\n开始建模: 预计耗时 {total_seconds}s, 跑圈数: {target_dist / lap_length:.2f}")

    for s in range(total_seconds + 1):
        # 计算在当前圈内的相对位移 (s=0 时为起点)
        dist_in_lap = (target_speed * s) % lap_length

        # 跑道建模
        if dist_in_lap < straight_len:  # 下直道
            raw_dx, raw_dy = dist_in_lap, 0
        elif dist_in_lap < straight_len + math.pi * radius:  # 右弯道
            theta = (dist_in_lap - straight_len) / radius
            raw_dx = straight_len + radius * math.sin(theta)
            raw_dy = radius - radius * math.cos(theta)
        elif dist_in_lap < 2 * straight_len + math.pi * radius:  # 上直道
            raw_dx = straight_len - (dist_in_lap - straight_len - math.pi * radius)
            raw_dy = 2 * radius
        else:  # 左弯道
            theta = (dist_in_lap - 2 * straight_len - math.pi * radius) / radius
            raw_dx = -radius * math.sin(theta)
            raw_dy = radius + radius * math.cos(theta)

        # 叠加抖动与平移
        # 模拟 GPS 漂移 (0.3米级别)
        raw_dx += random.uniform(-0.2, 0.2)
        raw_dy += random.uniform(-0.2, 0.2)

        # 应用旋转矩阵 + 用户偏移量
        # X_final = x*cosθ - y*sinθ + offset_x
        # Y_final = x*sinθ + y*cosθ + offset_y
        final_dx = raw_dx * math.cos(heading_rad) - raw_dy * math.sin(heading_rad) + offset_x
        final_dy = raw_dx * math.sin(heading_rad) + raw_dy * math.cos(heading_rad) + offset_y

        # 投影到经纬度
        delta_lat = (final_dy / R_EARTH) * (180 / math.pi)
        delta_lon = (final_dx / (R_EARTH * math.cos(math.pi * start_lat / 180))) * (180 / math.pi)

        current_lat = start_lat + delta_lat
        current_lon = start_lon + delta_lon

        # 记录首个点作为平移后的真实起点输出
        if s == 0:
            actual_start_lat, actual_start_lon = current_lat, current_lon

        path_coords.append([current_lat, current_lon])

        # 生成 GPX 节点
        t_str = (start_time + timedelta(seconds=s)).strftime('%Y-%m-%dT%H:%M:%SZ')
        gpx_points.append(f'    <wpt lat="{current_lat:.8f}" lon="{current_lon:.8f}"><time>{t_str}</time></wpt>')

    # 输出验证数据
    print("-" * 30)
    print(f"平移后的真实起始坐标 (Offset Result):")
    print(f"   Latitude:  {actual_start_lat:.8f}")
    print(f"   Longitude: {actual_start_lon:.8f}")
    print("-" * 30)

    # 生成 HTML 预览
    m = folium.Map(location=[actual_start_lat, actual_start_lon], zoom_start=18)
    folium.PolyLine(path_coords, color="blue", weight=4, opacity=0.7).add_to(m)
    folium.Marker([actual_start_lat, actual_start_lon], popup="New Start", icon=folium.Icon(color='green')).add_to(m)
    m.save("preview.html")

    # 保存 GPX 文件
    gpx_content = f'<?xml version="1.0" encoding="UTF-8"?>\n<gpx version="1.1" creator="Xcode">\n' + "\n".join(
        gpx_points) + '\n</gpx>'
    with open("route.gpx", "w", encoding='utf-8') as f:
        f.write(gpx_content)

    print(f"生成成功！")
    print(f"GPX文件: route.gpx")
    print(f"预览图: preview.html")


if __name__ == "__main__":
    generate_professional_track()