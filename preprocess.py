import csv
import pandas as pd
import numpy as np
from pprint import pprint


# def

files = list(map(str, range(201901, 201913)))
postfix = '-citibike-tripdata'

total_data = set()
for name in files:
    with open('./data/' + name + postfix + '.csv', 'r') as f:
        print(name)

        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                labels = row
            else:
                data = dict(zip(labels, row))

                # total_data
                start_selected = ['start station id', 'start station name', 'start station latitude', 'start station longitude']
                end_selected = ['end station id', 'end station name', 'end station latitude', 'end station longitude']

                start_data = [data[key] for key in start_selected]
                end_data = [data[key] for key in end_selected]

                total_data.add(tuple(start_data))
                total_data.add(tuple(end_data))

listed_total_data = [list(elem) for elem in total_data]
# pprint(list(listed_total_data))

dataframe = pd.DataFrame(listed_total_data)
dataframe.to_csv('./data/stations.csv', header=['id', 'name', 'latitude', 'longitude'], index=False)
