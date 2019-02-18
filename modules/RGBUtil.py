# -*- coding: utf-8 -*-
import  numpy            as np
# Home brewed
from sys import path
path.append('.')
from    .vectorizedMatrix  import Vec3

#**********
class RGB:
#**********
  def __init__(self, r, g, b):
    self.R = r
    self.G = g
    self.B = b

    self.__RGBVec = Vec3(r,g,b)
  
  def get_RGBVec(self):
    return self.__RGBVec
