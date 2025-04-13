from enum import Enum

class TerrainType(Enum):
    GRASSLAND = (34, 139, 34)
    FOREST = (0, 100, 0)
    MOUNTAIN = (105, 105, 105)
    OCEAN = (25, 25, 112)

    @property
    def color(self):
        return self.value
