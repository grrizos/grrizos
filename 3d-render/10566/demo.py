import ergasia2
import numpy as np
import math
from typing import Tuple
import  cv2
from ergasia2 import render_object,g_shading,check_for_duplicates,construct_edges,vector_interp,draw_img,is_vertice
import class1

img=np.ones((512,512, 3))
data = np.load('hw2.npy', allow_pickle=True)
data = data.item()

v_pos=data.get("v_pos")
v_clr=data.get("v_clr")
t_pos_idx=data.get("t_pos_idx")
plane_h=15
plane_w=15
res_h=512
res_w=512
focal=70
eye=data.get("eye")
up=data.get("up")
target=data.get("target")
theta=data.get("theta_0")
rot_axis_0=data.get("rot_axis_0")
t_0=data.get("t_0")
t_1=data.get("t_1")


transform = class1.Transform()



transform.rotate(theta, rot_axis_0)
transform.translate(t_0)
transform.translate(t_1)
transformed_points=transform.transform_pts(v_pos)
render_object(transformed_points, v_clr, t_pos_idx, plane_h, plane_w, res_h, res_w, focal, eye, up, target)
g_shading(img,transformed_points,v_clr)












# ergasia2.render_object()
# ergasia2.render_object(transformed_v_pos, transformed_v_clr)
# transformed_v_pos = ergasia2.translate_object(transformed_v_pos, t_1)
# ergasia2.render_object(transformed_v_pos, transformed_v_clr)
# transformed_v_pos = ergasia2.translate_object(transformed_v_pos, t_2)
# ergasia2.render_object(transformed_v_pos, transformed_v_clr)
# ergasia2.g_shading(img,transformed_v_pos,transformed_v_clr)
# cv2.imshow("Final", img)

