import json
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QGraphicsScene
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor
from PyQt5.QtCore import Qt, QSize, QTimer
from UI import PokemonList
from CustomizeFunction import IntTableWidgetItem, IconTableWidgetItem, resource_path, get_color_with_type



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
