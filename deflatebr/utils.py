import pandas as pd
from datetime import datetime

# Function to check real date
def clean_real_date(real_date):
    """
    Clean real_date

    """
    if (len(real_date) != 7) & (real_date[4] != "/"): 
        raise Exception("'real_date' must be a str in the YYYY-MM format.")
    
    return real_date + "-01"

def round_date_to_month(dt:datetime):
    dt = str(dt.replace(day=1).date())
    return dt
