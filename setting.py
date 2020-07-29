#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Li Haozheng
# @Time    : 2019/3/22 16:26

# 模式（GrayMode，ColorMode， MosaicMode）
MODEL = 'GrayMode'

# 图片路径，可以是http图片
PICTURE_PATH = r'demo/demo.jpg'

# 输出路径
OUTPUT_PATH = 'demo/grayMode.js'

# 图片高度（字符数量），宽度只有在输出图片异常的情况下使用
HEIGHT = 30
# WIDTH =

# 填充字符，单字推荐'#'，支持中文，但中文不能和英文或数字混杂
ColorModeChar = 'EMIYA'

# 输出字号
ColorModeFontSize = 12

# 背景颜色（仅限 GrayMode 或者 ColorMode）
BackgroundColor = '#ffffff'