#https://www.digikey.com/en/maker/projects/how-to-perform-object-detection-with-tensorflow-lite-on-raspberry-pi/b929e1519c7c43d5b2c6f89984883588

mkdir tfliteProject
cd tfliteProject
python3 -m pip install virtualenv
python3 -m venv tflite-env
source tflite-env/bin/activate
uname -m
python --version


sudo apt -y install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev
python3 -m pip install opencv-python
python3 -m pip install tflite-runtime # for Raspberry Pi
#python3 -m pip install tensorflow # for other systems
# check https://www.tensorflow.org/lite/guide/build_cmake_pip


mkdir -p object_detection/coco_ssd_mobilenet_v1
cd object_detection
wget https://storage.googleapis.com/download.tensorflow.org/models/tflite/coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip
unzip coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip -d coco_ssd_mobilenet_v1

wget https://raw.githubusercontent.com/porygon-tech/MIX/master/gadgets/object_detection/TFLite_detection_webcam.py
python3 TFLite_detection_webcam.py --modeldir=coco_ssd_mobilenet_v1
deactivate
