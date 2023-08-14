import os
import pytz
import time
from ...models import MasterDB, BTCUSDT_PERP
from datetime import datetime
from scipy.stats import linregress
import pandas as pd


FILE_NAME = os.path.basename(__file__).split('.')[0]
DEBUG = False


# , 30*60, 45 *60, 60*60,]
DURATION_LIST = [2*60, 3*60, 4*60, 5*60, 6 *
                 60, 7*60, 8*60, 9*60, 10*60, 15*60, 20*60]


def print_debug(file_name, function_name, status, debug):
    if debug:
        print(file_name + '.' + function_name + '(): ' + status)


def get_dataframe_within_timeframe(t):
    now = int(time.time())
    then = now - t
    queryset = BTCUSDT_PERP.objects.filter(unix__range=(then, now))
    data = list(queryset.values())
    return pd.DataFrame(data)


def getDeltaT():
    print("DELTA-T")
    analysis = MasterDB.objects.filter(
        selectionMenu='analysis',
        analysis='price-derivatives-dynamic',
    ).order_by('-unix')[:1].values()
    analysis = pd.DataFrame(list(analysis))

    return analysis


def get_index_for_duration_list():
    print("ACQUIRING INDEX")
    index = []
    deltaTValue = int(getDeltaT().iloc[0]['deltaT'])
    for idx, duration in enumerate(DURATION_LIST):
        if (duration == deltaTValue):
            if (idx > 0):
                index.append(idx-1)
            index.append(idx)
            if (idx < (len(DURATION_LIST)-1)):
                index.append(idx+1)
    return index


def linear_regression():
    r_value = []
    slope = []
    index = get_index_for_duration_list()
    for idx in index:
        df = get_dataframe_within_timeframe(DURATION_LIST[idx])

        x = df.unix.tolist()
        y = df.price.tolist()

        x = [float(i) for i in x]
        y = [float(i) for i in y]

        # calculate the regression parameters
        temp = linregress(x, y)

        # get the r_value and slope
        r_value.append(temp[2])
        slope.append(temp[0])

    return r_value, slope


def get_best_fit(r_values, slopes):
    # create a list of absolute r_value to compare against
    abs_r_values = [abs(x) for x in r_values]
    # find the maximum absolute r_value
    max_abs_r = max(abs_r_values)
    # find the index of the maximum absolute r_value
    best_fit_idx = abs_r_values.index(max_abs_r)
    # get the best fit r_value and the corresponding slope
    best_r = r_values[best_fit_idx]
    best_slope = slopes[best_fit_idx]
    best_duration = DURATION_LIST[best_fit_idx]
    # return best_r and best_slope
    return best_duration, best_r, best_slope


def updateDatabase():
    FUNCTION_NAME = 'updateDatabase'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    seconds = 30
    ticker = "BTCUSDT"
    #unix, price, volume = get_crypto_data(seconds, ticker)

    df = get_dataframe_within_timeframe(60)

    r_value, slope = linear_regression()
    best_duration, best_r, best_slope = get_best_fit(r_value, slope)

    mdb = MasterDB(

        selectionMenu='analysis',
        analysis='price-derivatives-dynamic',

        unix=datetime.now().timestamp(),
        time=str(datetime.now(pytz.timezone(
            'America/Vancouver'))).split('.')[0],

        price=df['price'][len(df)-1],
        dprice=best_slope,
        deltaT=best_duration,
        rValue=abs(best_r)




        # momentumMean=getMomentumMean(),

    )
    mdb.save()

    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)


def run():
    FUNCTION_NAME = 'run'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    # r_value, slope = linear_regression()

    # best_duration, best_r, best_slope = get_best_fit(r_value, slope)
    try:
        updateDatabase()
    except:
        pass
    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)
