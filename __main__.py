# -*- coding: utf-8 -*-
if __name__ == '__main__':                                                        # ensure following code is only called within main.py
  '''
    Created by Charlie GARDAI alias Moltenhead - 2019
    _________________________________________________
  '''
  # ------ IMPORTS ------ #
  from    modules.Imager    import Imager
  from    modules.Sounder   import Sounder

  # ------ IMG HANDLER ------ #
  imager = Imager()                                                               # create image handler
  imager.requestImgCursor()                                                       # request user input
  imager.verifySize()                                                             # verify chosen img size and shrink and save if user ask it
  img = imager.getCursorToPixarray()                                              # get chosen img to an Array of pixels

  # ------ SOUND HANDLER ------ #
  sounder = Sounder()                                                             # create sound handler
  sounder.pixarrayToNoise(img)                                                    # register noises using a pixarray for each pixel
  sounder.playNoise()                                                             # play the registered noise
