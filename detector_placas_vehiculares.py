# -*- coding: utf-8 -*-
"""Detector placas vehiculares.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1krgFhcZX6il8hjxFHMAH3ykPjulE61b5

Conectar y utilizar GPU

Se debe tener una carpeta llamada **yolov4** en el Drive, dentro de **yolov4** crear la carpeta **training**

# **1) Montar la carpeta yolov4 (codigo para generar link de navegacion)**
"""

# Commented out IPython magic to ensure Python compatibility.
#mount drive
# %cd ..
from google.colab import drive
drive.mount('/content/gdrive')

# this creates a symbolic link so that now the path /content/gdrive/My\ Drive/ is equal to /mydrive
!ln -s /content/gdrive/My\ Drive/ /mydrive

# list the contents of /mydrive
!ls /mydrive

#Navigate to /mydrive/yolov4
# %cd /mydrive/yolov4

"""# **2) Clonar darknet git repository**"""

!git clone https://github.com/AlexeyAB/darknet

"""# **3) Habilitar OpenCV and GPU**"""

# Commented out IPython magic to ensure Python compatibility.
# change makefile to have GPU and OPENCV enabled
# also set CUDNN, CUDNN_HALF and LIBSO to 1

# %cd darknet/
!sed -i 's/OPENCV=0/OPENCV=1/' Makefile
!sed -i 's/GPU=0/GPU=1/' Makefile
!sed -i 's/CUDNN=0/CUDNN=1/' Makefile
!sed -i 's/CUDNN_HALF=0/CUDNN_HALF=1/' Makefile
!sed -i 's/LIBSO=0/LIBSO=1/' Makefile

"""# **4) Ejecute el comando make para construir darknet**"""

# build darknet 
!make

"""# **5) Copiar archivos de la carpeta yolov4 al directorio Darknet**"""

# Commented out IPython magic to ensure Python compatibility.
# Clean the data and cfg folders first except the labels folder in data which is required

# %cd data/
!find -maxdepth 1 -type f -exec rm -rf {} \;
# %cd ..

# %rm -rf cfg/
# %mkdir cfg

# Unzip the obj.zip dataset and its contents so that they are now in /darknet/data/ folder 

!unzip /mydrive/yolov4/obj.zip -d data/

# Copy the yolov4-custom.cfg file so that it is now in /darknet/cfg/ folder 

!cp /mydrive/yolov4/yolov4-custom.cfg cfg

# verify if your custom file is in cfg folder
!ls cfg/

# Copy the obj.names and obj.data files from your drive so that they are now in /darknet/data/ folder 

!cp /mydrive/yolov4/obj.names data
!cp /mydrive/yolov4/obj.data  data

# verify if the above files are in data folder
!ls data/

# Copy the process.py file to the current darknet directory 

!cp /mydrive/yolov4/process.py .

"""# **6) Ejecutar archivo *process.py* para crear archivos *train,txt* y *test.txt* dentro de la carpeta *data*.**"""

# run process.py ( this creates the train.txt and test.txt files in our darknet/data folder )
!python process.py

# list the contents of data folder to check if the train.txt and test.txt files have been created 
!ls data/

"""# **7) Descargar pesos pre-entrenados de *yolov4*.**"""

# Download the yolov4 pre-trained weights file
!wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.conv.137

"""# **8) Entrenamiento**"""

# train your custom detector! (uncomment %%capture below if you run into memory issues or your Colab is crashing)
# %%capture

!./darknet detector train data/obj.data cfg/yolov4-custom.cfg yolov4.conv.137 -dont_show -map

# This stops 'Run all' at this cell by causing an error
assert False

"""## **Codigo para reiniciar el entrenamiento, en caso el entranamiento no haya terminado y se desconecto :(  el collab**
  ### **Entonces para reinicar correr los pasos 1, 3, 4 y luego el comando siguiente**
"""

#to restart training your custom detector where you left off(using the weights that were saved last)

!./darknet detector train data/obj.data cfg/yolov4-custom.cfg /mydrive/yolov4/training/yolov4-custom_last.weights -dont_show -map

"""## **Hack para evitar ser 'botado' del Collab VM**

Presionar la combinacion (Ctrl + Shift + i) . Luego ir a la consola y pegar las siguientes lineas y Enter.

```
function ClickConnect(){
console.log("Working"); 
document
  .querySelector('#top-toolbar > colab-connect-button')
  .shadowRoot.querySelector('#connect')
  .click() 
}
setInterval(ClickConnect,60000)
```

# **9) Probar el modelo entrenado**
Correr el siguiente codigo para cambiar seccion training del doc *`config`*:
- batch=1
- subdivisions=1
"""

# Commented out IPython magic to ensure Python compatibility.
#set your custom cfg to test mode 
# %cd cfg
!sed -i 's/batch=64/batch=1/' yolov4-custom.cfg
!sed -i 's/subdivisions=16/subdivisions=1/' yolov4-custom.cfg
# %cd ..

"""## **Detector de placas en imagen**
OJO: ejecutar los pasos 1, 3, y 4. Para corroborar que no haya errores correr el codigo anterior y verificar que no salga error. 
La imagen detectada se guarda en la carpeta test (sale error en el comando *`imShow`* por lo que no se puede mostrar)
"""

# run your custom detector with this command (upload an image to your google drive to test, the thresh flag sets the minimum accuracy required for object detection)
#la imagen detectata se guarda en la carpeta test
#from pylab import *
#def imShow(path):
 # import cv2
  #import matplotlib.pyplot as plt
#from google.colab.patches import cv2_imshow
!./darknet detector test data/obj.data cfg/yolov4-custom.cfg /mydrive/yolov4/training/yolov4-custom_best.weights /mydrive/test/image8.jpg -thresh 0.3 
!cp predictions.jpg "/mydrive/test/image8detect.jpg"
#imShow('predictions.jpg')