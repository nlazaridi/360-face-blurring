A repository for 360 Face blurring. Several state of the art face detection models have been tested and SCRFD was selected. The methodologie is for normal video processing, but the results are very good even with the distortion factor.

## SCRFD

Reference: https://arxiv.org/abs/2105.04714 

SCRFD is work from https://github.com/deepinsight/insightface/tree/master/detection/scrfd, providing several state of the art models for a lot of tasks regarding faces in the challenging [Wider Face hard test set](https://paperswithcode.com/sota/face-detection-on-wider-face-hard). Except for the scrfd, the RetinaFace is also theirs.

### Experiments

The default SCRFD was using 640x640 for detection which is quite low. When we change it with (2560, 1280) results improve significantly.
