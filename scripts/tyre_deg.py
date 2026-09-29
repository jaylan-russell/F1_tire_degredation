import fastf1
import matplotlib.pyplot as plt 
import numpy as np 

#creates a cache that is accessed when called 
fastf1.Cache.enable_cache('f1_cache')


#gets session information and loads it 
session = fastf1.get_session(2025, 'Bahrain', 'R')
session.load()
#-------------------------------------------------------
#
# Variable decleration
#
#-------------------------------------------------------
FUEL_CORRECTION = 0.06
PIT_LOSS =22
RACE_LAPS = 57
#set tyre compounds 
tyre_compound_one = "MEDIUM"
tyre_compound_two = "HARD"

laps = session.laps

# Gathers lap data for a certain driver using driver codes 
driver_laps = laps[laps['Driver'] == 'HAM'].copy()

driver_laps['LapTimeSecond'] = driver_laps['LapTime'].dt.total_seconds()
driver_laps['FuelCorrected'] = driver_laps['LapTimeSecond'] - ((RACE_LAPS - driver_laps['LapNumber']) * FUEL_CORRECTION)

# gets lap data from second tyre compound 
first_compound_laps = driver_laps[(driver_laps['PitInTime'].isnull()) & (driver_laps['PitOutTime'].isnull()) & (driver_laps['IsAccurate'] == True) & (driver_laps['Compound'] == tyre_compound_one) &(driver_laps['TrackStatus'] == '1')]
if len(first_compound_laps) == 0: 
    raise ValueError (f"No {tyre_compound_one} Data found for this driver")

# Gets lap data from second tyre compound
second_compound_laps = driver_laps[(driver_laps['PitInTime'].isnull()) & (driver_laps['PitOutTime'].isnull()) & (driver_laps['IsAccurate'] == True) & (driver_laps['Compound'] == tyre_compound_two) &(driver_laps['TrackStatus'] == '1')]
if len(second_compound_laps) == 0: 
    raise ValueError(f"No {tyre_compound_two} Data found for this driver")


#tyre life value for numpy 
tyre_life = first_compound_laps['TyreLife'].values
tyre_life_hards = second_compound_laps['TyreLife'].values

#lap time values for numpy consumption
f_comp_lap_times = first_compound_laps['FuelCorrected'].values
s_comp_lap_times = second_compound_laps['FuelCorrected'].values

#fits a line to the numbers in degree one
f_coeffs = np.polyfit(tyre_life, f_comp_lap_times, 1)
s_coeffs = np.polyfit(tyre_life_hards, s_comp_lap_times, 1)

#creates 100 evenly spaced points using the data gathered from the driver 
tyre_life_range = np.linspace(min(tyre_life), max(tyre_life), 100)
tyre_life_range_h = np.linspace(min(tyre_life_hards), max(tyre_life_hards), 100)

#calculates predictimes using the cretead tyre life array and slop intercept equaton
predicted_times = f_coeffs[0] *tyre_life_range + f_coeffs[1]
predicted_times_h = s_coeffs[0] *tyre_life_range_h + s_coeffs[1]



#---------------------------------------------------------
#
#          Creates A Graph to show relatioin ship
#
#---------------------------------------------------------
#plots a line trend on the graph depicting the effect of tyre life on performance over time 
plt.plot(tyre_life_range, predicted_times, color = 'red')
plt.plot(tyre_life_range_h, predicted_times_h, color = 'blue')
# scatters the filtered data from first and second compounds on to the graph
plt.scatter(first_compound_laps['TyreLife'], first_compound_laps['FuelCorrected'], color = 'red')
plt.scatter(second_compound_laps['TyreLife'],second_compound_laps['FuelCorrected'], color = 'blue')
plt.xlabel(f'Tyre Life (laps),{tyre_compound_one} red, {tyre_compound_two} blue')
plt.ylabel('Lap Times (seconds)')
plt.title('Tyre Degredation - 2025 Bahrain GP')
plt.show()


#-----------------------------------------------------
#
#               Functions
#
#-----------------------------------------------------
#simulates pit stop stratey 
def simulate_strategy(pit_lap):
    fc_time = 0
    sc_time = 0
    #cal first compound stint time
    for i in range(1, pit_lap +1):
       fc_time += f_coeffs[0] * i + f_coeffs[1]

    #adds calculated time to total time
    total_time =fc_time + PIT_LOSS

    remaining_laps = RACE_LAPS - pit_lap
    #cal second compound stint time 
    for i in range(1, remaining_laps +1):
        sc_time  += s_coeffs[0] * i + s_coeffs[1] 


    total_time += sc_time

    return total_time

# finds minume times 
def find_min_time(): 
    results = []
    for pit_lap in range(2, 46): 
        total_time = simulate_strategy(pit_lap)
        results.append((pit_lap, total_time))
        
    min_time = min(results, key=lambda result: result[1])
    
    return min_time

fastest_race_time = find_min_time()

print(f"fastest race time was {fastest_race_time[1]:.2f} seconds pitting on lap {fastest_race_time[0]} ")



