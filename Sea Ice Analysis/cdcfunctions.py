'''
cdcfunctions.py

- Written on 2/16/2018 for CLaSP 405 by Adam Benson. 
Purpose:
- To provide functions to manipulate and plot CDC data.
'''

def randomColor(x, rootMeanSquareError):
    '''
    This function calculates a random HEX Value

    Outputs the HEX Value to be used in plotting. 

    Hex Codes: https://htmlcolorcodes.com/

    '''
    import numpy as np
    
    import random

    r = lambda: random.randint(0,215) #reasonable range of visible HEX values

    randomColor = '#%02X%02X%02X'.format() % (r(),r(),r()) # proper HEX value format

    return randomColor
    
def stateframes(dFrame):
    '''
    This generates a dictionary of pandas Dataframes, where each DataFrame

    represents a state. A CDC dataframe is taken as an input, and a dictionary

    is returned as output. 
    '''
    import numpy as np
    import pandas as pandas

    stateDict = dict()

    for x in dFrame.State.unique():
        xDataMask = dFrame.State == x
        xData = dFrame.loc[xDataMask]
        stateDict[x] = xData

    return stateDict