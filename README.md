# Formula1-Strategy

This project uses the Transformer model from the paper 'Attention is all you need', to predict the location of all drivers in a race in Formula one. 

It uses data from the FastF1 API to collect telemetry data from a single race and with the transformer model estimate where a driver will be after a certain number of data points. 
Specifically, it collects 6 seconds worth of data to predict where each driver would be in the next 12 seconds. Using the distance information we will predict where the driver will be in terms of distance in the next 12 seconds. The racetrack selected for this project was the 2023 Bahrain Grand Prix.

Data:

The reasons for selecting the 2023 Bahrain Grand Prix are as follows:
1. 2022 was the last major rule change made by the FIA hence any data before 2022 has major car design changes the model cannot capture
2. During 2022 and 2023 the changes made to the vehicles in terms of design, engine and functionality were quite significant and this is shown in the data-analysis file
3. The Bahrain Grand Prix was the first race of the 2023 season, thus making it a relatively fair race for all teams as it was the race with the least amount of changes

The dataset:

Each driver has columns shown below, 

| Feature | Type | Description |
| --- | --- | --- |
| Date | TimeDelta | The timestamp of when the data was collected |
| SessionDate | TimeDelta | The relative timestamp of the session |
| RPM | int | The RPM of the vehicle |
| Speed | int | The speed of the vehicle |
| nGear | int | The gear status of the vehicle |
| Throttle | int | The % of throttle pressure |
| Brake | Bool | The brake status |
| DRS | Bool | The DRS status |
| RelativeDistance | int | Distance driven since first sample |
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

| Feature | Type | Description |
| --- | --- | --- |
| AirTemp | Int | Temperature |
| Humidity | Int | Humidity |
| Pressure | Int | Air pressure|
| RainFall | bool | Show if there is rainfall |
| TrackTemp | Int | Temperature of the track |
| WindDirection | Int | Direction of the wind |
| WindSpeed | Int | Speed of the wind | 

Here the categorical and boolean values will seperately be encoded as Dummy Variables. 
