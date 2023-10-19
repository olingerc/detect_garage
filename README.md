https://www.geeksforgeeks.org/how-to-detect-shapes-in-images-in-python-using-opencv/


apt-get install ffmpeg libsm6 libxext6  -y

pip3 install opencv-python numpy matplotlib


check if opencv as ffmepg support:

python -c "import cv2; print(cv2.getBuildInformation())"

Get image from stream:
ffmpeg -rtsp_transport tcp -y -i rtsp://admin:xxx@192.168.178.90:554/h264Preview_01_main -vframes 1 do.jpg

