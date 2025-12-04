
import platform
from types import ModuleType


def setup_plt(plt_module: ModuleType=None) -> ModuleType:
    if plt_module is None:
        import matplotlib.pyplot as plt_module
        
    # --- CHINESE FONT CONFIGURATION ---
    system_name = platform.system()
    if system_name == "Windows":
        # SimHei is the standard Chinese font on Windows
        plt_module.rcParams['font.sans-serif'] = ['SimHei'] 
    elif system_name == "Darwin": 
        # MacOS usually uses Heiti TC or Arial Unicode MS
        plt_module.rcParams['font.sans-serif'] = ['Arial Unicode MS'] 
    else:
        # Linux (requires installing a Chinese font, e.g., WenQuanYi)
        plt_module.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']

    # This fixes an issue where the minus sign '-' becomes a square when using Chinese fonts
    plt_module.rcParams['axes.unicode_minus'] = False
    # 1. SET THE FONT (Run this once)
    sys_os = platform.system()
    if sys_os == 'Windows':
        plt_module.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
    elif sys_os == 'Darwin': # Mac
        plt_module.rcParams['font.sans-serif'] = ['Heiti TC', 'PingFang HK', 'Arial Unicode MS']
    plt_module.rcParams['axes.unicode_minus'] = False
    return plt_module
