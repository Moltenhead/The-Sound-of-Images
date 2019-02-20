# -*- coding: utf-8 -*-
import  math
import  numpy     as np
from    sys       import path
path.append('.')
from    .RGBUtil  import RGB

#****************************************************
def splitPixarray(maxProcessNb, pixarray):
# split a pixarray into a given number of subpixarray
#****************************************************
  height = len(pixarray)
  width = len(pixarray[0])
  total = height * width

  splitStruct = [0] * maxProcessNb
  splitFactor = total / maxProcessNb

  passCount = 0
  while splitFactor < 1:                                         # reduce multiprocess if maximum is not needed
    passCount += 1                                               # reduce by one each time
    splitFactor = total / (maxProcessNb - passCount)
  splitFactor = int(splitFactor)                                 # turn into int when number of process is defined

  for idx in range(len(splitStruct)):
    splitStruct[idx] = [0] * splitFactor

  if height % splitFactor != 0:                                  # if split factor does not equivalently split
    rest = (height * width) % maxProcessNb                       # calculate rest
    for x in range(rest):
      splitStruct[x].append(0)                                   # distribute

  for idx, row in enumerate(splitStruct):
    for idy in range(len(row)):
      here = (idx * splitFactor + idy)
      x = math.floor(here / width)
      y = here % width
      splitStruct[idx][idy] = pixarray[x][y]
  
  return splitStruct

#*****************************************************************************
def pixelProcess(pixelCount, filledPixelCount, pixarray, colorSpace, sounder):
#*****************************************************************************
  print("\n      Initialized new pixelProcess.")
  countDecal = sum(x for x in pixelCount)
  count = 0
  filledCountDecal = sum(x for x in filledPixelCount)
  filledCount = 0
  for pixel in pixarray:                                                         # for each pixel in pixarray
    # print(pixel)
    count += 1
    RGBASum    = 0
    for value in pixel.copy():
      RGBASum += value
    
    if RGBASum * pixel[-1] > 0:                                                  # if (sum of RGB) * A > 0
      filledCount += 1
      # print("{} at: [{}]".format(pixel, countDecal + count))
      RGBColor = RGB(pixel[0], pixel[1], pixel[2])                                               # get sRGB values from RGB
      # c = RGBColor.get_RGBVec() 
      # print("{}:{}:{}".format(c.x, c.y, c.z))
      toXYZ     = colorSpace.RGBColorToXYZ(RGBColor)                             # get color XYZ position
      # print("XYZ{} at: [{}]".format(toXYZ.toArray(), countDecal + count))
      XYZarray  = toXYZ.toArray()
      sounder.requestXYZPlay(RGBColor, XYZarray, 0.2)
  
  pixelCount.append(count)
  filledPixelCount.append(filledCount)
  print("      Finalized pixelProcess.")
  return
