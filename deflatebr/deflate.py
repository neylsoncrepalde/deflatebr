import requests
import json
import pandas as pd
import numpy as np
from io import StringIO
from datetime import date
from deflatebr.utils import clean_real_date, round_date_to_month

def deflate(nominal_values, nominal_dates, real_date, index='ipca'):
    """
    deflatebr uses data from the Brazilian Institute for Applied Economic 
    Research's API (IPEADATA) to adjust nominal Brazilian Reais for inflation.

    Parameters
    ----------
    nominal_values : [int, float, np.array or pd.Series]
        An array containing nominal Brazilian Reais to deflate.
    nominal_dates : [str, date or list]
        A date vector with corresponding nominal dates (i.e., when nominal values were measured).
        Values are set to the previous month, following the
        standard methodology used by the Brazilian Central Bank
        https://www3.bcb.gov.br/CALCIDADAO/publico/metodologiaCorrigirIndice.do?method=metodologiaCorrigirIndice
    real_date : str
        A value indicating the reference date to deflate nominal values in the format
        'YYYY-MM' (e.g., '2018-01' for January 2018).
    index : str
        Indicates the price index used to deflate nominal Reais. 
        Valid options are: 'ipca', 'igpm,'igpdi', 'ipc', and 'inpc'.

    
    """
    # Prepare inputs
    nominal_values = np.array(nominal_values)
    real_date = clean_real_date(real_date)

    # If it is just one value, turn into a list
    if isinstance(nominal_dates, str):
        nominal_dates = [pd.to_datetime(nominal_dates)]
    elif isinstance(nominal_dates, date):
        nominal_dates = [nominal_dates]

    if len(nominal_dates) > 1:
        nominal_dates = pd.to_datetime(nominal_dates)
    
    # Round dates to first of each month
    nominal_dates = [round_date_to_month(dt) for dt in nominal_dates]    

    # Request to IPEA API
    if index == 'ipca':
        q = "http://ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='PRECOS12_IPCA12')"
    elif index == 'igpm':
        q = "http://ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='IGP12_IGPM12')"
    elif index == 'igpdi':
        q = "http://ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='IGP12_IGPDI12')"
    elif index == 'ipc':
        q = "http://ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='IGP12_IPC12')"
    elif index == 'inpc':
        q = "http://ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='PRECOS12_INPC12')"

    res = requests.get(q)
    indice = pd.DataFrame.from_dict(json.load(StringIO(res.text))['value'])
    indice['VALDATA'] = pd.to_datetime(indice['VALDATA'], utc=True).dt.date.astype(str)
        
    # Calculate changes in prices
    indice['indx'] = indice.VALVALOR[indice.VALDATA == real_date].values / indice.VALVALOR.values
    
    return (indice.loc[indice.VALDATA.isin(nominal_dates),'indx'] * nominal_values).values