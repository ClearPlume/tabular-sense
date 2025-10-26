import random


# TODO 分开两列 lat: 39.9042, lon: 116.4074
def generate_coordinate(china_only=True):
    """生成坐标（默认中国范围）"""
    if china_only:
        lat = random.uniform(18, 54)  # 中国纬度范围
        lon = random.uniform(73, 135)  # 中国经度范围
    else:
        lat = random.uniform(-90, 90)
        lon = random.uniform(-180, 180)

    return lat, lon


def dd_to_dms(dd):
    """十进制度转度分秒"""
    d = int(abs(dd))
    m = int((abs(dd) - d) * 60)
    s = ((abs(dd) - d) * 60 - m) * 60
    return d, m, s


def format_coordinate_variants(lat: float, lon: float, coordinate_format: int) -> str:
    """生成所有格式变体"""
    lat_d, lat_m, lat_s = dd_to_dms(lat)
    lon_d, lon_m, lon_s = dd_to_dms(lon)

    formats = [
        # === 小数格式 ===
        f"{lat:.4f},{lon:.4f}",
        f"{lat:.4f} {lon:.4f}",
        f"{lat:.4f};{lon:.4f}",
        f"{lat:.4f}\t{lon:.4f}",
        f"{lat:.2f},{lon:.2f}",
        f"{lat:.6f},{lon:.6f}",

        # === 带方向 ===
        f"{lat:.4f}° N, {lon:.4f}° E",
        f"{lat:.4f}°N, {lon:.4f}°E",
        f"{lat:.4f} N, {lon:.4f} E",
        f"N {lat:.4f}, E {lon:.4f}",
        f"N{lat:.4f} E{lon:.4f}",

        # === 正负号 ===
        f"{lat:+.4f},{lon:+.4f}",
        f"+{lat:.4f},+{lon:.4f}",

        # === 度分秒 ===
        f'{lat_d}°{lat_m}\'{lat_s:.2f}" N, {lon_d}°{lon_m}\'{lon_s:.2f}" E',
        f'{lat_d}°{lat_m}\'{lat_s:.2f}"N,{lon_d}°{lon_m}\'{lon_s:.2f}"E',
        f"{lat_d}°{lat_m}' N, {lon_d}°{lon_m}' E",

        # === 带标签 ===
        f"lat:{lat:.4f},lon:{lon:.4f}",
        f"lat:{lat:.4f}, lng:{lon:.4f}",
        f"latitude:{lat:.4f}, longitude:{lon:.4f}",
        f"纬度:{lat:.4f},经度:{lon:.4f}",

        # === 括号 ===
        f"({lat:.4f},{lon:.4f})",
        f"({lat:.4f}, {lon:.4f})",
        f"[{lat:.4f},{lon:.4f}]",

        # === URL格式 ===
        f"@{lat:.6f},{lon:.6f}",
        f"?lat={lat:.6f}&lon={lon:.6f}",

        # === 中文格式 ===
        f"北纬{lat:.4f}°，东经{lon:.4f}°",
        f"北纬{lat:.4f} 东经{lon:.4f}",
    ]

    return formats[coordinate_format]


def coordinates(num: int) -> list[str]:
    samples = []
    coordinate_format = random.randint(0, 25)

    for _ in range(num):
        lat, lon = generate_coordinate(china_only=False)
        samples.append(format_coordinate_variants(lat, lon, coordinate_format))

    return samples
