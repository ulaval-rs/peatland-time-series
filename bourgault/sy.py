from typing import Union

import numpy as np
import pandas
import pandas as pd


def calculate_sy(
        data: pd.DataFrame,
        gap: int = 5,
        max_hour: int = 5,
        threshold: float = 0.3,
        resample: Union[pandas.DateOffset, pandas.Timedelta, str] = "H") -> pd.DataFrame:
    """ Calculate Sy

    Parameters
    ----------
    data : pandas.Dataframe
        DataFrame of time series with at least the 3 following columns: 'date', 'data_wtd' and 'data_prec'.
        'date' refers to the date of the data acquisition ("YYYY-MM-DD hh:mm:ss", ex. "2011-06-15 15:00:00").
        'data_wtd' refers to the measure TODO.
        'data_prec' refers to the precision of the measure.
    gap : int
        TODO
    max_hour : int
        Maximum hour to consider.
    threshold : float
        Precision threshold.
    resample : str
        Resample rule. See pandas.DataFrame.resample doc for more details.

    Returns
    -------
    pandas.DataFrame
        TODO
    """
    ####### DEFINE_DATA ########
    time = data["date"].astype('datetime64[ns]')
    wtd = data["data_wtd"]
    prec = data["data_prec"]

    ####### TRANSFORM_IN_PANDAS_DATAFRAME #######
    df_wtd = pd.DataFrame(wtd)
    df_wtd.index = time
    df_prec = pd.DataFrame(prec)
    df_prec.index = time

    ####### RESAMPLE DATA #########
    df_wtd = df_wtd.resample(resample).mean()
    df_prec = df_prec.resample(resample).sum()

    ####### FIND PRECIPITATION EVENTS #########
    position60 = np.array(np.where(df_prec.data_prec.values > threshold)).squeeze()
    diff60 = np.diff(position60)
    gap60 = np.array(np.where(diff60 >= gap)).squeeze()
    gap61 = np.insert(gap60, 0, -1)
    gap61 = gap61[:-1]

    ####### ISOLATION_PRECIPITATION_EVENT ######
    list_event = list()
    sommeprec = np.zeros(len(gap61))
    for j in range(0, len(gap61)):
        # j=2
        prec_event = position60[gap61[j] + 1:gap60[j] + 1]
        list_event.append(prec_event)
        sommeprec[j] = df_prec.iloc[prec_event].sum().values

    ####### BEGIN_END_NB_EVENTS #######
    nb_event = len(sommeprec)
    debut = position60[gap61 + 1]
    fin = position60[gap60]
    date_debut = df_prec.iloc[position60[gap61 + 1]].index
    date_fin = df_prec.iloc[position60[gap60]].index

    ######## CREATE_MATRIX_FOR_MIN_MAX_IDENTIFICATION ########
    wtd_list = list()
    idx_max = list()
    idx_min = list()

    for i in range(0, len(debut)):
        wtd_list.append(df_wtd.iloc[debut[i]:fin[i] + max_hour].values.squeeze())
        idx_max.append(df_wtd.iloc[debut[i]:fin[i] + max_hour].idxmax().tolist()[0])
        idx_min.append(df_wtd.iloc[debut[i]:fin[i] + max_hour].idxmin().tolist()[0])

    ######## CALCULATE MIN_MAX_WTD ########
    max_wtd = np.array([i.max() for i in wtd_list])
    min_wtd = np.array([i.min() for i in wtd_list])

    ######## ACCURACY CALCULATION ########
    wtd_list_it_all = []
    for j in [*range(5, 15)]:
        wtd_list_it = list()

        for i in range(0, len(debut)):
            wtd_list_it.append(df_wtd.iloc[debut[i]:fin[i] + j].values.squeeze())

        max_wtd_it = [i.max() for i in wtd_list_it]
        wtd_list_it_all.append(max_wtd_it)

    accuracy_mean = (pd.DataFrame(wtd_list_it_all).diff(axis=0).mean(axis=0)).values
    accuracy_std = (pd.DataFrame(wtd_list_it_all).diff(axis=0).std(axis=0)).values

    ######## SY_CALCULATION_AND_PREC_INTENSITY ########
    #### Module Ajouter pour tenir compte des précipitations rapides ######
    dur = []
    for k in range(0, len(date_debut)):
        if ((date_fin[k] - date_debut[k]).seconds) == 0:
            dur.append(0.5)
        else:
            dur.append((date_fin[k] - date_debut[k]).seconds // 3600)
    #  else:
    #    dur.append(date_fin[i]-date_debut[i]).seconds//3600
    #  print((date_fin[i]-date_debut[i]).seconds)

    duree = np.array(dur)
    intensite = sommeprec / duree
    delta_h = max_wtd - min_wtd
    sy = (sommeprec / delta_h) / 1000
    depth = (max_wtd + min_wtd) / 2

    ######## CREATE SUMMARY TABLE ########
    summary_table = pd.DataFrame({
        "date_debut": date_debut,
        "date_fin": date_fin,
        "sommeprec": sommeprec,
        "max_wtd": max_wtd,
        "min_wtd": min_wtd,
        "duree": dur,
        "intensite": intensite,
        "delta_h": delta_h,
        "depth": depth,
        "sy": sy,
        "idx_max": idx_max,
        "idx_min": idx_min,
        "accuracy_mean": accuracy_mean,
        "accuracy_std": accuracy_std
    })

    return summary_table


# Function to calculate the power-law with constants a and b
def power_law(x, a, b):
    return a * np.power(x, b)
