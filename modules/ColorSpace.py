# -*- coding: utf-8 -*-
import sys
sys.path.append(".\\")
import vectorizedMatrix as vmat

#****************
class ColorSpace:
#****************
  def __init__(self, red_xy, green_xy, blue_xy, white_xy):
    self.red = red_xy
    self.green = green_xy
    self.blue = blue_xy
    self.white = white_xy

    self.toXYZ = self.get_ConvertedToXYZ()

  # --------------------------------------------
  def get_ConvertedToXYZ(self):
  # Convert a linear sRGB color to an sRGB color
  # --------------------------------------------
    # generate xyz chromaticity coordinates (x + y + z = 1) from xy coordinates
    r = vmat.Vec3(self.red.x, self.red.y, 1.0 - (self.red.x + self.red.y))
    g = vmat.Vec3(self.green.x, self.green.y, 1.0 - (self.green.x + self.green.y))
    b = vmat.Vec3(self.blue.x, self.blue.y, 1.0 - (self.blue.x + self.blue.y))
    w = vmat.Vec3(self.white.x, self.white.y, 1.0 - (self.white.x + self.white.y))

    # Convert white xyz coordinate to XYZ coordinate by letting that the white
    # point have and XYZ relative luminance of 1.0. Relative luminance is the Y
    # component of and XYZ color.
    #   XYZ = xyz * (Y / y)
    w.x /= self.white.y
    w.y /= self.white.y
    w.z /= self.white.y

    # Solve for the transformation matrix 'M' from RGB to XYZ
    # * We know that the columns of M are equal to the unknown XYZ values of r, g and b.
    # * We know that the XYZ values of r, g and b are each a scaled version of the known
    #   corresponding xyz chromaticity values.
    # * We know the XYZ value of white based on its xyz value and the assigned relative
    #   luminance of 1.0.
    # * We know the RGB value of white is (1,1,1).
    #                  
    #   white_XYZ = M * white_RGB
    #
    #       [r.x g.x b.x]
    #   N = [r.y g.y b.y]
    #       [r.z g.z b.z]
    #
    #       [sR 0  0 ]
    #   S = [0  sG 0 ]
    #       [0  0  sB]
    #
    #   M = N * S
    #   white_XYZ = N * S * white_RGB
    #   N^-1 * white_XYZ = S * white_RGB = (sR,sG,sB)
    #
    # We now have an equation for the components of the scale matrix 'S' and
    # can compute 'M' from 'N' and 'S'

    m = vmat.Mat3x3()
    m.setCol(0, r)
    m.setCol(1, g)
    m.setCol(2, b)

    mInv = m.copy()
    mInv.invert()
    mScale = mInv.mulVec(w)

    m.mulAllByVec(mScale)
    return m
  
  # --------------------------------------
  def sRGBColorToXYZ(self, sRGBColor):
  # returns given color converted into XYZ
  # --------------------------------------
    return self.toXYZ.mulVec(sRGBColor.get_sRGBVec().copy().gammaExpand())
  
  # -------------------------------------
  def XYZColorTosRGB(self, XYZColor):
  # returns given XYZ converted into sRGB
  # -------------------------------------
    return self.toXYZ.copy().invert().mulVec(XYZColor.copy()).gammaCompress()
