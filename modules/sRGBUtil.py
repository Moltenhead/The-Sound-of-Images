# -*- coding: utf-8 -*-
import numpy as np

import sys
sys.path.append(".\\")
import vectorizedMatrix as vmat

#**********
class SRGB:
#**********
  def __init__(self, i, r, g, b):
    self.I = i
    self.R = r
    self.G = g
    self.B = b

    self.__sRGBVec = vmat.Vec3(r,g,b)
  
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

#**************************************************************
def gammaExpand(nonlinear):
# Convert an sRGB color channel to a linear sRGB color channel.
#**************************************************************
  return (nonlinear / 12.92) if (nonlinear <= 0.04045) else (np.float_power((nonlinear+0.055)/1.055, 2.4))

#*************************************************************
def gammaCompress(linear):
# Convert a linear sRGB color channel to a sRGB color channel.
#*************************************************************
  return (12.92*linear) if (linear <= 0.0031308) else (1.055 * np.float_power(linear, 1.0/2.4) - 0.055)
