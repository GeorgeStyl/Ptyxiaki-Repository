import math

def lat_lng_to_tile_coords(lat, lng, zoom):
    n = 2 ** zoom
    x_tile = int(n * ((lng + 180) / 360))
    lat_rad = math.radians(lat)  # Convert latitude to radians
    y_tile = int(n * (1 - (math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi)) / 2)
    return x_tile, y_tile

print(lat_lng_to_tile_coords(40.7128, -74.0060, 8))
