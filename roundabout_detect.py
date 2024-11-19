import cv2
import os
import numpy as np
# Configuration
folder = "roundabout-1"
image_path = f"/home/george/VROOM/frames/{folder}"
images = sorted(os.listdir(image_path))

def arc_detect(frame, step, boom, min_to_boom, boom_to_platue, min_pixels_to_platue, 
               winning_percentage, lower_pixel_limit, upper_pixel_limit, confidence_interval):
    height=frame.shape[0]
    print("the HEIGHT IS",height)
    print("the WIDTH IS",frame.shape[1])    
    width = frame.shape[1]
    points = list()
    pixels = list()

   
    for x in range(0, width, step):  # Scanning column by column
        is_ascending = False
        ascent_y = 0
        ascent_value = 255
        pixels = []

        for y in range(1, height):  # Moving across each column
            # Detect start of an ascent
            if (frame[y][x] - frame[y][x - 1] > min_to_boom and
                frame[y][x] >= boom and
                frame[y - 1][x] <= boom and not is_ascending):
                ascent_y = y - 1
                ascent_value = frame[y - 1][x]
                is_ascending = True

            # Detect end of the ascent and evaluate plateau
            elif (frame[y][x] <= boom or len(pixels) > upper_pixel_limit) and is_ascending:
                if len(pixels) > 0:
                    # Convert pixels to a NumPy array for efficient processing
                    pixels_array = np.array(pixels)
                    
                    # Calculate plateau using confidence interval
                    platue = np.mean(pixels_array)
                    platue_range = ((1 - confidence_interval) * platue, (1 + confidence_interval) * platue)
                    counter = np.sum((pixels_array >= platue_range[0]) & (pixels_array <= platue_range[1]))

                    # Calculate pixels to plateau
                    pixels_to_platue = np.sum(pixels_array < platue)

                    # Check conditions for valid arc point
                    if (platue - ascent_value >= boom_to_platue and
                        counter >= len(pixels) * winning_percentage and
                        pixels_to_platue <= min_pixels_to_platue and
                        lower_pixel_limit <= len(pixels) <= upper_pixel_limit):
                        points.append((x, int((y + ascent_y) / 2)))  # Detected point

                is_ascending = False
                ascent_y = 0
                pixels.clear()

            # Continue collecting pixels during ascent
            if is_ascending:
                pixels.append(frame[y][x])

    return points



def process_frames():
    for frame_path in images:
        frame = cv2.imread(os.path.join(image_path, frame_path))
        if frame is None:
            print(f"Failed to load image: {frame_path}")
            continue

        # Preprocess the frame
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gaus_frame = cv2.GaussianBlur(gray_frame, (5, 5), 1)
        canny_frame = cv2.Canny(gaus_frame, 100, 250)
        new_gaus_frame=gaus_frame[100:480, 0:860]
        new_canny_frame=canny_frame[100:480, 0:838]
        new_frame=frame[100:480, 0:838]
        new_gray_frame=gray_frame[100:480, 0:838]
        # Detect arcs
        points = arc_detect(
            new_gaus_frame, step=8, boom=200, min_to_boom=30, boom_to_platue=30,
            min_pixels_to_platue=4, winning_percentage=0.25,
            lower_pixel_limit=4, upper_pixel_limit=300, confidence_interval=0.08
        )
      
        # Draw points on the frame
        for point in points:
            cv2.circle(new_frame, point, 3, (0, 50, 255), -1)  # Green circles for points

        # Print points to console
        print(f"Points detected in {points}")

        # Display the frame
        cv2.imshow('Arc Detection', new_frame)
        
        # Break on 'q' key press
        cv2.waitKey(0)
            
    cv2.destroyAllWindows()




if __name__ == "__main__":
    process_frames()
