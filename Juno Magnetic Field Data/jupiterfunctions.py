

'''

jupiterfunctions.py 


Name and Date: 
- Written on 2/7/2018 for CLaSP 405 by Adam Benson. 

Purpose:
- This module contains functions to read in and manipulate Juno Magntometer (FGM) calibrated data from the Juno Jupiter oribtal phases. 
~ 
'''


def readFGM(year, dayOfYear):
    '''
    Function to read in Juno FluxGate Magnetometer (FGM) data. It takes two strings, year and
    day of year, as inputs. The function finds the specified data and returns a pandas
    dataframe with datetime objects as an index. 
    '''

    # localized variable
    import pandas as pd

    # these files have 116 lines of header.
    numLines = 116

    # proper columns for FGM data
    colNames = ['YEAR', 'DOY', 'HOUR', 'MIN', 'SEC', 'MSEC', 'DEC_DAY',
                'B_X', 'B_Y', 'B_Z', 'OUTBOARD_B_J2000',
                'POS_X', 'POS_Y', 'POS_Z']


    #and then parses dates into a new column named datetime
    data = pd.read_csv('./JunoData/fgm_jno_l3_{}{}ss_r1s_v01.sts'
                       .format(year, dayOfYear), header = numLines,
                       index_col = False, names = colNames,
                       parse_dates = {'DATETIME':colNames[0:5]}, 
                       sep = '\s+')


    #Dropping Milliseconds for indexDates
    indexDates = pd.to_datetime(data['DATETIME'],
                infer_datetime_format = False, 
                format = '%Y %j %H %M %S')

    #Reindex
    data.index = indexDates

    #Dropping the DATETIME, because it is now the index,  and the OUTBOARD_B_J2000 columns.
    data = data.drop(['OUTBOARD_B_J2000', 'DEC_DAY'], axis = 1)

    return(data)


def convertJupiterR(columns):
    '''
    Takes in a dataframe subset of coordinates and converts them
    into radii of Jupiter by creating new columns.
    '''

    jupiterRadius = 71492.0 #in kilometers
    #format for division - in case of issue 1.0 forcing
    #a non-int division

    convertedColumns = columns * ((1.0) / (jupiterRadius))

    return(convertedColumns)

def addQuadrature(X, Y, Z):
    '''
    Calculates a quadrature sum of three values. 
    Formula = np.sqrt(x^2 + y^2 + z^2)
    Useful when calculating the  magnitude of X, Y, Z vector components. 
    '''

    import numpy as np

    magnitude = np.sqrt(X**2 + Y**2 + Z**2)

    return(magnitude)


def errorFunction(x):
    import numpy as np
    '''
    Takes in a FGM dataframe eand calculates the error on the magnitude
    for each X,Y, and Z. In this function, I am using the standard deviation
    of each Bx,By, and Bz using the N-1 method. Returns a tupe of errors of (X,Y, Z).
    '''
    errorX = (x['B_X'] / x['B_MAG']) * np.std(x['B_X'], ddof = 1)
    errorY = (x['B_Y'] / x['B_MAG']) * np.std(x['B_Y'], ddof = 1)
    errorZ = (x['B_Z'] / x['B_MAG']) * np.std(x['B_Z'], ddof = 1)

    return(errorX,errorY,errorZ)

