from enum import Enum

from basic import Rect
from sr.screen_area import ScreenArea


class ScreenPhoneMenu(Enum):

    EXIT_BTN = ScreenArea(pc_rect=Rect(1840, 25,1895, 80))  # 关闭按钮

    ELLIPSIS_BTN = ScreenArea(pc_rect=Rect(1390, 50, 1810, 350))  # 省略号...的位置 包含弹出的中文框

    TRAILBLAZE_LEVEL_PART = ScreenArea(pc_rect=Rect(1280, 240, 1505, 275), text='开拓等级', lcs_percent=0.55)

    POWER_BTN = ScreenArea(pc_rect=Rect(1834, 951, 1897, 1008), status='返回登陆')

    ASSIGNMENTS_CLAIM = ScreenArea(pc_rect=Rect(370, 886, 573, 933), text='一键领取')  # 委托
    ASSIGNMENTS_SEND_AGAIN = ScreenArea(pc_rect=Rect(1037, 927, 1374, 981), text='再次派遣')  # 委托
