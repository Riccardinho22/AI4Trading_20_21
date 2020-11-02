import pandas as pd
from datetime import timedelta


def add_readble_time(start_date, df):
    """ change index of dataframe. """
    df = df.copy()
    df.insert(0, "date", [start_date + timedelta(seconds=i) for i in df["time"]])
    return df


def adj_level(series: pd.Series):
    '''Reset the pandas Series with a single index level'''
    series.index = series.index.droplevel()


def create_ohlc_df(df: pd.DataFrame, selected_time: str, price_column: str = 'price',
                   volume_column: str = 'size', column_r=True) -> pd.DataFrame:
    open_price = df[price_column].resample(selected_time).agg({"open": 'first'}).rename('Open')
    adj_level(open_price)
    high_price = df[price_column].resample(selected_time).agg({"high": 'max'}).rename('High')
    adj_level(high_price)
    low_price = df[price_column].resample(selected_time).agg({"low": 'min'}).rename('Low')
    adj_level(low_price)
    close_price = df[price_column].resample(selected_time).agg({"close": 'last'}).rename('Close')
    adj_level(close_price)
    volume = df[volume_column].resample(selected_time).agg({"volume": 'sum'}).rename('Volume')
    adj_level(volume)

    ohlc_df = pd.concat([high_price, low_price, open_price, close_price, volume], axis=1)
    print("CREATE OHLC DATAFRAME FOR %s" % selected_time)
    return ohlc_df


def add_column_r(df: pd.DataFrame, k: int):
    '''Add the column R, the formula is defined in the hmw2 file'''
    df['R'] = 0
    r_column_idx = df.columns.get_loc('R')
    open_column_idx = df.columns.get_loc('Open')
    df.iloc[0:k, r_column_idx] = 0
    for i in range(k, len(df)):
        m_neg = df.iloc[(k - i + 1):(i + 1), open_column_idx].sum() * (1 / k)
        m_pos = df.iloc[i:(i + k), open_column_idx].sum() * (1 / k)
        r_value = 0
        if m_neg != 0:
            r_value = (m_pos - m_neg) / m_neg
        df.iloc[i, r_column_idx] = r_value
    return df
