import json
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5.QtGui import QIcon, QPixmap, QColor, QFont
from PyQt5.QtCore import Qt, QSize, QTimer
from UI import AbilityList
from CustomizeFunction import IntTableWidgetItem, IconTableWidgetItem, resource_path


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
