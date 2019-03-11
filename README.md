# rectified-homographies (Slowglass research)
For auto classifying the quality of photos as good and bad by analyzing the left homographies of photos.

## HOW TO RUN
```
# run with the complete/ dir
python3 ml-complete.py

# run with the incomplete/ dir
python3 ml-incomplete.py

# for a plot showing the distribution of data points
python3 scatter.py
```

### sample output
```
../processed_dataset/cmp/complete/ 99%
[Rot+Proj] result goods=[4733, 4771, 4775, 4823, 4839, 4845, 4849, 4851, 4853, 4859, 4865, 4867, 4877, 4879, 4919, 4973, 4987, 4993, 4999, 5003, 5013, 5031, 5033, 5037, 5043, 5047, 5053, 5057, 5059, 5067, 5077, 5097, 5141, 5167, 5169, 5179, 5181, 5197, 5201, 5203, 5211, 5215, 5223, 5229,...]
...
[Rot+Proj] Results:
 result good=5919
 result bad=2207
 result border=1806
 result border_good=1408
 result border_bad=398
goods/all =0.5959524768425292
```

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
### 03/06/2019-03/13/2019
- Finished:
    - Depth Doc
    - Depth examples
        - On Google Drive
    - Classification of ~500 images
        - On grail server
- Meeting on Sat notes:
	Left graph: Color image Right graph: Depth image 3D Reconstruction: left -> right 
	Blue – close White – far 
	Classify photos into 5 categories: 
	- Flip 
	- All-Blue 
	- Bad: Should be on one plane and no sudden color change, but large or sudden depth  change(color change in depth graph) 
	- Sky-but-not-bad 
	- Good 
	    - Light effect – consistent ok 
	    - Window – consistent ok 

### 02/27/2019-03/06/2019
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
- Min max results in table
	- rotation: <5
	- projective: >=3.5

|rotation (100)	|	min 	|	max			|
|:--------------|----------:|--------------:|
|good (73)	   	|	0 (2)	|	5.72 (1)	|
|bad (17)		|	1.18 (2)|	118.73(1)	|
|borderline (10)|	0.13 (1)|	6.3 (1)		|

|projective (100)	|	min 	|	max 	|
|:------------------|----------:|----------:|
|good (73)			|3.32 (1)	|	5.59 (1)|
|bad (17)			|2.74 (1)	|	3.88 (1)|
|borderline (10)	|3.29 (3)	|	4.47 (1)|

- Not effective
	- may depend on rotation or projective 
	- So there may not be overlaps

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