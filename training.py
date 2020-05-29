from keras.layers import Input, Dense, Dropout, concatenate
from keras.models import Model, load_model
from keras.optimizers import Adam
import csv
import numpy as np
from sklearn.model_selection import train_test_split
from random import randint, random
import copy


def read_data(name):
    input_data = []
    label_data = []

    with open('./data/' + name, 'r') as f:
        print(name)

        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                labels = row
            else:
                if 'NULL' in row:
                    pass
                else:
                    # input_data.append(row[:-2] + [row[-2]])
                    input_data.append(row[:-2])
                    label_data.append([row[-1]])

    return input_data, label_data


def to_categorical(L):
    refined = list(set(L))  # remove duplicated data
    encoded = [[0 for _ in range(len(refined))] for _ in range(len(L))]  # init

    for i, l in enumerate(L):
        target = refined.index(l)
        encoded[i][target] = 1

    return encoded


def fit_transform(L, max_val, min_val):
    original = L.reshape(1, -1)[0]
    return (original - min_val) / (max_val - min_val)


def build_model(input_shapes, n_output):
    input_shape_time, input_shape_id = input_shapes

    x1 = Input(shape=input_shape_time)
    h1 = Dense(10, activation='relu', kernel_initializer='he_normal')(x1)
    # h1 = Dropout(0.5)(h1)

    x2 = Input(shape=input_shape_id)
    h2 = Dense(10)(x2)
    # h2 = Dropout(0.5)(h2)

    c = concatenate([h1, h2])
    h = Dense(6, activation='relu', kernel_initializer='he_normal')(c)
    # h = Dropout(0.5)(h)
    y = Dense(n_output, activation='linear', name='y')(h)

    return Model(
        inputs=[x1, x2],
        outputs=y,
        name='model')


if __name__ == "__main__":
    training = False

    """model"""
    input_shape_time = (3, )
    input_shape_id = (1, )
    input_shapes = [input_shape_time, input_shape_id]
    output_shape = 1

    model = build_model(input_shapes, output_shape)
    # model.summary()  # TODO: image
    model.compile(loss='mae', optimizer=Adam(), metrics=['mse', 'acc'])
    print(">>> compiling model complete")

    if training:
        """data"""
        file_names = list(map(str, range(201901, 201913)))
        postfix = '-refined.csv'

        x, y = [], []
        for file_name in file_names:
            _x, _y = read_data(file_name + postfix)
            x += _x
            y += _y

        x = np.array(x).astype('int32')
        y = np.array(y).astype('int32')

        max_val = np.max(x[:, 3])
        min_val = np.min(x[:, 3])
        print('max:', max_val, 'min:', min_val)  # using max and min in inference time

        x_train, x_test, y_train, y_test = train_test_split(
            x,
            y,
            test_size=0.2,
            random_state=950327)

        x_train_months = x_train[:, 0].reshape(-1, 1)
        x_train_weekdays = x_train[:, 1].reshape(-1, 1)
        x_train_hours = x_train[:, 2].reshape(-1, 1)
        # x_train_days = x_train[:, 3].reshape(-1, 1)
        x_train_times = np.concatenate((x_train_months, x_train_weekdays, x_train_hours), axis=-1)
        x_train_ids = fit_transform(x_train[:, 3].reshape(-1, 1), max_val, min_val)

        x_test_months = x_test[:, 0].reshape(-1, 1)
        x_test_weekdays = x_test[:, 1].reshape(-1, 1)
        x_test_hours = x_test[:, 2].reshape(-1, 1)
        # x_test_days = x_test[:, 3].reshape(-1, 1)
        x_test_times = np.concatenate((x_test_months, x_test_weekdays, x_test_hours), axis=-1)
        x_test_ids = fit_transform(x_test[:, 3].reshape(-1, 1), max_val, min_val)
        print(">>> loading data complete")

        """learn"""
        model.fit(
            [x_train_times, x_train_ids],
            y_train,
            epochs=1,
            batch_size=64)
        model.save('citibike_DNN_model.h5')  # save weights
        print(">>> training model complete")

        """"eval."""
        metrics = model.evaluate(
            [x_test_times, x_test_ids],
            y_test)  # loss(mae), mse, acc
        print(">>> evaluating model complete")
        print(metrics)

    else:
        max_val, min_val = 3911, 72  # max: 3911 min: 72

        model = load_model('citibike_DNN_model.h5')
        print(">>> loading model complete")

    """inference"""
    rand_times = np.array([[randint(1, 12), randint(0, 6), randint(0, 23)] for _ in range(10)])
    rand_ids = np.array([[randint(72, 3911)] for _ in range(10)])
    refined_ids = copy.deepcopy(rand_ids)
    refined_ids = fit_transform(refined_ids.reshape(-1, 1), max_val, min_val)

    pred = model.predict([rand_times, refined_ids])  # month, weekday, hour | id

    from pprint import pprint
    pprint(np.around(np.hstack((
        rand_times,
        rand_ids,
        pred))))  # month, weekday, hour, id, pred
