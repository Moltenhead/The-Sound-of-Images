# -*- coding: utf-8 -*-
import  numpy            as np
# Home brewed
from sys import path
path.append('.')
from    .vectorizedMatrix  import Vec3

#**********
class SRGB:
#**********
  def __init__(self, i, r, g, b):
    self.I = i
    self.R = r
    self.G = g
    self.B = b

    self.__sRGBVec = Vec3(r,g,b)
  
  def get_sRGBVec(self):
    return self.__sRGBVec

#******************************
def RGBToSRGB(rgb):
# Convert RGB to its sRGB value
#******************************
  baseR = rgb[0]
  baseG = rgb[1]
  baseB = rgb[2]

  # int conversion needed since summing uint8 was missbehaviour (overflow in ubyte_scalars)
  I = (int(baseR) + int(baseG) + int(baseB))/3                                 # intensity
  sR = int(baseR)/(int(baseR) + int(baseG) + int(baseB))                       # normalized red
  sG = int(baseG)/(int(baseR) + int(baseG) + int(baseB))                       # normalized green
  sB = int(baseB)/(int(baseR) + int(baseG) + int(baseB))                       # normalized blue
  return SRGB(I, sR, sG, sB)