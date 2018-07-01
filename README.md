# river_sliding-window-counter

## by Helen Han
## 2018-07-01

### Problem

Implement a sliding window counter that keeps track of events by timestamp. The window may be of variable lengths. Specifically, here we implement three windows of one hour, one minute, and one second.

### Data Structures

+ s_deq is the deque containing event timestamps in the last second, updated each time we increment or query

+ m_deq is the deque containing event timestamps in the last minute, except for the last second, updated each time we increment or query

+ h_deq is the deque containing evnt timestamps in the last hour, except for the last minute, updated each time we increment or query

+ The choice of using deques to hold data is so we have constant time access to the beginning and end to pop and append as our window rolls forward. As a doubly-linked list, a deque takes up more memory, but that additional memory compared to a list should be fairly neglible in practice as long as the deque is not extremely long.

+ The tradeoff of using a deque versus a simple list is that access to the middle of the deque is O(n), compared to O(1) for a list, so we are sacrificing access speed to the specific elements in the middle of the window in preference to knowing how many total events in the window.


### Assumptions
+ If input data is scarce and infrequent, there's no need to maintain the separate data structures described below. It is only necessary to maintain one deque and just update/query this for the appropriate time window. I assume this is not the case as it is a simple solution and less frequently applicable in the real world.

+ Assuming input data is a stream of many events occurring very frequently, we want to manage the inputs as efficiently as possible both in terms of processing and storage. For this reason, we are not maintaining data structures containing repeat elements in case they can get very large (i.e. if events occur on a sub-second level, and say if we want to query one-second window extending to one day, having 86400 data structures containing repeat data can get out of hand.)

+ We are assuming modern computer architecture that can store the timestamps at least once in one data structure. If storage were an issue - say if we are not storing timestamps but large multi-attribute event objects - the problem might be simplified to just update a counter instead of holding the actual events in deques.


### Algorithm Explanation

#### During an update after an event occurred:
+ We insert the current timestamp into the s_deq. We now need to maintain the three deques to be holding correctly the elements in their specified windows.
  + For h_deq, anything at the head should be discarded if it is more than an hour old.
  + For m_deq, for each element at the head:
    + if more than one hour old, discard.
    + if leq one hour old, but more than one minute old, pop out of m_deq and append to end of h_deq.
    + if leq one minute old, keep and end loop.
  + For s_deq, for each element at the head:
    + if more than one hour old, discard.
    + if leq one hour old but more than one minute old, pop out of s_deq and append to end of h_deq.
    + if leq one minute old but more than one second old, pop out of s_deq and append to end of m_deq.
    + if leq one second old, keep and end loop.

#### During a query:
+ Check the current timestamp, and update all three deques similarly as during an event update. Then return the count of events in the deque(s) of interest. Specifically, the count of events in the last hour is the lengths of all three deques summed, the count of events in the last minute is the lengths of m_deq and s_deq summed, and the count of events in the last second is the length of s_deq.

### Extensions and Considerations:
+ If events happen at a very fast rate, and we do not want to waste processing power each time during an update and a query to maintain our rolling windows, AND we are ok with an approximation of the number of events in each window, say, to within the last second, we can pass off the update algorithm that maintains the rolling windows to another process that checks the windows each second, while the live incrementing function only records the events as they come in. In this way, the processing thread can even store the last count of each window as a separate counter so that any queries for number of events in a rolling window can be returned immediately (we can also do this for any other data feature of interest, in case it's not just counting that we're interested in. This can be especially handy for some more intense calculations like variances or matrix operations.)

+ If events are bursty, bandwidth and packet loss considerations might become important. Creative solutions such as FPGA-based packet processing (for when the packets are large but predictable in format, and one needs only some small parts of the packet as key information), reprogramming drivers so that the Linux kernel to pass on packets faster, etc., can be employed depending on the situation.

+ If different rolling windows need to be implemented, the class can be rewritten to take dynamic arguments specifying the size of the windows and how many there are to be. At some point maintaining so many deques will become too much of a hassle, and we can instead maintain counters of the number of events in each window of interest. Doing this at each update may be too much processing, so the approximation method described in the first bullet point of this section can be applied again, so that the counters are maintained separately for approximate accuracy. (For example, if we need to know 1000 rolling windows for each of the past 1000 seconds.)
