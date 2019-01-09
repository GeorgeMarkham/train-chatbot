import pandas as pd 
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pickle
from get_train_fares import get_station_code

class predict_delay:
    def __init__(self, model_file='./model.pkl'):
        self.model = pickle.load(open(model_file, 'rb'))

    def predict(self, arr_diff, day_of_service, date_of_service, month_of_service, year_of_service, time_of_service, from_stn, to_stn, CHM=0, COL=0, DIS=0, HAP=0, IFD=0, INT=0, IPS=0, KEL=0, LST=0, MKT=0, MNG=0, NMT=0, NRW=0, SMK=0, SNF=0, SRA=0, WTM=0):
        if len(from_stn) > 3:
            from_stn = get_station_code(from_stn)

        if len(to_stn) > 3:
            to_stn = get_station_code(to_stn)

        from_stn = from_stn.upper()
        to_stn = to_stn.upper()

        temp_arr = [arr_diff, day_of_service, date_of_service, month_of_service, year_of_service, time_of_service, CHM, COL, DIS, HAP, IFD, INT, IPS, KEL, LST, MKT, MNG, NMT, NRW, SMK, SNF, SRA, WTM]
        temp_arr[self.get_stn_pos(from_stn)] = 1
        temp_arr[self.get_stn_pos(to_stn)] = 1

        trip_info = np.array([temp_arr])
        
        return self.model.predict(trip_info)[0]

    def get_stn_pos(self, stn):
        if stn == "CHM":
            return 6
        elif stn == "COL":
            return 7
        elif stn == "DIS":
            return 8
        elif stn == "HAP":
            return 9
        elif stn == "IFD":
            return 10
        elif stn == "INT":
            return 11
        elif stn == "IPS":
            return 12
        elif stn == "KEL":
            return 13
        elif stn == "LST":
            return 14
        elif stn == "MKT":
            return 15
        elif stn == "MNG":
            return 16
        elif stn == "NMT":
            return 17
        elif stn == "NRW":
            return 18
        elif stn == "SMK":
            return 19
        elif stn == "SNF":
            return 20
        elif stn == "SRA":
            return 21
        elif stn == "WTM":
            return 22



if __name__ == "__main__":
    predictor = predict_delay()
    print(predictor.predict_delay(0, 8, 80119, 1, 19, 1700, "chm", "MNG"))