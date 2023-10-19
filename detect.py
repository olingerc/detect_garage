import subprocess
import cv2


with open('CAM_PW', 'r') as f:
    CAM_PW = f.read().strip()


def save_image(path):
    cam_url = "rtsp://admin:{}@192.168.178.90:554/h264Preview_01_main".format(CAM_PW)
    command = """ffmpeg -rtsp_transport tcp -y -i {0} -r 1/1 -vframes 1 {1}""".format(cam_url, path)
    subprocess.call(command, shell=True)

def detect_garage(src):

    # reading image 
    img = cv2.imread(src) 

    
    # Specify area to crop to based on 320 * 640 image and convert to place in image of current size
    h, w, _ = img.shape
    h0 = 360.0 / 170.0
    h1 = 360.0 / 210.0
    w0 = 640.0 / 595.0
    w1 = 640.0 / 640.0
    img = img[int(float(h) / h0):int(float(h) / h1), int(float(w) / w0):int(float(w) / w1)] # rows cols # zoom on area with triangle

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Convert to binary: setting threshold of gray image 20 was a god threshold. Everythiing above 20 will be set to 255
    _, threshold_img = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(threshold_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    i = 0
    count_triangles = 0
    
    # list for storing names of shapes 
    for contour in contours:
    
        # here we are ignoring first counter because  
        # findcontour function detects whole image as shape 
        if i == 0: 
            i = 1
            continue
    
        # look for shapes i am looking for a triangle so make epsilon quite high, otherwise i will begome a polygon or circle
        approx = cv2.approxPolyDP(contour, 0.05 * cv2.arcLength(contour, True), True) 
        
        # using drawContours() function 
        cv2.drawContours(img, [contour], 0, (0, 0, 255), 1) 
    
        # finding center point of shape 
        M = cv2.moments(contour) 
        if M['m00'] != 0.0: 
            x = int(M['m10']/M['m00']) 
            y = int(M['m01']/M['m00']) 
        else:
            continue

        # putting shape name at center of each shape 
        if len(approx) == 3: 
            cv2.putText(img, 'Triangle', (x, y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            count_triangles += 1
    
        elif len(approx) == 4: 
            cv2.putText(img, 'Quadrilateral', (x, y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1) 
    
        elif len(approx) == 5: 
            cv2.putText(img, 'Pentagon', (x, y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1) 
    
        elif len(approx) == 6: 
            cv2.putText(img, 'Hexagon', (x, y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1) 
    
        else: 
            cv2.putText(img, 'circle', (x, y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1) 
    
    if count_triangles == 1:
        return "closed"
    elif count_triangles == 0:
        return "open"
    else:
        return "unk"

# Actual code
path = "img.png"

save_image(path)
state = detect_garage(path)

print(state)
