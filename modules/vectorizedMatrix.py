# -*- coding: UTF-8 -*-
import copy

import sys
sys.path.append(".\\")
import sRGBUtil

#**********************
class Vec2:
# 2-dimensional vector.
#**********************
  # -----------------------
  def __init__(self, x, y):
  # -----------------------
    self.x = x
    self.y = y

#**********************
class Vec3(Vec2):
# 3-dimensional vector.
#**********************
  # --------------------------
  def __init__(self, x, y, z):
  # --------------------------
    super().__init__(x,y)
    self.z = z
  
  # -------------
  def copy(self):
  # -------------
    return copy.deepcopy(self)

  # ----------------
  def toArray(self):
  # ----------------
    return [self.x, self.y, self.z]
  
  # --------------------
  def gammaExpand(self):
  # cf sRGBUtil
  # --------------------
    self.x = sRGBUtil.gammaExpand(self.x)
    self.y = sRGBUtil.gammaExpand(self.y)
    self.z = sRGBUtil.gammaExpand(self.z)
    return self
  
  # ----------------------
  def gammaCompress(self):
  # cf sRGBUtil
  # ----------------------
    self.x = sRGBUtil.gammaCompress(self.x)
    self.y = sRGBUtil.gammaCompress(self.y)
    self.z = sRGBUtil.gammaCompress(self.z)
    return self

#**************
class Mat3x3():
# 3x3 matrix
#**************
  # --------------------------
  def __init__(self):
  # --------------------------
    self.m = [[0] * 3] * 3
  
  # --------------------------
  def get(self, row, col):
  # Returns value at subset
  # --------------------------
    return self.m[row][col]
  
  # -------------------------------
  def setAt(self, row, col, value):
  # Set value at subset
  # -------------------------------
    self.m[row][col] = value

  # -----------------------------------------------
  def setCol(self, colId, vec3):
  # Set an indexed matrix column to a given vector.
  # -----------------------------------------------
    for idx, row in enumerate(self.m):
      row[colId] = vec3.toArray()[idx]
  
  # ----------------------------------------------------
  def copy(self):
  # Returns a copy of this Matrix at the execution state
  # ----------------------------------------------------
    return copy.deepcopy(self)
  
  
  # --------------------------------------
  def invert(self):
  # Calculate the inverse of a 3x3 matrix.
  # Returns false if it is non-invertible.
  # --------------------------------------
    # calculate minors for the frist row
    minor00 = self.get(1,1)*self.get(2,2) - self.get(1,2)*self.get(2,1)
    minor01 = self.get(1,2)*self.get(2,0) - self.get(1,0)*self.get(2,2)
    minor02 = self.get(1,0)*self.get(2,1) - self.get(1,1)*self.get(2,0)

    # calculate the determinant
    determinant = self.get(0,0) * minor00 + self.get(0,1) * minor01 + self.get(0,2) * minor02

    # check if the input is a singular matrix (non-invertable)
    # (note that the epsilon here was arbitrarily chosen)
    if determinant > -0.000001 and determinant < 0.000001:
      return False

    # inverse of Matrix is (1 / determinant) * adjoint(Matrix)
    invDet = 1.0 / determinant
    self.setAt(0,0,invDet * minor00)
    self.setAt(0,1,invDet * (self.get(2,1)*self.get(0,2) - self.get(2,2)*self.get(0,1)))
    self.setAt(0,2,invDet * (self.get(0,1)*self.get(1,2) - self.get(0,2)*self.get(1,1)))

    self.setAt(1,0,invDet * minor01)
    self.setAt(1,1,invDet * (self.get(2,2)*self.get(0,0) - self.get(2,0)*self.get(0,2)))
    self.setAt(1,2,invDet * (self.get(0,2)*self.get(1,0) - self.get(0,0)*self.get(1,2)))

    self.setAt(2,0,invDet * minor02)
    self.setAt(2,1,invDet * (self.get(2,0)*self.get(0,1) - self.get(2,1)*self.get(0,0)))
    self.setAt(2,2,invDet * (self.get(0,0)*self.get(1,1) - self.get(0,1)*self.get(1,0)))

    return True
  
  # --------------------------------------
  def mulVec(self, vec3):
  # multiply given vector with the matrix
  # return the resulting vector
  # --------------------------------------
    vec3Out = Vec3(self.get(0,0)*vec3.x + self.get(0,1)*vec3.x + self.get(0,2)*vec3.x, self.get(1,0)*vec3.y + self.get(1,1)*vec3.y + self.get(1,2)*vec3.y, self.get(2,0)*vec3.z + self.get(2,1)*vec3.z + self.get(2,2)*vec3.z)
    return vec3Out

  # ----------------------------------
  def mulByAt(self, value,  row, col):
  # multiply target subset by value
  # ----------------------------------
    self.setAt(row,col,self.get(row,col)*value)

  # ------------------------------------
  def mulRowByVec(self, row, vec3):
  # multiply target matrix row by vector
  # ------------------------------------
    for idx, colValue in enumerate(self.m[row]):
      self.mulByAt(colValue * vec3.toArray()[idx], row, idx)
  
  # -----------------------------------
  def mulAllByVec(self, vec3):
  # multiply the whole matrix by vector
  # -----------------------------------
    for idx, row in enumerate(self.m):
      self.mulRowByVec(idx, vec3)
