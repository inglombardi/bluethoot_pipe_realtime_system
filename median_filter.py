"""
 =================================================================
 |	Author	of	the	Project	-	Engineer	Nicola	Lombardi	|
 =================================================================
 |	MSc.	in	Telecommunications	and	Internet	of	Things	|
 |	Telecommunications Engineering    	|	SW HW	ENGINEER	|

 |Professional	Profile
 |		it.linkedin.com/in/nicola-lombardi-09046b205


Example to demonstrate: Data Cleaning:
 ======> Remove noise and correct inconsistencies in the data.
          https://www.researchgate.net/publication/382851188_A_whole_method_to_do_Data_Analysis


# Dimostrato che median_filter.py   è un invariante per lunghezza


Input DataFrame:
       timestamp            tag_id  angle  tag_height
0  1733062840000  4baf351178aa9b0e    -30         1.2
1  1733062840100  4baf351178aa9b0e    -28         1.2
2  1733062840200  4baf351178aa9b0e    -39         1.2
3  1733062840300  4baf351178aa9b0e    -27         1.2
4  1733062840400  4baf351178aa9b0e     -4         1.2  Anomalous Sample ... ==> Data Cleaning

				#####################################

					Test	Number	1	Preview
			    #####################################


Filtered DataFrame:
       timestamp            tag_id  angle  tag_height
0  1733062840000  4baf351178aa9b0e  -30.0         1.2
1  1733062840100  4baf351178aa9b0e  -29.0         1.2
2  1733062840200  4baf351178aa9b0e  -30.0         1.2
3  1733062840300  4baf351178aa9b0e  -29.0         1.2
4  1733062840400  4baf351178aa9b0e  -28.0         1.2

"""

import sys
import time
from constant import *
import pandas as pd
import statistics
from collections import defaultdict, deque
import datetime
from useful_subroutines import *




#	========================================================
#	   ------------	DataFrame	test	----------------
#	========================================================

def my_test():
    """
    :documentation:

    My test to completely understand the median_filter logic and the difference in terms of samples
    between input and output


    :block diagram:
                     _____________________________________
    input.csv ----> |   median _ filter . py              | ------> Output.csv
                     _____________________________________


    :return: NONE
    """
    df = pd.read_csv("input.csv", header=None,
                     names=["timestamp", "tag_id", "angle", "tag_height"]) # Features Naming
    print("Input DataFrame:")
    print(df.head(5))
    count = 0
    print(header.format(count + 1))

    # filter call (median_filter.py)
    filtered_df = median_filter_df_version(df)
    print("\nFiltered DataFrame:")
    print(filtered_df.head(5))
    print(f"{sep}\n Check of the Length:\n Input csv DF: {len(df)}\n Output csv DF: {len(filtered_df)}")

    # Save output.csv from DataFrame
    filtered_df.to_csv("output.csv", index=False, header=False)


def median_filter_df_version(df, time_window=1000):
    """

    :param df: dataframe in which apply Data Cleaning phase
    :param time_window: time window size of the tolerance in seconds [s]
    :return: new filtered dataframe with same size in terms of cols and rows

    :DOCUMENTATION: defaultdict

    1. defaultdict – why use it
    The defaultdict is a subclass of dict that allows you to avoid errors when accessing keys that are not yet present. Instead of raising a KeyError, it
    automatically creates a default value. It is especially useful when you need to accumulate values in lists or counts associated with dynamic keys.

    from collections import defaultdict

    d = defaultdict(list)
    d['a'].append(1)
    d['a'].append(2)
    d['b'].append(3)
    print(d)
    # Output: defaultdict(<class 'list'>, {'a': [1, 2], 'b': [3]})

    :DOCUMENTATION: deque

    from collections import defaultdict, deque
    from datetime import datetime, timedelta

    window = timedelta(seconds=60)
    tag_queue = defaultdict(deque)

    for row in dataframe.itertuples():
        tag = row.tag  # ad esempio
        timestamp = row.timestamp

        queue = tag_queue[tag]

        # Elimina tutti i vecchi timestamp fuori dalla finestra
        while queue and (timestamp - queue[0] > window):
            queue.popleft()

        queue.append(timestamp)

        # Ora queue contiene solo i timestamp "validi" entro la finestra per quel tag
        if len(queue) > 1:
            print(f"{len(queue)} eventi recenti per il tag {tag}")


    Median_filter algorithm:

    tag_queue is a dictionary that maps each tag to a deque of timestamps.

    For each row in the DataFrame, you update the queue corresponding to the tag.

    Remove timestamps that are too old (outside the tolerance window).

    After cleanup, you can see how many recent events are still valid for that tag.

    """
    data_store = defaultdict(deque)
    filtered_data = []

    for index, row in df.iterrows():
        timestamp, tag_id, angle, tag_height = row

        # Remove outdated entries
        # Clear all old timestamps out of the window
        tag_queue = data_store[tag_id]
        while tag_queue and tag_queue[0][0] < timestamp - time_window:
            tag_queue.popleft()

        # Add new entry
        tag_queue.append((timestamp, angle))

        # Compute median
        median_angle = statistics.median(pos for _, pos in tag_queue)

        # Store filtered data
        filtered_data.append([timestamp, tag_id, median_angle, tag_height])

    return pd.DataFrame(filtered_data, columns=df.columns)



def median_filter(input_pipe, output_pipe, time_window=1000):
    """
    Original filter using pipe instead of Dataframe
    :param input_pipe: pipe in which there is the flow
    :param output_pipe:  output pipe
    :param time_window: time window size of the tolerance in seconds [s]
    :return: NONE
    """
    data_store = defaultdict(deque)  # Dictionary of deques to store timestamped positions per tag
    
    with open(input_pipe, 'r') as infile, open(output_pipe, 'w') as outfile:
        for line in infile:
            try:
                timestamp, tag_id, position = line.strip().split(',')
                timestamp = int(timestamp)
                position = float(position)
            except ValueError:
                sys.stderr.write(f"Error parsing line: {line}")
                continue
            
            # Remove outdated entries
            tag_queue = data_store[tag_id]
            while tag_queue and tag_queue[0][0] < timestamp - time_window:
                tag_queue.popleft()
            
            # Add new entry
            tag_queue.append((timestamp, position))
            
            # Compute median
            median_position = statistics.median(pos for _, pos in tag_queue)
            
            # Write to output pipe
            outfile.write(f"{timestamp},{tag_id},{median_position:.2f}\n")
            outfile.flush()

if __name__ == "__main__":
    # call the optional test of median_filter.py
    my_test()

    if len(sys.argv) < 3:
        sys.stderr.write("Usage: python median_filter.py <input_pipe> <output_pipe> [time_window_ms]\n")
        sys.exit(1)
    
    input_pipe = sys.argv[1]
    output_pipe = sys.argv[2]
    time_window = int(sys.argv[3]) if len(sys.argv) > 3 else 1000  # Default to 1 second (1000 ms)
    
    median_filter(input_pipe, output_pipe, time_window)


