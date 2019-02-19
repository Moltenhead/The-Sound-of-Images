# -*- coding: utf-8 -*-
from __future__ import division
# ------ IMPORTS ------ #
# Ext
import  csv
import  numpy               as     np
from    pyaudio             import PyAudio
# from    scipy.interpolate   import griddata 
# Local
import  math
import  itertools
from    time                import time
from    operator            import or_, and_
from    os                  import path, pardir
# Home brewed
import  sys
sys.path.append('.')
from    .RGBUtil            import RGB

# ------ CONSTANTS ------ #
# ROOT            = path.dirname(path.abspath(path.join(__file__, pardir)))
# CONVERTER_PATH  = ROOT + "\\ressources\\XYZ_to_Wavelength_nm.csv"         # conversion table of XYZ to Wavelength in nanometer
HZ_TO_M         = 299792458                                                 # 1 THz = THZ_TO_M wavelength in meter
BITRATE         = 16000                                                     # number of frames per seconds
numberOfFrames  = int(BITRATE * 0.2)                                        # set time for each sound

#*************
class Sounder:
#*************
  # ----------------------
  def __init__(self):
  # ----------------------
    self.noise = b''
    ''' will be needed once MATH
    self.cursor = -1

    self.__wavelengthTable = []
    with open(CONVERTER_PATH, 'r') as csvfile:
      dictReader = csv.DictReader(csvfile)
      for row in dictReader:
        self.__wavelengthTable.append(row)
      csvfile.close()
    
    self.table = {
      'X': [],
      'Y': [],
      'Z': [],
      'WL': []
    }
    for row in self.__wavelengthTable:
      self.table['X'].append(float(row['X']))
      self.table['Y'].append(float(row['Y']))
      self.table['Z'].append(float(row['Z']))
      self.table['WL'].append(float(row['WL']))
    '''

  ''' The WIP side of things, one day it will math
  # ------------------------------------
  def get_tableAt(self, rowIdx,  label):
  # ------------------------------------
    if rowIdx >= self.get_tableLength():
      return False
    return self.__wavelengthTable[rowIdx][label.upper()]

  # ----------------------------
  def get_cursorAt(self, label):
  # ----------------------------
    return self.get_tableAt(self.cursor, label)
  
  # ------------------------
  def get_tableLength(self):
  # ------------------------
    return len(self.__wavelengthTable)
  
  # --------------------
  def cursorReset(self):
  # --------------------
    self.cursor = -1

  # -----------------------------------------
  def cursorMatchAt(self, matchValue, label):
  # -----------------------------------------
    while matchValue != self.get_cursorAt(label):
      self.cursor += 1
      if self.cursor > self.get_tableLength():
        return False
    
    return self.get_cursorAt(label)
  
  # -----------------------------------------
  def findNearestAt(self, matchValue, label):
  # -----------------------------------------
    array = np.asarray(self.table[label])
    idx = (np.abs(array - matchValue)).argmin()
    return idx
  
  # -----------------------------------------
  def findNearestWithin(self, matchValue, label, sample):
  # -----------------------------------------
    idxLimits = [x - 380 for x in sample]
    sliced = []
    for value in itertools.islice(self.table[label], idxLimits[0], idxLimits[1]):
      sliced.append(value)
    
    array = np.array(sliced)
    idx = (np.abs(array - matchValue)).argmin() + idxLimits[0]
    return idx
  
  # can't use while I don't know what I'm doing
  # def interpolate(self, matchValue):
  #   points = np.array(self.table['X'], self.table['Y'], self.table['Z'])
  #   grid_x, grid_y = np.mgrid[0:1:100j, 0:1:200j]
  #   grid = griddata(points, matchValue, (grid_x, grid_y), method='nearest')
  #   print(grid)
  #   return grid
  
  # -------------------------------------
  def aproxMatch(self, rgb, XYZArray):
  # -------------------------------------
    wlTendency = waveTendency(rgb)

    x = float(round(XYZArray[0] * 10, 4))
    y = float(round(XYZArray[1] * 10, 4))
    z = float(round(XYZArray[2] * 10, 4))
    # print("\n    [{}:{}:{}]".format(x,y,z))
    xfound = self.findNearestWithin(x, 'X', wlTendency)
    yfound = self.findNearestWithin(y, 'Y', wlTendency)
    zfound = self.findNearestWithin(z, 'Z', wlTendency)
    # print("    [{}:{}:{}]".format(xfound,yfound,zfound))
    
    mx = max([xfound, yfound, zfound])
    mn = min([xfound, yfound, zfound])
    diff = mx - mn
    print(diff)

    if diff > 5 or mx <= 0:
      return False
   
    print("    [{}:{}:{}]".format(xfound,yfound,zfound))
    return (xfound + yfound + zfound)/3
  '''
  ''' Previous test iterator
  # -------------------------------------
  def cursorIterateMatch(self, XYZArray):
  # -------------------------------------
    x = float(round(XYZArray[0]*10, 4))
    y = float(round(XYZArray[1]*10, 4))
    z = float(round(XYZArray[2]*10, 4))
    # print("[{}:{}:{}]".format(x,y,z))
    # self.findNearestAt(XYZArray)
    found = False
    while found == False:
      if self.cursor >= self.get_tableLength():
        break
      found = self.cursorMatchAt(x, 'X')
      if found != False:
        # print("x:{}".format(x))
        found = self.cursorMatchAt(y, 'Y')
        if found != False:
          # print("y:{}".format(y))
          found = self.cursorMatchAt(z, 'Z')
          if found != False:
            # print("z:{}".format(z))
            self.cursorReset
            return found
      # print(found)
      found = False
      self.cursorReset()
      return found
  '''
  '''
  # --------------------------------
  def estimateWaveAtXYZ(self, rgb, XYZArray):
  # --------------------------------
    # found = self.cursorIterateMatch(XYZArray)
    found = self.aproxMatch(rgb, XYZArray)
    print(found)
    if found is False:
      # print("Ended with no match for {}:{}:{}".format(
      #   XYZArray[0],
      #   XYZArray[1],
      #   XYZArray[2]))
      return found
    
    if isinstance(found, list):
      return found['WL']
    return found

  def requestTHzAtXYZ(self, rgb, XYZArray):
    wavelength = self.estimateWaveAtXYZ(rgb, XYZArray)
    # print(wavelength)
    if wavelength is False:
      # print("    No match.")
      return
    
    return convertWlToHz(wavelength)
  '''
  def pixarrayToNoise(self, pixarray):#, colorSpace):
    t = time()
    pixelCount = 0
    filledCount = 0
    
    noise = b''
    for row in pixarray:
      for pixel in row:
        pixelCount += 1
        RGBASum    = sum(v for v in pixel)
        
        if RGBASum * pixel[-1] > 0:                                                  # if (sum of RGB) * A > 0
          filledCount += 1
          RGBColor = RGB(pixel[0], pixel[1], pixel[2])                               # get sRGB values from RGB
          ''' when MATH
          # c = RGBColor.get_RGBVec() 
          # print("{}:{}:{}".format(c.x, c.y, c.z))
          # toXYZ     = colorSpace.RGBColorToXYZ(RGBColor)                           # get color XYZ position
          # print("XYZ{} at: [{}]".format(toXYZ.toArray(), countDecal + count))
          # XYZArray  = toXYZ.toArray()
          # frequency = self.requestTHzAtXYZ(RGBColor, XYZArray)
          '''
          aproxWl = waveTendency(RGBColor)
          wl = aproxWl['wave']
          # print(wl)

          if isinstance(wl, (float, int)):
            pitch = downToPitch(convertWlToHz(wl))
            noise += createWaveData(pitch)
    
    self.noise = noise
    print("\n  Noise of length {} has been registered in {} seconds".format(filledCount, time() - t))
    return self.noise
    
  # --------------------------------
  def playNoise(self, noise_Ext = False):
  # --------------------------------
    t = time()
    noise = noise_Ext
    if noise is False:
      noise = self.noise
    
    pA = PyAudio()
    stream = pA.open(
      format = pA.get_format_from_width(1),
      channels = 1,
      rate = BITRATE,
      output = True)
    stream.write(noise)
    stream.stop_stream()
    stream.close()
    pA.terminate()
    print("  Noise has been played in {} seconds\n".format(time() - t))

#*****************************************************************
def waveTendency(rgb):
# returns the aproximated wavelength based on based on observation
# not math and not "right", but working as a demo
# will get replaced in time
#*****************************************************************
  r = rgb.r
  g = rgb.g
  b = rgb.b
  if isinstance(r, np.float32) or isinstance(g, np.float32) or isinstance(b, np.float32):         # if is an np float 32
    if r <= 1 and g <= 1 and b <= 1:                                                              # and is between 0.0 and 1.0
      r = int(r * 255)                                                                            # turn into base rgb values
      g = int(g * 255)
      b = int(b * 255)

  mx = max([r, g, b])
  mn = min([r, g, b])
  mid = r + g + b - mx - mn
  total = mx + mid + mn

  tendency = None
  aproxFactor = 0
  if mx <= 0 :                                                # fristly : restrict special cases like 0 value
    return { 'wave' : 0, 'factor' : 0 }

  if or_(
    and_(mx == r, mid == b),
    and_(
      and_(mx == b, mid == r),
      and_(r > (mx / 2), g <= r / 2))
    ):                                                        # , low spectrum
    tendency = [380, 414]
  elif mx == r and r < 255 and mn + mid < (mx / 2):           # and high spectrum
    tendency = [651, 780]
  else:
    if mx == b and mid == r:                                  # if any of above find wavelength tendency
      tendency = [415, 440]
    elif mx == b and mid == g:
      tendency = [441, 490]
    elif mx == g and mid == b:
      tendency = [491, 508]
    elif mx == g and mid == r:
      tendency = [509, 580]
    elif mx == r and mid == g:
      tendency = [581, 650]
  
  aproxFactor = (mx + mid) / (255*2)                          # math bleed upon this day
  aproxInRange = aproxFactor * (tendency[1] - tendency[0])
  aproxWl = tendency[0] + aproxInRange
  
  return { 'wave' : aproxWl, 'factor' : aproxFactor }

#******************************
def convertWlToHz(wavelength):
# wavelength in nm to THz
#******************************
  if isinstance(wavelength, float):
    return HZ_TO_M / (wavelength * 10**-9)
  return False

#********************
def downToPitch(freq):
#********************
  if isinstance(freq, float):
    return freq / 2**40                          # THz electro magnetic value reduced by 40 octaves to match a sound
  return False

#***************************
def createWaveData(
  frequency,
  duration = numberOfFrames,
  volume=1,
  sample_rate=BITRATE):
#***************************
  n_samples = int(sample_rate * duration)
  restFrames = n_samples % sample_rate

  waveData = b''.join(str.encode(chr(int(math.sin(x / ((BITRATE / frequency) / 2*math.pi)) * 127 + 128))) for x in range(duration))
  waveData.join([str.encode(chr(128))] * restFrames)        # fill remainder of frameset with silence
  
  return waveData
