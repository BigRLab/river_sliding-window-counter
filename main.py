import pandas as pd
import numpy as np

from datetime import datetime

from sliding_window_counter import SlidingWindowCounter

DT_FORMAT = "%Y-%m-%d %H:%M:%S:%f"

def run(test_df):
    counter = SlidingWindowCounter(DT_FORMAT)

    # the following are only for printing purposes
    h_counts = []
    m_counts = []
    s_counts = []


    for row in test_df.itertuples():

        ts = row.Index
        counter.increment_test(ts)
        last_h = counter.num_last_hour_test(ts)
        last_m = counter.num_last_minute_test(ts)
        last_s = counter.num_last_second_test(ts)
        h_counts.append(last_h)
        m_counts.append(last_m)
        s_counts.append(last_s)

        assert last_h == row.evt_ct_1h, "did not match"
        assert last_m == row.evt_ct_1m, "did not match"
        assert last_s == row.evt_ct_1s, "did not match"



def generate_test_data(X, n):
    """
    Use pandas to generate n random timestamps in the last X time period, and use the rolling window implementation in pandas to calculate the event counts as if the stream of data were coming in.

    Attributes:
        X: pandas acceptable string identifier for time timedelta
        n: integer specifying test data size
    """

    X_dt = pd.datetime.now()- pd.Timedelta(X)
    ts_by_microsec = pd.date_range(start=X_dt, end=pd.datetime.now(),
        freq='L')

    df = pd.DataFrame({'time': np.random.choice(ts_by_microsec, size = n),
                        'evt': [1] * n})
    df = df.sort_values(by=['time'])
    df = df.set_index('time')

    one_sec_roll = df.rolling('1s').count()['evt']
    one_min_roll = df.rolling('60s').count()['evt']
    one_hr_roll = df.rolling('3600s').count()['evt']
    new_df = pd.concat([df, one_sec_roll, one_min_roll, one_hr_roll], axis=1)
    new_df.columns=['evt', 'evt_ct_1s', 'evt_ct_1m', 'evt_ct_1h']
    print (new_df)

    return new_df



if __name__ == "__main__":
    test_values = generate_test_data('2H', 20)
    run(test_values)

    # test our algo produces same result as pandas rolling window counters
