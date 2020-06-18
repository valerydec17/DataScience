# Polynomial Regression: Office Prices
# https://www.hackerrank.com/challenges/predicting-office-space-price/problem?h_r=next-challenge&h_v=zen

# Enter your code here. Read input from STDIN. Print output to STDOUT
import sys, re
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression


line0 = input()
nums = [int(s) for s in re.findall(r'\b\d+\b', line0)]
num_of_features = nums[0]
num_of_rows = nums[1]

features = []
price = []
for y in range(0, num_of_features):
    features.append([])

for x in range(0, num_of_rows):
    line = input()
    line_numbers = [float(s) for s in re.findall(r'\b\d+\.\d+\b', line)]
    for y in range(0, num_of_features):
        features[y].append(line_numbers[y])
    price.append(line_numbers[num_of_features])

features = [[features[j][i] for j in range(len(features))] for i in range(len(features[0]))] 
# transposed features

# find polynom 
poly_reg = PolynomialFeatures(degree=3)
pol_reg = LinearRegression()

X_poly = poly_reg.fit_transform(features)
pol_reg.fit(X_poly, price)


line1 = input()
nums = [int(s) for s in re.findall(r'\b\d+\b', line1)]
num_of_rows = nums[0]
features_for_prediction = []
for y in range(0, num_of_features):
    features_for_prediction.append([])
for x in range(0, num_of_rows):
    line = input()
    line_numbers = [float(s) for s in re.findall(r'\b\d+\.\d+\b', line)]
    for y in range(0, num_of_features):
        features_for_prediction[y].append(line_numbers[y])
# transposing features_for_prediction 
features_for_prediction = [[features_for_prediction[j][i] for j in range(len(features_for_prediction))] for i in range(len(features_for_prediction[0]))] 
result = pol_reg.predict(poly_reg.fit_transform(features_for_prediction))
# print(result)
for x in result:
    print(round(x,2))



