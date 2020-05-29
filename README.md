# citibike-DNN
DNN models for citibike prediction

# Implementation

## loss
We use MAE(Mean Absolute Error):
```
loss: 1.9897
```

# Evaluation

```bash
python training.py
```

```
>>> loading model complete
array([[ 1.000e+01,  0.000e+00,  9.000e+00,  2.230e+02,  0.000e+00],
       [ 9.000e+00,  3.000e+00,  0.000e+00,  4.330e+02,  0.000e+00],
       [ 1.000e+01,  6.000e+00,  9.000e+00,  7.400e+01,  0.000e+00],
       [ 4.000e+00,  0.000e+00,  1.000e+01,  2.072e+03,  1.000e+00],
       [ 8.000e+00,  4.000e+00,  1.500e+01,  3.737e+03,  0.000e+00],
       [ 3.000e+00,  0.000e+00,  2.200e+01,  8.060e+02,  2.000e+00],
       [ 1.200e+01,  5.000e+00,  5.000e+00,  3.086e+03, -0.000e+00],
       [ 1.200e+01,  4.000e+00,  6.000e+00,  2.800e+02, -0.000e+00],
       [ 1.100e+01,  0.000e+00,  2.200e+01,  2.955e+03,  0.000e+00],
       [ 6.000e+00,  0.000e+00,  1.300e+01,  2.402e+03,  0.000e+00]])
```
month, weekday, hour, id, and prediction result, respectively.

# References
* https://www.citibikenyc.com/system-data
