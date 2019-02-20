# -*- coding: utf-8 -*-
import  numpy              as np
import  matplotlib.image   as mpimg

import  re
import  sys
import  math
import  glob

from    PIL       import Image
from    shutil    import copyfile
from    fractions import Fraction
from    os        import path, pardir

ROOT              = path.dirname(path.abspath(path.join(__file__, pardir)))
TRANSFORMED_PATH  = ROOT + "\\.transformed\\"                                      # where are stored transformed imgs
MAX_PIXELS        = int(10**2 * 1.5)                                               # max pixel treshold

#************
class Imager:
#************
  # ------------------------------------------------------------------
  def __init__(self, ext = ['.png', '.jpg'], img_paths= ['.\\img\\']):
  # ------------------------------------------------------------------
    self.img_ext = ext
    self.img_paths = img_paths

    self.cursor = -1
    self.img_list = []

    self.img_pixels = []

    self.storeImgs()

  # --------------------------------
  def appendImg(self, img_fullPath):
  # --------------------------------
    self.img_list.append({
      'name': re.split(r'\\', img_fullPath)[-1],
      'fullPath': img_fullPath,
      'resized': None})
  
  # ------------------
  def storeImgs(self):
  # ------------------
    imgCount = 0
    for path in self.img_paths:
      for ext in self.img_ext:
        for img_fullPath in glob.glob(path + "*" + ext):
          self.appendImg(img_fullPath)
          imgCount += 1
  
  # -----------------------------------------
  def get_img(self, img_idx, part = 'whole'):
  # -----------------------------------------
    if part is 'whole':
      return self.img_list[img_idx]
    else:
      return self.img_list[img_idx][part]
  
  # ------------------------------------
  def imgAtCursor(self, part = 'whole'):
  # ------------------------------------
    return self.get_img(self.cursor, part)
  
  # -----------------
  def getImgNb(self):
  # -----------------
    return len(self.img_list)
  
  # -----------------------
  def showStoredImgs(self):
  # -----------------------
    print("\n  {} images found in specified directories:".format(self.getImgNb()))
    for idx, img in enumerate(self.img_list):
      print("    [{}]: {}".format(idx, img))

  # ----------------------------
  def error(self, errorIdx = 0):
  # ----------------------------
    string = ""
    if errorIdx is 0:
      string = "\n\n  Wrong selection."
      string += "\n  Please choose a valid option."
      string += "\n  ---------------------------------------------------------------------"
      print(string)
    
    return False

  # -------------------------
  def requestImgCursor(self):
  # -------------------------
    if self.getImgNb() <= 0:
      sys.exit("\n  No images to choose from.")
    
    userInput = False
    while userInput == False:                                                                              # keep asking if wrong input | TODO: add exit choice
      self.showStoredImgs()
      userInput = input("\n  Please pass the image id you want to sound - number between brackets: ")      # request image path index within selection

      if userInput.isdigit():
        userInput = int(userInput)
        if userInput >= 0 and userInput < len(self.img_list):
          self.cursor = userInput
          userInput = True
      else:
        userInput = self.error()

  # ---------------------------------------
  def shrinkImg(self, img_idx, maxPixelNb):
  # ---------------------------------------
    targetImg = self.get_img(img_idx)
    resized = None
    with Image.open(targetImg['fullPath']) as img:
      w = img.size[0]
      h = img.size[1]
      ratio = Fraction(w / h)
      ratio_unit = math.sqrt(MAX_PIXELS / (ratio.numerator * ratio.denominator))
      wSize = int(ratio.numerator * ratio_unit)
      hSize = int(ratio.denominator * ratio_unit)

      print("    Shrinked to {}x{} pixels.".format(wSize, hSize))
      img = img.resize((wSize, hSize))
      img.save(TRANSFORMED_PATH + "resized_" + targetImg['name'])
      img.close()

    self.img_list[self.cursor]['resized'] = TRANSFORMED_PATH + "resized_" + targetImg['name']
    return self.imgAtCursor()
  
  # ----------------------------------
  def verifySize(self):
  # verify if img size is not too long
  # shrink if user asks
  # ----------------------------------
    target = self.imgAtCursor()
    img = Image.open(target['fullPath'])
    pixelsNb = img.size[0] * img.size[1]

    if pixelsNb > MAX_PIXELS:
      userInput = False
      while userInput is False:
        string = "\n  Image is {}pixels long. Would you like to shrink it to around {} pixels?".format(pixelsNb, MAX_PIXELS)
        string += "\n  No shrink could make the process realy long - approximatly 1 second / 100px. (y/n):"
        userInput = input(string)
        if userInput == 'y' or userInput == 'n':
          if userInput is 'y':
            self.shrinkImg(self.cursor, MAX_PIXELS)
        else:
          userInput = self.error()
  
  # ------------------------------
  def getCursorToPixarray(self):
  # returns img at cursor position
  # ------------------------------
    resized = self.imgAtCursor('resized')
    targetLabel = 'fullPath'
    if resized is not None:                                         # select resized img if resized img is registered
      targetLabel = 'resized'
    img = mpimg.imread(self.imgAtCursor(targetLabel))
    
    if img.dtype == np.uint8:                                       # if result isn't integer array
      img   = (img / 255).astype(np.float32)
    return img
