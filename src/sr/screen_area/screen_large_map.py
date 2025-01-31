from enum import Enum

from basic import Rect
from sr.screen_area import ScreenArea


class ScreenLargeMap(Enum):

    SUB_MAP_BACK = ScreenArea(pc_rect=Rect(1675, 110, 1838, 150), text='返回')  # 二级地图中 需要返回

    MAIN_SCALE_MINUS = ScreenArea(pc_rect=Rect(623, 986, 623, 986))  # 缩小地图
    MAIN_SCALE_PLUS = ScreenArea(pc_rect=Rect(999, 984, 999, 984))  # 缩小地图

    SUB_SCALE_MINUS = ScreenArea(pc_rect=Rect(819, 987, 819, 987))  # 缩小地图
    SUB_SCALE_PLUS = ScreenArea(pc_rect=Rect(1194, 984, 1194, 984))  # 缩小地图

    PLANET_NAME = ScreenArea(pc_rect=Rect(100, 60, 350, 100))  # 左上角 - 星球名字
    STAR_RAIL_MAP = ScreenArea(pc_rect=Rect(1580, 120, 1750, 160), text='星轨航图')  # 右上角 - 星轨航图
    REGION_LIST = ScreenArea(pc_rect=Rect(1480, 200, 1820, 1000))  # 右侧区域列表

    TP_BTN = ScreenArea(pc_rect=Rect(1500, 950, 1800, 1000), text='传送')  # 右侧 传送按钮
