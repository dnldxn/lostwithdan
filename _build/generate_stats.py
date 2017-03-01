import os
import pandas as pd
import json
from datetime import datetime
from datetime import timedelta
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression, LassoCV, RidgeCV, ElasticNetCV
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.model_selection import cross_val_score


# Define input and output file locations
fileInPath = os.path.join(os.path.dirname(__file__), '../_data/atdb.092116023143.ALL.csv')
fileOutPath = os.path.join(os.path.dirname(__file__), '../_data/stats.json')

# Constants
TYPE_COL = 'type'
NAME_COL = 'name'
STATE_COL = 'state'
LAT_COL = 'lat'
LONG_COL = 'lon'
DATE_COL = 'dt_reached'
TO_SPRINGER_COL = 'to_spgr'
ELEV_COL = 'elev'

ESTIMATED_START_DT = '2017-03-13'
ESTIMATED_FINISH_DT = '2017-09-01'


def get_completed(df):
    return df[df[DATE_COL].notnull()]


def current_location(df):
    miles_hiked = 0
    miles_remaining = df["to_spgr"].iloc[-1]

    df = df.copy()  # work on a copy

    # Concat name and state
    df[NAME_COL] = df[NAME_COL] + ', ' + df[STATE_COL]

    # Fix rounding issue with lat longs
    df[LAT_COL] = df[LAT_COL].apply(lambda x: "{:.4f}".format(x))
    df[LONG_COL] = df[LONG_COL].apply(lambda x: "{:.4f}".format(x))

    # Find the completed sections
    completed = get_completed(df)[[NAME_COL, LAT_COL, LONG_COL, TO_SPRINGER_COL, DATE_COL ]]

    if len(completed) > 0:
        completed[DATE_COL] = completed[DATE_COL].dt.strftime('%Y-%m-%d')
        last_completed = completed.iloc[-1]
        miles_hiked = last_completed[TO_SPRINGER_COL]
        miles_remaining = miles_remaining - miles_hiked
    else:
        last_completed = df.iloc[0]
        last_completed.set_value(DATE_COL, ESTIMATED_START_DT)

    last_completed = last_completed[[NAME_COL, LAT_COL, LONG_COL, DATE_COL]]
    last_completed['miles_hiked'] = "{:.1f}".format(miles_hiked)
    last_completed['miles_remaining'] = "{:.1f}".format(miles_remaining)
    return {'current_location': last_completed.to_dict()}


def miles_hiked_per_day(df):
    completed = get_completed(df)[[DATE_COL, TO_SPRINGER_COL]]
    completed[DATE_COL] = completed[DATE_COL].dt.strftime('%Y-%m-%d')

    # Need to shift the values, since the last checkpoint of each day should be the first checkpoint of the next day
    completed['to_spgr_shifted'] = completed[TO_SPRINGER_COL].shift(1)
    completed['dt_reached_shifted'] = completed[DATE_COL].shift(1)

    # Exclude calculating the overnight duration by filtering where the dates are different
    completed = completed[completed['dt_reached'] == completed['dt_reached_shifted']]

    # Group by day
    f = {TO_SPRINGER_COL: 'last', 'to_spgr_shifted': 'first'}
    miles_per_day = completed.groupby(DATE_COL).agg(f)
    miles_per_day['miles'] = miles_per_day.to_spgr - miles_per_day.to_spgr_shifted

    # Fix rounding issue by converting each mileage value into a string
    miles_per_day = miles_per_day['miles'].apply(lambda x: '{:.1f}'.format(x))

    return {'miles_per_day': miles_per_day.to_dict()}


def start_date(df):
    dt = datetime.strptime(ESTIMATED_START_DT, '%Y-%m-%d')

    completed = get_completed(df)

    if len(completed) > 0:
        dt = df.iloc[0][DATE_COL]

    # Output is formatted like "Mar 3, 2017"
    return {'start_date': "{d:%b} {d.day}, {d.year}".format(d=dt)}


def days_on_trail(df):
    days = 0

    completed = get_completed(df)[DATE_COL]

    if len(completed) > 0:
        start = completed.iloc[0].date()
        end = completed.iloc[-1].date()
        days = (end - start).days + 1  # +1 to include the last day too

    return {'days_on_trail': days}


def predict_completion(df):
    df = df[df[TYPE_COL].isin(['FEATURE', 'SHELTER', 'HUT'])]
    df = df[[TO_SPRINGER_COL, ELEV_COL, DATE_COL]]
    df['dt_reached_dt'] = df['dt_reached'].dt.date

    # Make a working copy of the data, and shift the rows so the row diffs can be computed
    shifted = df.copy()
    shifted['to_spgr_shifted'] = df[TO_SPRINGER_COL].shift(1)
    shifted['elev_shifted'] = df[ELEV_COL].shift(1)
    shifted['dt_reached_shifted'] = df[DATE_COL].shift(1)
    shifted['dt_reached_dt_shifted'] = shifted['dt_reached_dt'].shift(1)

    # Remove the first row, since there is no diff between the first row and before it
    shifted = shifted.ix[1:]

    # Compute the diffs
    shifted['elev_diff'] = shifted[ELEV_COL] - shifted['elev_shifted']
    shifted['mileage'] = shifted[TO_SPRINGER_COL] - shifted['to_spgr_shifted']
    shifted['time_diff'] = shifted[DATE_COL] - shifted['dt_reached_shifted']

    # Use rows that have completed dates to do the training, use the rest for prediction
    # Notice we exclude calculating the overnight duration by filtering where the dates are different
    training = shifted[shifted['dt_reached_dt'] == shifted['dt_reached_dt_shifted']]
    training = training[['elev_diff', 'mileage', 'time_diff']]
    predict = shifted[pd.isnull(shifted[DATE_COL])][['elev_diff', 'mileage']]

    # If not enough training data, output the manually estimated finish date
    if len(training) < 6:
        estimated = datetime.strptime(ESTIMATED_FINISH_DT, '%Y-%m-%d')
        formatted_dt = "{d:%b} {d.day}, {d.year}".format(d=estimated)
        return {'estimated_completion': {'date': formatted_dt}}

    # Extract features and labels
    X_train = training.ix[:,0:2]
    y_train = training.ix[:,2].map(lambda x: x.total_seconds())
    X_predict = predict.ix[:, 0:2]

    # Generate polynomial features
    poly = PolynomialFeatures(2)
    X_train = poly.fit_transform(X_train)
    X_predict = poly.fit_transform(X_predict)

    # Create prediction objects
    num_folds = min(round(len(X_train) / 10 + 1), 10)

    regr = LinearRegression()
    lasso = LassoCV(cv=num_folds, alphas=(1.0, 10.0, 20.0, 30.0, 40.0, 50.0), max_iter=10000)
    ridge = RidgeCV(cv=num_folds, alphas=(1.0, 10.0, 20.0, 30.0, 40.0, 50.0))
    elastic = ElasticNetCV(cv=num_folds, l1_ratio=[0.01, 0.05, .1, .3, .5, .7, .9, 1])
    svr = SVR()
    dtr = DecisionTreeRegressor()
    ada_dtr = AdaBoostRegressor(DecisionTreeRegressor(), n_estimators=500)
    knn = KNeighborsRegressor(n_neighbors=round(len(training) / 5 + 1), weights='distance')
    ada_knn = AdaBoostRegressor(KNeighborsRegressor(n_neighbors=round(len(training) / 5 + 1), weights='distance'), n_estimators=500)

    estimators = [
        ('reg', regr, False),
        ('lasso', lasso, True),
        ('ridge', ridge, True),
        ('elastic', elastic, True),
        ('svr', svr, False),
        ('dtr', dtr, False),
        ('ada_dtr', ada_dtr, True),
        ('knn', knn, False),
        ('ada_knn', ada_knn, True)
    ]

    # Calculate error separately for all methods.  The error is expressed in absolute mean hours.
    errors = {}
    for name, estimator, include_in_prediction in estimators:
        estimator.fit(X_train, y_train)
        if include_in_prediction:
            predict[name] = estimator.predict(X_predict)

        scores = cross_val_score(estimator, X_train, y_train, cv=num_folds, scoring='neg_mean_absolute_error')
        errors[name+"_error"] = "{:.2f} (+/- {:.2f})".format(scores.mean() / 60 / 60, scores.std() / 60 / 60 * 2)

    # Run a simple linear regression using all the predictions as meta-features
    stacker = LinearRegression()
    prediction_cols = [e[0] for e in estimators if e[2]]
    stacker.fit(training[prediction_cols], y_train)
    predictions = stacker.predict(predict[prediction_cols])

    # Sum the predictions for all the remaining segments.  notice we add a 10% buffer to the estimate.
    # Also this assumes 8 hours of hiking per day
    predicted_time_to_finish_sec = predictions.sum()
    predicted_time_to_finish_days = predicted_time_to_finish_sec * 1.1 / 60 / 60 / 8

    # Average the predicted finish and estimated finish.  This ensures the prediction doesn't get too crazy,
    # especially in the first few weeks when there is little training data.
    predicted_finish = checkpoints.ix[0, DATE_COL] + timedelta(days=predicted_time_to_finish_days)
    estimated_finish = datetime.strptime(ESTIMATED_FINISH_DT , '%Y-%m-%d')

    final_estimate = min(estimated_finish, predicted_finish) + abs(estimated_finish - predicted_finish)/2

    # Format the output
    final_formatted_dt = "{d:%b} {d.day}, {d.year}".format(d=final_estimate)
    predicted_formatted_dt = "{d:%b} {d.day}, {d.year}".format(d=predicted_finish)
    ec = { 'estimated_completion': {'date':  final_formatted_dt, 'predicted':  predicted_formatted_dt, **errors}}
    return ec


if __name__ == "__main__":
    checkpoints = pd.read_csv(fileInPath, parse_dates=[DATE_COL], infer_datetime_format=True)

    cl = current_location(checkpoints)
    mpd = miles_hiked_per_day(checkpoints)
    sd = start_date(checkpoints)
    dat = days_on_trail(checkpoints)
    pc = predict_completion(checkpoints)

    # Write json file
    with open(fileOutPath, 'w') as outfile:
        json.dump({**cl, **mpd, **sd, **dat, **pc}, outfile)
