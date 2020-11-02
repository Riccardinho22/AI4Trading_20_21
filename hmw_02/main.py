from hmw_02.utils import *
import pandas as pd
from datetime import datetime
NUMBER_LEVEL = 10
oderbook_column_list = []
flatten = lambda t: [item for sublist in t for item in sublist]
COLUMNS_NAMES = {
        "orderbook": flatten([["sell_level_" + str(level), "vsell_level_" + str(level), "buy_level_" + str(level), "vbuy_level_" + str(level)] for level
                      in range(1, NUMBER_LEVEL+1)]),
        "message": ["time", "event_type", "order_id", "size", "price", "direction"]}

messages = pd.read_csv("data/AAPL_2012-06-21_34200000_57600000_message_10.csv", names=COLUMNS_NAMES["message"])
orderbook = pd.read_csv("data/AAPL_2012-06-21_34200000_57600000_orderbook_10.csv", names=COLUMNS_NAMES["orderbook"])
all_lob_data = messages.copy()
all_lob_data[COLUMNS_NAMES["orderbook"]] = orderbook



start_date = datetime.strptime("21.06.2012", "%d.%m.%Y")
all_lob_data = add_readble_time(start_date, all_lob_data)
all_lob_data.set_index('date',inplace=True)

ohlc_one_sec = create_ohlc_df(all_lob_data,selected_time="1s")
ohlc_ten_sec = create_ohlc_df(all_lob_data,selected_time="10s")
ohlc_one_min = create_ohlc_df(all_lob_data,selected_time="1m")
ohlc_one_hour = create_ohlc_df(all_lob_data,selected_time="1h")

ohlc_one_sec = add_column_r(ohlc_one_sec,5)
ohlc_ten_sec = add_column_r(ohlc_ten_sec,5)
ohlc_one_min = add_column_r(ohlc_one_min,5)
ohlc_one_hour = add_column_r(ohlc_one_hour,5)

