# face_detect

#概述
人脸检测采用了三种方法:
* facepp（http://www.faceplusplus.com.cn）
* opencv（http://opencv.org）
* dlib（http://dlib.net/）


运行方式

> python2.6  face_detect.py [facepp|opencv|dlib]



#安装方法

* cmake

```
cd /tmp
wget https://cmake.org/files/v3.4/cmake-3.4.0.tar.gz --no-check-certificate
tar -xvzf cmake-3.4.0.tar.gz
cd cmake-3.4.0
./bootstrap && make && make install
cp  /etc/bashrc  /etc/bashrc.bak
echo "export PATH=$PATH:/usr/local/bin" >>  /etc/bashrc
source /etc/bashrc  
```


 
* boost
```
wget http://sourceforge.net/projects/boost/files/latest/download?source=files
./bootstrap.sh --with-libraries=python
./b2
sudo ./b2 install`
```
 

* numpy
```
http://sourceforge.net/projects/numpy/files/NumPy/1.7.1/numpy-1.7.1.tar.gz/download
python setup.py install
```
</code></pre>
注意：
新版本的numpy需要gcc-4.4以上，所以需要用1.7.1
</code></pre>
 
* dlib
```
python2.6 setup.py install
```
<pre><code>
注意: 如果gcc是4.1.2，那么
vim ./dlib/cmake 
\#add_definitions(-msse4)
注释这一行
</code></pre>

* opencv
```
cd ~/opencv
mkdir build
cd build

cmake -D CMAKE_BUILD_TYPE=RELEASE \
-D CMAKE_INSTALL_PREFIX=/usr/local \
-D INSTALL_C_EXAMPLES=ON \
-D INSTALL_PYTHON_EXAMPLES=ON \
-D WITH_PARALLEL_PF=OFF \
-D BUILD_EXAMPLES=ON \
-D PYTHON_INCLUDE_DIRS=/data1/python2.6/include/python2.6/ \
-D PYTHON2_EXECUTABLE=/data1/python2.6/bin/python2.6 \
-D PYTHON_LIBRARY=/data1/python2.6/lib/libpython2.6.so ..

make -j8

make install
```
<pre><code>
注意：
1）/tmp/opencv-3.0.0/modules/imgproc/src/hough.cpp:1: error: stray ‘\357’ in program
这个文件头多了一个<feff> ，删除即可
2） ../../lib/libopencv_core.so.3.0.0: undefined reference to `parallel_pthreads_set_threads_num(int)' 
这是一个bug，详细见http://code.opencv.org/issues/4386， 需要对照修改需要对照修改源文件https://github.com/Itseez/opencv/pull/4106/files
</code></pre>


#效果和性能
*  facepp

True Positive: 72.83

False Negative: 27.17

True Negative: 98.21

False Positive: 1.79

响应时间1s+

*  opencv
True Positive: 75.0

False Negative: 25.0

True Negative: 82.14

False Positive: 17.86

平均响应时间200ms

*  dlib
True Positive: 85.87

False Negative: 14.13

True Negative: 94.64

False Positive: 5.36

平均响应时间2s+（有点奇怪，在我的mac pro上，平均响应时间只有500ms，在10.13.2.108上居然平均要2s）
 

#参考资料
> http://www.faceplusplus.com.cn/detection_detect/

> http://python.jobbole.com/82546/

> http://dlib.net/face_detector.py.html

> http://abruzzi.iteye.com/blog/463668
