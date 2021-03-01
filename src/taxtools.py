import pandas as pd
import numpy as np
import pandas_datareader as pdr
from functools import reduce
import click
import os

def subsetByYear(data, year):
    index = list(
        filter(
            lambda row: isInYear(row[1], year)
        ,
        data.index.values))
    return data.loc[index]

def findLastDay(data):
    return data.tail(1)

def isInYear(time, year):
    return ((time >= pd.Timestamp(f"{year}-01-01", tz='UTC')) and
     (time <= pd.Timestamp(f"{year}-12-31", tz='UTC')))

def findMaxClose(data):
    return data['close'].max()

def findTotalDividends(data):
    return data['divCash'].sum()

def readAssetList(path):
    assets =  pd.read_csv(path)
    assets['MaxValue'] = 0.0
    assets['LastValue'] = 0.0
    assets['Dividends'] = 0.0
    return assets

def processAssetList(assets, year):
    for index, asset in assets.iterrows():
        ticker = asset['Symbol']
        qty = asset['Qty']
        data = pdr.get_data_tiingo(ticker, api_key=os.getenv('TIINGO_API_KEY'))
        subset = subsetByYear(data, year)
        maxValue = findMaxClose(subset)
        lastValue = subset['close'].tail(1).min()
        dividends = findTotalDividends(subset)
        assets.at[index, 'MaxValue'] = round(qty * maxValue, 2)
        assets.at[index, 'LastValue'] = round(qty * lastValue, 2)
        assets.at[index, 'Dividends'] = round(qty * dividends, 2)

    return assets

@click.command()
@click.argument('year')
@click.argument('inputpath', type=click.Path(exists=True))
@click.argument('outputpath', type=click.Path(exists=False))
def process(year, inputpath, outputpath):
    assets = readAssetList(inputpath)
    processedAssets = processAssetList(assets, year)
    processedAssets.to_csv(outputpath, index = False)

if __name__ == '__main__':
    process()
