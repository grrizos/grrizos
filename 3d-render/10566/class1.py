import numpy as np
import cv2 as cv
from typing import Tuple
import math
import matplotlib
class Transform:
    def __init__(self):
        self.mat = np.eye(4)
    
    def rotate(self, theta: float, u: np.ndarray) -> None:
    # Ensure u is a unit vector
        # Compute rotation matrix
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        ux, uy, uz = u
        rotation_matrix = np.identity(4)
        #     [cos_theta + ux**2*(1-cos_theta), ux*uy*(1-cos_theta) - uz*sin_theta, ux*uz*(1-cos_theta) + uy*sin_theta, 0],
        #     [uy*ux*(1-cos_theta) + uz*sin_theta, cos_theta + uy**2*(1-cos_theta), uy*uz*(1-cos_theta) - ux*sin_theta, 0],
        #     [uz*ux*(1-cos_theta) - uy*sin_theta, uz*uy*(1-cos_theta) + ux*sin_theta, cos_theta + uz**2*(1-cos_theta), 0],
        #     [0, 0, 0, 1]
        # ])
        rotation_matrix[0][0]= cos_theta + ux*ux*(1-cos_theta)
        rotation_matrix[0][1]= ux*uy*(1-cos_theta) - uz*sin_theta
        rotation_matrix[0][2]= ux*uz*(1-cos_theta) + uy*sin_theta
        rotation_matrix[0][3]= 0
        
        rotation_matrix[1][0]= uy*ux*(1-cos_theta) + uz*sin_theta
        rotation_matrix[1][1]= cos_theta + uy**2*(1-cos_theta)
        rotation_matrix[1][2]= uy*uz*(1-cos_theta) - ux*sin_theta
        rotation_matrix[1][3]= 0

        rotation_matrix[2][0]= uz*ux*(1-cos_theta) - uy*sin_theta
        rotation_matrix[2][1]= uz*uy*(1-cos_theta) + ux*sin_theta
        rotation_matrix[2][2]= cos_theta + uz**2*(1-cos_theta)
        rotation_matrix[2][3]=0

        rotation_matrix[3][0]= 0
        rotation_matrix[3][1]= 0
        rotation_matrix[3][2]= 0
        rotation_matrix[3][3]= 1
        # Update transformation matrix
        self.mat = np.dot(rotation_matrix, self.mat)



    def translate(self, t: np.ndarray) -> None:
   
    # Create translation matrix
        tx,ty,tz=t
        translation_matrix = np.identity(4)
        translation_matrix[0][3]=tx
        translation_matrix[1][3]=ty
        translation_matrix[2][3]=tz
    # Update transformation matrix
        self.mat = np.dot(translation_matrix, self.mat)
    
    def transform_pts(self, pts: np.ndarray) -> np.ndarray:
    
        homogeneous_v_pos = []
        for point in pts:
    
            homogeneous_point = np.append(point, 1)
    
            homogeneous_point = homogeneous_point.reshape(1, -1)
            homogeneous_v_pos.append(homogeneous_point)

# Stack all points to form the final homogeneous array
        homogeneous_v_pos = np.vstack(homogeneous_v_pos)
        return homogeneous_v_pos
