#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Li Haozheng
# @Time    : 2019/3/22 16:23

from PIL import Image
from urllib.request import urlretrieve
from setting import *

class MyImage():
    def __init__(self):
        # 设置图片路径
        if PICTURE_PATH[:4] == 'http':
            urlretrieve(PICTURE_PATH, 'cache/cache.jpg')
            self.path = 'cache/cache.jpg'
        else:
            self.path = PICTURE_PATH
        # 设置宽度
        self.width = self.getWidth(self.path)
        # 设置高度
        self.height = HEIGHT
        # 设置字号
        self.fontSize = 'font-size:' + str(ColorModeFontSize) + 'px;' if(self.varIsDefined('ColorModeFontSize')) else ''
        # 设置js输出路径
        self.outputPath = OUTPUT_PATH if(self.varIsDefined('OUTPUT_PATH')) else 'consolePicture.js'
        # 按照设置宽高调整图片大小
        self.resizeImage = self.resizeImg(self.path,self.width,self.height)
        # 设置马赛克模式中的数据
        self.mosaicModeWidth = self.width
        self.resizeImageForMosaicMode = self.resizeImg(self.path,self.width*1,self.height)
        self.mosaicModeWidthStep = 1



    def resizeImg(self,path,width,height):
        im = Image.open(path)
        im = im.resize((width, height), Image.NEAREST)
        return im

    def is_all_chinese(self, strs):
        for _char in strs:
            if not '\u4e00' <= _char <= '\u9fa5':
                return False
        return True

    def getWidth(self,path):
        if self.varIsDefined('WIDTH'):
            width = WIDTH
        else:
            try:# 获取字号
                if ColorModeFontSize < 12:
                    fontSizeCoefficient = 12/ColorModeFontSize
                else:
                    fontSizeCoefficient = 1
            except:
                fontSizeCoefficient = 1
            im = Image.open(path)
            width = int(HEIGHT * im.size[0]/im.size[1]*fontSizeCoefficient*2.2)# 2.2为标准英文宽高比，fontSizeCoefficient 为字号小于12时的调整系数
            if self.is_all_chinese(ColorModeChar):# 中文
                width = int(HEIGHT * im.size[0]/im.size[1]*fontSizeCoefficient*1.18)
        return width

    def varIsDefined(self,varName):
        try:
            a = eval(varName)
            return True
        except:
            return False
    

class pic2str():

    # 黑白模式
    def grayMode(self,imgObj):
        img = imgObj.resizeImage
        height = imgObj.height
        width = imgObj.width
        content_txt = '\\n\\\n'

        for i in range(height):
            for j in range(width):
                content_txt += self.getGrayModeChar(*img.getpixel((j, i)))# 这里的*不能少
            content_txt = content_txt + '\\n\\\n'# 写完一行后换行
        
        return 'grayModeConsoleOut',content_txt



    # 彩色模式
    def colorMode(self,imgObj):
        myCharacter = ColorModeChar
        content_txt = '\\n\\\n'
        css_txt = ''
        height = imgObj.height
        width = imgObj.width
        fontSize = imgObj.fontSize
        img = imgObj.resizeImage
        backgroundColor = self.color16toRgb(BackgroundColor)

        for i in range(height):
            for j in range(width):
                pixelColor = str(img.getpixel((j, i)))# 获取像素颜色值
                css_txt += ',"background-color:rgb'+backgroundColor+';'+fontSize+'color:rgb'+pixelColor+'"'
                if self.isEquality(backgroundColor,pixelColor,10):# 与背景色相同或者rgb加起来差距在10以内的就用随便什么字符代替，不能占用txt中的字符（因为必须和txt中的文本相同大小，所以就选取了txt[0]）
                    content_txt += "%c"+myCharacter[0]
                else:
                    content_txt += "%c"+myCharacter[0]# 取txt第一个字母
                    myCharacter = myCharacter[1:] + myCharacter[0]# 用完就把第一个字母放在最后, 相当于一个队列
            content_txt = content_txt + '\\n\\\n'# 写完一行后换行

        content = content_txt + '"' + css_txt[:-1]# 去掉最后一个引号，否则执行后会多出来一个引号
        return 'colorModeConsoleOut',content



    # 马赛克模式
    def mosaicMode(self,imgObj):
        myCharacter = ColorModeChar
        content_txt = '\\n\\\n'
        css_txt = ''
        height = imgObj.height
        width = imgObj.mosaicModeWidth
        fontSize = imgObj.fontSize
        img = imgObj.resizeImageForMosaicMode
        step = imgObj.mosaicModeWidthStep

        for i in range(height):
            for j in range(0,width,step):
                pixelColor = str(img.getpixel((j, i)))# 获取像素颜色值
                nextIndex = j+1
                if nextIndex >= width:
                    nextIndex = j
                nextPixelColor = str(img.getpixel((nextIndex, i)))# 下一个像素颜色值，用于字符色
                css_txt += ',"background-color:rgb'+pixelColor+';'+fontSize+'color:rgb'+pixelColor+'"'

                content_txt += "%c"+myCharacter[0]# 取txt第一个字母
                myCharacter = myCharacter[1:] + myCharacter[0]# 用完就把第一个字母放在最后, 相当于一个队列
            content_txt = content_txt + '\\n\\\n'# 写完一行后换行

        content = content_txt + '"' + css_txt[:-1]# 去掉最后一个引号，否则执行后会多出来一个引号
        return 'mosaicModeConsoleOut',content



    # 黑白模式 颜色->字符
    def getGrayModeChar(self,r,g,b,alpha=255):
        ascii_char = list(r"@$B%&W%M#*XhkbdpqwmZO0QLCJUYoazcvunxrjft/|()1{}[[-_+~<>i!lI;:,^`'.  ")
        if alpha == 0:
            return ' '
        length = len(ascii_char)
        gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
        unit = (256.0 + 1)/length
        return ascii_char[int(gray/unit)]

    def creatJsContent(self,functionName,content):
        content =   functionName + '();                                                     \
                    function '+ functionName +'(){                                          \
                        console.log("' + content +'");                                      \
                        console.log("Make this: https://github.com/Emiyaaaaa/pic2char");    \
                    }'
        return content

    def creatFile(self,content,path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    def creatJsFile(self,functionNameAndContent,path):
        functionName = functionNameAndContent[0]
        content = functionNameAndContent[1]
        jsContent = self.creatJsContent(functionName,content)
        self.creatFile(jsContent,path)

    def color16toRgb(self,color16):
        if len(color16) == 4:# 将三位数的颜色值转换为六位数的颜色值
            a = '#' + color16[1] + color16[1] + color16[2] + color16[2] + color16[3] + color16[3]
            color16 = a
        color16 = color16[1:]
        r = int('0x'+color16[0:2], 16)
        g = int('0x'+color16[2:4], 16)
        b = int('0x'+color16[4:6], 16)
        rgb = '(' + str(r) + ', ' + str(g) + ', ' + str(b) + ')'
        return rgb

    # 两个rgb颜色相差小于num
    # rgb1,rgb2输入格式 '(125,125,125)'
    def isEquality(self,rgb1,rgb2,num):
        rgb1sum = self.getRgbSum(rgb1)
        rgb2sum = self.getRgbSum(rgb2)
        if rgb1sum - rgb2sum < num and rgb1sum - rgb2sum > -num:
            return True
        else:
            return False

    def getRgbSum(self,rgb):
        rgb = rgb[1:-1].split(',')
        r_num = int(rgb[0])
        g_num = int(rgb[1])
        b_num = int(rgb[2])
        return r_num+g_num+b_num

    def main(self,imgObj):
        model_dict = {
            'ColorMode':self.colorMode,
            'GrayMode':self.grayMode,
            'MosaicMode':self.mosaicMode
        }
        path = imgObj.outputPath
        self.creatJsFile(model_dict[MODEL](imgObj),path)

if __name__=='__main__':
    imgObj = MyImage()
    pic2str().main(imgObj)