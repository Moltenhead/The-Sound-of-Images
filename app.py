# -*- coding: UTF-8 -*-
'''**********************************************************************************
  Created by Charlie GARDAI alias Moltenhead - 2019
  ___________________________________________________________________________________

  Thanks to Ryan Juckett online ressource
  @http://www.ryanjuckett.com/programming/rgb-color-space-conversion/

  I would have not been able to math as good for the sRGB to XYZ convertion, and this
  would not have been possible without he's app references ; at least not as fast.
  Its base example has been here completly reworked into python and also has been
  reoriented mostlty into POO for convenience.
**********************************************************************************'''

# ------ IMPORTS ------ #
# Ext
import numpy              as np
import colorsys           as clrs
import matplotlib.image   as mpimg
# Local
import re
import csv
import glob
import os.path            as path
# Home brewed
import sys
sys.path.append(".\\modules")
import  sRGBUtil
from    vectorizedMatrix  import Vec2
from    Imager            import Imager
from    ColorSpace        import ColorSpace

# ------ COLORSPACE DEFINITION ------ #
red_xy     = Vec2(0.64, 0.32)                                                   # Red           Coordinates vectors
green_xy   = Vec2(0.30, 0.60)                                                   # Green         Coordinates vectors
blue_xy    = Vec2(0.15, 0.06)                                                   # Blue          Coordinates vectors
white_xy   = Vec2(0.3127, 0.3290)                                               # White         Coordinates vectors

sRGBSpace  = ColorSpace(red_xy, green_xy, blue_xy, white_xy)                    # sRGB          ColorSpace

# ------ PATHING DEFINITIONS ------ #
ROOT      = path.dirname(path.abspath(__file__))
CONVERTER = ROOT + "\\ressources\\XYZ_to_Wavelength_nm.csv"

imageList = []
for f in glob.glob("./*.png"):
  imageList.append(re.split(r'\\', f)[1])

# ------ USER INPUT MANAGEMNT ------ #
def error():
  string =              "\n\n  Wrong selection."
  string +=               "\n  Please choose a valid option."
  string +=               "\n  ---------------------------------------------------------------------"
  print(string)
  return           False

# Displayer
userInput        = False
while userInput == False:                                                                                    # keep asking if wrong input | TODO: add exit choice
  print                  ("\n  {} image found within application root directory:".format(len(imageList)))
  for idx, img in enumerate(imageList):
    print                  ("    [{}]. {}".format(idx, img))
  userInput       = input("\n  Please pass the image id you want to sound - number between brackets: ")      # request image path index within selection

  if userInput.isdigit():
    userInput     = int(userInput)
    if userInput >= 0 and userInput < len(imageList):
      break

  userInput       = error()

# Image target definition
imgPath = ROOT + "\\" + imageList[userInput]
# TODO: Imager implementation
# imager = Imager(imgPath)
img     = mpimg.imread(imgPath)
if img.dtype == np.float32:                                                        # if result isn't integer array
  img   = (img * 255).astype(np.uint8)

# ------ WAVELENGTH TABLE CREATION ------ #
wavelengthTable = {}
with open(CONVERTER, 'rb') as csvfile:
  spamreader = csv.reader(csvfile, delimiter=', ', quotechar='|')

# ------ PIXEL BY PIXEL PROCESS ------ #
pixelCount       = 0
filledPixelCount = 0

for pixelRow in img:
  for pixel in pixelRow:                                                           # for each pixel in img
    pixelCount += 1
    RGBASum    = 0
    for value in pixel.copy().pop(-1):
      RGBASum += value
    
    if RGBASum * pixel[-1] > 0:                                                    # if (sum of RGB) * A > 0
      filledPixelCount += 1
      # print("{} at: [{}]".format(pixel, pixelCount))
      sRGBColor = sRGBUtil.RGBToSRGB(pixel)                                        # get sRGB values from RGB
      toXYZ     = sRGBSpace.sRGBColorToXYZ(sRGBColor)                              # get color XYZ position
      # print("XYZ{} at: [{}]".format(toXYZ.toArray(), pixelCount))
      XYZarray  = toXYZ.toArray()

# def rgbToHertz(rgb):
#   hsv = clrs.rgb_to_hsv(rgb[0],rgb[1],rgb[2])
#   aproxTone = getTonefromHSV(hls)
