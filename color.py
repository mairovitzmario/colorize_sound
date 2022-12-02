import numpy as np
import cv2 as cv

# (B,G,R)
# B - 0; G - 1; R - 2

HEIGHT, WIDTH = 500, 500
FRAME_RATE = 30
AUX_VIDEO_PATH = 'videos/visualizer.mp4'

def update_color_vector(color_vct, rgb_vals, selected_val, increment = 1):
    rgb_vals = list(rgb_vals)
    for i in range(255):
        rgb_vals[selected_val]+=increment
        color_vct.append(tuple(rgb_vals[:]))
    return color_vct

def generate_img(color):
    img = np.zeros((HEIGHT,WIDTH,3), dtype=np.uint8)
    img[:] = color
    return img

def create_color_vector():

    # B cr; 2,1
    # R dc; 0,-1
    # G cr; 1,1
    # B dc; 2,-1
    # R cr; 0,1
    # G dc; 1,-1

    color_vector = []
    color_vector.append((0,0,255))
    color_vector = update_color_vector(color_vector, color_vector[len(color_vector)-1], 0)
    color_vector = update_color_vector(color_vector, color_vector[len(color_vector)-1], 2, -1)
    color_vector = update_color_vector(color_vector, color_vector[len(color_vector)-1], 1)
    color_vector = update_color_vector(color_vector, color_vector[len(color_vector)-1], 0, -1)
    color_vector = update_color_vector(color_vector, color_vector[len(color_vector)-1], 2)
    #color_vector = update_color_vector(color_vector, color_vector[len(color_vector)-1], 1, -1)
    #color_vector.pop()
    return color_vector

def show_img(color, time_ms):
    img = generate_img(color)
    cv.imshow('image', img)
    cv.waitKey(time_ms)

def create_video(images):
    vid = cv.VideoWriter(AUX_VIDEO_PATH,cv.VideoWriter_fourcc(*'XVID'), FRAME_RATE, (WIDTH,HEIGHT))

    for img in images:
        vid.write(img)
    vid.release()

if __name__ == '__main__':
    color_vector = create_color_vector()

    for x in color_vector:
        print(x)
    print(len(color_vector))

    for color in color_vector:
        img = generate_img(color)
        cv.imshow('image', img)
        cv.waitKey(1)
