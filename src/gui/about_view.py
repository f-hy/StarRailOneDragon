import webbrowser
from typing import Optional

import flet as ft

from basic import os_utils
from basic.i18_utils import gt
from basic.log_utils import log
from gui import components, version, snack_bar
from gui.sr_basic_view import SrBasicView
from sr.context import Context
from sr.one_dragon_config import PROXY_TYPE_LIST


class AboutView(SrBasicView, components.Card):

    def __init__(self, page: ft.Page, ctx: Context):
        SrBasicView.__init__(self, page, ctx)

        self.home_btn = components.RectOutlinedButton(gt('访问', 'ui'), on_click=self._visit_home)
        self.report_btn = components.RectOutlinedButton(gt('访问', 'ui'), on_click=self._report_problem)

        self.check_update_btn = components.RectOutlinedButton(text='检查更新', on_click=self.check_update)
        self.update_btn = components.RectOutlinedButton(text='更新', on_click=self.do_update, visible=False)
        self.specified_version_input = ft.TextField(hint_text='指定需要更新的版本 例如 v1.0.0')
        self.proxy_type_dropdown = ft.Dropdown(
            options=[
                ft.dropdown.Option(text=gt(i.cn, 'ui'), key=i.id) for i in PROXY_TYPE_LIST
            ],
            width=150, on_change=self._on_proxy_type_changed
        )
        self.personal_proxy_input = ft.TextField(hint_text='host:port', width=150,
                                                 value='http://127.0.0.1:8234', disabled=True,
                                                 on_change=self._on_personal_proxy_changed)

        plan_list = components.SettingsList(
            controls=[
                components.SettingsListGroupTitle(gt('喜欢脚本记得到主页点Star', 'ui')),
                components.SettingsListItem(gt('Github主页', 'ui'), self.home_btn),
                components.SettingsListItem(gt('问题反馈', 'ui'), self.report_btn),
                components.SettingsListGroupTitle('更新'),
                components.SettingsListItem('指定版本', self.specified_version_input),
                components.SettingsListItem('代理类型', self.proxy_type_dropdown),
                components.SettingsListItem('代理地址', self.personal_proxy_input),
                components.SettingsListItem('检查更新', ft.Row(controls=[self.check_update_btn, self.update_btn])),
            ],
            width=400
        )

        components.Card.__init__(self, plan_list, width=800)

    def handle_after_show(self):
        self._load_config_and_display()

    def _load_config_and_display(self):
        """
        加载配置显示
        :return:
        """
        self.proxy_type_dropdown.value = self.sr_ctx.one_dragon_config.proxy_type
        self.personal_proxy_input.value = self.sr_ctx.one_dragon_config.personal_proxy
        self._update_proxy_part_display()

    def _visit_home(self, e=None):
        webbrowser.open("https://github.com/DoctorReid/StarRailOneDragon")

    def _report_problem(self, e=None):
        webbrowser.open("https://github.com/DoctorReid/StarRailOneDragon/issues/new/choose")

    def check_update(self, e):
        if self.specified_version_input.value is None or self.specified_version_input.value == '':
            version_result = version.check_new_version(proxy=self.sr_ctx.one_dragon_config.proxy_address)
        else:
            version_result = version.check_specified_version(self.specified_version_input.value,
                                                             proxy=self.sr_ctx.one_dragon_config.proxy_address)

        if version_result == 2:
            msg: str = gt('检测更新请求失败', 'ui')
            snack_bar.show_message(msg, self.flet_page)
            log.info(msg)
        elif version_result == 1:
            if os_utils.run_in_flet_exe() or self.sr_ctx.one_dragon_config.is_debug:
                msg: str = gt('检测到新版本 再次点击进行更新 更新过程会自动关闭脚本 完成后将自动启动', 'ui')
                snack_bar.show_message(msg, self.flet_page)
                log.info(msg)
                self.update_btn.visible = True
                self.check_update_btn.visible = False
                self.update()
            else:
                msg: str = gt('检测到新版本 请自行使用 git pull 更新', 'ui')
                snack_bar.show_message(msg, self.flet_page)
                log.info(msg)
        else:
            msg: str = gt('已是最新版本', 'ui')
            snack_bar.show_message(msg, self.flet_page)
            log.info(msg)

    def do_update(self, e):
        msg: str = gt('即将开始更新 更新过程会自动关闭脚本 完成后将自动启动', 'ui')
        snack_bar.show_message(msg, self.flet_page)
        log.info(msg)
        self.update_btn.disabled = True
        self.update()
        try:
            if self.specified_version_input.value is None or self.specified_version_input.value == '':
                ver = None
            else:
                ver = self.specified_version_input.value
            version.do_update(version=ver,
                              proxy=self.sr_ctx.one_dragon_config.proxy_address)
            self.flet_page.window_close()
        except Exception:
            msg: str = gt('下载更新失败', 'ui')
            snack_bar.show_message(msg, self.flet_page)
            log.error(msg, exc_info=True)
            self.update_btn.disabled = False
            self.update()

    def _update_proxy_part_display(self):
        """
        更新代理部分的显示
        :return:
        """
        self.personal_proxy_input.disabled = self.proxy_type_dropdown.value != 'personal'
        self.update()

    def _on_proxy_type_changed(self, e):
        """
        更改代理类型
        :param e:
        :return:
        """
        self.sr_ctx.one_dragon_config.proxy_type = self.proxy_type_dropdown.value
        self._update_proxy_part_display()

    def _on_personal_proxy_changed(self, e):
        self.sr_ctx.one_dragon_config.personal_proxy = self.personal_proxy_input.value



_about_view: Optional[AboutView] = None


def get(page: ft.Page, ctx: Context) -> AboutView:
    global _about_view
    if _about_view is None:
        _about_view = AboutView(page, ctx)
    return _about_view
