#%% Imports
import pandas as pd

#%% Define math for CV calculation
def cv_calc(dataframe,price,timestamps):

    '''Function that calculates the collateral value given prices and timestamps.
    
        Price is a parameter and can be set to eth or usd at runtime.
        
        Output is the input dataframe with the cv value as a new column.'''

    #Copy dataset to a temp dataframe
    df = dataframe.copy()

    #Set time index
    time_index = pd.to_datetime(df[timestamps])
    df.index = time_index
    df.drop(timestamps,axis=1)

    #Remove 0 value transactions to not affect minimum threshold values
    df = df.loc[df['eth_price'] > 0]

    #Calculate the daily minimum threshold for prices
    price_threshold = 0.15*df[price].resample('1D').quantile(0.25)
    price_threshold.name = 'price_threshold'
    
    #Merge the daily thresholds onto the temp dataset
    df = pd.merge(df,price_threshold,'left',left_index=True,right_on=timestamps)
    
    #Filter transactions under the threshold
    filtered = df.loc[df[price] > df['price_threshold']]

    #Calculate the CV value as a 30 day moving average of the daily minimum filtered transaction price.
    #Also shifts the time series 1 day forward to only get past data.
    cv = filtered[price].resample('1D').min().rolling('30D').mean().shift(1,'D')
    cv.name = 'col_value'

    #Merges daily CV values back onto the main dataset for exporting
    out = pd.merge(filtered,cv,'left',left_index=True,right_on=timestamps)
    out.drop('price_threshold',axis=1)
    
    return out

