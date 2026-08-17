
This project is a Python tool that models F1 tyre degredation from real race telemetry data and recommends an optimal on stop pit strategy. 
Using the FastF1 library to pull real session data it fits a polynomial regression model to each tire compound and simulates total race time across every possible pit window. 


F1 race stategy is a crucial part of team decision making in a race. This tool aims to recreate how real telemetry data can be used to predict 
optimal pit windows. The model accurately matched Lewis Hamilton's actual pit lap of 32 at the 2025 Bahrain Grand Prix, validating the approach taken. 

HOW DO I RUN IT? 
1.Install Python
2.Install the required libraries with python -m pip install fastf1
3.Create cache folder
4.configure script to fit paritular need Driver, Race, and compounds 
5.Run with python .\f1_data.py

Limitations
1.Data may be inconsitent if team decided to two or three stop strageies. 
2.The model also may become inconsistent if one compound was used for a very short stint
due to lack of data. 
3. Does not account for safety cars
4. Fuel correction is a constant of 0.06 as an estimate instead of a measured value 
5. Does not account for track position and traffic, clean air degrades tyres differently than dirty air 