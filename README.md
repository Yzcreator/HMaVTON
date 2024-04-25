# Smart Fitting Room: A One-stop Framework for Matching-aware Virtual Try-On
This is the implementation of our paper at ICMR 2024:
> [Smart Fitting Room: A One-stop Framework for Matching-aware Virtual Try-On](https://arxiv.org/abs/2401.16825)
> 
> Mingzhe Yu, Yunshan Ma, Lei Wu*, Kai Cheng, Xue Li, Lei Meng, Tat-Seng Chua

![Model for this project](figures/model.png)

## TODO List
- [x] Environment
- [ ] Datasets
- [ ] Shape Constraint Network
- [ ] Matching Clothes Diffusion Network
- [ ] Try-on Condition Generator
- [ ] Denoising Generator
- [ ] Release checkpoint

## Installation
Clone this repository:
```
git clone https://github.com/Yzcreator/HMaVTON.git
cd ./HMaVTON/
```
Install PyTorch and other dependencies:
```
conda env create -f environment.yaml
conda activate control
```
## Datasets
We employ two datasets, POG and VITON-HD, where POG is used as an external dataset for the task of mix-and-match and VITON-HD is directly used for the evaluation of virtual try-on and the overall framework. 
### POG Dataset
We perform n-core filtering on the POG dataset, where we keep only the fashion items that occur between 5 and 100 times, resulting in 119,978 top-bottom pairs, 14,064 tops, and 8,124 bottoms.



