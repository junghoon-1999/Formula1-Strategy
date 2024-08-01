import fastf1 as f1
import pandas as pd 

    # Angular information regarding turns 

class data_importer():

    def __init__(self, year, race_no):
        self.Events = f1.get_event_schedule(year)
        self.Events_Race = self.Events[self.Events['Session5'] == 'Race']
        self.Event = self.Events_Race.loc[race_no, :]

    def data_creator(self, turn):

        # Load session object
        session = f1.core.Session(self.Event, session_name = 'Race', f1_api_support = True)
        session.load(laps = True, telemetry = True, weather = True, messages = True)

        total_tele = pd.DataFrame()
        # Load laps and results data
        sesh_l = session.laps
        sesh_r = session.results
        sesh_c = session.get_circuit_info().corners.drop(columns = ['X', 'Y', 'Number', 'Letter'])

        # 0-45: Low
        # 45-90: Med-Low
        # 90-120: Med-High
        # 120-180: High

        sesh_c['Angle'] = turn 
        sesh_c.rename(columns = {'Distance': 'Corner'}, inplace = True)

        # Attain all the drivers from the lap
        drivers = list(sesh_l['Driver'].unique())

        for drv in drivers:
            total_drv = pd.DataFrame()

            # Total number of laps the driver had 
            total_laps = int(sesh_l.pick_driver(drv).LapNumber.iloc[-1])
            
            distance = 0

            for j in range(total_laps):

                temp_tele = sesh_l.pick_driver(drv).iloc[j].get_telemetry().add_distance()
                temp_tele = pd.merge_asof(temp_tele, sesh_c, left_on = 'Distance', right_on = 'Corner', direction = 'nearest')
                temp_tele['Brake'] = temp_tele['Brake'].astype(int)

                # Adding data from session.Laps
                # Laps: which lap the driver is in
                # Compound: Which compound it's in
                # TyreLife: How long the Tyre has been used 
                # TrackStatus: What the track status is 
                temp_tele['Lap'] = j+1
                temp_tele['Compound'] = sesh_l.pick_driver(drv).iloc[j]['Compound']
                temp_tele['TyreLife'] = sesh_l.pick_driver(drv).iloc[j]['TyreLife']
                temp_tele['TrackStatus'] = sesh_l.pick_driver(drv).iloc[j]['TrackStatus']

                # Combining the dataset 
                total_drv = pd.concat([total_drv, temp_tele.reset_index(drop=True)], axis=0)

            # Drop columns we don't need 
            total_drv.drop(columns = ['Time', 'Source', 'DriverAhead', 'DistanceToDriverAhead'], inplace=True)

            # Add a status column for each telemetry input
            outcome = sesh_r[sesh_r['Abbreviation'] == drv]['Status'].values[0]

            if outcome == 'Finished':
                total_drv['Status'] = 'Finished'
            
            elif '+' in outcome:
                total_drv['Status'] = 'Finished'
                total_drv['Status'].iloc[-1] = 'Lapped'
            
            else:
                total_drv['Status'] = 'Finished'
                total_drv['Status'].iloc[-1] = 'DNF'

            for i in total_drv.columns:
                new_col = drv + '_' + i
                total_drv.rename(columns = {i: new_col}, inplace = True)

            # Concatenate all the data from a single race together
            total_tele = pd.concat([total_tele, total_drv.reset_index(drop = True)], axis = 1)

        return total_tele


    def weather_creator(self, total_tele):

        # Load session object
        session = f1.core.Session(self.Event, session_name = 'Race', f1_api_support = True)
        session.load(laps = True, telemetry = True, weather = True, messages = True)

        # Add weatherdata 
        weather_data = session.weather_data
        weather_data['Time'] = pd.to_timedelta(weather_data['Time'])
        weather_data['Rainfall'] = weather_data['Rainfall'].astype(int)

        # Add the weather data df to the total_tele df and drop SessionTime as it is no longer needed
        total_tele = pd.merge_asof(total_tele, weather_data, left_on = 'SessionTime', right_on = 'Time', direction = 'nearest')
        total_tele.drop(columns=['Time'], inplace=True)
        
        return total_tele
    
