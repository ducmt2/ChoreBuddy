Prerequisites:

Below are all packages that will be needed and instructions on how to install on Raspberry Pi.

1a. **Start with this installation**

sudo apt install cmake build-essential pkg-config git

sudo apt install libjpeg-dev libtiff-dev libjasper-dev libpng-dev libwebp-dev libopenexr-dev

sudo apt install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libdc1394-22-dev libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev

sudo apt install libgtk-3-dev libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5

sudo apt install libatlas-base-dev liblapacke-dev gfortran

sudo apt install libhdf5-dev libhdf5-103

sudo apt install python3-dev python3-pip python3-numpy

1b. **Temporarily change the size in swapfile from 2048 to 100**

sudo nano /etc/dphys-swapfile

After the change saved, run:

sudo systemctl restart dphys-swapfile

1c. **Resume installation**

git clone https://github.com/opencv/opencv.git

git clone https://github.com/opencv/opencv_contrib.git

mkdir ~/opencv/build

cd ~/opencv/build

cmake -D CMAKE_BUILD_TYPE=RELEASE \
-D CMAKE_INSTALL_PREFIX=/usr/local \
-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
-D ENABLE_NEON=ON \
-D ENABLE_VFPV3=ON \
-D BUILD_TESTS=OFF \
-D INSTALL_PYTHON_EXAMPLES=OFF \
-D OPENCV_ENABLE_NONFREE=ON \
-D CMAKE_SHARED_LINKER_FLAGS=-latomic \
-D BUILD_EXAMPLES=OFF ..

make -j$(nproc)

sudo make install

sudo ldconfig

1d. **Change the size in swapfile back from 100 to 2048**

sudo nano /etc/dphys-swapfile

After the change saved, run:

sudo systemctl restart dphys-swapfile

2. **Install face recognition packages** (with python3, I used pip3) You can use virtual environment if you want.

pip install face-recognition

pip install imutils

To check if packages were succesfully installed run:

```
python3

import face_recognition

face_recognition.__version__
```


3. **Clone the face_recognition** repository to your Raspberry Pi

4. In the dataset folder, **create a folder** with person's name

5. Open the **headshots_picam.py** and change the name of the folder on line 5 to the one that was just created:

name='Folder_Name'

6. **Run headshots_picam.py** and use spacebar to take pictures of the face. (Make sure that the pictures are not upside down). Take about 10 pictures from different angles. Repeat step 4-6 for each person you want to add to the training model.

7. After cd to the correct folder, **run train_model.py**. This step takes a minute and creates the 'encodings.pickle' file that will serve as the face recognition backbone.

8. Now, **run facial_req.py** with python3. The camera should turn on and recognize your face. 

PS. I had to rotate the camera for my own application, because it was upside down. If your image shows up upside down, you can comment out line 39:

frame=frame.rotate(frame,180)

