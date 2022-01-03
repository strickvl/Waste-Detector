# Waste-Detector
This repository contains a deep learning-based system to detect and classify waste according to which container it should be thrown into. 

There are six garbage bins in Spain:

- Organic: Orange

- Carton and paper: Blue

- Glass: Green

- General waste: Gray

- Plastics: Yellow

- Dangerous waste: Red

  <img src="docs/colores-del-reciclaje.webp" alt="MJU-dataset" style="zoom:10%;" />
  
### Project Demo
There is a demo deployed in [Hugginface spaces](https://huggingface.co/spaces/hlopez/Waste-Detector). It allows a user to upload a custom image or to select an image from a set of example images to test the model. Also, the user can change both the detection threshold and the NMS threshold to optimize the object detection.

<img src="docs/hugginface_example.png" alt="MJU-dataset" style="zoom:50%;" />

### Datasets

- [MJU-Waste dataset](https://github.com/realwecan/mju-waste) [1]. This dataset contains a set of images annotated in PASCAL VOC [2] format. Object instance annotations in COCO [2] format are also available. This dataset contains RGB images and depth image pairs. The bounding boxes are wrong so they have been calculated using the provided masks. Also, the images were manually labeled into the six desired categories.

  

  ![MJU-dataset](docs/MJU-dataset.jpg)

  

- [TACO dataset](http://tacodataset.org/) [4]. This dataset a public benchmark for waste object segmentation. Images are collected from mainly outdoor environments such as woods, roads and beaches. It is also annotated in COCO [2] format.

  ![MJU-dataset](docs/taco-dataset.png)
  
### State
Performing both the box and class prediction at the same time leads to poor results. Therefore, the problem was divided into two scenarios: first, the bounding boxes prediction using a unique waste class, and second, the classification of the waste inside the bounding box as in [5].

**Roadmap:**

- [x] First version using only the TACO dataset
- [x] Fix the MJU bounding boxes annotations and manually label each image
- [x] Add the MJU data to the system
- [x] Deploy on HugginfaceSpaces
- [ ] Decide whether to add images from other datasets or implement data-centric approaches.
- [ ] Set a custom infrastructure
- [ ] Create a CI/CD pipeline
- [ ] Create a Continuous Training pipeline
- [ ] Set up a model monitoring system 

### References

[1] Tao Wang, Yuanzheng Cai, Lingyu Liang, Dongyi Ye. [A Multi-Level Approach to Waste Object Segmentation](https://doi.org/10.3390/s20143816). Sensors 2020, 20(14), 3816.

[2] Everingham, M., Van Gool, L., Williams, C. K., Winn, J., &  Zisserman, A. (2010). The pascal visual object classes (voc) challenge.  International journal of computer vision, 88(2), 303-338.

[3] Lin, T. Y., Maire, M., Belongie, S., Hays, J., Perona, P., Ramanan,  D., ... & Zitnick, C. L. (2014, September). Microsoft coco: Common  objects in context. In European conference on computer vision (pp.  740-755). Springer, Cham.

[4] Proença, P.F.; Simões, P. TACO: Trash Annotations in Context for Litter Detection. arXiv **2020**, arXiv:2003.06975.

[5] S. Majchrowska et al., “Waste detection in Pomerania: non-profit project for detecting waste in environment,” CoRR, vol. abs/2105.06808, 2021.
