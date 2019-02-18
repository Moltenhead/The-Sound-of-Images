# -*- coding: utf-8 -*-
if __name__ == '__main__':                                                            # ensure multiprocessing won't call the main
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
  # Local
  import re
  import glob
  import time
  import multiprocessing
  import os.path            as path
  # Home brewed
  import  modules.RGBUtil  as RGBUtil
  from    modules.vectorizedMatrix        import Vec2
  from    modules.Imager                  import Imager
  from    modules.Sounder                 import Sounder
  from    modules.ColorSpace              import ColorSpace
  from    modules.processUtil             import splitPixarray, pixelProcess

  MAX_PROCESS_NB = 1

  # ------ COLORSPACE DEFINITION ------ #
  red_xy     = Vec2(0.64, 0.32)                                                   # Red           Coordinates vectors
  green_xy   = Vec2(0.30, 0.60)                                                   # Green         Coordinates vectors
  blue_xy    = Vec2(0.15, 0.06)                                                   # Blue          Coordinates vectors
  white_xy   = Vec2(0.3127, 0.3290)                                               # White         Coordinates vectors

  sRGBSpace  = ColorSpace(red_xy, green_xy, blue_xy, white_xy)                    # sRGB          ColorSpace

  # ------ IMG HANDLER ------ #
  imager = Imager()                                                               # create image handler
  imager.requestImgCursor()                                                       # request user input
  imager.verifySize()                                                             # verify chosen img size and shrink and save if user ask it
  img = imager.getCursorToPixarray()                                              # get chosen img to an Array of pixels

  # ------ PIXEL BY PIXEL PROCESS ------ #
  sounder          = Sounder()

  pixelCount       = []
  filledPixelCount = []

  splitted = splitPixarray(MAX_PROCESS_NB, img)
  t = time.time()
  processes = []
  for i in range(len(splitted)):
    p = multiprocessing.Process(
      name="pixelProcess{}".format(i),
      target=pixelProcess(pixelCount, filledPixelCount, splitted[i], sRGBSpace, sounder))
    processes.append(p)
    p.start()
  for p in processes:
    p.join()
  
  print("\n  Ended at pixel: [{}] in {}".format(sum(x for x in pixelCount), time.time() - t))
