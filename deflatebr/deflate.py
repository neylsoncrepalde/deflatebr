import requests
import json
import pandas as pd
import numpy as np
from io import StringIO
from datetime import date
from .utils import clean_real_date, round_date_to_month

def deflate(nominal_values, nominal_dates, real_date, index='ipca', progress_bar=False, on_jupyter=False):
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
    progress_bar : bool
        True to display a progress bar. False by default.
    on_jupyter : bool
        True to display an HTML progress bar on jupyter notebook or jupyter lab.

    Returns
    -------
    np.ndarray : an array of deflated values.
    
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
    
    # Round dates to first of each month and get one month earlier
    nominal_dates = [round_date_to_month(dt) for dt in nominal_dates]

    # Test index input
    if index not in ['ipca', 'igpm', 'igpdi', 'ipc', 'inpc']:
        raise Exception("index must be one of 'ipca', 'igpm', 'igpdi', 'ipc', 'inpc'")

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
        
    # Calculate changes in values
    real_indx = indice.loc[indice.VALDATA == real_date,'VALVALOR'].values
    df = pd.DataFrame({'nom_values': nominal_values,
                        'VALDATA': nominal_dates})

    df = df.merge(indice[['VALDATA', 'VALVALOR']], how='left', on='VALDATA')

    if progress_bar:
        if on_jupyter:
            from tqdm.notebook import tqdm
            tqdm.pandas()
            df['deflated'] = df[['nom_values', 'VALVALOR']].progress_apply(lambda x: ((real_indx/x[1]) * x[0])[0], axis=1)
        else:
            from tqdm import tqdm
            tqdm.pandas()
            df['deflated'] = df[['nom_values', 'VALVALOR']].progress_apply(lambda x: ((real_indx/x[1]) * x[0])[0], axis=1)
    else:
        df['deflated'] = df[['nom_values', 'VALVALOR']].apply(lambda x: ((real_indx/x[1]) * x[0])[0], axis=1)
    
    return df.deflated.values