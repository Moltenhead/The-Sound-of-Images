# -*- coding: utf-8 -*-
if __name__ == '__main__':                                                        # ensure following is only called within main.py
  '''
    Created by Charlie GARDAI alias Moltenhead - 2019
    _________________________________________________
  '''
  # ------ IMPORTS ------ #
  # Ext
  # import numpy              as np
  # Local
  # import re
  # import glob
  # import time
  # import multiprocessing
  # import os.path            as path
  # Home brewed
  # import  modules.RGBUtil  as RGBUtil
  # from    modules.vectorizedMatrix        import Vec2
  from    modules.Imager                  import Imager
  from    modules.Sounder                 import Sounder
  # from    modules.ColorSpace              import ColorSpace
  # from    modules.processUtil             import splitPixarray, pixelProcess
  ''' Will be needed once MATH
  MAX_PROCESS_NB = 1

  # ------ COLORSPACE DEFINITION ------ #
  red_xy     = Vec2(0.64, 0.32)                                                   # Red           Coordinates vectors
  green_xy   = Vec2(0.30, 0.60)                                                   # Green         Coordinates vectors
  blue_xy    = Vec2(0.15, 0.06)                                                   # Blue          Coordinates vectors
  white_xy   = Vec2(0.3127, 0.3290)                                               # White         Coordinates vectors

  sRGBSpace  = ColorSpace(red_xy, green_xy, blue_xy, white_xy)                    # sRGB          ColorSpace
  '''
  # ------ IMG HANDLER ------ #
  imager = Imager()                                                               # create image handler
  imager.requestImgCursor()                                                       # request user input
  imager.verifySize()                                                             # verify chosen img size and shrink and save if user ask it
  img = imager.getCursorToPixarray()                                              # get chosen img to an Array of pixels

  # ------ PIXEL BY PIXEL PROCESS ------ #
  sounder = Sounder()                                                             # create sound handler
  sounder.pixarrayToNoise(img)#, sRGBSpace)                                       # register noise from a pixarray
  sounder.playNoise()                                                             # play

  ''' MULTIPROC TEST, NO USE FOR THIS VERSION
  # pixelCount       = []
  # filledPixelCount = []

  # splitted = splitPixarray(MAX_PROCESS_NB, img)
  # processes = []  
  
  # for i in range(len(splitted)):
  #   p = multiprocessing.Process(
  #     name="pixelProcess{}".format(i),
  #     target=pixelProcess(pixelCount, filledPixelCount, splitted[i], sRGBSpace, sounder))
  #   processes.append(p)
  #   p.start()
  # for p in processes:
  #   p.join()
  '''
