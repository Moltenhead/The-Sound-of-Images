# -*- coding: utf-8 -*-
from __future__ import division
# ------ IMPORTS ------ #
# Ext
import  numpy               as     np
from    pyaudio             import PyAudio
# Local
import  math
from    time                import time
from    operator            import or_, and_
from    os                  import path, pardir
# Home brewed
import  sys
sys.path.append('.')
from    .RGBUtil            import RGB

# ------ CONSTANTS ------ #
HZ_TO_M         = 299792458                                                 # 1 Hz = HZ_TO_M wavelength in meter
BITRATE         = 22050                                                     # number of frames per seconds
numberOfFrames  = int(BITRATE * 0.2)                                        # set time for each sound

#*************
class Sounder:
#*************
  # ----------------------
  def __init__(self):
  # ----------------------
    self.noise = b''
  
  # ----------------------------------
  def pixarrayToNoise(self, pixarray):
  # ----------------------------------
    t = time()
    pixelCount = 0
    filledCount = 0
    
    noise = b''
    for row in pixarray:
      for pixel in row:
        pixelCount += 1
        RGBASum    = sum(v for v in pixel)
        
        if RGBASum * pixel[-1] > 0:                                   # if (sum of RGB) * A > 0
          filledCount += 1
          RGBColor = RGB(pixel[0], pixel[1], pixel[2])                # get sRGB values from RGB
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
      format = pA.get_format_from_width(1),       # 8 bit
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
