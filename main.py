import json
import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, QGraphicsScene, QMainWindow
from PyQt5.QtGui import QIcon, QPixmap, QColor, QDesktopServices, QFont
from PyQt5.QtCore import Qt, QSize, QUrl, QTimer
from res.UI import MainWindow, PokemonList, MoveList, AbilityList


def resource_path(relative_path):
    """获取资源文件的绝对路径，适用于打包后的程序"""
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def get_color_with_type(type):
    colors = {
        "一般": "color: rgb(159,161,159);",
        "火": "color: rgb(230,40,41);",
        "水": "color: rgb(41,128,239);",
        "电": "color: rgb(250,192,0);",
        "草": "color: rgb(63,161,41);",
        "冰": "color: rgb(63,216,255);",
        "格斗": "color: rgb(255,128,0);",
        "毒": "color: rgb(145,65,203);",
        "地面": "color: rgb(145,81,33);",
        "飞行": "color: rgb(129,185,239);",
        "超能力": "color: rgb(239,65,121);",
        "虫": "color: rgb(145,161,25);",
        "岩石": "color: rgb(175,169,129);",
        "幽灵": "color: rgb(112,65,112);",
        "龙": "color: rgb(80,96,225);",
        "恶": "color: rgb(80,65,63);",
        "钢": "color: rgb(96,161,184);",
        "妖精": "color: rgb(239,112,239);",
        "？": "color: rgb(68,104,94);"
    }
    return colors.get(type, "color: black;")

class IconTableWidgetItem(QTableWidgetItem):
    """自定义的 QTableWidgetItem，用于按属性名称排序"""
    def __init__(self, icon, icon_name):
        super().__init__()
        self.setIcon(icon)  # 设置图标
        self.icon_name = icon_name  # 保存属性名称作为排序键

    def __lt__(self, other):
        """重写小于比较方法，按属性名称排序"""
        if isinstance(other, IconTableWidgetItem):
            # 如果当前项或对方项为空，将空值视为排序的最低优先级
            if not self.icon_name:
                return False
            if not other.icon_name:
                return True
            return self.icon_name < other.icon_name
        return super().__lt__(other)

class IntTableWidgetItem(QTableWidgetItem):
    """自定义的 QTableWidgetItem，用于按整数排序"""

    def __init__(self, value):
        super().__init__(str(value))  # 将值存储为字符串，但保留整数的比较规则

    def __lt__(self, other):
        """重写小于比较方法，按整数比较"""
        if isinstance(other, IntTableWidgetItem):
            # 将字符串转换为整数进行比较，将“-”视为0
            self_value = self.text() if self.text() != '变化' else 0
            self_value = -1 if self.text() == '—' else self_value
            other_value = other.text() if other.text() != '变化' else 0
            other_value = -1 if other.text() == '—' else other_value
            return int(self_value) < int(other_value)
        return super().__lt__(other)

class LvTableWidgetItem(QTableWidgetItem):
    """自定义的 QTableWidgetItem，用于按技能学习方式的数值排序"""

    def __init__(self, value):
        super().__init__(str(value))  # 将技能学习方式存储为字符串

    def __lt__(self, other):
        """重写小于比较方法，按技能学习方式的数值比较"""
        if isinstance(other, LvTableWidgetItem):
            # 计算技能学习方式的数值
            self_value = self.text()
            if "HM" in self_value:
                self_value = int(self_value.replace("HM", "")) + 100
            elif "TM" in self_value:
                self_value = int(self_value.replace("TM", "")) + 200
            elif self_value == "进化":
                self_value = 0
            elif self_value == "教授":
                self_value = 400
            elif self_value == "遗传":
                self_value = 500

            other_value = other.text()
            if "HM" in other_value:
                other_value = int(other_value.replace("HM", "")) + 100
            elif "TM" in other_value:
                other_value = int(other_value.replace("TM", "")) + 200
            elif other_value == "进化":
                other_value = 0
            elif other_value == "教授":
                other_value = 400
            elif other_value == "遗传":
                other_value = 500

            return int(self_value) < int(other_value)
        return super().__lt__(other)


class MyMainWindow(QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.move_list_window = None
        self.pokemon_list_window = None  # 初始化为 None，用于存储 PokemonList 窗口实例
        self.ability_list_window = None
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

    def closeEvent(self, event):
        """重写关闭事件"""
        if self.pokemon_list_window:  # 如果 PokemonList 窗口存在
            self.pokemon_list_window.close()  # 关闭 PokemonList 窗口
        if self.move_list_window:
            self.move_list_window.close()
        if self.ability_list_window:
            self.ability_list_window.close()
        event.accept()  # 确保 MainWindow 也可以正常关闭

class PokemonWidget(QWidget, PokemonList.Ui_Win_PokemonList):
    def __init__(self, parent = None):
        super(PokemonWidget, self).__init__(parent)
        self.pokemon_list = None
        self.ability_data = None
        self.ability_dict = None
        self.evol_chain_data = None
        self.pokemon_moves = None
        self.move_list = None
        self.types_hit_data = None
        self.all_attributes = None
        self.setupUi(self)
        self.init_style()
        self.load_data()
        self.load_pokemon()
        self.showEvent = self.custom_show_event  # 确保在窗口显示后再次更新大小
        self.connect_ability_buttons()  # 连接特性按钮的点击事件
        self.searchPokemon.textChanged.connect(self.filter_table)  # 输入框内容变化时筛选表格
        self.tablePokemon.itemSelectionChanged.connect(self.update_pokemon_info)  # 选中行变化时更新宝可梦信息
        self.tableEvol.itemDoubleClicked.connect(self.on_evolution_chain_double_click)  # 为进化链表格设置双击事件

        # 默认选中第一行
        if self.tablePokemon.rowCount() > 0:
            self.tablePokemon.selectRow(0)

    def custom_show_event(self, event):
        # 调用原始的 showEvent 方法
        super(PokemonWidget, self).showEvent(event)
        # 强制更新大小
        self.update_size()

    def closeEvent(self, event):
        """重写关闭事件，确保父窗口中的引用被清空"""
        self.pokemon_list = None
        self.ability_data = None
        self.ability_dict = None
        self.evol_chain_data = None
        self.pokemon_moves = None
        self.move_list = None
        self.types_hit_data = None
        self.all_attributes = None
        event.accept()  # 确保当前窗口可以正常关闭

    def init_style(self):
        """初始化界面样式设置"""
        # tablePokemon 宝可梦列表 表头设置
        font = QFont()
        font.setBold(True)  # 设置字体为加粗
        font.setPointSize(9)  # 设置字体大小
        pokemon_header = self.tablePokemon.horizontalHeader()
        pokemon_header.setFont(font)  # 应用字体设置
        pokemon_header.setStyleSheet("QHeaderView::section {font-weight: bold; font-size: 9pt;}")
        self.tablePokemon.horizontalHeader().setFixedHeight(50)  # 表头行高为 50

        # tableMove 技能列表
        # 表头设置
        move_header = self.tableMove.horizontalHeader()
        move_header.setFont(font)  # 应用字体设置
        move_header.setStyleSheet("QHeaderView::section {font-weight: bold; font-size: 9pt;}")
        self.tableMove.horizontalHeader().setFixedHeight(40)  # 表头行高为 40
        # 列宽
        self.tableMove.setColumnWidth(2, 90)
        self.tableMove.setColumnWidth(3, 70)

        # tableEvol 进化链表格 设置列宽
        self.tableEvol.setColumnWidth(0, 1)

    def load_data(self):
        """读取Pokemon数据"""
        pokemon_path = resource_path("data/Pokemon_List.json")
        with open(pokemon_path, "r", encoding = "utf-8") as file:
            data = json.load(file)
        self.pokemon_list = data["pokemon"]

        """加载特性数据"""
        ability_path = resource_path("data/Ability.json")
        with open(ability_path, "r", encoding = "utf-8") as file:
            self.ability_data = json.load(file)["ability"]
        self.ability_dict = {ability["id"]: ability for ability in self.ability_data}

        """加载进化链数据"""
        evol_chain_path = resource_path("data/Evol_Chain.json")
        with open(evol_chain_path, "r", encoding = "utf-8") as file:
            data = json.load(file)  # 加载整个 JSON 文件
            self.evol_chain_data = {chain["id"]: chain["chain"] for chain in data["evolutionChain"]}

        """加载技能数据"""
        pokemon_moves_path = resource_path("data/Pokemon_Moves.json")
        with open(pokemon_moves_path, "r", encoding = "utf-8") as file:
            self.pokemon_moves = json.load(file)["pokemon"]

        move_list_path = resource_path("data/Move_List.json")
        with open(move_list_path, "r", encoding = "utf-8") as file:
            self.move_list = {move["id"]: move for move in json.load(file)["skill"]}

        """读取属性克制数据"""
        types_hit_path = resource_path("data/typesHit.json")
        with open(types_hit_path, "r", encoding = "utf-8") as file:
            self.types_hit_data = json.load(file)

        # 定义所有属性
        self.all_attributes = [
            "一般", "毒", "虫", "火", "电", "龙",
            "格斗", "地面", "幽灵", "水", "超能力", "恶",
            "飞行", "岩石", "钢", "草", "冰", "妖精"
        ]

    def on_evolution_chain_double_click(self, item):
        """双击进化链中的宝可梦图标，跳转到对应的宝可梦"""
        col = item.column()  # 获取双击的单元格所在的列

        # 只处理宝可梦图标列（假设宝可梦图标在第1列和第3列）
        if col in [1, 3]:
            # 获取宝可梦的 Pic
            pokemon_pic = item.data(Qt.UserRole)  # 从 UserRole 中获取 Pic
            if not pokemon_pic:
                return  # 如果没有找到 Pic，则直接返回

            # 在主表格中查找对应的宝可梦
            for main_row in range(self.tablePokemon.rowCount()):
                main_pokemon_pic = self.tablePokemon.item(main_row, 1).data(Qt.UserRole)  # 假设 Pic 存储在第1列的 UserRole 中
                if main_pokemon_pic == pokemon_pic:
                    # 清空搜索栏
                    self.searchPokemon.clear()
                    # 选中对应的行
                    self.tablePokemon.selectRow(main_row)
                    # 延迟滚动到选中的行
                    QTimer.singleShot(0, lambda: self.tablePokemon.scrollToItem(self.tablePokemon.item(main_row, 0)))

                    break

    def connect_ability_buttons(self):
        """连接特性按钮的点击事件"""
        self.Button_Ability1.clicked.connect(lambda: self.handle_ability_click(0))
        self.Button_Ability2.clicked.connect(lambda: self.handle_ability_click(1))
        self.Button_Ability3.clicked.connect(lambda: self.handle_ability_click(2))
        self.Button_Ability4.clicked.connect(lambda: self.handle_ability_click(3))

    def handle_ability_click(self, index):
        """处理特性按钮点击事件"""
        selected_row = self.tablePokemon.currentRow()
        if selected_row != -1:
            pic = self.tablePokemon.item(selected_row, 1).data(Qt.UserRole)
            pokemon = next((p for p in self.pokemon_list if p["Pic"] == pic), None)
            ability_id = pokemon["Ability"][index]
            self.update_type_def(pokemon["Type"], ability_id)  # 更新属性抗性表

    def load_pokemon(self):
        """加载宝可梦列表"""
        self.tablePokemon.setRowCount(len(self.pokemon_list))

        for row, pokemon in enumerate(self.pokemon_list):
            self.tablePokemon.setRowHeight(row, 65)  # 所有行高为 65

            national_code = int(pokemon["NationalCode"])
            name = pokemon["cName"]
            types = pokemon["Type"]
            hp, attack, defense, special_attack, special_defense, speed, total = pokemon["Stats"]

            # 设置图标
            icon_name = pokemon["Pic"]
            icon_path = resource_path(f"res/pkmn_icon/{icon_name}.png")  # 图标文件路径
            # 设置图标大小
            pixmap = QPixmap(icon_path)
            pixmap = pixmap.scaled(QSize(60, 60), Qt.KeepAspectRatio, Qt.SmoothTransformation)  # 统一图标大小
            icon = QIcon(pixmap)
            icon_size = QSize(60, 60)  # 设置图标大小为 60x60 像素
            self.tablePokemon.setIconSize(icon_size)  # 设置表格的图标大小
            icon_item = QTableWidgetItem()
            icon_item.setIcon(icon)
            icon_item.setData(Qt.UserRole, icon_name)  # 存储 Pic
            self.tablePokemon.setItem(row, 1, icon_item)  # 图标列

            # 属性1
            type_size = QSize(80, 50)
            self.tablePokemon.setIconSize(type_size)
            type1 = types[0]
            type1_path = resource_path(f"res/type/{type1}.png")
            type1_pixmap = QPixmap(type1_path)
            type1_pixmap = type1_pixmap.scaled(QSize(80, 50), Qt.KeepAspectRatio, Qt.SmoothTransformation)  # 统一图标大小
            type1_icon = QIcon(type1_pixmap)
            type1_item = IconTableWidgetItem(type1_icon, type1)  # 使用自定义的 TypeTableWidgetItem
            self.tablePokemon.setItem(row, 3, type1_item)  # 属性1 列

            # 属性2
            type2 = pokemon["Type"][1] if len(pokemon["Type"]) > 1 else ""
            type2_path = resource_path(f"res/type/{type2}.png") if type2 else ""
            type2_pixmap = QPixmap(type2_path) if type2 else QPixmap()
            type2_icon = QIcon(type2_pixmap)
            type2_item = IconTableWidgetItem(type2_icon, type2)  # 使用自定义的 TypeTableWidgetItem
            self.tablePokemon.setItem(row, 4, type2_item)  # 属性2 列

            name_item = QTableWidgetItem("    " + name)
            name_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 名字靠左对齐，垂直居中
            self.tablePokemon.setItem(row, 2, name_item)  # 名字

            # 设置表格数据
            self.tablePokemon.setItem(row, 0, IntTableWidgetItem(national_code))  # 图鉴编号
            self.tablePokemon.setItem(row, 5, IntTableWidgetItem(hp))  # HP
            self.tablePokemon.setItem(row, 6, IntTableWidgetItem(attack))  # 攻击
            self.tablePokemon.setItem(row, 7, IntTableWidgetItem(defense))  # 防御
            self.tablePokemon.setItem(row, 8, IntTableWidgetItem(special_attack))  # 特攻
            self.tablePokemon.setItem(row, 9, IntTableWidgetItem(special_defense))  # 特防
            self.tablePokemon.setItem(row, 10, IntTableWidgetItem(speed))  # 速度
            self.tablePokemon.setItem(row, 11, IntTableWidgetItem(total))  # 合计

        # 设置其他列居中
        for col in range(12):
            for row in range(len(self.pokemon_list)):
                item = self.tablePokemon.item(row, col)
                if col != 2:  # 排除名字列
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)  # 水平居中，垂直居中

    def filter_table(self):
        """根据输入框内容筛选表格"""
        search_text = self.searchPokemon.text().lower()
        for row, pokemon in enumerate(self.pokemon_list):
            # 获取当前行的 Pic
            pic = self.tablePokemon.item(row, 1).data(Qt.UserRole)
            # 通过 Pic 查找对应的宝可梦数据
            pokemon = next((p for p in self.pokemon_list if p["Pic"] == pic), None)

            # 提取宝可梦的属性
            types = pokemon["Type"]
            type1 = types[0].lower() if types else ""
            type2 = types[1].lower() if types[1] else ""

            # 搜索图鉴编号、名字、英文名
            if (search_text in str(pokemon["NationalCode"]).lower() or
                    search_text in pokemon["cName"].lower() or
                    search_text in pokemon.get("oldName", "").lower() or
                    search_text in pokemon["eName"].lower() or
                    search_text in pokemon["Region"].lower() or
                    search_text in type1 or  # 模糊匹配单属性
                    search_text in type2 or  # 模糊匹配单属性
                    search_text in f"{type1}{type2}" or  # 模糊匹配双属性
                    search_text in f"{type2}{type1}"):  # 模糊匹配双属性
                self.tablePokemon.setRowHidden(row, False)
            else:
                self.tablePokemon.setRowHidden(row, True)

    def update_basic(self, pokemon):
        """更新基本信息和图片"""
        name = pokemon.get("cName", "")
        eName = pokemon.get("eName", "")
        Height = str(pokemon.get("Height"))
        Weight = str(pokemon.get("Weight"))
        Region = pokemon.get("Region", "")
        Sex = pokemon.get("Sex", "")

        description = pokemon.get("Description", "暂无描述")  # 获取描述，如果没有则显示默认文本
        species = pokemon.get("Species", "")
        description = name + '，' + species + '，' + description
        Height = "身高：" + Height + " m"
        Weight = "体重：" + Weight + " kg"
        Region = "地区：" + Region
        Sex = "雌雄比例：" + Sex

        # 更新图片
        file_name = pokemon["Pic"]
        icon_path = resource_path(f"res/pkmn_pic/{file_name}.png")
        pixmap = QPixmap(icon_path)
        size = min(self.PokemonPic.width(), self.PokemonPic.height())
        pixmap = pixmap.scaled(QSize(size - 20, size - 20), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.PokemonPic.setScene(QGraphicsScene())
        self.PokemonPic.scene().addPixmap(pixmap)

        # 更新信息、描述
        self.Description.setPlainText(f"{description}")
        self.cName.setText(f"{name}")
        self.eName.setText(f"{eName}")
        self.Height.setText(f"{Height}")
        self.Weight.setText(f"{Weight}")
        self.Region.setText(f"{Region}")
        self.sex.setText(f"{Sex}")

        # 根据属性设置名字颜色
        color = get_color_with_type(pokemon["Type"][0])
        self.cName.setStyleSheet(color)
        self.eName.setStyleSheet(color)

        # 设置字体大小变化
        info_height = self.groupBox_2.height()
        font_size = int(info_height / 29)
        if font_size < 8:
            font_size = 8
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(font_size)
        self.Height.setFont(font)
        self.Weight.setFont(font)
        self.Region.setFont(font)
        self.sex.setFont(font)
        font.setPointSize(font_size + 1)
        self.Description.setFont(font)
        font.setBold(True)
        self.eName.setFont(font)
        font.setPointSize(font_size + 2)
        self.cName.setFont(font)

    def update_evolution_chain(self, pokemon):
        """更新进化链"""
        evolution_chain_id = pokemon["EvolutionChain"]
        evolution_chain = self.evol_chain_data.get(evolution_chain_id)

        self.tableEvol.setRowCount(0)  # 如果没有找到进化链，清空表格

        self.tableEvol.setRowCount(len(evolution_chain))  # 设置表格行数

        # 获取表格的宽度和高度
        table_width = self.tableEvol.width()
        table_height = self.tableEvol.height()
        # 计算行高和列宽
        row_height = (table_height // 3) - 1
        icon_size = int(row_height - 10)

        self.tableEvol.setColumnWidth(1, row_height + 15)
        self.tableEvol.setColumnWidth(2, row_height + 5)
        self.tableEvol.setColumnWidth(3, row_height + 30)
        sun_width = 0
        for i in range(4):
            sun_width += self.tableEvol.columnWidth(i)
        last_width = table_width - sun_width - 30
        self.tableEvol.setColumnWidth(4, last_width)

        for row, chain in enumerate(evolution_chain):
            self.tableEvol.setRowHeight(row, row_height)  # 设置行高

            # 设置图标
            from_id = chain["from"]
            to_id = chain["to"]
            evol = chain["icon"]
            from_icon_path = resource_path(f"res/pkmn_icon/{from_id}.png")  # 图标文件路径
            to_icon_path = resource_path(f"res/pkmn_icon/{to_id}.png")  # 图标文件路径
            arrow_icon_path = resource_path("res/icon/right.png")  # 图标文件路径
            evol_icon_path = resource_path(f"res/evol/{evol}.png")  # 图标文件路径
            # 设置图标大小
            from_pixmap = QPixmap(from_icon_path)
            from_pixmap = from_pixmap.scaled(QSize(icon_size, icon_size), Qt.KeepAspectRatio, Qt.SmoothTransformation)  # 统一图标大小
            from_icon = QIcon(from_pixmap)

            arrow_pixmap = QPixmap(arrow_icon_path)
            arrow_pixmap = arrow_pixmap.scaled(QSize(icon_size - 10, icon_size - 10), Qt.KeepAspectRatio, Qt.SmoothTransformation)  # 统一图标大小
            arrow_icon = QIcon(arrow_pixmap)

            to_pixmap = QPixmap(to_icon_path)
            to_pixmap = to_pixmap.scaled(QSize(icon_size, icon_size), Qt.KeepAspectRatio, Qt.SmoothTransformation)  # 统一图标大小
            to_icon = QIcon(to_pixmap)

            evol_pixmap = QPixmap(evol_icon_path)
            evol_pixmap = evol_pixmap.scaled(QSize(icon_size - 15, icon_size - 15), Qt.KeepAspectRatio, Qt.SmoothTransformation)  # 统一图标大小
            evol_icon = QIcon(evol_pixmap)

            size = QSize(icon_size, icon_size)  # 设置图标大小为 60x60 像素
            self.tableEvol.setIconSize(size)  # 设置表格的图标大小

            icon_item = QTableWidgetItem()
            icon_item.setIcon(from_icon)
            icon_item.setData(Qt.UserRole, from_id)
            from_pokemon = next((p for p in self.pokemon_list if p["Pic"] == from_id), None)
            icon_item.setToolTip(from_pokemon["cName"])
            self.tableEvol.setItem(row, 1, icon_item)

            icon_item = QTableWidgetItem()
            icon_item.setIcon(to_icon)
            icon_item.setData(Qt.UserRole, to_id)
            to_pokemon = next((p for p in self.pokemon_list if p["Pic"] == to_id), None)
            icon_item.setToolTip(to_pokemon["cName"])
            self.tableEvol.setItem(row, 3, icon_item)

            # 设置进化箭头
            arrow_item = QTableWidgetItem()
            arrow_item.setIcon(arrow_icon)
            self.tableEvol.setItem(row, 2, arrow_item)

            # 设置进化条件
            condition_item = QTableWidgetItem("  " + chain["str"])
            condition_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            condition_item.setIcon(evol_icon)
            self.tableEvol.setItem(row, 4, condition_item)

    def update_moves(self, pokemon):
        """更新技能列表"""
        pokemon_id = str(pokemon["NationalCode"])  # 假设图鉴编号是唯一的标识
        pokemon_pic = str(pokemon["Pic"])
        if pokemon_pic in ["12_P","19_A","20_A","26_A","26_Y"]:
            if pokemon_pic == "26_Y":
                pokemon_id = "26_A"
            else:
                pokemon_id = pokemon_pic

        # 清空表格
        self.tableMove.setRowCount(0)
        # 查找该宝可梦的技能列表
        pokemon_moves = next((pm for pm in self.pokemon_moves if pm["id"] == pokemon_id), None)
        if not pokemon_moves:
            return

        # 获取技能信息
        moves = []
        for move_type in ["Level", "TM", "Tutor", "Egg"]:
            moves.extend(pokemon_moves.get(move_type, []))

        # 设置表格行数
        self.tableMove.setRowCount(len(moves))

        table_width = self.tableMove.width()
        name_width = int((table_width - 160) * 0.39)
        other_width = int((table_width - 160 - name_width) / 3 - 10)

        self.tableMove.setColumnWidth(0, other_width)
        self.tableMove.setColumnWidth(1, name_width)
        self.tableMove.setColumnWidth(4, other_width)
        self.tableMove.setColumnWidth(5, other_width)

        for row, move in enumerate(moves):
            self.tableMove.setRowHeight(row, 48)  # 每行高度为45

            move_id = move["skill"]
            move_info = self.move_list.get(move_id, {})
            condition = move["condition"]

            # 填充表格
            self.tableMove.setItem(row, 0, QTableWidgetItem(condition))  # 技能学习方式
            self.tableMove.setItem(row, 4, QTableWidgetItem(move_info["power"]))  # 威力
            self.tableMove.setItem(row, 5, QTableWidgetItem(move_info["pp"]))  # PP

            # 技能名称
            move_name = "    " + move_info["cName"]
            item = QTableWidgetItem(move_name)
            item.setToolTip(move_info["explain"])
            item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 名字靠左对齐，垂直居中
            self.tableMove.setItem(row, 1, item)

            # 设置图标
            move_type = move_info["type"]
            move_attack = move_info["attack"]
            move_type_path = resource_path(f"res/type/{move_type}.png")  # 图标文件路径
            move_attack_path = resource_path(f"res/attack/{move_attack}.png")  # 图标文件路径

            # 设置图标大小
            move_type_pixmap = QPixmap(move_type_path)
            move_type_pixmap = move_type_pixmap.scaled(QSize(80, 50), Qt.KeepAspectRatio, Qt.SmoothTransformation)  # 统一图标大小
            move_type_icon = QIcon(move_type_pixmap)

            move_attack_pixmap = QPixmap(move_attack_path)
            move_attack_pixmap = move_attack_pixmap.scaled(QSize(60, 50), Qt.KeepAspectRatio, Qt.SmoothTransformation)  # 统一图标大小
            move_attack_icon = QIcon(move_attack_pixmap)

            icon_size = QSize(80, 50)  # 设置图标大小
            self.tableMove.setIconSize(icon_size)  # 设置表格的图标大小

            icon_item = QTableWidgetItem()
            icon_item.setIcon(move_type_icon)
            icon_item.setToolTip(move_type)
            self.tableMove.setItem(row, 2, icon_item)   # 属性

            icon_item = QTableWidgetItem()
            icon_item.setIcon(move_attack_icon)
            icon_item.setToolTip(move_attack)
            self.tableMove.setItem(row, 3, icon_item)   # 分类

            # 设置其他列居中
        for col in range(6):
            for row in range(len(moves)):
                item = self.tableMove.item(row, col)
                if col != 1:  # 排除名字列
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)  # 水平居中，垂直居中

    def update_abilities(self, pokemon):
        """更新特性按钮"""
        abilities = pokemon["Ability"]
        for i in range(4):  # 遍历4个特性按钮
            ability_id = abilities[i]
            button = getattr(self, f"Button_Ability{i + 1}")  # 获取对应的按钮对象
            if ability_id is None:
                button.setText("")  # 显示为空字符串
                button.setToolTip("")  # 设置特性描述为提示信息
                button.setEnabled(False)  # 设置按钮为不可点击状态
            else:
                ability_info = self.ability_dict.get(ability_id)
                button.setText(ability_info["cName"])  # 显示特性名称
                button.setToolTip(ability_info["description"])  # 设置特性描述为提示信息
                button.setEnabled(True)  # 设置按钮为可点击状态

            # 如果特性会改变属性抗性，则变为红色
            if ability_id in [10, 11, 18, 25, 26, 31, 47, 78, 85, 87, 111, 114, 116, 157, 199, 218, 232, 273, 297]:
                font_style = """
                    QPushButton {
                        font: bold 9pt "Microsoft YaHei UI";
                        color: red;  /* 字体颜色为红色 */
                    }
                """
            else:
                font_style = """
                    QPushButton {
                        font: bold 9pt "Microsoft YaHei UI";
                        color: rgb(0, 0, 0);  /* 字体颜色为黑色 */
                    }
                """
            button.setStyleSheet(font_style)

        # 自动触发特性1按钮的点击事件，更新属性抗性表
        self.handle_ability_click(0)

    def update_type_def(self, types, ability_id = None):
        """根据宝可梦的属性，计算其对每一种属性的抗性，并显示在type_def表格中"""
        # 获取表格的宽度和高度
        type_def_width = self.type_def.width()
        type_def_height = self.type_def.height()
        # 计算行高和列宽
        row_height = type_def_height // 3
        col_width = type_def_width // 6
        # 设置行高
        for row in range(self.type_def.rowCount()):
            self.type_def.setRowHeight(row, row_height)
        # 设置列宽
        for col in range(self.type_def.columnCount()):
            self.type_def.setColumnWidth(col, col_width)

        # 遍历所有属性，计算抗性并设置图标和倍率
        for index, attribute in enumerate(self.all_attributes):
            row = index // 6  # 计算行号
            col = index % 6  # 计算列号

            # 计算抗性
            resistance = 1
            if types[1]:
                resistance = self.types_hit_data[attribute][types[0]] * self.types_hit_data[attribute][types[1]]
            else:
                resistance = self.types_hit_data[attribute][types[0]]

            # 特性影响
            if ability_id == 10 and attribute == "电":    # 蓄电
                resistance = 0
            elif ability_id == 11 and attribute == "水":    # 蓄水
                resistance = 0
            elif ability_id == 18 and attribute == "火":    # 引火
                resistance = 0
            elif ability_id == 25 and resistance <= 1:    # 神奇守护
                resistance = 0
            elif ability_id == 26 and attribute == "地面":    # 飘浮
                resistance = 0
            elif ability_id == 31 and attribute == "电":    # 避雷针
                resistance = 0
            elif ability_id == 47 and (attribute == "火" or attribute == "冰"):    # 厚脂肪
                resistance *= 0.5
            elif ability_id == 78 and attribute == "电":    # 电气引擎
                resistance = 0
            elif ability_id == 85 and attribute == "火":    # 耐热
                resistance *= 0.5
            elif ability_id == 87:    # 干燥皮肤
                if attribute == "水":
                    resistance = 0
                elif attribute == "火":
                    resistance *= 1.25
            elif (ability_id == 111 or ability_id == 116 or ability_id == 232) and resistance > 1:    # 过滤、坚硬岩石、棱镜装甲
                resistance *= 0.75
            elif ability_id == 114 and attribute == "水":  # 引水
                resistance = 0
            elif ability_id == 157 and attribute == "草":  # 食草
                resistance = 0
            elif ability_id == 199 and attribute == "火":  # 水泡
                resistance *= 0.5
            elif ability_id == 218 and attribute == "火":  # 毛茸茸
                resistance *= 2
            elif ability_id == 273 and attribute == "火":  # 焦香之躯
                resistance = 0
            elif ability_id == 297 and attribute == "地面":  # 食土
                resistance = 0

            # 创建图标
            icon_width = int(type_def_width / 6 * 0.55)
            icon_height = int(type_def_height / 3)

            icon_path = resource_path(f"res/type/{attribute}.png")  # 图标文件路径
            icon_pixmap = QPixmap(icon_path)
            icon_pixmap = icon_pixmap.scaled(QSize(icon_width, icon_height), Qt.KeepAspectRatio, Qt.SmoothTransformation)  # 统一图标大小
            icon = QIcon(icon_pixmap)
            icon_size = QSize(icon_width, icon_height)
            self.type_def.setIconSize(icon_size)

            # 创建表格项
            item = QTableWidgetItem()
            item.setIcon(icon)  # 设置图标

            # 显示抗性倍率
            resistance_text = f"{resistance:.2f}".rstrip('0').rstrip('.')
            item.setText(resistance_text)  # 设置文本
            item.setTextAlignment(Qt.AlignCenter)  # 文本居中显示

            font = QFont()
            font.setBold(True)  # 设置字体为加粗
            font.setPointSize(int(type_def_width / 86))  # 设置字体大小
            self.type_def.setFont(font)  # 应用字体到表格

            # 设置文本颜色
            if resistance_text == "0":
                item.setForeground(Qt.black)  # 黑色表示免疫
            elif resistance < 1:
                item.setForeground(Qt.blue)  # 蓝色表示抵抗
            elif resistance > 1:
                item.setForeground(Qt.red)  # 红色表示被克
            else:
                item.setForeground(QColor(0, 153, 0))  # 默认绿色

            # 设置到表格中
            self.type_def.setItem(row, col, item)

    def update_pokemon_info(self):
        """更新选中的宝可梦信息"""
        selected_row = self.tablePokemon.currentRow()
        if selected_row != -1:
            # 获取当前行的唯一标识（图鉴编号）
            pic = self.tablePokemon.item(selected_row, 1).data(Qt.UserRole)
            # 在 self.pokemon_list 中查找对应的宝可梦数据
            pokemon = next((p for p in self.pokemon_list if p["Pic"] == pic), None)

            self.update_basic(pokemon)  # 更新基本信息
            self.update_evolution_chain(pokemon)  # 更新进化链表格
            self.update_moves(pokemon)  # 更新技能表格
            self.update_abilities(pokemon)  # 更新特性和属性抗性表
            self.update_type_def(pokemon["Type"], pokemon["Ability"][0])  # 更新属性抗性表

    def update_size(self):
        """动态更新表格的行高和列宽"""
        # 宝可梦列表
        self.tablePokemon.resizeColumnsToContents()  # 其他列自适应宽度
        pokemon_list_width = self.tablePokemon.width()
        self.tablePokemon.setColumnWidth(2, int(pokemon_list_width * 0.23))     # 名字列
        width_1_5 = 0
        for i in range(5):
            width_1_5 += self.tablePokemon.columnWidth(i)
        pokemon_list_col_width = (pokemon_list_width - width_1_5) // 7
        for col in range(5, 12):
            self.tablePokemon.setColumnWidth(col, pokemon_list_col_width - 4)

        self.update_pokemon_info()

    def resizeEvent(self, event):
        """重写窗口大小改变事件"""
        super(PokemonWidget, self).resizeEvent(event)
        # 每次窗口大小改变时，更新属性抗性表的大小
        self.update_size()

class MoveWidget(QWidget, MoveList.Ui_Win_MoveList):
    def __init__(self, parent = None):
        super(MoveWidget, self).__init__(parent)
        self.move_list = None
        self.pokemon_moves = None
        self.pokemon_list = None
        self.setupUi(self)
        self.init_style()
        self.load_data()
        self.load_move()
        self.showEvent = self.custom_show_event  # 确保在窗口显示后再次更新大小
        self.searchMove.textChanged.connect(self.filter_table)  # 输入框内容变化时筛选表格
        self.tableMove.itemSelectionChanged.connect(self.update_move_info)  # 选中行变化时更新宝可梦信息

        # 默认选中第一行
        if self.tableMove.rowCount() > 0:
            self.tableMove.selectRow(0)

    def custom_show_event(self, event):
        # 调用原始的 showEvent 方法
        super(MoveWidget, self).showEvent(event)
        # 强制更新大小
        self.update_size()

    def closeEvent(self, event):
        """重写关闭事件，确保父窗口中的引用被清空"""
        self.move_list = None
        self.pokemon_moves = None
        self.pokemon_list = None
        event.accept()  # 确保当前窗口可以正常关闭

    def init_style(self):
        """初始化界面样式设置"""
        # tableMove 技能列表
        # 表头设置
        font = QFont()
        font.setBold(True)  # 设置字体为加粗
        font.setPointSize(9)  # 设置字体大小
        move_header = self.tableMove.horizontalHeader()
        move_header.setFont(font)  # 应用字体设置
        move_header.setStyleSheet("QHeaderView::section {font-weight: bold; font-size: 9pt;}")
        self.tableMove.horizontalHeader().setFixedHeight(50)  # 表头行高为 50

        # tablePokemon 宝可梦列表 表头设置
        pokemon_header = self.tablePokemon.horizontalHeader()
        pokemon_header.setFont(font)  # 应用字体设置
        pokemon_header.setStyleSheet("QHeaderView::section {font-weight: bold; font-size: 9pt;}")
        self.tablePokemon.horizontalHeader().setFixedHeight(40)  # 表头行高为 40

    def load_data(self):
        """读取Pokemon数据"""
        pokemon_path = resource_path("data/Pokemon_List.json")
        with open(pokemon_path, "r", encoding = "utf-8") as file:
            data = json.load(file)
        self.pokemon_list = data["pokemon"]

        """加载技能数据"""
        pokemon_moves_path = resource_path("data/Pokemon_Moves.json")
        with open(pokemon_moves_path, "r", encoding = "utf-8") as file:
            self.pokemon_moves = json.load(file)["pokemon"]

        move_list_path = resource_path("data/Move_List.json")
        with open(move_list_path, "r", encoding = "utf-8") as file:
            data = json.load(file)
        self.move_list = data["skill"]

    def load_move(self):
        """加载招式列表"""
        self.tableMove.setRowCount(len(self.move_list))

        for row, move in enumerate(self.move_list):
            self.tableMove.setRowHeight(row, 60)  # 所有行高为 60

            moveID = move["id"]
            name = move["cName"]
            move_type = move["type"]
            attack = move["attack"]
            power = move["power"]
            pp = move["pp"]

            # 设置图标
            type_path = resource_path(f"res/type/{move_type}.png")
            type_pixmap = QPixmap(type_path)
            type_pixmap = type_pixmap.scaled(QSize(80, 50), Qt.KeepAspectRatio, Qt.SmoothTransformation)  # 统一图标大小
            type_icon = QIcon(type_pixmap)

            attack_path = resource_path(f"res/attack/{attack}.png")
            attack_pixmap = QPixmap(attack_path)
            attack_pixmap = attack_pixmap.scaled(QSize(60, 50), Qt.KeepAspectRatio, Qt.SmoothTransformation)  # 统一图标大小
            attack_icon = QIcon(attack_pixmap)

            icon_size = QSize(80, 50)  # 设置图标大小
            self.tableMove.setIconSize(icon_size)  # 设置表格的图标大小

            icon_item = IconTableWidgetItem(type_icon, move_type)
            self.tableMove.setItem(row, 2, icon_item)  # 属性

            icon_item = IconTableWidgetItem(attack_icon, attack)
            icon_item.setToolTip(attack)
            self.tableMove.setItem(row, 3, icon_item)  # 分类

            name_item = QTableWidgetItem("     " + name)
            name_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 名字靠左对齐，垂直居中
            self.tableMove.setItem(row, 1, name_item)  # 名字

            # 设置表格数据
            self.tableMove.setItem(row, 0, IntTableWidgetItem(moveID))  # 编号
            self.tableMove.setItem(row, 4, IntTableWidgetItem(power))  # 威力
            self.tableMove.setItem(row, 5, IntTableWidgetItem(pp))  # PP

        # 设置其他列居中
        for col in range(6):
            for row in range(len(self.move_list)):
                item = self.tableMove.item(row, col)
                if col != 1:  # 排除名字列
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)  # 水平居中，垂直居中

        self.tableMove.resizeColumnsToContents()

    def filter_table(self):
        """根据输入框内容筛选表格"""
        search_text = self.searchMove.text().lower()
        for row, move in enumerate(self.move_list):
            # 获取当前行的 Pic
            moveID = self.tableMove.item(row, 0).text()
            # 通过 Pic 查找对应的宝可梦数据
            move = next((p for p in self.move_list if p["id"] == moveID), None)

            move_type = move["type"]
            attack = move["attack"]

            # 搜索名字、英文名、属性、分类
            if (search_text in move["cName"].lower() or
                    search_text in move.get("oldName", "").lower() or
                    search_text in move["eName"].lower() or
                    search_text in move_type.lower() or
                    search_text in attack.lower() or
                    search_text in f"{move_type}{attack}" or
                    search_text in f"{attack}{move_type}"):
                self.tableMove.setRowHidden(row, False)
            else:
                self.tableMove.setRowHidden(row, True)

    def update_basic(self, move):
        """更新基本信息和图片"""
        name = move["cName"]
        eName = move["eName"]
        attack = move["attack"]
        power = move["power"]
        pp = move["pp"]
        explain = move["explain"]
        effect = move["effect"]

        attack = "分类：" + attack
        power = "威力：" + power
        pp = "ＰＰ：" + pp
        description = explain + "\n\n" + effect

        # 更新信息、描述
        self.cName.setText(f"{name}")
        self.eName.setText(f"{eName}")
        self.attack.setText(f"{attack}")
        self.Power.setText(f"{power}")
        self.PP.setText(f"{pp}")
        self.Description.setPlainText(f"{description}")

        # 根据属性设置名字颜色
        color = get_color_with_type(move["type"])
        self.cName.setStyleSheet(color)
        self.eName.setStyleSheet(color)
        if move["attack"] == "物理":
            self.attack.setStyleSheet("color: rgb(255,68,2);")
        elif move["attack"] == "特殊":
            self.attack.setStyleSheet("color: rgb(40,97,205);")
        else:
            self.attack.setStyleSheet("color: rgb(154,152,150);")

        # 设置字体大小变化
        info_height = self.groupBox_2.height()
        font_size = int(info_height / 29) + 1
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(font_size)
        self.Power.setFont(font)
        self.PP.setFont(font)
        font.setBold(True)
        self.attack.setFont(font)
        font.setBold(False)
        font.setPointSize(font_size + 1)
        self.Description.setFont(font)
        font.setBold(True)
        self.eName.setFont(font)
        font.setPointSize(font_size + 3)
        self.cName.setFont(font)

    def update_pokemons(self, move):
        """更新技能列表"""
        moveID = move["id"]  # 假设图鉴编号是唯一的标识

        # 禁用排序
        self.tablePokemon.setSortingEnabled(False)

        # 清空表格
        self.tablePokemon.setRowCount(0)

        # 遍历pokemon_moves数据，查找所有能学习该技能的宝可梦
        matching_pokemons = []
        for pokemon in self.pokemon_moves:
            # 检查该宝可梦是否能学习当前技能，并保存匹配的condition
            for move_type in ["Level", "TM", "Tutor", "Egg"]:
                for move in pokemon.get(move_type, []):
                    if move["skill"] == moveID:
                        matching_pokemons.append({
                            "id": pokemon["id"],
                            "condition": move["condition"]
                        })

        # 如果没有找到任何宝可梦
        if not matching_pokemons:
            return

        # 更新表格
        self.tablePokemon.setRowCount(len(matching_pokemons))
        for row, match_pokemon in enumerate(matching_pokemons):
            self.tablePokemon.setRowHeight(row, 55)  # 每行高度为55

            # 获取宝可梦的基本信息
            pokemon = next((p for p in self.pokemon_list if p["Pic"] == match_pokemon["id"]), None)

            national_code = pokemon["NationalCode"]
            name = pokemon["cName"]
            types = pokemon["Type"]

            # 设置图标
            icon_name = pokemon["Pic"]
            icon_path = resource_path(f"res/pkmn_icon/{icon_name}.png")  # 图标文件路径
            # 设置图标大小
            pixmap = QPixmap(icon_path)
            pixmap = pixmap.scaled(QSize(45, 45), Qt.KeepAspectRatio, Qt.SmoothTransformation)  # 统一图标大小
            icon = QIcon(pixmap)
            icon_size = QSize(45, 45)  # 设置图标大小为 45x45 像素
            self.tablePokemon.setIconSize(icon_size)  # 设置表格的图标大小
            icon_item = QTableWidgetItem()
            icon_item.setIcon(icon)
            icon_item.setData(Qt.UserRole, icon_name)  # 存储 Pic
            self.tablePokemon.setItem(row, 1, icon_item)  # 图标列

            # 属性1
            type_size = QSize(80, 50)
            self.tablePokemon.setIconSize(type_size)
            type1 = types[0]
            type1_path = resource_path(f"res/type/{type1}.png")
            type1_pixmap = QPixmap(type1_path)
            type1_pixmap = type1_pixmap.scaled(QSize(80, 50), Qt.KeepAspectRatio, Qt.SmoothTransformation)  # 统一图标大小
            type1_icon = QIcon(type1_pixmap)
            type1_item = IconTableWidgetItem(type1_icon, type1)  # 使用自定义的 TypeTableWidgetItem
            self.tablePokemon.setItem(row, 3, type1_item)  # 属性1 列

            # 属性2
            type2 = pokemon["Type"][1] if len(pokemon["Type"]) > 1 else ""
            type2_path = resource_path(f"res/type/{type2}.png") if type2 else ""
            type2_pixmap = QPixmap(type2_path) if type2 else QPixmap()
            type2_icon = QIcon(type2_pixmap)
            type2_item = IconTableWidgetItem(type2_icon, type2)  # 使用自定义的 TypeTableWidgetItem
            self.tablePokemon.setItem(row, 4, type2_item)  # 属性2 列

            name_item = QTableWidgetItem("    " + name)
            name_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 名字靠左对齐，垂直居中
            self.tablePokemon.setItem(row, 2, name_item)  # 名字

            # 设置表格数据
            self.tablePokemon.setItem(row, 0, IntTableWidgetItem(national_code))  # 图鉴编号

            # 填充表格
            self.tablePokemon.setItem(row, 5, LvTableWidgetItem(match_pokemon["condition"]))  # 技能学习方式

        # 设置其他列居中
        for col in range(6):
            for row in range(len(matching_pokemons)):
                item = self.tablePokemon.item(row, col)
                if col != 2:  # 排除名字列
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)  # 水平居中，垂直居中

        # 重新启用排序
        self.tablePokemon.setSortingEnabled(True)

        self.tablePokemon.resizeColumnsToContents()  # 其他列自适应宽度
        table_list_width = self.tablePokemon.width()
        self.tablePokemon.setColumnWidth(2, int(table_list_width * 0.35))  # 名字列

        width = 0
        for i in range(5):
            width += self.tablePokemon.columnWidth(i)
        table_list_col_width = table_list_width - width
        self.tablePokemon.setColumnWidth(5, table_list_col_width - 30)

    def update_move_info(self):
        """更新选中的招式信息"""
        selected_row = self.tableMove.currentRow()
        if selected_row != -1:
            # 获取当前行的唯一标识（图鉴编号）
            moveID = self.tableMove.item(selected_row, 0).text()
            # 在 self.pokemon_list 中查找对应的宝可梦数据
            move = next((p for p in self.move_list if p["id"] == moveID), None)

            self.update_basic(move)  # 更新基本信息
            self.update_pokemons(move)

    def update_size(self):
        """动态更新表格的行高和列宽"""
        # 宝可梦列表
        self.tableMove.resizeColumnsToContents()  # 其他列自适应宽度
        table_list_width = self.tableMove.width()
        self.tableMove.setColumnWidth(0, int(table_list_width * 0.12))  # 编号列
        self.tableMove.setColumnWidth(1, int(table_list_width * 0.35))  # 名字列

        width = 0
        for i in range(4):
            width += self.tableMove.columnWidth(i)
        table_list_col_width = (table_list_width - width) // 2
        self.tableMove.setColumnWidth(4, table_list_col_width - 15)
        self.tableMove.setColumnWidth(5, table_list_col_width - 15)

        self.update_move_info()

    def resizeEvent(self, event):
        """重写窗口大小改变事件"""
        super(MoveWidget, self).resizeEvent(event)
        # 每次窗口大小改变时，更新属性抗性表的大小
        self.update_size()

class AbilityWidget(QWidget, AbilityList.Ui_Win_AbilityList):
    def __init__(self, parent = None):
        super(AbilityWidget, self).__init__(parent)
        self.ability_list = None
        self.pokemon_list = None
        self.setupUi(self)
        self.init_style()
        self.load_data()
        self.load_ability()
        self.showEvent = self.custom_show_event  # 确保在窗口显示后再次更新大小
        self.searchAbility.textChanged.connect(self.filter_table)  # 输入框内容变化时筛选表格
        self.tableAbility.itemSelectionChanged.connect(self.update_ability_info)  # 选中行变化时更新特性信息
        self.tablePokemon.itemDoubleClicked.connect(self.pokemon_ability_double_click)  # 为宝可梦表格设置双击事件

        # 默认选中第一行
        if self.tableAbility.rowCount() > 0:
            self.tableAbility.selectRow(0)

    def custom_show_event(self, event):
        # 调用原始的 showEvent 方法
        super(AbilityWidget, self).showEvent(event)
        # 强制更新大小
        self.update_size()

    def closeEvent(self, event):
        """重写关闭事件，确保父窗口中的引用被清空"""
        self.ability_list = None
        self.pokemon_list = None
        event.accept()  # 确保当前窗口可以正常关闭

    def init_style(self):
        """初始化界面样式设置"""
        # tableAbility 技能列表
        # 表头设置
        font = QFont()
        font.setBold(True)  # 设置字体为加粗
        font.setPointSize(9)  # 设置字体大小
        ability_header = self.tableAbility.horizontalHeader()
        ability_header.setFont(font)  # 应用字体设置
        ability_header.setStyleSheet("QHeaderView::section {font-weight: bold; font-size: 9pt;}")
        self.tableAbility.horizontalHeader().setFixedHeight(50)  # 表头行高为 50

        # tablePokemon 宝可梦列表 表头设置
        pokemon_header = self.tablePokemon.horizontalHeader()
        pokemon_header.setFont(font)  # 应用字体设置
        pokemon_header.setStyleSheet("QHeaderView::section {font-weight: bold; font-size: 9pt;}")
        self.tablePokemon.horizontalHeader().setFixedHeight(40)  # 表头行高为 40

    def load_data(self):
        """读取Pokemon数据"""
        pokemon_path = resource_path("data/Pokemon_List.json")
        with open(pokemon_path, "r", encoding = "utf-8") as file:
            data = json.load(file)
        self.pokemon_list = data["pokemon"]

        """加载特性数据"""
        ability_list_path = resource_path("data/Ability.json")
        with open(ability_list_path, "r", encoding = "utf-8") as file:
            data = json.load(file)
        self.ability_list = data["ability"]

    def pokemon_ability_double_click(self, item):
        """双击宝可梦列表中的特性，跳转到对应的特性"""
        col = item.column()  # 获取双击的单元格所在的列

        # 只处理特性列
        if col in [5, 6, 7, 8]:
            # 获取特性ID
            abilityID = item.data(Qt.UserRole)  # 从 UserRole 中获取 ID
            if not abilityID:
                return  # 如果没有找到 Pic，则直接返回

            # 在主表格中查找对应的宝可梦
            for main_row in range(self.tableAbility.rowCount()):
                main_abilityID = int(self.tableAbility.item(main_row, 0).text())  # 假设 Pic 存储在第1列的 UserRole 中
                if main_abilityID == abilityID:
                    # 清空搜索栏
                    self.searchAbility.clear()
                    # 选中对应的行
                    self.tableAbility.selectRow(main_row)
                    # 延迟滚动到选中的行
                    QTimer.singleShot(0, lambda: self.tableAbility.scrollToItem(self.tableAbility.item(main_row, 0)))
                    break


    def load_ability(self):
        """加载特性列表"""
        self.tableAbility.setRowCount(len(self.ability_list))

        for row, ability in enumerate(self.ability_list):
            self.tableAbility.setRowHeight(row, 60)  # 所有行高为 60

            abilityID = ability["id"]
            name = ability["cName"]

            # 设置表格数据
            id_item = IntTableWidgetItem(abilityID)
            id_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)  # 水平居中，垂直居中
            self.tableAbility.setItem(row, 0, id_item)  # 编号

            name_item = QTableWidgetItem("     " + name)
            name_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 名字靠左对齐，垂直居中
            self.tableAbility.setItem(row, 1, name_item)  # 名字

    def filter_table(self):
        """根据输入框内容筛选表格"""
        search_text = self.searchAbility.text().lower()
        for row, ability in enumerate(self.ability_list):
            # 搜索名字、英文名、属性、分类
            if (search_text in ability["cName"].lower() or
                    search_text in ability["eName"].lower()):
                self.tableAbility.setRowHidden(row, False)
            else:
                self.tableAbility.setRowHidden(row, True)

    def update_basic(self, ability):
        """更新基本信息和图片"""
        name = ability["cName"]
        eName = ability["eName"]
        description = ability["description"] + "\n\n" + ability["effect"]

        # 更新信息、描述
        self.cName.setText(f"{name}")
        self.eName.setText(f"{eName}")
        self.Description.setPlainText(f"{description}")

        # 设置字体大小变化
        info_height = self.groupBox_2.height()
        font_size = 10 if ((info_height // 12) - 3) < 10 else ((info_height // 12) - 3)
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setBold(False)
        font.setPointSize(font_size)
        self.Description.setFont(font)
        font.setBold(True)
        self.eName.setFont(font)
        font.setPointSize(font_size + 1)
        self.cName.setFont(font)

    def update_pokemons(self, ability):
        """更新宝可梦列表"""

        # 禁用排序
        self.tablePokemon.setSortingEnabled(False)

        # 清空表格
        self.tablePokemon.setRowCount(0)

        # 遍历pokemon_list数据，查找所有具有该特性的宝可梦
        matching_pokemons = []
        for pokemon in self.pokemon_list:
            for pkmn_ability in pokemon["Ability"]:
                if pkmn_ability == ability["id"]:
                    matching_pokemons.append(pokemon["Pic"])

        # 如果没有找到任何宝可梦
        if not matching_pokemons:
            return

        # 更新表格
        self.tablePokemon.setRowCount(len(matching_pokemons))
        for row, match_pokemon in enumerate(matching_pokemons):
            self.tablePokemon.setRowHeight(row, 55)  # 每行高度为55

            # 获取宝可梦的基本信息
            pokemon = next((p for p in self.pokemon_list if p["Pic"] == match_pokemon), None)

            # 设置图标
            icon_name = pokemon["Pic"]
            icon_path = resource_path(f"res/pkmn_icon/{icon_name}.png")  # 图标文件路径
            # 设置图标大小
            pixmap = QPixmap(icon_path)
            pixmap = pixmap.scaled(QSize(45, 45), Qt.KeepAspectRatio, Qt.SmoothTransformation)  # 统一图标大小
            icon = QIcon(pixmap)
            icon_size = QSize(45, 45)  # 设置图标大小为 45x45 像素
            self.tablePokemon.setIconSize(icon_size)  # 设置表格的图标大小
            icon_item = QTableWidgetItem()
            icon_item.setIcon(icon)
            icon_item.setData(Qt.UserRole, icon_name)  # 存储 Pic
            self.tablePokemon.setItem(row, 1, icon_item)  # 图标列

            # 属性1
            type_size = QSize(80, 50)
            self.tablePokemon.setIconSize(type_size)
            type1 = pokemon["Type"][0]
            type1_path = resource_path(f"res/type/{type1}.png")
            type1_pixmap = QPixmap(type1_path)
            type1_pixmap = type1_pixmap.scaled(QSize(80, 50), Qt.KeepAspectRatio, Qt.SmoothTransformation)  # 统一图标大小
            type1_icon = QIcon(type1_pixmap)
            type1_item = IconTableWidgetItem(type1_icon, type1)  # 使用自定义的 TypeTableWidgetItem
            self.tablePokemon.setItem(row, 3, type1_item)  # 属性1 列

            # 属性2
            type2 = pokemon["Type"][1] if len(pokemon["Type"]) > 1 else ""
            type2_path = resource_path(f"res/type/{type2}.png") if type2 else ""
            type2_pixmap = QPixmap(type2_path) if type2 else QPixmap()
            type2_icon = QIcon(type2_pixmap)
            type2_item = IconTableWidgetItem(type2_icon, type2)  # 使用自定义的 TypeTableWidgetItem
            self.tablePokemon.setItem(row, 4, type2_item)  # 属性2 列

            name_item = QTableWidgetItem("    " + pokemon["cName"])
            name_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 名字靠左对齐，垂直居中
            self.tablePokemon.setItem(row, 2, name_item)  # 名字

            # 设置表格数据
            self.tablePokemon.setItem(row, 0, IntTableWidgetItem(pokemon["NationalCode"]))  # 图鉴编号

            # 填充表格
            for i in range(4):
                if pokemon["Ability"][i]:
                    pm_ability = next((p for p in self.ability_list if p["id"] == pokemon["Ability"][i]), None)
                    ability_item = QTableWidgetItem(pm_ability["cName"])
                    ability_item.setData(Qt.UserRole, pm_ability["id"])
                    if pm_ability["id"] == ability["id"]:  # 如果该特性与所选特性一致
                        itemfont = ability_item.font()
                        itemfont.setBold(True)  # 设置字体加粗
                        ability_item.setFont(itemfont)
                        ability_item.setForeground(QColor("red"))  # 设置字体颜色为红色
                    self.tablePokemon.setItem(row, i + 5, ability_item)
                else:
                    self.tablePokemon.setItem(row, i + 5, QTableWidgetItem(""))

        # 设置其他列居中
        for col in range(9):
            for row in range(len(matching_pokemons)):
                item = self.tablePokemon.item(row, col)
                if col != 2:  # 排除名字列
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)  # 水平居中，垂直居中

        # 重新启用排序
        self.tablePokemon.setSortingEnabled(True)

        self.tablePokemon.resizeColumnsToContents()  # 其他列自适应宽度
        table_list_width = self.tablePokemon.width()
        self.tablePokemon.setColumnWidth(2, int(table_list_width * 0.22))  # 名字列

        width = 0
        for i in range(5):
            width += self.tablePokemon.columnWidth(i)
        table_list_col_width = (table_list_width - width - 28) // 4
        for i in range(5,9):
            self.tablePokemon.setColumnWidth(i, table_list_col_width)

    def update_ability_info(self):
        """更新选中的特性信息"""
        selected_row = self.tableAbility.currentRow()
        if selected_row != -1:
            # 获取当前行的唯一标识（图鉴编号）
            abilityID = int(self.tableAbility.item(selected_row, 0).text())
            # 在 self.pokemon_list 中查找对应的宝可梦数据
            ability = next((p for p in self.ability_list if p["id"] == abilityID), None)

            self.update_basic(ability)  # 更新基本信息
            self.update_pokemons(ability)

    def update_size(self):
        """动态更新表格的行高和列宽"""
        table_width = self.tableAbility.width() - 20
        self.tableAbility.setColumnWidth(0, int(table_width * 0.32))  # 名字列
        self.tableAbility.setColumnWidth(1, int(table_width * 0.65))
        self.update_ability_info()

    def resizeEvent(self, event):
        """重写窗口大小改变事件"""
        super(AbilityWidget, self).resizeEvent(event)
        # 每次窗口大小改变时，更新属性抗性表的大小
        self.update_size()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MyMainWindow()  # 创建主窗口实例
    mainWindow.show()  # 显示主窗口
    sys.exit(app.exec_())
