import json
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QSize
from UI import MoveList
from CustomizeFunction import IntTableWidgetItem, IconTableWidgetItem, LvTableWidgetItem, resource_path, get_color_with_type


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
