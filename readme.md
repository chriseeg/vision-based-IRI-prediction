# Vision-based IRI prediction

This repository contains the code and the datasets used in my master's thesis *_Application of deep Learning Methods for the Analysis of Road Surface Quality_* at Karlsruhe Institute of Technology (Forschungszentrum Informatik).

## Abstract:
Various methods are used in practice to measure the roughness of road surfaces. Advances in the field of deep learning and automatic image processing are creating new opportunities to use data for this purpose. The aim of this study is to investigate whether image data is sufficient to determine the International Roughness Index (IRI), which describes road evenness. Therefore, datasets were generated consisting of camera images of the road surface and IRI values recorded via *lidar*. Using transfer learning, convolutional neural nets were trained to assign the road images to a discrete IRI class.

In the most successful configuration of training parameters the *EfficientNet* model achieved with the available data a Macro F1-score of 55 %. The values of the most frequently occurring class 4 (IRI values between 4 m/km and 6 m/km) were detected with 67 %. However, neither supplementing the data with images from another region nor reducing the training data to one road type led to an improvement of the roughness detection. Thus, the models trained with the available data seem to be specialized for the application of the respective region. From the present investigation it can be concluded that for a more accurate determination of the IRI further surface information is needed, which is not contained in the visual image information.

<img src="Data/01 IRI prediction/02 Karlsruhe/karlsruhe_C/20200624_09-34-48-177_sgm00040.jpg" alt="road image" width="400"/>
