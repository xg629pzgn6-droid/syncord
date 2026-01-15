"""
PyInstaller hook for discord.py
"""
from PyInstaller.utils.hooks import (
    collect_submodules, collect_data_files, get_module_file_attribute
)

hiddenimports = collect_submodules('discord')
datas = collect_data_files('discord')
