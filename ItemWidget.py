import json
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QGraphicsScene
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor
from PyQt5.QtCore import Qt, QSize, QTimer
from UI import ItemList
from CustomizeFunction import IntTableWidgetItem, IconTableWidgetItem, resource_path, get_color_with_type



class ItemWidget(QWidget, ItemList.Ui_Win_ItemList):
    def __init__(self, parent = None):
        super(ItemWidget, self).__init__(parent)
        self.item_list = None
        self.setupUi(self)
        self.init_style()
        self.load_data()
        self.load_item()
        self.searchItem.textChanged.connect(self.searchBox)  # 输入框内容变化时筛选表格
        self.tableItem.itemSelectionChanged.connect(self.update_item_info)  # 选中行变化时更新道具信息

        # 默认选中第一行
        if self.tableItem.rowCount() > 0:
            self.tableItem.selectRow(0)
            
        # 定义按钮名称与道具类型的映射关系
        self.button_type_mapping = {
            "Button_KeyItems": "重要物品",
            "Button_PokeBalls": "精灵球",
            "Button_TM": "招式学习器",
            "Button_Medicines": "回复道具",
            "Button_Berries": "树果",
            "Button_Strategy": "战斗道具",
            "Button_Improvements": "强化道具",
            "Button_Valuable": "贵重物品",
            "Button_Evolution": "进化道具",
            "Button_ZCrystals": "Z纯晶",
            "Button_Megastones": "超级石",
            "Button_Utilities": "实用道具"
        }
        
        self.active_type = {"重要物品","精灵球","招式学习器","回复道具","树果","战斗道具","强化道具","贵重物品","进化道具","Z纯晶","超级石","实用道具"}

        # 绑定按钮点击事件
        self.Button_all.clicked.connect(lambda: self.isSelectAll(True))
        self.Button_cancel.clicked.connect(lambda: self.isSelectAll(False))
        self.Button_KeyItems.clicked.connect(lambda: self.filter_table("Button_KeyItems"))
        self.Button_PokeBalls.clicked.connect(lambda: self.filter_table("Button_PokeBalls"))
        self.Button_TM.clicked.connect(lambda: self.filter_table("Button_TM"))
        self.Button_Medicines.clicked.connect(lambda: self.filter_table("Button_Medicines"))
        self.Button_Berries.clicked.connect(lambda: self.filter_table("Button_Berries"))
        self.Button_Strategy.clicked.connect(lambda: self.filter_table("Button_Strategy"))
        self.Button_Improvements.clicked.connect(lambda: self.filter_table("Button_Improvements"))
        self.Button_Valuable.clicked.connect(lambda: self.filter_table("Button_Valuable"))
        self.Button_Evolution.clicked.connect(lambda: self.filter_table("Button_Evolution"))
        self.Button_ZCrystals.clicked.connect(lambda: self.filter_table("Button_ZCrystals"))
        self.Button_Megastones.clicked.connect(lambda: self.filter_table("Button_Megastones"))
        self.Button_Utilities.clicked.connect(lambda: self.filter_table("Button_Utilities"))

    def closeEvent(self, event):
        """重写关闭事件，确保父窗口中的引用被清空"""
        self.item_list = None
        self.button_type_mapping = None
        self.active_type = None
        event.accept()  # 确保当前窗口可以正常关闭

    def init_style(self):
        """初始化界面样式设置"""
        # tableItem 宝可梦列表 表头设置
        font = QFont()
        font.setBold(True)  # 设置字体为加粗
        font.setPointSize(9)  # 设置字体大小
        item_header = self.tableItem.horizontalHeader()
        item_header.setFont(font)  # 应用字体设置
        item_header.setStyleSheet("QHeaderView::section {font-weight: bold; font-size: 9pt;}")
        self.tableItem.horizontalHeader().setFixedHeight(50)  # 表头行高为 50

    def load_data(self):
        """读取道具数据"""
        item_path = resource_path("data/Item_List.json")
        with open(item_path, "r", encoding = "utf-8") as file:
            data = json.load(file)
        self.item_list = data["item"]

    def load_item(self):
        """加载道具列表"""
        self.tableItem.setRowCount(len(self.item_list))

        for row, item in enumerate(self.item_list):
            self.tableItem.setRowHeight(row, 60)  # 所有行高为 60

            itemID = item["id"]
            name = item["cName"]
            type = item["type"]
            
            id_item = IntTableWidgetItem(itemID)
            id_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)  # 水平居中，垂直居中
            self.tableItem.setItem(row, 0, id_item)  # 编号

            # 设置图标
            icon_size = QSize(55, 55)  # 设置图标大小为 55x55 像素
            self.tableItem.setIconSize(icon_size)  # 设置表格的图标大小
            # icon_path = resource_path(f"res/item_icon/{name}.png")  # 图标文件路径
            icon_path = resource_path(f"res/item_icon/move.png")  # 图标文件路径
            pixmap = QPixmap(icon_path)
            pixmap = pixmap.scaled(QSize(55, 55), Qt.KeepAspectRatio, Qt.SmoothTransformation)  # 统一图标大小
            icon = QIcon(pixmap)
            icon_item = IconTableWidgetItem(icon, name)
            self.tableItem.setItem(row, 1, icon_item)  # 道具图标列

            type_path = resource_path(f"res/item_type/{type}.png")
            type_pixmap = QPixmap(type_path)
            type_pixmap = type_pixmap.scaled(QSize(45, 45), Qt.KeepAspectRatio, Qt.SmoothTransformation)  # 统一图标大小
            type_icon = QIcon(type_pixmap)
            type_item = IconTableWidgetItem(type_icon, type)  # 使用自定义的 IconTableWidgetItem
            self.tableItem.setItem(row, 3, type_item)  # 类型图标列

            name_item = QTableWidgetItem("  " + name)
            name_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 名字靠左对齐，垂直居中
            self.tableItem.setItem(row, 2, name_item)  # 道具名
            
            typename_item = QTableWidgetItem("  " + type)
            typename_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 名字靠左对齐，垂直居中
            self.tableItem.setItem(row, 4, typename_item)  # 类型

    def isSelectAll(self, flag):
        for button_name in self.button_type_mapping.items():
            button = getattr(self, button_name[0])
            if flag:
                button.setChecked(True)
                self.active_type.add(button_name[1])
            else:
                button.setChecked(False)
                self.active_type.discard(button_name[1])
        self.filter_table()
                
    def searchBox(self):
        self.filter_table()

    def filter_table(self, button_name = None):
        """根据输入框内容、按钮类型筛选表格"""
        # 根据按钮状态筛选类型
        if button_name in self.button_type_mapping:
            button = getattr(self, button_name)
            if button.isChecked():
                self.active_type.add(self.button_type_mapping[button_name])
            else:
                self.active_type.discard(self.button_type_mapping[button_name])
        
        search_text = self.searchItem.text().lower()
        for row, item in enumerate(self.item_list):
            description = item["explain"] + "\n" + item["effect"]
            
            # 搜索名字、英文名、描述
            if (search_text in item["cName"].lower() or
                    search_text in item["eName"].lower() or
                    search_text in description.lower()):
                # 类型筛选
                if item["type"] in self.active_type:
                    self.tableItem.setRowHidden(row, False)
                else:
                    self.tableItem.setRowHidden(row, True)
            else:
                self.tableItem.setRowHidden(row, True)

    def update_basic(self, item):
        """更新基本信息和图片"""
        name = item["cName"]
        description = item["explain"] + "\n\n" + item["effect"]

        # 更新图片
        # icon_path = resource_path(f"res/item_icon/{name}.png")
        icon_path = resource_path(f"res/item_icon/move.png")
        pixmap = QPixmap(icon_path)
        size = min(self.ItemPic.width(), self.ItemPic.height())
        pixmap = pixmap.scaled(QSize(size - 20, size - 20), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ItemPic.setScene(QGraphicsScene())
        self.ItemPic.scene().addPixmap(pixmap)

        # 更新信息、描述
        self.cName.setText(name)
        self.eName.setText(item["eName"])
        self.itemType.setText("道具类型：" + item["type"])
        self.Description.setPlainText(description)


        # 根据属性设置名字颜色
        # color = get_color_with_type(item["Type"][0])
        # self.cName.setStyleSheet(color)
        # self.eName.setStyleSheet(color)

        # 设置字体大小变化
        # info_height = self.groupBox_2.height()
        # font_size = int(info_height / 29)
        # if font_size < 8:
        #     font_size = 8
        # font = QFont()
        # font.setFamily("Microsoft YaHei UI")
        # font.setPointSize(font_size)
        # self.Height.setFont(font)
        # self.Weight.setFont(font)
        # self.Region.setFont(font)
        # self.sex.setFont(font)
        # font.setPointSize(font_size + 1)
        # self.Description.setFont(font)
        # font.setBold(True)
        # self.eName.setFont(font)
        # font.setPointSize(font_size + 2)
        # self.cName.setFont(font)

    def update_item_info(self):
        """更新选中的道具信息"""
        selected_row = self.tableItem.currentRow()
        if selected_row != -1:
            # 获取当前行的唯一标识（编号）
            itemID = int(self.tableItem.item(selected_row, 0).text())
            # 在 self.item_list 中查找对应的道具数据
            item = next((p for p in self.item_list if p["id"] == itemID), None)
            # 更新基本信息
            self.update_basic(item)

    def update_size(self):
        """动态更新表格的行高和列宽"""
        self.tableItem.resizeColumnsToContents()  # 其他列自适应宽度
        item_list_width = self.tableItem.width()
        self.tableItem.setColumnWidth(0, int(item_list_width * 0.12))   # ID列
        self.tableItem.setColumnWidth(2, int(item_list_width * 0.35))   # 名字列
        width_1_4 = 0
        for i in range(4):
            width_1_4 += self.tableItem.columnWidth(i)
        item_list_col_width = item_list_width - width_1_4

        self.tableItem.setColumnWidth(4, item_list_col_width - 30)

        self.update_item_info()

    def resizeEvent(self, event):
        """重写窗口大小改变事件"""
        super(ItemWidget, self).resizeEvent(event)
        # 每次窗口大小改变时，更新属性抗性表的大小
        self.update_size()
