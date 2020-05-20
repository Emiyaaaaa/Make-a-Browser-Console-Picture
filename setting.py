#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Li Haozheng
# @Time    : 2019/3/22 16:26

# 模式（GrayMode，ColorMode， MosaicMode）
MODEL = 'GrayMode' # GrayMode or ColorMode or MosaicMode

# 图片路径，可以是http图片
PICTURE_PATH = r'demo/demo.jpg' # Set local picture or internet picture.

# 输出路径
OUTPUT_PATH = 'demo/grayMode.js'

# 图片高度（字符数量），宽度只有在输出图片变形的情况下使用
HEIGHT = 30
# WIDTH =
# WIDTH is not necessary.

# MosaicMode和ColorMode的填充字符，可以是单字，推荐'#'，可以是中文或数字，但中文不能和英文或数字混杂
ColorModeChar = 'EMIYA' # Don't set '%' ! Recommend character: '#', '@', '&'.

# 输出字号
ColorModeFontSize = 12 # minimum size is 10, default size is 12

# 背景颜色（仅限 GrayMode 或者 ColorMode）
BackgroundColor = '#ffffff'