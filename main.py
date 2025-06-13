import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from UI import MainWindow
from AbilityWidget import AbilityWidget
from MoveWidget import MoveWidget
from PokemonWidget import PokemonWidget
from ItemWidget import ItemWidget


class MyMainWindow(QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.move_list_window = None
        self.pokemon_list_window = None  # 初始化为 None，用于存储 PokemonList 窗口实例
        self.ability_list_window = None
        self.item_list_window = None
        self.setupUi(self)

        # 为 action 添加触发事件
        self.action_52poke.triggered.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://wiki.52poke.com/wiki/%E4%B8%BB%E9%A1%B5")))
        self.action_wiki.triggered.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://pokemonreloaded.fandom.com/es/wiki/Wiki_PokemonReloaded")))
        self.action_starter.triggered.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://pokemonreloaded.fandom.com/es/wiki/Pok%C3%A9mon_inicial")))
        self.action_unique.triggered.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://pokemonreloaded.fandom.com/es/wiki/Pok%C3%A9mon_%C3%BAnicos")))
        self.action_legend.triggered.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://pokemonreloaded.fandom.com/es/wiki/Localizaci%C3%B3n_de_Pok%C3%A9mon_Legendarios_y_Singulares")))
        self.action_ultra.triggered.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://pokemonreloaded.fandom.com/es/wiki/Localizaci%C3%B3n_de_Ultraentes")))
        self.action_process_video.triggered.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://www.bilibili.com/list/2906344?sid=4539569&spm_id_from=333.999.0.0&desc=1&oid=113672785497909&bvid=BV1nskwYXEFz")))
        self.action_process_1.triggered.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://pokemonreloaded.fandom.com/es/wiki/Gu%C3%ADa_de_Pok%C3%A9mon_Reloaded")))
        self.action_process_2.triggered.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://pokemonreloaded.fandom.com/es/wiki/Pok%C3%A9mon_Reloaded:_Despu%C3%A9s_de_la_Liga")))
        self.action_process_3.triggered.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://pokemonreloaded.fandom.com/es/wiki/Pok%C3%A9mon_Reloaded:_Despu%C3%A9s_del_Frente")))
        self.action_egg_1.triggered.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://b23.tv/F0oVU5o")))
        self.action_egg_2.triggered.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://b23.tv/qvfgyhF")))
        self.action_character_video.triggered.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://b23.tv/PDEzha6")))
        self.action_ZCrystal_paper.triggered.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://b23.tv/RLt1YYn")))
        self.action_ZCrystal_video.triggered.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://b23.tv/nM1XHIY")))

        # 绑定按钮点击事件
        self.Button_Pokemon.clicked.connect(self.open_pokemon_list)
        self.Button_Move.clicked.connect(self.open_move_list)
        self.Button_Ability.clicked.connect(self.open_ability_list)
        self.Button_Item.clicked.connect(self.open_item_list)

    def open_pokemon_list(self):
        """打开宝可梦列表界面"""
        if self.pokemon_list_window and self.pokemon_list_window.pokemon_list:
            self.pokemon_list_window.raise_()  # 将窗口置顶
            self.pokemon_list_window.activateWindow()  # 激活窗口，使其获得焦点
        else:
            self.pokemon_list_window = None
            self.pokemon_list_window = PokemonWidget()
            self.pokemon_list_window.show()

    def open_move_list(self):
        """打开招式列表界面"""
        if self.move_list_window and self.move_list_window.move_list:
            self.move_list_window.raise_()  # 将窗口置顶
            self.move_list_window.activateWindow()  # 激活窗口，使其获得焦点
        else:
            self.move_list_window = None
            self.move_list_window = MoveWidget()
            self.move_list_window.show()

    def open_ability_list(self):
        """打开特性列表界面"""
        if self.ability_list_window and self.ability_list_window.ability_list:
            self.ability_list_window.raise_()  # 将窗口置顶
            self.ability_list_window.activateWindow()  # 激活窗口，使其获得焦点
        else:
            self.ability_list_window = None
            self.ability_list_window = AbilityWidget()
            self.ability_list_window.show()   
            
    def open_item_list(self):
        """打开特性列表界面"""
        if self.item_list_window and self.item_list_window.item_list:
            self.item_list_window.raise_()  # 将窗口置顶
            self.item_list_window.activateWindow()  # 激活窗口，使其获得焦点
        else:
            self.item_list_window = None
            self.item_list_window = ItemWidget()
            self.item_list_window.show() 

    def closeEvent(self, event):
        """重写关闭事件"""
        if self.pokemon_list_window:  # 如果 PokemonList 窗口存在
            self.pokemon_list_window.close()  # 关闭 PokemonList 窗口
        if self.move_list_window:
            self.move_list_window.close()
        if self.ability_list_window:
            self.ability_list_window.close()
        if self.item_list_window:
            self.item_list_window.close()
        event.accept()  # 确保 MainWindow 也可以正常关闭


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MyMainWindow()  # 创建主窗口实例
    mainWindow.show()  # 显示主窗口
    sys.exit(app.exec_())
