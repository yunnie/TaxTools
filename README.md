# TaxTools

As an American living in Canada, I am required to disclose my foreign assets to the Canada Revenue Agency (CRA). This includes the maximum values of the asset during the year. As you might imagine, this is pretty tedious. So I wrote a little command line utility that reads in a CSV file and returns the max value of each asset. 

I use [TIINGO](https://www.tiingo.com) as the data source. TIINGO does require an API key, which I store as an environmental variable. 

## Setup

Register with `TIINGO` and get an API key. Then create an environmental variable `TIINGO_API_KEY` and store the api. Since I `zsh` as my shell, I store in the `.zshrc` file. 

Input file should be a CSV file. Fields are `Account: String`, `Ticker: String`,` NameOfAsset: String`, `Shares: Float`

`Account` is just string indicator that I use to record the financial instution that holds the asset. So if you stored everything an an E-trade account, you would just wite 'E-trade'.

`Ticker` is the ticker symbol. For example `AAPL` for Apple shares.

`NameOfAsset` is a string that records the name of the asset. For example `Apple` for Apple shares. 

`Shares` is the number of shares of the asset held in the account. So if you owned 150 shares of Apple stock, you would write `100`.

## Use

`python3 taxtools.py [year] [inputpath] [outputpath]` where `year`is the tax year, `inputpath` is the path to a csv file containing Account, Ticker, NameOfAsset, and Shares. `outputpath` is the path where you would like the output. 

