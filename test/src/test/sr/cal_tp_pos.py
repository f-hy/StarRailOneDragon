import os

import cv2

from basic import os_utils
from basic.img import cv2_utils
from basic.img.os import get_debug_image
from basic.log_utils import log
from sr import cal_pos
from sr.const import map_const
from sr.const.map_const import TransportPoint
from sr.image.cv2_matcher import CvImageMatcher
from sr.image.image_holder import ImageHolder
from sr.image.sceenshot import mini_map, large_map, LargeMapInfo


def get_tp_image_path(tp: TransportPoint):
    dir_path = os_utils.get_path_under_work_dir('test', 'resources', 'images', 'cal_pos', 'tp_pos')
    return os.path.join(dir_path, '%s.png' % tp.unique_id)


def cal_one(tp: TransportPoint, debug_image: str = None, show: bool = False):
    image_path = get_tp_image_path(tp)
    if debug_image is not None:
        image = get_debug_image(debug_image)
        mm = mini_map.cut_mini_map(image, self.ctx.game_config.mini_map_pos)
        cv2.imwrite(image_path, mm)
    else:
        mm = cv2_utils.read_image(image_path)

    possible_pos = (*(tp.lm_pos.tuple()), 50)
    lm_info: LargeMapInfo = ih.get_large_map(tp.region)
    lm_rect = large_map.get_large_map_rect_by_pos(lm_info.gray.shape, mm.shape[:2], possible_pos)
    mm_info = mini_map.analyse_mini_map(mm, im)
    result = cal_pos.cal_character_pos(im, lm_info, mm_info, lm_rect=lm_rect, show=show, retry_without_rect=False, running=False)

    log.info('%s 传送落地坐标 %s', tp.display_name, result.center)
    cv2.waitKey(0)


if __name__ == '__main__':
    ih = ImageHolder()
    im = CvImageMatcher(ih)

    sp_list = [
        map_const.P01_R04_SP01,
        map_const.P01_R04_SP02,
        map_const.P01_R04_SP03,
        map_const.P01_R04_SP04,
        map_const.P01_R04_SP06,
        # map_const.P03_R08_SP06,
        # map_const.P03_R08_SP13,
        # map_const.P04_R05_SP10,
        # map_const.P04_R05_SP11,
    ]
    img_list = [
        '_1707495310738',
        '_1707495319219',
        '_1707495325562',
        '_1707495332597',
        # '_1707493245071',
        # '_1707493254438',
        # '_1707482626035',
        # '_1707482634160',
        # '_1707482641493',
    ]
    for i in range(len(sp_list)):
        # cal_one(sp_list[i], debug_image=img_list[i], show=True)
        cal_one(sp_list[i])