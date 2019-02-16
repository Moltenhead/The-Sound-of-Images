# -*- coding: utf-8 -*-
from __future__ import division
# ------ IMPORTS ------ #
__package__  = './'
# Ext
import  csv
from    pyaudio        import PyAudio
# Local
import  math
# Home brewed
from    os            import path, pardir

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
    self.cursor = 0

    self.__wavelengthTable = []
    with open(CONVERTER_PATH, 'r') as csvfile:
      dictReader = csv.DictReader(csvfile)
      for row in dictReader:
        self.__wavelengthTable.append(row)
      csvfile.close()
  
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
    self.cursor = 0

  # -----------------------------------------
  def cursorMatchAt(self, matchValue, label):
  # -----------------------------------------
    while matchValue != self.get_cursorAt(label):
      self.cursor += 1
      if self.cursor > self.get_tableLength():
        return False
    
    return self.get_cursorAt(label)
  
  # -------------------------------------
  def cursorIterateMatch(self, XYZArray):
  # -------------------------------------
    x = round(XYZArray[0]*10, 4)
    y = round(XYZArray[1]*10, 4)
    z = round(XYZArray[2]*10, 4)
    print("[{}:{}:{}]".format(x,y,z))
    found = False
    while found == False:
      if self.cursor < self.get_tableLength():
        break
      found = self.cursorMatchAt(x, 'X')
      if found != False:
        found = self.cursorMatchAt(y, 'Y')
        if found != False:
          found = self.cursorMatchAt(z, 'Z')
          if found != False:
            self.cursorReset
            return found
      
      found = False
      self.cursorReset()
      return found
  
  # --------------------------------
  def findWaveAtXYZ(self, XYZArray):
  # --------------------------------
    found = self.cursorIterateMatch(XYZArray)
    if found is False:
      print("Ended with no match for {}:{}:{}".format(
        XYZArray[0],
        XYZArray[1],
        XYZArray[2]))
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
    print(wavelength)
    if wavelength is False:
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

    


