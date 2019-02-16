# -*- coding: utf-8 -*-
# ------ IMPORTS ------ #
from __future__ import division
# Ext
import  csv
from    pyaudio import PyAudio
# Local
import  math
# Home brewed
from    sys     import path
path.append("../")
from    app     import ROOT

# ------ CONSTANTS ------ #
CONVERTER_PATH  = ROOT + "\\ressources\\XYZ_to_Wavelength_nm.csv"       # conversion table of XYZ to Wavelength in nanometer
THZ_TO_NM       = 299792.458                                            # 1 THz = THZ_TO_NM wavelength in nanometer
BITRATE         = 16000                                                 # number of frames per seconds

#*************
class Sounder:
#*************
  # ----------------------
  def __init__(self, csv):
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
    found = False
    while found == False and self.cursor < self.get_tableLength():
      found = self.cursorMatchAt(XYZArray[0], 'X')
      if found != False:
        found = self.cursorMatchAt(XYZArray[1], 'Y')
        if found != False:
          found = self.cursorMatchAt(XYZArray[2], 'Z')
          if found != False:
            return found
      else:
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
    
    return found['WL']
  
  # --------------------------------
  def play(self, frequency, seconds):
  # --------------------------------
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
    if wavelength is False:
      return
    
    toTHz = convertWlToTHz(wavelength)
    self.play(toTHz, seconds)

#************************************
def convertWlToTHz(wavelength):
# wavelength in nm to THz
#************************************
  return THZ_TO_NM / wavelength

    


