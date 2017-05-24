import constants

import pandas as pd
import numpy as np
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


def current_location(df):
    # Find the completed sections
    completed = constants.get_completed(df)

    # Find the last completed row, or if no completed sections use the default values
    if len(completed) > 0:
        completed[constants.DATE_COL] = completed[constants.DATE_COL].dt.strftime('%Y-%m-%d')
        last_completed = completed.iloc[-1]
    else:
        last_completed = df.iloc[0]
        last_completed[constants.DATE_COL] = constants.ESTIMATED_START_DT

    # Concat name and state
    last_completed[constants.NAME_COL] = last_completed[constants.NAME_COL] + ', ' + last_completed[constants.STATE_COL]

    # Calculate mileage
    first_mileage = df[constants.TO_SPRINGER_COL].iloc[0]  # this is a negative value, because of the approach trail
    last_mileage = df[constants.TO_SPRINGER_COL].iloc[-1]
    miles_hiked = last_completed[constants.TO_SPRINGER_COL] - first_mileage
    miles_remaining = last_mileage - first_mileage - miles_hiked
    last_completed['miles_hiked'] = "{:.1f}".format(miles_hiked)
    last_completed['miles_remaining'] = "{:.1f}".format(miles_remaining)

    # Fix rounding issue with lat longs
    last_completed[constants.LAT_COL] = "{:.4f}".format(last_completed[constants.LAT_COL])
    last_completed[constants.LONG_COL] = "{:.4f}".format(last_completed[constants.LONG_COL])

    # Select columns to include in output
    last_completed = last_completed[[constants.NAME_COL, constants.LAT_COL, constants.LONG_COL, constants.DATE_COL,
                                     'miles_hiked', 'miles_remaining']]

    return {'current_location': last_completed.to_dict()}


def miles_hiked_per_day(df):
    completed = constants.get_completed(df)[[constants.DATE_COL, constants.TO_SPRINGER_COL]]
    completed[constants.DATE_COL+"_dt"] = completed[constants.DATE_COL].dt.strftime('%Y-%m-%d')

    # Need to shift the values, since the last checkpoint of each day should be the first checkpoint of the next day
    completed[constants.TO_SPRINGER_COL + '_shifted'] = completed[constants.TO_SPRINGER_COL].shift(1)
    completed[constants.DATE_COL + '_shifted'] = completed[constants.DATE_COL].shift(1)
    completed[constants.DATE_COL + '_dt_shifted'] = completed[constants.DATE_COL + '_dt'].shift(1)

    # Exclude calculating the overnight duration by filtering where the dates are different
    completed = completed[completed[constants.DATE_COL + '_dt'] == completed[constants.DATE_COL + '_dt_shifted']]

    # Group by day
    f = {constants.TO_SPRINGER_COL: 'last', 'to_spgr_shifted': 'first', constants.DATE_COL: 'last', constants.DATE_COL + '_shifted': 'first'}
    miles_per_day = completed.groupby(constants.DATE_COL+'_dt').agg(f)
    miles_per_day['miles'] = miles_per_day[constants.TO_SPRINGER_COL] - miles_per_day[constants.TO_SPRINGER_COL + '_shifted']
    miles_per_day['duration'] = miles_per_day[constants.DATE_COL] - miles_per_day[constants.DATE_COL + '_shifted']

    # Calculate Average Miles per Day (does not include zero days)
    avg_mileage = "0.0"
    if len(completed) > 0:
        avg_mileage = "{:.1f}".format(miles_per_day['miles'].mean())

    # Fill missing dates with zero miles
    miles_per_day.index = pd.DatetimeIndex(miles_per_day.index)
    start = miles_per_day.index[0]
    end = miles_per_day.index[-1]
    idx = pd.date_range(start, end)
    miles_per_day = miles_per_day.reindex(idx, fill_value=None)
    miles_per_day['miles'] = miles_per_day['miles'].fillna(0.0)
    miles_per_day['duration'] = miles_per_day['duration'].fillna(0.0)
    miles_per_day['to_spgr'] = miles_per_day['to_spgr'].fillna(method='ffill')
    
    # Calculate rolling 2 week mean over miles per day
    mean_excluding_zero = lambda x: x[np.nonzero(x)].mean()
    miles_per_day['rolling'] = miles_per_day['miles'].rolling(14, min_periods=1).apply(mean_excluding_zero)
    
    # Calculate how many miles I need to average to finish on time.  This assumes I take a zero every 10 days (* 0.9)
    estimated_finish = datetime.strptime(constants.ESTIMATED_FINISH_DT , '%Y-%m-%d')
    
    miles_per_day['days_to_finish'] = (estimated_finish - miles_per_day.index).total_seconds() * 0.9 / (24 * 60 * 60)
    miles_per_day['miles_remaining'] = df[constants.TO_SPRINGER_COL].iloc[-1] - miles_per_day['to_spgr']
    miles_per_day['need_to_avg'] = miles_per_day['miles_remaining'] / miles_per_day['days_to_finish']
    
    # Fix rounding issue by converting each mileage value into a string
    miles_per_day['date'] = miles_per_day.index
    miles_per_day['date'] = miles_per_day['date'].dt.strftime('%Y-%m-%d')
    miles_per_day['miles'] = miles_per_day['miles'].apply(lambda x: float('{:.1f}'.format(x)))
    miles_per_day['duration'] = miles_per_day['duration'].apply(lambda x: int('{:.0f}'.format(x.total_seconds() / 60)))
    miles_per_day['rolling'] = miles_per_day['rolling'].apply(lambda x: float('{:.1f}'.format(x)))
    miles_per_day['need_to_avg'] = miles_per_day['need_to_avg'].apply(lambda x: float('{:.1f}'.format(x)))

    # Fill in the missing days so we can calculate the number of zero days
    num_zeros = 0
    if len(completed) > 0:
        zeros = miles_per_day.copy()
        idx = pd.date_range(zeros.index.min(), zeros.index.max())
        zeros.index = pd.DatetimeIndex(zeros.index)
        zeros = zeros.reindex(idx, fill_value=0)
        num_zeros = len(zeros[zeros['miles'] == 0])

    return {'mileage': miles_per_day[['date', 'miles', 'duration', 'rolling', 'need_to_avg']].to_dict('records'), 'avg_mileage': avg_mileage, 'num_zeros': num_zeros}


def start_date(df):
    dt = datetime.strptime(constants.ESTIMATED_START_DT, '%Y-%m-%d')

    completed = constants.get_completed(df)

    if len(completed) > 0:
        dt = df.iloc[0][constants.DATE_COL]

    # Output is formatted like "Mar 3, 2017"
    return {'start_date': "{d:%b} {d.day}, {d.year}".format(d=dt)}


def days_on_trail(df):
    days = 0
    zero_days = 0

    completed = constants.get_completed(df)[constants.DATE_COL]

    if len(completed) > 0:
        start = completed.iloc[0].date()
        end = completed.iloc[-1].date()
        days = (end - start).days + 1  # +1 to include the last day too

    return {'days_on_trail': days}


def predict_completion(df):
    df = df[df[constants.TYPE_COL].isin(['FEATURE', 'SHELTER', 'HUT'])]
    df = df[[constants.TO_SPRINGER_COL, constants.ELEV_COL, constants.DATE_COL]]
    df['dt_reached_dt'] = df['dt_reached'].dt.date

    # Make a working copy of the data, and shift the rows so diffs between rows can be computed
    shifted = df.copy()
    shifted['to_spgr_shifted'] = shifted[constants.TO_SPRINGER_COL].shift(1)
    shifted['elev_shifted'] = shifted[constants.ELEV_COL].shift(1)
    shifted['dt_reached_shifted'] = shifted[constants.DATE_COL].shift(1)
    shifted['dt_reached_dt_shifted'] = shifted['dt_reached_dt'].shift(1)

    # Remove the first row, since there is no diff between the first row and before it
    shifted = shifted.ix[1:]

    # Compute the diffs
    shifted['elev_diff'] = shifted[constants.ELEV_COL] - shifted['elev_shifted']
    shifted['mileage'] = shifted[constants.TO_SPRINGER_COL] - shifted['to_spgr_shifted']
    shifted['time_diff'] = shifted[constants.DATE_COL] - shifted['dt_reached_shifted']

    # Use rows that have completed dates to train the model, use the rest for prediction
    # Notice we exclude calculating the overnight duration by filtering out where the dates are different
    training = shifted[shifted['dt_reached_dt'] == shifted['dt_reached_dt_shifted']]
    training = training[['elev_diff', 'mileage', 'time_diff', constants.DATE_COL]]
    predict = shifted[pd.isnull(shifted[constants.DATE_COL])][['elev_diff', 'mileage']]

    # If not enough training data, output the manually estimated finish date
    if len(training) < 6:
        estimated = datetime.strptime(constants.ESTIMATED_FINISH_DT, '%Y-%m-%d')
        formatted_dt = "{d:%b} {d.day}, {d.year}".format(d=estimated)
        return {'estimated_completion': {'date': formatted_dt}}

    # Extract features and labels
    X_train = training[['elev_diff', 'mileage']]
    y_train = training['time_diff'].map(lambda x: x.total_seconds())
    X_predict = predict[['elev_diff', 'mileage']]

    # Generate polynomial features (x1, x2, x1*x2, x1^2, x2^2)
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
            training[name] = estimator.predict(X_train)

        scores = cross_val_score(estimator, X_train, y_train, cv=num_folds, scoring='neg_mean_absolute_error')
        errors[name+"_error"] = "{:.2f} (+/- {:.2f})".format(scores.mean() / 60 / 60, scores.std() / 60 / 60 * 2)

    # Run a simple linear regression using all the 1st-level predictions as meta-features
    stacker = LinearRegression()
    estimator_prediction_cols = [e[0] for e in estimators if e[2]]
    stacker.fit(training[estimator_prediction_cols], y_train)
    predictions = stacker.predict(predict[estimator_prediction_cols])

    # Sum the predictions for all the remaining segments.  notice we add a 15% buffer to the estimate.
    # Also this assumes 7.2 hours of hiking per day
    predicted_time_to_finish_sec = predictions.sum()
    predicted_time_to_finish_days = predicted_time_to_finish_sec * 1.15 / 60 / 60 / 7.2

    # Average the predicted finish and estimated finish.  This ensures the prediction doesn't get too crazy,
    # especially in the first few weeks when there is little training data.
    print(training[constants.DATE_COL].iloc[-1])
    predicted_finish = training[constants.DATE_COL].iloc[-1] + timedelta(days=predicted_time_to_finish_days)
    estimated_finish = datetime.strptime(constants.ESTIMATED_FINISH_DT , '%Y-%m-%d')

    final_estimate = min(estimated_finish, predicted_finish) + abs(estimated_finish - predicted_finish)/2

    # Format the output
    final_formatted_dt = "{d:%b} {d.day}, {d.year}".format(d=final_estimate)
    predicted_formatted_dt = "{d:%b} {d.day}, {d.year}".format(d=predicted_finish)
    ec = { 'estimated_completion': {'date':  final_formatted_dt, 'predicted':  predicted_formatted_dt, **errors}}
    return ec


if __name__ == "__main__":
    checkpoints = constants.read_poi_file()

    cl = current_location(checkpoints)
    mpd = miles_hiked_per_day(checkpoints)
    sd = start_date(checkpoints)
    dat = days_on_trail(checkpoints)
    pc = predict_completion(checkpoints)

    # Write json file
    with open(constants.statsFilePath, 'w') as outfile:
        json.dump({**cl, **mpd, **sd, **dat, **pc}, outfile)
