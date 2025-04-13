import numpy as np
from noise import pnoise2
from map.terrain import TerrainType

class MapGenerator:
    def __init__(self, width, height, scale=100, seed=None):
        self.width = width
        self.height = height
        self.scale = scale
        self.seed = seed if seed is not None else np.random.randint(0, 10000)

    def generate(self):
        map_data = np.empty((self.height, self.width), dtype=object)
        elevation = np.zeros((self.height, self.width))

        cx, cy = self.width / 2, self.height / 2

        for y in range(self.height):
            for x in range(self.width):
                nx = x / (self.scale * 0.6)
                ny = y / (self.scale * 0.6)

                base = pnoise2(nx + self.seed, ny + self.seed, octaves=4)
                detail = pnoise2((nx + self.seed) * 3, (ny + self.seed) * 3, octaves=6)
                noise_value = 0.5 * base + 0.5 * detail

                # 距離補正を弱めて外周も海にしやすくする
                dx = (x - cx) / cx
                dy = (y - cy) / cy
                distance = (dx * dx + dy * dy) ** 0.5
                distance_factor = max(0, 1 - distance * 1.2)

                elevation[y][x] = noise_value * distance_factor

        # elevation の min/max を安全に確保
        max_e = np.percentile(elevation, 98)  # 上位2%を除外
        min_e = np.percentile(elevation, 2)   # 下位2%を除外
        normalized = np.clip((elevation - min_e) / (max_e - min_e), 0, 1)


        # 地形分類
        for y in range(self.height):
            for x in range(self.width):
                val = normalized[y][x]

                if val < 0.5:
                    map_data[y][x] = TerrainType.OCEAN
                elif val < 0.65:
                    map_data[y][x] = TerrainType.GRASSLAND
                elif val < 0.8:
                    map_data[y][x] = TerrainType.FOREST
                else:
                    map_data[y][x] = TerrainType.MOUNTAIN


        return map_data
