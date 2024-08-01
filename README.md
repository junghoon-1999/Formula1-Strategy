# Formula1-Strategy

# Description

This project uses the Transformer model from the paper 'Attention is all you need', to predict the location of all drivers in a race in Formula one. 


## Model Description

The model we will be using is as shown below. 

![img](Images/model_diagram.png "Logo Title Text 1")

The number of layers and heads were decided with hyperparameter tuning using *Optuna*. Each hidden feedforward network layer and attention layer used GELU as its activation function. 

The objective function was an altered custom MAE function that was needed to correct some of the losses the model was incorrectly classifying. 

The Adam optimizer was used to optimize the parameter space. 

## Data Description 

The data is consisted of 927 columns and around 430000 rows. For each driver we have, 

|  Feature | Type | Description |
| --- | --- | --- |
| Date | TimeDelta | The timestamp of when the data was collected |
| SessionDate | TimeDelta | The relative timestamp of the session |
| RPM | int | The RPM of the vehicle |
| Speed | int | The speed of the vehicle |
| nGear | int | The gear status of the vehicle |
| Throttle | int | The % of throttle pressure |
| Brake | Bool | The brake status |
| DRS | Bool | The DRS status |
| X | int | X position (1/10 m) |
| Y | int | Y position (1/10 m) |
| Z | int | Z position (1/10 m) |
| Status | Cat (str) | Current status of the driver (DNF, Finished etc) |
| TrackStatus | Cat (str) | Flag (Yellow flag, Safety Car, Red Flag, Virtual Safety Car) | 
| Compound | Cat (str)|The Tyre Compound (Soft, Medium, Hard, Intermediate, Wet) |
| PitIn | Bool | Driver pit in status |
| PitOut | Bool | Driver pit out status |
| Distance | int | The total distance driven for the lap |
| Corner | int| The distance to the nearest turn |
| Angle | Cat (str) | The severity of the turn divided into 4 classes (Low (0-45), Med-Low (45-90), Med-High (90-120), High (120-180)) |
| Acc_Distance | int | The accumulated distance driven by the driver for the entire race |

Then we will also add weather related data

| Feature | Type | Description |
| --- | --- | --- |
| AirTemp | Int | Temperature |
| Humidity | Int | Humidity |
| Pressure | Int | Air pressure|
| RainFall | bool | Show if there is rainfall |
| TrackTemp | Int | Temperature of the track |
| WindDirection | Int | Direction of the wind |
| WindSpeed | Int | Speed of the wind | 


We will then group each rows with 50 rows, with one-hot encoding and some feature engineering (50, 927) and use this to predict the next consecutive 100 positions of the drivers (50, 40). The position will be measure using the **Distance** column. 


# Results

## Average loss per driver across different iterations

The performance and loss values of the model were divided into 4 sub groups and were as shown below. 

![img](Images/group_2.png "Logo Title Text 1")

![img](Images/group_3.png "Logo Title Text 1")

![img](Images/group_4.png "Logo Title Text 1")

Most of the error values occurred for the following reasons:

1. The model output had a decreasing trend when drivers were 70-80% completed with the race for some datapoints. This may be due to the fact that sudden changes from the end of the race to the starting point was something the model was not able to fully comprehend and produce

2. The model had trouble fitting drivers at the start of the race for some datapoints. 

3. Team strategic decisions (e.g. switching positions between the first and second driver) was something the model was not able to predict, but this is expected as the data did not hold information regarding this. 

4. When the drivers are near the starting point at the end/beginning of the lap, and the predictions are made on the opposite side, the loss is calculated by subtracting around the race not the distance between. This explains some of the drastic error values ranging from 4000-5000. This was addressed using a Custom MAE that would calculate the short distance, but the threshold was set at 4800 meters, leading to losses having extreme values. 

Overall, the issue seems to be with the way the datapoints were scaled and not on the model itself. Moreover, these problems can be addressed with more data. 

## Average loss per driver at a certain iteration

Some iterations exhibited a good fit for the model as shown below where the loss values are contained within 100 meters

![img](Images/good_exm.png "Logo Title Text 1")

While some iterations exhibited a poor fit as shown below. 

![img](Images/bad_exm.png "Logo Title Text 1")


# How to Run

First install the libraries



It uses data from the FastF1 API to collect telemetry data from a single race and with the transformer model estimate where a driver will be after a certain number of data points. 
Specifically, it collects 6 seconds worth of data to predict where each driver would be in the next 12 seconds. Using the distance information we will predict where the driver will be in terms of distance in the next 12 seconds. The racetrack selected for this project was the 2023 Bahrain Grand Prix.

Data:

The reasons for selecting the 2023 Bahrain Grand Prix are as follows:
1. 2022 was the last major rule change made by the FIA hence any data before 2022 has major car design changes the model cannot capture
2. During 2022 and 2023 the changes made to the vehicles in terms of design, engine and functionality were quite significant and this is shown in the data-analysis file
3. The Bahrain Grand Prix was the first race of the 2023 season, thus making it a relatively fair race for all teams as it was the race with the least amount of changes

