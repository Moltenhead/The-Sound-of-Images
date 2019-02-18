# -*- coding: utf-8 -*-
from __future__ import division
# ------ IMPORTS ------ #
__package__  = './'
# Ext
import  csv
import  numpy               as     np
from    pyaudio             import PyAudio
from    scipy.interpolate   import griddata 
# Local
import  math
# Home brewed
from    os                  import path, pardir

# ------ CONSTANTS ------ #
ROOT            = path.dirname(path.abspath(path.join(__file__, pardir)))
CONVERTER_PATH  = ROOT + "\\ressources\\XYZ_to_Wavelength_nm.csv"       # conversion table of XYZ to Wavelength in nanometer
THZ_TO_NM       = 299792.458                                            # 1 THz = THZ_TO_NM wavelength in nanometer
BITRATE         = 16000                                                 # number of frames per seconds

#*************
class Sounder:
#*************
  # ----------------------
  def __init__(self):
  # ----------------------
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
  
  def findNearestAt(self, matchValue, label):
    array = np.asarray(self.table[label])
    idx = (np.abs(array - matchValue)).argmin()
    return idx
  
  def interpolate(self, matchValue):
    points = np.array([self.x, self.y, self.z])
    grid_x, grid_y = np.mgrid[0:1:100j, 0:1:200j]
    grid = griddata(points, matchValue, (grid_x, grid_y), method='nearest')
    print(grid)
    return grid

  # -----------------------------------------
  def cursorMatchAt(self, matchValue, label):
  # -----------------------------------------
    while matchValue != self.get_cursorAt(label):
      self.cursor += 1
      if self.cursor > self.get_tableLength():
        return False
    
    return self.get_cursorAt(label)
  
  # -------------------------------------
  def aproxMatch(self, XYZArray):
  # -------------------------------------
    x = float(round(XYZArray[0], 4))
    y = float(round(XYZArray[1], 4))
    z = float(round(XYZArray[2], 4))
    # print("[{}:{}:{}]".format(x,y,z))
    xfound = self.findNearestAt(x, 'X')
    yfound = self.findNearestAt(y, 'Y')
    zfound = self.findNearestAt(z, 'Z')
    # print("[{}:{}:{}]".format(xfound,yfound,zfound))
    
    mx = max([xfound, yfound, zfound])
    mn = min([xfound, yfound, zfound])
    diff = mx - mn

    if diff > 5:
      return False
   
    print("[{}:{}:{}]".format(xfound,yfound,zfound))
    return (xfound + yfound + zfound)/3

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
        print("x:{}".format(x))
        found = self.cursorMatchAt(y, 'Y')
        if found != False:
          print("y:{}".format(y))
          found = self.cursorMatchAt(z, 'Z')
          if found != False:
            print("z:{}".format(z))
            self.cursorReset
            return found
      # print(found)
      found = False
      self.cursorReset()
      return found
  
  # --------------------------------
  def findWaveAtXYZ(self, XYZArray):
  # --------------------------------
    # found = self.cursorIterateMatch(XYZArray)
    found = self.aproxMatch(XYZArray)
    # print(found)
    if found is False:
      # print("Ended with no match for {}:{}:{}".format(
      #   XYZArray[0],
      #   XYZArray[1],
      #   XYZArray[2]))
      return found
    
    if isinstance(found, list):
      return found['WL']
    return found
  
  # --------------------------------
  def play(self, frequency, seconds):
  # --------------------------------
    if not isinstance(frequency, float):
      return False
    numberOfFrames = int(BITRATE * seconds)
    restFrames = numberOfFrames % BITRATE
    waveData = ''

    for x in range(numberOfFrames):
      waveData += chr(int(math.sin(x / ((BITRATE / frequency) / 2*math.pi)) * 127 + 128))
    
    # fill remainder of frameset with silence
    for x in range(restFrames):
      waveData += chr(128)
    
    pA = PyAudio()
    stream = pA.open(
      format = pA.get_format_from_width(1),
      channels = 1,
      rate = BITRATE,
      output = True)
    stream.write(waveData)
    stream.stop_stream()
    stream.close()
    pA.terminate()

  def requestXYZPlay(self, XYZArray, seconds):
    wavelength = self.findWaveAtXYZ(XYZArray)
    # print(wavelength)
    if wavelength is False:
      # print("    No match.")
      return
    
    toTHz = convertWlToTHz(wavelength)
    self.play(toTHz, seconds)

#************************************
def convertWlToTHz(wavelength):
# wavelength in nm to THz
#************************************
  if isinstance(wavelength, float):
    return THZ_TO_NM / wavelength
  return False
