# rectified-homographies (Slowglass research)
For auto classifying the quality of photos as good and bad by analyzing the left homographies of photos.

## Current indicator
- goods: [3.75, infty]
- bads: [-infty, 3.4)
- border_goods: [3.5, 3.75)
- border_bads: [3.4, 3.5)
 
## Structure
### complete/
- ml-complete for complete/
- complete-result.txt results saved
- `json/*10075.json`

### incomplete/
- ml-incomplete for incomplete/
    - incomplete-result.txt results saved
    - `json/*18873.json`

## Update log
### 03/03/2019
- Updated scripts for it working with complete/ incomplete/
- Using the following indicators
	- goods: [3.75, infty]
	- bads: [-infty, 3.4)
	- border_goods: [3.5, 3.75)
	- border_bads: [3.4, 3.5) 
- ml-4.py for solely 3.5 and 5
- ml-5 for borders (border_up= 3.75, border_down = 3.4)
    - ml-complete for complete/
        - complete-result.txt results saved
        - `json/*10075.json`
    - ml-incomplete for incomplete/
        - incomplete-result.txt results saved
        - `json/*18873.json`

### 02/20/2019-02/27/2019
- Updated to a new way of getting the effect of projection on the distortion of photos
	- (u,v,w) => z’=ux+vy+w
	- (x’,y’,z’) = () * (x,y,1)
	- (u,v,w)=>(u’,v’,1) => sqrt(u’^2+v’^2)
- Good indicator after test and adjustments: 
	- 5, 3.5
- train/result/ detailed tables
- train/ classified photo for test
- Updated to an Insequence version for classification: 1) rotation 2) projective
	- ml-3.py
	- updated peek.py

### 02/13/2019-02/20/2019
- ML Purpose:
	- Minimize the distortion (consider as bad if distortion too large)
	- Decides Acceptability/ pretty level of images
- histogram and tables show distribution of projective & rotation transform
- 3 steps:
- 1) train 60 data
- 2) an initial indicator decides good/bad
- 3) validate with the other 40
- 4) test with rest images
  - from tomography to theta:http://answers.opencv.org/question/203890/how-to-find-rotation-angle-from-homography-matrix/
- (good course on 3D vision) https://www.coursera.org/lecture/robotics-perception/bundle-adjustment-i-oDj0o 
- Affine:http://mathworld.wolfrm.com/AffineTransformation.html
- Example of getting the homographies
	```
	x = scipy.io.loadmat('rectification_mats.mat')
	# the left and right homography matrices can be accessed by 
	Hl = x['tl']
	Hr = x['tr']
	# Let (u,v,1) be the pixel positions in the original image, new pixel position after the homography is given by (u',v',1) = (u,v,1)*Hl
	```
- ml.py peek.py lookup.py hist.py first version

### 02/06/2019-02/13/2019
- Read resea
rch paper/ wikipedia 
- Computing Rectifying Homographies for Stereo Vision 
- Computer Vision: Algorithms and Applications—Richard Szeliski 
- Homographies
- affine transformation (translation, scale, shear, rotation)
    - 2d - 3x3
    - 3d - 4x4
    - last col 0 0 1
- openCV cvtoarray intensity
- numpy mat
- projection