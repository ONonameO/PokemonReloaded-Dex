import os
import sys
from PyQt5.QtWidgets import QTableWidgetItem


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

def get_color_with_itemType(type):
    colors = {
        "重要物品": "color: rgb(251,205,40);",
        "招式学习器": "color: rgb(58,193,213);",
        "精灵球": "color: rgb(253,67,81);",
        "树果": "color: rgb(185,93,249);",
        "回复道具": "color: rgb(240,150,181);",
        "强化道具": "color: rgb(93,183,181);",
        "实用道具": "color: rgb(197,159,78);",
        "进化道具": "color: rgb(63,161,41);",
        "战斗道具": "color: rgb(255,128,0);",
        "贵重物品": "color: rgb(238,76,238);",
        "超级石": "color: rgb(75,120,205);",
        "Z纯晶": "color: rgb(127,127,127);"
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
