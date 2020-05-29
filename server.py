from training import build_model, fit_transform

import numpy as np
from keras.optimizers import Adam
from keras.models import load_model
from random import uniform, seed
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/post', methods=['POST'])
def post():
    data = request.get_json()
    print(data)  # dictionary

    N = len(data["ids"])
    # print(N)
    times = np.array([[data["month"], data["weekday"], data["hour"]] for _ in range(N)])
    ids = np.array([[e] for e in data["ids"]])
    refined_ids = fit_transform(ids.reshape(-1, 1), max_val, min_val)
    pred = model.predict([times, refined_ids])  # month, weekday, hour | id
    print(pred)

    pred = pred.tolist()
    res = [e[0] for e in pred]

    if data["adj"] != 0:
        # res = [e - 2 for e in res]  # Adjusting

        loss = 2
        seed(data["month"] * 1000 + data["weekday"] * 100 + data["hour"])
        res = [e + uniform(-loss, loss) for e in res]  # Adjusting loss
    else:
        pass

    res = [round(e) if e > 0 else round(e) - 1 for e in res]  # Adjusting minus values
    print(res)

    return jsonify({"res": res})


if __name__ == '__main__':
    # print("DEV")

    """model"""
    input_shape_time = (3, )
    input_shape_id = (1, )
    input_shapes = [input_shape_time, input_shape_id]
    output_shape = 1
    model = build_model(input_shapes, output_shape)
    model.compile(loss='mae', optimizer=Adam(), metrics=['mse', 'acc'])
    model = load_model('citibike_DNN_model.h5')

    """inference"""
    max_val, min_val = 3911, 72  # max: 3911 min: 72

    app.run(host='0.0.0.0', port=8327)
