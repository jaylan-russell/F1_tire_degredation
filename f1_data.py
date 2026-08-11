import fastf1
import matplotlib.pyplot as plt 
import numpy as np 

#creates a cache that is accessed when called 
fastf1.Cache.enable_cache('f1_cache')


#gets session information from Bahrain and loads it 
session = fastf1.get_session(2025, 'Bahrain', 'R')
session.load()

FUEL_CORRECTION = 0.06

# gets the data from all laps of the race 
laps = session.laps

# gets the laps specific from verstappen 
driver_laps = laps[laps['Driver'] == 'HAM'].copy()
PIT_LOSS =22
RACE_LAPS = 57
driver_laps['LapTimeSecond'] = driver_laps['LapTime'].dt.total_seconds()
driver_laps['FuelCorrected'] = driver_laps['LapTimeSecond'] - ((RACE_LAPS - driver_laps['LapNumber']) * FUEL_CORRECTION)

# gets lap data from soft and hard tire laps where the was no pits and laps were clean 
clean_softs = driver_laps[(driver_laps['PitInTime'].isnull()) & (driver_laps['PitOutTime'].isnull()) & (driver_laps['IsAccurate'] == True) & (driver_laps['Compound'] == 'SOFT') &(driver_laps['TrackStatus'] == '1')]
clean_hards = driver_laps[(driver_laps['PitInTime'].isnull()) & (driver_laps['PitOutTime'].isnull()) & (driver_laps['IsAccurate'] == True) & (driver_laps['Compound'] == 'HARD') &(driver_laps['TrackStatus'] == '1')]
print(driver_laps['Compound'].value_counts())


#print(clean_laps[['Driver', 'LapTimeSeconds','AvgPace','NormalizedPace', 'TyreLife']].head(50))
#print(f"len of hard laps {len(clean_laps_hards)}")




#tyre life value for numpy 
tyre_life = clean_softs['TyreLife'].values
tyre_life_hards = clean_hards['TyreLife'].values

#lap time values for numpy consumption
lap_times = clean_softs['FuelCorrected'].values
lap_times_h = clean_hards['FuelCorrected'].values

#fits a line to the numbers in degree one
coeffs = np.polyfit(tyre_life, lap_times, 1)
coeffs_h = np.polyfit(tyre_life_hards, lap_times_h, 1)

tyre_life_range = np.linspace(min(tyre_life), max(tyre_life), 100)
tyre_life_range_h = np.linspace(min(tyre_life_hards), max(tyre_life_hards), 100)

predicted_times = coeffs[0] *tyre_life_range + coeffs[1]
predicted_times_h = coeffs_h[0] *tyre_life_range_h + coeffs_h[1]



print(f"Degradation rate: {coeffs[0]:.4f} seconds per lap")
print(f"Intercept: {coeffs[1]:.4f} seconds")
print(f"Degradation rate: {coeffs_h[0]:.4f} seconds per lap(HARDS)")
print(f"Intercept: {coeffs_h[1]:.4f} seconds(HARDS)")

plt.plot(tyre_life_range, predicted_times, color = 'red')
plt.plot(tyre_life_range_h, predicted_times_h, color = 'blue')

plt.scatter(clean_softs['TyreLife'], clean_softs['FuelCorrected'], color = 'red')
plt.scatter(clean_hards['TyreLife'],clean_hards['FuelCorrected'], color = 'blue' )
plt.xlabel('tyre Life (laps)')
plt.ylabel('Lap Time (seconds)')
plt.title('Verstappen Tyre Degredation - 2023 Bahrain GP')
plt.show()

def simulate_strategy(pit_lap):
    soft_time = 0 
    hard_time = 0 
    #cal soft stint time
    for i in range(1, pit_lap +1):
        soft_time += coeffs[0] * i + coeffs[1] 
        #print(soft_time)
    #adds calculated time to total time 
    total_time = soft_time + PIT_LOSS
    
    remaining_laps = RACE_LAPS - pit_lap
    for i in range(1, remaining_laps +1): 
        hard_time  += coeffs_h[0] * i + coeffs_h[1] 
        #print(hard_time)
    
    total_time += hard_time 
    
    #print( f'total race time:  {total_time:.2f}')
    
    return total_time

def find_min_time(): 
    results = []
    for pit_lap in range(2, 46): 
        total_time = simulate_strategy(pit_lap)
        print(f" pit lap{pit_lap}: {total_time:.2f}")
        results.append((pit_lap, total_time))
        
    min_time = min(results, key=lambda result: result[1])
    
    return min_time

fastest_race_time = find_min_time()

print(f"fastest race time was {fastest_race_time[1]:.2f}  pitting on lap {fastest_race_time[0]} ")
    
     


#print(laps.head(10))
#print(laps[['Driver', 'LapTime','Compound', 'TyreLife' ]].head(20))


