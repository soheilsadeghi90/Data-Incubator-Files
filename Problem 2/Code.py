from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import math

# read raw data
data_1 = pd.read_csv("C:\\Users\\ses516\\Desktop\\Data Incubator\\Problem 2\\MT_cleaned.csv")
data_2 = pd.read_csv("C:\\Users\\ses516\\Desktop\\Data Incubator\\Problem 2\\VT_cleaned.csv")

# find counts of each gender
[ln,temp] = data_1.shape
gender_count = pd.DataFrame({'count': data_1.groupby("driver_gender").size()}).reset_index()

# arrested + out of state or not
arrested = data_1[(data_1['is_arrested']==1)]
[arrested_ln,temp] = arrested.shape
arrested_OS = pd.DataFrame({'count': arrested.groupby("out_of_state").size()}).reset_index()

# speeding
violation_type = pd.DataFrame({'count': data_1.groupby("violation").size()}).reset_index()
violation_speed = pd.DataFrame(violation_type[violation_type['violation'].str.contains('Speeding')]).reset_index()
speed_total = violation_speed['count'].sum()

# DUI in Montana
violation_DUI_mon = pd.DataFrame(violation_type[violation_type['violation'].str.contains('DUI')]).reset_index()
DUI_total_mon = violation_DUI_mon['count'].sum()
R1 = DUI_total_mon/(ln-DUI_total_mon)

# DUI in Vermont
[ln_ver,temp] = data_2.shape
violation_type_vt = pd.DataFrame({'count': data_2.groupby("violation").size()}).reset_index()
violation_DUI_ver = pd.DataFrame(violation_type_vt[violation_type_vt['violation'].str.contains('DUI')]).reset_index()
DUI_total_ver = violation_DUI_ver['count'].sum()
R2 = DUI_total_ver/(ln_ver-DUI_total_ver)

# ratio between DUI rate in Montana vs. Vermont
ratio = R1/R2

# Year vs. model linear regression
data_1["time"] = pd.to_datetime(data_1["stop_date"])
data_1["year"] = data_1["time"].dt.year
data_1_nomissing = data_1[data_1['year'].notnull()]
data_1_nomissing['vehicle_year'] = data_1_nomissing['vehicle_year'].apply(pd.to_numeric, errors='coerce')
reg_data = pd.DataFrame(data_1_nomissing.groupby('year', as_index=False)['vehicle_year'].mean()).reset_index()

import sklearn
from sklearn import linear_model as linmod
lm = linmod.LinearRegression()
x = reg_data.year.values.reshape((8,1))
y = reg_data.vehicle_year.values.reshape((8,1))
result = lm.fit(x,y)

# prediction for 2020
y_2020 = result.predict(2020)

# p_value
temp, p_val = sklearn.feature_selection.f_regression(x, y, center=True)

# two states combined, grouped by hours
bigdata = data_1.append(data_2, ignore_index=True)
bigdata["time"] = pd.to_datetime(bigdata["stop_time"])
bigdata["hr"] = bigdata["time"].dt.hour
hour_size = pd.DataFrame({'count': bigdata.groupby("hr").size()}).reset_index()
diff = hour_size.count.max()-hour_size.count.min()

# county area
data_1['county_id'] = pd.Categorical(data_1['county_name']).codes
lon_std = pd.DataFrame({'std': data_1.groupby("county_id")['lon'].std()}).reset_index()
lat_std = pd.DataFrame({'std': data_1.groupby("county_id")['lat'].std()}).reset_index()
lon_std['Area'] = lon_std['std']*lat_std['std']*math.pi*111*111*np.cos(lat_std['std'])
lon_std['Area'].max()

# chi_cquared test
arrested_mon = pd.DataFrame({'count': data_1.groupby("is_arrested").size()}).reset_index()
arrested_ver = pd.DataFrame({'count': data_2.groupby("is_arrested").size()}).reset_index()

table_df = pd.DataFrame({'montana':[807923,17195], 'vermont':[279954,3331]}, index = ['not_arrested','arrested'])
from scipy.stats import chi2_contingency
chi2, p, dof, expected = chi2_contingency(table_df, correction=False)




