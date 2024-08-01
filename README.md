# Formula1-Strategy

# Description

This project uses the Transformer model from the paper 'Attention is all you need', to predict the location of all drivers in a race in Formula one. 

# How to Run

First install the libraries



It uses data from the FastF1 API to collect telemetry data from a single race and with the transformer model estimate where a driver will be after a certain number of data points. 
Specifically, it collects 6 seconds worth of data to predict where each driver would be in the next 12 seconds. Using the distance information we will predict where the driver will be in terms of distance in the next 12 seconds. The racetrack selected for this project was the 2023 Bahrain Grand Prix.

Data:

The reasons for selecting the 2023 Bahrain Grand Prix are as follows:
1. 2022 was the last major rule change made by the FIA hence any data before 2022 has major car design changes the model cannot capture
2. During 2022 and 2023 the changes made to the vehicles in terms of design, engine and functionality were quite significant and this is shown in the data-analysis file
3. The Bahrain Grand Prix was the first race of the 2023 season, thus making it a relatively fair race for all teams as it was the race with the least amount of changes

