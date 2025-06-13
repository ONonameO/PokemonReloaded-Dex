import os
import sys

def resource_path(relative_path):
    """获取资源文件的绝对路径，适用于打包后的程序"""
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)