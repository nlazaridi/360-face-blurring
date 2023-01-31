# 360-face-blurring# MV_FaceBlurring_360

A repository for 360 Face blurring. 

# Folder description

* data: We use the pre-trained models for inference. Therefore we do not use any dataset for training. The data for inference is a combination of several 360 videos provided by Vragment or online. The data are stored in the [Gdrive](https://drive.google.com/drive/folders/1cNpIMtLp9wkfduL0Bnx-9vVJIwjhW6_K)

* src: The final scripts used for face blurring

# Video processing

## MTCNN

Reference: https://arxiv.org/abs/1604.02878 



### installation
* conda create -n face_detection_py3_8 python=3.8

    For Python 3.10 was taking too long because of some dependences

* conda activate face_detection_py3_8

* facenet-pytorch: pip install facenet-pytorch (for mtcnn) 

* conda install -c conda-forge opencv 

* mmcv 1.3.15: pip3 install mmcv (if you have CUDA: conda install -c esri mmcv-full)

After this pipeline there was a mismatch between torch and torchvision (**probably cased by conda install -c seri mmcv-full**), which gave the following error:

`Couldn't load custom C++ ops. This can happen if your PyTorch and torchvision versions are incompatible, or if you had errors while compiling torchvision from source. For further information on the compatible versions, check https://github.com/pytorch/vision#installation for the compatibility matrix. Please check your PyTorch version with torch.__version__ and your torchvision version with torchvision.__version__ and verify if they are compatible, and if not please reinstall torchvision so that it matches your PyTorch install.`

So just upgrade/downgrade torchvision. For example  conda install -c pytorch torchvision==0.9.1

#### or
* Create the environment from the face_blurring_env.yaml file: conda env create -n face_detection_py3_8 --filename face_blurring_env.yaml

* Activate the new environment: conda activate face_detection_py3_8

* Verify that the new environment was installed correctly: conda env list


### Experiments

Script has 2 input arguments:
* file_path: path where the video is stored
* filename: name of the specific video example

python face_detector_MTCNN.py --file_path "/home/nlazaridi/Projects/MediaVerse/360-processing/face_detection/data/VRAG_videos" --filename "Timelapse"  


## SCRFD

Reference: https://arxiv.org/abs/2105.04714 

### installation



* Create a conda environment: conda create -n insightface python=3.8 (Gives error for higher versions)

* pip install -U insightface==0.5 (the latest version)
    I may give error for not founding cython. If it does run:
    *   pip install cython

* To solve ModuleNotFoundError: No module named 'onnxruntime':  pip install onnxruntime-gpu

* For using SCRFD, you need to activate the specific environment: conda activate insightface


* There are other libraries that we need to use such as mmcv
    * pip install mmcv-full
    * DO NOT use: conda install -c esri mmcv-full --> conflicts with numpy

    The following things have been tried, but only installing the package with pip worked:
    *  First mmcv and then insightface) gives error for numpy for some reason 
    *  Different python version --> For higher does not work at all

#### or


You can also use the insightface_env.yaml to directly create the conda environment.

* Create the environment from the insightface_env.yaml file: conda env create -n insightface_env --filename insightface_env.yaml

* Activate the new environment: conda activate insightface_env

* Verify that the new environment was installed correctly: conda env list


### Experiments

For inference, run the script (after activating the conda env):

python face_detector_SCRFD.py --file_path --filename 

There are other parameters that can be change, but they have default values as well (see face_detector_SCRFD.py)

NOTE: for resolution 720p was giving error: "ValueError: operands could not be broadcast together with shapes (1760,) (1840,)"

Check this issue: https://github.com/deepinsight/insightface/issues/1578

Solution: Change the working resolution
