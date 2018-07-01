from collections import deque
from datetime import datetime, timedelta


class SlidingWindowCounter(object):
    """
    Record events that occurred at a given time, with only timestamp as
    feature. Includes various utility functions to query how many events
    occurred in given time periods.
    """

    def __init__(self, dt_format):
        self.s_deq = deque()
        self.m_deq = deque()
        self.h_deq = deque()

        self.dt_format = dt_format # specify the dt str format we are to expect


    def increment(self, new_ts):
        assert new_ts    # can be expanded to test that ts is in correct format
        new_ts_dt = datetime.strptime(new_ts, self.dt_format)
        self.__update(new_ts)


    def num_last_second(self):
        curr_ts = datetime.utcnow()
        self.__update(curr_ts)
        return len(self.s_deq)


    def num_last_minute(self):
        curr_ts = datetime.utcnow()
        self.__update(curr_ts)
        return len(self.m_deq) + len(self.s_deq)


    def num_last_hour(self):
        curr_ts = datetime.utcnow()
        self.__update(curr_ts)
        return len(self.h_deq) + len(self.m_deq) + len(self.s_deq)


    def __update(self, curr_ts):
        """
        This method maintains the three deques and should be called during
        each update and each query
        """

        assert curr_ts   # can be expanded to test that ts is in correct format

        one_hr = timedelta(seconds=3600)
        one_min = timedelta(seconds=60)
        one_sec = timedelta(seconds=1)

        # copy the deques so we can mutate the original ones
        h_deq_copy = list(self.h_deq)
        m_deq_copy = list(self.m_deq)
        s_deq_copy = list(self.s_deq)

        if self.h_deq:
            for evt in h_deq_copy:
                if curr_ts - evt > one_hr:
                    self.h_deq.popleft()
                else:
                    break

        if self.m_deq:
            for evt in m_deq_copy:
                if curr_ts - evt > one_hr:
                    self.m_deq.popleft()
                elif curr_ts - evt <= one_hr and curr_ts - evt > one_min:
                    self.h_deq.append(self.m_deq.popleft())
                else:
                    break

        if self.s_deq:
            for evt in s_deq_copy:
                if curr_ts - evt > one_hr:
                    self.s_deq.popleft()
                elif curr_ts - evt <= one_hr and curr_ts - evt > one_min:
                    self.h_deq.append(self.s_deq.popleft())
                elif curr_ts - evt <= one_min and curr_ts - evt > one_sec:
                    self.m_deq.append(self.s_deq.popleft())
                else:
                    break
        else:
            self.s_deq.append(curr_ts)



    # The following versions are for testing only

    def increment_test(self, new_ts):
        assert new_ts    # can be expanded to test that ts is in correct format
        self.__update(new_ts)

    def num_last_second_test(self, curr_ts):
        assert curr_ts
        self.__update(curr_ts)
        return len(self.s_deq)


    def num_last_minute_test(self, curr_ts):
        assert curr_ts
        self.__update(curr_ts)
        return len(self.m_deq) + len(self.s_deq)


    def num_last_hour_test(self, curr_ts):
        assert curr_ts
        self.__update(curr_ts)
        return len(self.h_deq) + len(self.m_deq) + len(self.s_deq)
