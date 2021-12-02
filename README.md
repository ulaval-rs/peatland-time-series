# Peatland Time Series

This Python library contains functions which make it possible to analyze the water retention in a peatland from time series of precipitation and water table depth.

## Installation
```bash
pip install peatland-time-series
```


## Usage

### Calculating the Specific Yield (Sy)
The `calculate_sy` function allows you to calculate the specific yield (Sy)
from a time series of precipitation and the water table depth.

Lets take the example of a CSV file `./data/time-series.csv`, a time-series of precipitation and water table depth. The table must have at least the columns "date", "data_prec" and "data_wtd". There is an example of CSV file:
```
date,data_prec,data_wtd
2011-06-16 12:00:00,-0.098,0
2011-06-16 13:00:00,-0.103,0
2011-06-16 14:00:00,-0.109,10.3
2011-06-16 15:00:00,-0.089,0
2011-06-16 16:00:00,-0.084,0
```

To calculate the Sy with other pertinents information:
```python
import pandas
from peatland_time_series import calculate_sy

data = pandas.read_csv()

result = calculate_sy()
print(results)
```
Output:
```
,date_beginning,date_ending,precision_sum,max_wtd,min_wtd,durations,intensities,delta_h,depth,sy,idx_max,idx_min,accuracy_mean,accuracy_std
0,2011-06-16 14:00:00,2011-06-16 14:00:00,10.3,-0.084,-0.109,0.5,20.6,0.025,-0.0965,0.412,2011-06-16 16:00:00,2011-06-16 14:00:00,0.0013,0.00332
1,2011-06-16 20:00:00,2011-06-16 21:00:00,3.7,-0.072,-0.1,1.0,3.7,0.028,-0.086,0.132,2011-06-16 23:00:00,2011-06-16 20:00:00,0.0,0.0
2,2011-06-18 04:00:00,2011-06-18 05:00:00,1.2,-0.067,-0.084,1.0,1.2,0.017,-0.076,0.07058823529411763,2011-06-18 04:00:00,2011-06-18 09:00:00,0.0,0.0
```

