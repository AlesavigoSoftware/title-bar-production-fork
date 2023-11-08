import os
import kivy

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.material_resources import DEVICE_TYPE
from kivymd.uix.button import MDIconButton
from kivymd.uix.behaviors import HoverBehavior

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.properties import ListProperty, BooleanProperty, StringProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.logger import Logger


Builder.load_file(
    os.path.join(os.path.dirname(__file__), "title_bar.kv")
)


class CustomMDTitleBarButton(MDIconButton, HoverBehavior):
    default_bg_color = StringProperty()

    def on_enter(self):
        super().on_enter()

        self.default_bg_color = "#fffcf4"

        if self.icon == 'close-circle-outline':
            self.md_bg_color = '#ff000080'
        elif self.icon in ('window-minimize', 'window-restore'):
            self.md_bg_color = '#e4e4e4'

        Window.set_system_cursor("hand")

    def on_leave(self):
        super().on_leave()

        self.md_bg_color = self.default_bg_color

        Window.set_system_cursor("arrow")

    def on_press(self):
        super().on_press()

        Window.set_system_cursor("arrow")


class MDTitleBar(MDBoxLayout):
    title_color = ListProperty()
    """
    :attr:`title_color` is an :class:`~kivy.properties.ListProperty`
    and defaults to `[]`.
    """

    title_halign = StringProperty('left')
    """
    :attr:`title_halign` is an :class:`~kivy.properties.StringProperty`
    and defaults to `left`.
    """

    separator = BooleanProperty(True)
    """
    :attr:`title_color` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `True`, if `False` separator will be delete.
    """

    icon = StringProperty(
        os.path.join(os.path.dirname(kivy.__file__), 'data', 'logo', 'kivy-icon-64.png'),
        allownone=True
    )
    """
    :attr:`icon` is an :class:`~kivy.properties.StringProperty`
    and defaults to `kivy-icon-64.png`, `None` allowed.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        App.get_running_app().bind(icon=self._change_icon)
        self.window_size = None, None

        self._set_custom_titlebar()
        Clock.schedule_once(self._remove_separator)

    def _set_custom_titlebar(self):
        if DEVICE_TYPE == 'desktop':
            if not Window.custom_titlebar:
                Window.custom_titlebar = True

                self.md_bg_color = '#fffcf4'

                if Window.set_custom_titlebar(self):
                    return
            else:
                Logger.warning("Window: titlebar already added")
                return

        Clock.schedule_once(lambda dt: self._rm_widget())
        Logger.error("Window: setting custom titlebar Not allowed on this system")

    def _rm_widget(self):
        self.clear_widgets()
        self.height = 0

    def _remove_separator(self, dt: float):
        if not self.separator:
            self.remove_widget(self.ids.separator)

    def _change_icon(self, inst, icon: str):
        """
        if `MDTitleBar` icon is `None`, so the change in the application `icon` should not be reflected on the widget
        """

        if self.icon:
            self.icon = icon

    @staticmethod
    def roll_up(inst):
        inst.anim_complete()
        Window.minimize()

    def restore(self, inst):
        inst.anim_complete()

        if all(not x for x in self.window_size):
            Window.maximize()
            self.window_size = Window.size
        else:
            if Window.size == self.window_size:
                Window.restore()
            else:
                Window.maximize()
                self.window_size = Window.size


if __name__ == '__main__':
    from kivymd.app import MDApp
    from kivy.lang.builder import Builder

    KV = """
MDScreen:
    MDTitleBar:
        id: title_bar

    MDTopAppBar:
        id: toolbar
        title: "MDTopAppBar"
        size_hint_y: None
        y: title_bar.y - self.height

    ScrollView:
        id: scroll_view
        size_hint: (None, None)
        size: (root.width, root.height - title_bar.height - toolbar.height - dp(10))
        always_overscroll: False

        MDBoxLayout:
            orientation: 'vertical'
            adaptive_height: True
            padding: dp(0), max(scroll_view.height / 2 - primary_color_btn.height - dp(5), dp(0)), dp(0), dp(0)
            spacing: dp(10)

            MDRaisedButton:
                id: primary_color_btn
                text: "Update primary color"
                pos_hint: {"center_x": .5}
                on_release: app.update_color()

            MDRaisedButton:
                text: "Update theme"
                pos_hint: {"center_x": .5}
                on_release: app.change_theme()
    """

    colors = ['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue', 'Cyan', 'Teal', 'Green',
              'LightGreen',
              'Lime', 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']


    class CustomTitleBar(MDApp):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.colors = colors.copy()
            self.screen = Builder.load_string(KV)

            self.title = "My App"
            self.icon = r'F:\Coding_Win\AgroUAV_Control\agro-uav-app\Libs\title-bar-production-fork\examples\full_example\icon.png'

        def build(self):
            return self.screen

        def update_color(self):
            self.colors.remove(self.theme_cls.primary_palette)

            if not self.colors:
                self.colors = colors.copy()

            self.theme_cls.primary_palette = self.colors[0]

        def change_theme(self):
            if self.theme_cls.theme_style == 'Dark':
                self.theme_cls.theme_style = 'Light'
            else:
                self.theme_cls.theme_style = 'Dark'


    CustomTitleBar().run()
