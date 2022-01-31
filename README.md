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

To calculate the Sy with other pertinent information:
```python
import pandas
from peatland_time_series import calculate_sy, read_time_series, visualization

time_series = read_time_series('./data/time-series.csv')

result = calculate_sy(time_series)
print(results.head())
```
Output:
```
       date_beginning         date_ending  precision_sum  max_wtd  min_wtd  durations  intensities  delta_h   depth        sy             idx_max             idx_min  accuracy_mean  accuracy_std
0 2011-06-16 14:00:00 2011-06-16 14:00:00           10.3   -0.084   -0.109        0.5         20.6    0.025 -0.0965  0.412000 2011-06-16 16:00:00 2011-06-16 14:00:00       0.001333      0.003317
1 2011-06-16 20:00:00 2011-06-16 21:00:00            3.7   -0.072   -0.100        1.0          3.7    0.028 -0.0860  0.132143 2011-06-16 23:00:00 2011-06-16 20:00:00       0.000000      0.000000
2 2011-06-18 04:00:00 2011-06-18 05:00:00            1.2   -0.067   -0.084        1.0          1.2    0.017 -0.0755  0.070588 2011-06-18 04:00:00 2011-06-18 09:00:00       0.000000      0.000000
3 2011-06-18 12:00:00 2011-06-18 12:00:00            0.4   -0.085   -0.094        0.5          0.8    0.009 -0.0895  0.044444 2011-06-18 12:00:00 2011-06-18 15:00:00       0.001556      0.002603
4 2011-06-18 17:00:00 2011-06-18 17:00:00            1.6   -0.077   -0.087        0.5          3.2    0.010 -0.0820  0.160000 2011-06-18 18:00:00 2011-06-18 17:00:00       0.000667      0.001000
```

### Plotting water level in function of the time
```python
time_series = read_time_series('path/to/time-series.csv')
sy = calculate_sy(time_series)

visualization.show_water_level(
    time_series,
    sy,
    event_index=30,
    time_before=pandas.Timedelta(hours=10),
    time_after=pandas.Timedelta(hours=20)
)
```
Output:
![water_level_by_time](https://github.com/ulaval-rs/peatland-time-series/blob/main/docs/images/water_level_by_time1.png)

For more information, see the `visualization.show_water_level` docstring. 

### Plot depth(Sy) 
It is possible to plot the depth in function of Sy.
Note that the Sy DataFrame can by filtered with the `filter_sy` function.
```python
time_series = read_time_series('path/to/time-series.csv')
sy = calculate_sy(time_series=time_series)
sy = filter_sy(sy, sy_min=0, delta_h_min=.01, precipitation_sum_min=10, precipitation_sum_max=100)

visualization.show_depth(sy, heigh_of_file=-3)
```
Output:
![depth_by_sy](https://github.com/ulaval-rs/peatland-time-series/blob/main/docs/images/depth_by_sy.png)


### Interactively select data points.
The `visualization.show_depth(..., select=True)` function plots an interactive selector of the Depth(Sy)
graph. You can click on the data points you wish to exclude.
A set of indexes of the selected data points is returned.
```python
selected_indexes = show_depth(sy, select=True)

# selected_indexes
{0, 100, 5, 101, 103, 46, 79, 47, 19, 24}
```

## Reference / Citation
We kindly ask users who produce scientific works to cite the following paper when using this library or algorithms :
Quantification of peatland water storage capacity using the water table fluctuation method (https://doi.org/10.1002/hyp.11116)

