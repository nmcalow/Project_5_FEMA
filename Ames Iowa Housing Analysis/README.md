# Project 2: Outline
    The goal of this project is to analyze housing data from Ames, Iowa, create models, and participate in an online Kaggle competition with the models I created. After cleaning and preparing the data to be fed into the model, and using a long loop to find the perfect combination of features, I created a linear model with Ridge regression that could adequately predict future housing data based upon a long list of data points. 
   
# Description of Data
    This data set was truly vast, and after feature creation and dummy variables, each row had 147 columns! I focused in on SalePrice as my predictor target, and these 46 features as my predictor features:
    
    
| Name                 | Description                                           |   |
|----------------------|-------------------------------------------------------|---|
| 3Ssn Porch           | Size of 3 season porch(if any)                        |   |
| Alley_Grvl           | Gravel alley access                                   |   |
| Alley_Pave           | Pavement alley access                                 |   |
| Bsmt Full Bath       | Basement full bathrooms                               |   |
| Bsmt Half Bath       | Basement half bathrooms                               |   |
| Bsmt Qual            | Basement quality 1-5(0 for no basement)               |   |
| BsmtFin SF 2         | Square feet of second finished area in basement       |   |
| Total_Bsmt SF        | Basement total area(finished and unfinished)          |   |
| Bsmt_Total           | All basement qualities multiplied together            |   |
| Exter Qual           | External quality 0-4                                  |   |
| Exter_Overall        | External quality and overall quality interaction      |   |
| Exterior 1st_AsbShng | Asbestos shingles exterior covering                   |   |
| Exterior 1st_BrkFace | Brickface exterior covering                           |   |
| Exterior 1st_CemntBd | Cement board exterior covering                        |   |
| Exterior 1st_MetalSd | Metal siding exterior covering                        |   |
| Foundation_BrkTil    | Brick and tile foundation                             |   |
| Foundation_CBlock    | Cinderblock foundation                                |   |
| Foundation_PConc     | Poured concrete foundation                            |   |
| Foundation_Slab      | Slab foundation                                       |   |
| Functional           | Home functionality rating 0-7                         |   |
| Garage Area          | Total garage area                                     |   |
| Gr Liv Area          | Living area above ground in SF                        |   |
| House Style_2Story   | Two story house                                       |   |
| House Style_SFoyer   | Split foyer house                                     |   |
| House Style_SLvl     | Split level house                                     |   |
| Kitchen Qual         | Kitchen quality 0-4                                   |   |
| Lot Area             | Total area of the property                            |   |
| MS SubClass          | codes for different building class                    |   |
| MS Zoning_I (all)    | Industrial zoning                                     |   |
| MS Zoning_RL         | Residential low density zoning                        |   |
| MS Zoning_RM         | Residential medium density zoning                     |   |
| Mas Vnr Area         | Total area of masonry veneer area                     |   |
| Misc Val             | Total value of extra feature(pool, tennis court, etc) |   |
| Neighborhood_Blmngtn | Bloomington Heights                                   |   |
| Neighborhood_BrDale  | Briardale                                             |   |
| Neighborhood_BrkSide | Brookside                                             |   |
| Neighborhood_Crawfor | Crawford                                              |   |
| Neighborhood_Gilbert | Gilbert                                               |   |
| Neighborhood_NridgHt | Northridge Heights                                    |   |
| Neighborhood_Sawyer  | Sawyer                                                |   |
| Neighborhood_StoneBr | Stone Brook                                           |   |
| Neighborhood_Veenker | Veenker                                               |   |
| Open Porch SF        | Open porch area in SF                                 |   |
| Overall Cond         | Overall condition 1-10                                |   |
| Overall Qual         | Overall quality 1-10                                  |   |
| TotRms_GrLiv         | Total rooms above ground(excluding bathrooms)         |   |
| Total Bsmt SF        | Basement total area(finished and unfinished)          |   |  


# Conclusions

- Just because you can't quite make the logical leaps necessary to select the proper features on your own does not mean you can't find another way to do it, using the power of technology
- Quality and size make the largest difference in housing prices, and which neighborhood the house is in matters as well.