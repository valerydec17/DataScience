# Temperature Predictions
# https://www.hackerrank.com/challenges/temperature-predictions/problem

## Plan 

# parse data into arrays

# dates convert to numbers

# sort complete data into one array, and the missing data into two other arrays

# build models for tmax and tmin on complete data

# use models to predict missing data

## Realization
import re
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
# parse data
line0 = input()
nums = [int(s) for s in re.findall(r'\b\d+\b', line0)]
num_of_rows = nums[0]
head_of_table = input()

# 3 arrays 
# each for complete data, for tmax missing, for tmin missing correspondingly
data_complete = [[], [], []] # [time, tmax, tmin]
data_tmax_missing = [[], [], []]
data_tmin_missing = [[], [], []]
place_of_missing_value = [] 


convert_month = {
    'January': 0.0,
    'February': 0.0833,
    'March': 0.1666,
    'April': 0.25,
    'May': 0.3333,
    'June': 0.4166,
    'July': 0.5,
    'August': 0.5833,
    'September': 0.6666,
    'October': 0.75,
    'November': 0.8333,
    'December': 0.9166
}
    
for x in range(0, num_of_rows):
    line = input()
    # year = re.findall(r'\b\d{4}\b', line)[0]
    year = [int(s) for s in re.findall(r'\b\d{4}\b', line)][0]
    month = re.findall(r'\b(?:January?|February?|'+
    'March?|April?|May|June?|July?|'+
    'August?|September?|October?|November?|December?)', line)[0] 
    month_numerical = convert_month[month]
    time = year + month_numerical 

    numbers = re.findall(r'\-?\d+\.\d+\s+\-?\d+\.\d+', line)
    missing_tmax = re.findall(r'Missing\w*\s+\-?\d+\.\d+', line)
    missing_tmin = re.findall(r'\-?\d+\.\d+\s+Missing\w*', line)
    if numbers:
        # put numbers to tmin and tmax
        floats = [float(s) for s in re.findall(r'\-?\d+\.\d+', line)]
        tmax = floats[0]
        tmin = floats[1]
        # (time tmax tmin) = data 
        data_complete[0].append(time)
        data_complete[1].append(tmax)
        data_complete[2].append(tmin)
    elif missing_tmax:
        # put numbers to tmin and tmax
        floats = [float(s) for s in re.findall(r'\-?\d+\.\d+', line)]
        tmax = ''
        tmin = floats[0]
        data_tmax_missing[0].append(time)
        data_tmax_missing[1].append(tmax)
        data_tmax_missing[2].append(tmin)
        place_of_missing_value.append("tmax")
    elif missing_tmin:
        # put numbers to tmin and tmax
        tmax = floats[0]
        tmin = ''
        data_tmin_missing[0].append(time)
        data_tmin_missing[1].append(tmax)
        data_tmin_missing[2].append(tmin)
        place_of_missing_value.append("tmin")
    else:
        print(line, "error")

# create 2 models based on complete data
# use calculated coefficients
# to predict 1) missing tmax 2) missing tmin

# model for tmax
# divide to training set
# and testing set to understand what 
# degree of polynom fits the best
validation_indexes_tmax = [8] # generate indexes
y_tmax_for_train = []
y_tmax_for_validation = []
features_tmax_for_train = [[],[]]
features_tmax_for_validation = [[], []]
for i in range(0, len(data_complete[0])):
    if i in validation_indexes_tmax:
        y_tmax_for_validation.append(data_complete[1][i])
        features_tmax_for_validation[0].append(data_complete[0][i])
        features_tmax_for_validation[1].append(data_complete[2][i])
    else: 
        y_tmax_for_train.append(data_complete[1][i]) #tmax
        features_tmax_for_train[0].append(data_complete[0][i])
        features_tmax_for_train[1].append(data_complete[2][i])
        # time tmin

poly = PolynomialFeatures(degree=3)
lin_regressor_tmax = LinearRegression()

# transposing, is needed for PolynomialFeatures input format
features_tmax_for_train = [[features_tmax_for_train[j][i] for j in range(len(features_tmax_for_train))] for i in range(len(features_tmax_for_train[0]))]
features_tmax_for_validation = [[features_tmax_for_validation[j][i] for j in range(len(features_tmax_for_validation))] for i in range(len(features_tmax_for_validation[0]))]
# fitting
X_transform_for_train = poly.fit_transform(features_tmax_for_train)
X_transform_for_validation = poly.fit_transform(features_tmax_for_validation)
lin_regressor_tmax.fit(X_transform_for_train, y_tmax_for_train)
# validating
y_tmax_trained = lin_regressor_tmax.predict(X_transform_for_train)
y_tmax_validated = lin_regressor_tmax.predict(X_transform_for_validation)

# norm for arrays of equal length
# my norm = 2 *|a - b|/ (|a| + |b|)
def norm(array_a, array_b):
    sum = 0
    for x, y in zip(array_a, array_b):
        sum += 2 * abs(x - y) / (abs(x) + abs(y))
    return sum/min(len(array_a), len(array_b))    

# prediction for missing tmax
features_tmax_for_prediction = [[], []]
features_tmax_for_prediction = [data_tmax_missing[0], data_tmax_missing[2]]
# transposing, is needed for PolynomialFeatures input format
features_tmax_for_prediction = [[features_tmax_for_prediction[j][i] for j in range(len(features_tmax_for_prediction))] for i in range(len(features_tmax_for_prediction[0]))]
tmax_predicted = lin_regressor_tmax.predict(poly.fit_transform(features_tmax_for_prediction))

# model for tmin
validation_indexes_tmin = [12] # generate indexes
y_tmin_for_train = []
y_tmin_for_validation = []
features_tmin_for_train = [[],[]]
features_tmin_for_validation = [[], []]
for i in range(0, len(data_complete[0])):
    if i in validation_indexes_tmin:
        y_tmin_for_validation.append(data_complete[2][i])
        features_tmin_for_validation[0].append(data_complete[0][i])
        features_tmin_for_validation[1].append(data_complete[1][i])
    else: 
        y_tmin_for_train.append(data_complete[2][i]) #tmax
        features_tmin_for_train[0].append(data_complete[0][i])
        features_tmin_for_train[1].append(data_complete[1][i])
        # time tmin

poly = PolynomialFeatures(degree=1)
lin_regressor_tmin = LinearRegression()

# transposing, is needed for PolynomialFeatures input format
features_tmin_for_train = [[features_tmin_for_train[j][i] for j in range(len(features_tmin_for_train))] for i in range(len(features_tmin_for_train[0]))]
features_tmin_for_validation = [[features_tmin_for_validation[j][i] for j in range(len(features_tmin_for_validation))] for i in range(len(features_tmin_for_validation[0]))]
# fitting
X_transform_for_train = poly.fit_transform(features_tmin_for_train)
X_transform_for_validation = poly.fit_transform(features_tmin_for_validation)
lin_regressor_tmin.fit(X_transform_for_train, y_tmin_for_train)
# validating
y_tmin_trained = lin_regressor_tmin.predict(X_transform_for_train)
y_tmin_validated = lin_regressor_tmin.predict(X_transform_for_validation)

# prediction for missing tmax
features_tmin_for_prediction = [[], []]
features_tmin_for_prediction = [data_tmin_missing[0], data_tmin_missing[1]]
# transposing, is needed for PolynomialFeatures input format
features_tmin_for_prediction = [[features_tmin_for_prediction[j][i] for j in range(len(features_tmin_for_prediction))] for i in range(len(features_tmin_for_prediction[0]))]
tmin_predicted = lin_regressor_tmin.predict(poly.fit_transform(features_tmin_for_prediction))

# print output as the solution
i = 0
j = 0
for row in place_of_missing_value:
    if row == "tmax":
        print(tmax_predicted[i])
        i += 1
    elif row == "tmin":
        print(tmin_predicted[j])
        j += 1
    else: 
        print("error") 


