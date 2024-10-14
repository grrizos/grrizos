import numpy as np
import cv2
import matplotlib
import math

def vector_interp(p1, p2, V1, V2, coord, dim):
    # if dim == 1:
    #     x1, y1 = p1
    #     x2, y2 = p2
    #     x = coord
    #     # Calculaiton of y using integral interporlation
    #     y = ((x2 - x) * V1[0] + (x - x1) * V2[0]) / (x2 - x1)
    #     return [y]
    # elif dim == 2:
    #     x1, y1 = p1
    #     x2, y2 = p2
    #     y = coord
    #     # Calculaiton of x using integral interporlation
    #     x = ((y2 - y) * V1[1] + (y - y1) * V2[1]) / (y2 - y1)
    #     return [x]
    # else:
    #     raise ValueError("DIM 1 OR 2")
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

def is_vertice(x, y, vertices):

    for vertice in vertices:
        if vertice[0] == x and vertice[1] == y:
            return True

    return False

def draw_img(img, x, y, x1, y1, x2, y2):
    img[y, x] = np.array([vector_interp((x1,y1),(x2,y2),vcolors[0][0],vcolors[1][0],y,2),
                        vector_interp((x1,y1),(x2,y2),vcolors[0][1],vcolors[1][1],y,2),
                        vector_interp((x1,y1),(x2,y2),vcolors[0][2],vcolors[1][2],y,2)])

def f_shading(img, vertices, vcolors):
        
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

        line1, line2 = check_for_duplicates(line1, line2, vertices)
        line2, line3 = check_for_duplicates(line2, line3, vertices)
        line1, line3 = check_for_duplicates(line1, line3, vertices)
        
        print(line1, line2, line3)

        for y in range(ymin, ymax + 1):
            cross_count=0

            for x in range(512):
                if is_vertice(int(x), int(y), vertices):
                    img[y, x] = [B, G, R]
                    break

                
                if [x,y] in line1 or [x,y] in line2 or [x,y] in line3:
                    cross_count=cross_count+1
                
                if cross_count % 2 != 0:
                    img[y, x] = [B, G, R]

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

                    
img=np.ones((512,512, 3))
data = np.load('hw1.npy', allow_pickle=True)
data = data.item()

depth = data.get("depth")
faces = data.get("faces")
vertices = data.get("vertices")
vcolors = data.get("vcolors")

sorted_indices = np.argsort(depth)
print(sorted_indices)

sorted_faces = faces[sorted_indices]
for face in sorted_faces:
    current_vertices = [vertices[node] for node in face]
    current_vcolors = [vcolors[node] for node in face]
    # f_shading(img,vertices=current_vertices, vcolors=current_vcolors)
    g_shading(img,vertices=current_vertices, vcolors=current_vcolors)
    # cv2.imshow("Final", img)
    # cv2.waitKey(0)
cv2.imshow("Final", img)
cv2.waitKey(0)

# img=np.ones((512,512, 3))
# flat_shading(img,vertices=None, vcolors=None)
# cv2.imshow("Final", img)
# cv2.waitKey(0)
                
