import csv
import pandas as pd
import numpy as np
from datetime import datetime
import time
from pprint import pprint


def read_data(name):
    stations, starts, ends = [], [], []

    with open('./data/' + name, 'r') as f:
        print(name)

        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                labels = row
            else:
                data = dict(zip(labels, row))

                if data['start station id'] not in stations:
                    stations.append(data['start station id'])
                if data['end station id'] not in stations:
                    stations.append(data['end station id'])
                starts.append({'id': data['start station id'], 'time': data['starttime']})
                ends.append({'id': data['end station id'], 'time': data['stoptime']})

    return stations, starts, ends


def preprocess(ids, starts, ends):
    bikes = dict()
    for i, row_start in enumerate(starts):
        row_end = ends[i]

        # start
        dt = datetime.strptime(row_start['time'], '%Y-%m-%d %H:%M:%S.%f')
        month, day, hour, _, weekday = dt.month, dt.day, dt.hour, dt.minute, dt.weekday()  # JavaScript 0 = Sunday, Python 0 = Monday

        key = (month, weekday, hour, row_start['id'], day)

        if key not in bikes:
            bikes[key] = 0
        bikes[key] -= 1  # out

        # end
        dt = datetime.strptime(row_end['time'], '%Y-%m-%d %H:%M:%S.%f')
        month, day, hour, minute, weekday = dt.month, dt.day, dt.hour, dt.minute, dt.weekday()

        key = (month, weekday, hour, row_end['id'], day)

        if key not in bikes:
            bikes[key] = 0
        bikes[key] += 1  # in

    return bikes


if __name__ == "__main__":
    file_names = list(map(str, range(201901, 201913)))  # TODO: more data
    postfix = '-citibike-tripdata.csv'

    for file_name in file_names:
        ids, starts, ends = read_data(file_name + postfix)

        bikes = preprocess(ids, starts, ends)
        # pprint(bikes)

        refined_data = []
        for item in bikes.items():
            key, value = item

            refined = [elem for elem in key]
            refined.append(value)
            refined_data.append(refined)  # [month, weekday, hour, id, amount]

        dataframe = pd.DataFrame(refined_data)
        dataframe.to_csv('./data/' + file_name + '-refined.csv', header=['month', 'weekday', 'hour', 'id', 'day', 'amount'], index=False)
