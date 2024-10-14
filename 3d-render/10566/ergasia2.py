import numpy as np
import cv2 as cv
from typing import Tuple
import math
import matplotlib


  
def world2view(pts: np.ndarray, R: np.ndarray, c0: np.ndarray) -> np.ndarray:
        Rinv=np.linalg.inv(R)
        newpoint=np.zeros((pts.shape[1],pts.shap[0]))
        i=0
        for point in pts:
            if point.shape == (3,1):
                
                newpoint[i]=np.dpt(Rinv,(point-c0))
                i=+1
        newpoint=newpoint.T
        
        return newpoint
  
def lookat(eye: np.ndarray, up: np.ndarray, target: np.ndarray) ->  tuple[np.ndarray,np.ndarray]:
        
    
        zc= target - eye
        zc /= np.linalg.norm(zc)

        inner=np.inner(up.T,zc.T)
        t1= up - np.dot(inner,zc.T)
        # Calculate the right vector
        yc = t1.T/np.linalg.norm(t1.T)
    
        # Recalculate the up vectors
        xc = np.cross(yc.T,zc.T)
        xc=xc.T
        # Construct the rotation matrix
        R = np.zeros((3,3))
        for i in range(3):
            R[i][0] = xc[i][0]
            R[i][1] = yc[i][0]
            R[i][2] = zc[i][0]
            
        # Calculate the translation vector
        t = eye
        print(R)
        return R, t
   
   
def perspective_project(pts: np.ndarray, focal: float, R:np.ndarray, t: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    # Apply the rotation and translation to the points
        transformed_pts = np.dot(R, pts) + t[:, np.newaxis]
    
    # Project the points onto the image plane
        depth = transformed_pts[2]  # Extract the depth
        projected_pts = (focal / depth) * transformed_pts[:2]
    
        return projected_pts, depth
    
def rasterize(pts_2d: np.ndarray, plane_w: int, plane_h: int, res_w: int, res_h: int) -> np.ndarray:
    # Scale the points to fit the resolution of the image
        x_scale = res_w / plane_w
        y_scale = res_h / plane_h
        scaled_pts = pts_2d * np.array([x_scale, y_scale])
    
    # Round the scaled points to the nearest integer coordinates
        rasterized_pts = np.round(scaled_pts).astype(int)
    
    # Flip the y-coordinates to match the image coordinate system
        rasterized_pts[:, 1] = res_h - rasterized_pts[:, 1]
    
        return rasterized_pts
        
    
    
  
def render_object(v_pos, v_clr, t_pos_idx, plane_h, plane_w, res_h, res_w, focal, eye, up, target) -> np.ndarray:
        # Calculate the camera's view matrix using the lookat function
        R, t = lookat(eye, up, target)

        # Apply camera transformation to the vertices of the object
        transformed_vertices = world2view(v_pos, R, eye)

        # Perform perspective projection to project vertices onto the image plane
        projected_pts, depth = perspective_project(transformed_vertices.T, focal, R, t)

        # Rasterize the projected vertices to obtain pixel coordinates on the image
        rasterized_pts = rasterize(projected_pts.T, plane_w, plane_h, res_w, res_h)

        return rasterized_pts
    
    
def construct_edges(img, x1, x2, y1, y2, a, b, B, G, R):

        line = list()
        if a == 0.0:
            for x in range(min(x1, x2) , max(x1, x2) + 1 ):
                img[y1, x] = [B, G, R]
        elif not math.isinf(a):
            for y in range(min(y1, y2) , max(y1, y2) + 1 ):
                line.append([(y - b) / a, y])
        else:
            for y in range(min(y1, y2) , max(y1, y2) + 1):
                line.append([x1, y])

        return line
def vector_interp(p1, p2, V1, V2, coord, dim):

    x1, y1 = p1
    x2, y2 = p2

    # Υπολογίστε την τιμή V με βάση τις διαστάσεις dim
    if dim == 1:  # Εάν η dim είναι 1 (σχετική με το x)
        V = V1 + (V2 - V1) * ((coord - x1) / (x2 - x1))
    elif dim == 2:  # Εάν η dim είναι 2 (σχετική με το y)
        V = V1 + (V2 - V1) * ((coord - y1) / (y2 - y1))
    else:
        raise ValueError("THE DIM MUST BE 1 OR 2")

    return V
def check_for_duplicates(line1, line2, vertices): 

        for i in range(len(line1)):
            for j in range(len(line2)):

                if not is_vertice(line1[i][0], line1[i][1], vertices) and not is_vertice(line2[j][0], line2[j][1], vertices) and line1[i][1] == line2[j][1] and round(line1[i][0]) == round(line2[j][0]):
                    if line1[i][0] < line2[j][0]:
                        line1[i][0] = int(line1[i][0])
                        line2[j][0] = int(line2[j][0]) + 1
                    else:
                        line1[i][0] = int(line1[i][0]) + 1
                        line2[j][0] = int(line2[j][0])
                else:
                    line1[i][0] = int(line1[i][0])
                    line2[j][0] = int(line2[j][0])
        
        return line1, line2
    
def draw_img(img, x, y, x1, y1, x2, y2):
        img[y, x] = np.array([vector_interp((x1,y1),(x2,y2),vcolors[0][0],vcolors[1][0],y,2),
                            vector_interp((x1,y1),(x2,y2),vcolors[0][1],vcolors[1][1],y,2),
                            vector_interp((x1,y1),(x2,y2),vcolors[0][2],vcolors[1][2],y,2)])
     
def is_vertice(x, y, vertices):

        for vertice in vertices:
            if vertice[0] == x and vertice[1] == y:
                return True

        return False   
    
def g_shading(img,vertices,vcolors):     
        x1=vertices[0][0]
        y1=vertices[0][1]
        x2=vertices[1][0]
        y2=vertices[1][1]
        x3=vertices[2][0]
        y3=vertices[2][1]

        # x1=10
        # y1=56
        # x2=100
        # y2=100
        # x3=20
        # y3=100

        print(x1, y1, x2, y2, x3, y3)

        ymin=min(y1,y2,y3)
        ymax = max(y1,y2,y3)

        if x1 != x2:
            a1=(y2-y1)/(x2-x1)
        else:
            a1 = float("inf")
        if x2 != x3:
            a2=(y3-y2)/(x3-x2)
        else:
            a2 = float("inf")
        if x1 != x3:
            a3=(y3-y1)/(x3-x1)
        else:
            a3 = float("inf")

        b1=y1-a1*x1
        b2=y2-a2*x2
        b3=y3-a3*x3
        
        R = (vcolors[0][0] + vcolors[1][0] + vcolors[2][0]) / 3
        B = (vcolors[0][1] + vcolors[1][1] + vcolors[2][1]) / 3
        G = (vcolors[0][2] + vcolors[1][2] + vcolors[2][2]) / 3
        # R = 0.5
        # G = 0.5
        # B = 0.5
        
        line1 = construct_edges(img, x1, x2, y1, y2, a1, b1, B, G, R)
        line2 = construct_edges(img, x2, x3, y2, y3, a2, b2, B, G, R)
        line3 = construct_edges(img, x1, x3, y1, y3, a3, b3, B, G, R)

        check_for_duplicates(line1, line2, vertices)
        check_for_duplicates(line2, line3, vertices)
        check_for_duplicates(line1, line3, vertices)
        
        print(line1, line2, line3)

        curr_x = list()
        for y in range(ymin, ymax + 1):
            cross_count=0

            curr_x.clear()
            hit_line1 = False
            hit_line2 = False
            hit_line3 = False
            for x in range(512):
                if is_vertice(int(x), int(y), vertices):
                    img[y, x] = [B, G, R]
                    break
                
                if [x,y] in line1:
                    color_A = np.array([vector_interp((x1,y1),(x2,y2),vcolors[0][0],vcolors[1][0],y,2),
                                       vector_interp((x1,y1),(x2,y2),vcolors[0][1],vcolors[1][1],y,2),
                                       vector_interp((x1,y1),(x2,y2),vcolors[0][2],vcolors[1][2],y,2)])
                    img[y, x]=color_A
                    cross_count=cross_count+1
                    hit_line1 = True
                elif [x,y] in line2:
                    color_B = np.array([vector_interp((x2,y2),(x3,y3),vcolors[1][0],vcolors[2][0],y,2),
                                       vector_interp((x2,y2),(x3,y3),vcolors[1][1],vcolors[2][1],y,2),
                                       vector_interp((x2,y2),(x3,y3),vcolors[1][2],vcolors[2][2],y,2)])
                    img[y, x]=color_B
                    cross_count=cross_count+1
                    hit_line2 = True
                elif [x,y] in line3:
                    color_C = np.array([vector_interp((x1,y1),(x3,y3),vcolors[0][0],vcolors[2][0],y,2),
                                       vector_interp((x1,y1),(x3,y3),vcolors[0][1],vcolors[2][1],y,2),
                                       vector_interp((x1,y1),(x3,y3),vcolors[0][2],vcolors[2][2],y,2)])
                    img[y, x]=color_C
                    cross_count=cross_count+1
                    hit_line3 = True

                if cross_count % 2 != 0:
                    curr_x.append(x)

            for x in curr_x:
                if hit_line1 and hit_line2:
                    draw_img(img, x, y, x1, y1, x2, y2)
                elif hit_line2 and hit_line3:
                    draw_img(img, x, y, x2, y2, x3, y3)
                elif hit_line1 and hit_line3:
                    draw_img(img, x, y, x1, y1, x3, y3)

