CREATE TABLE FSIndices(
id INTEGER,
symbol VARCHAR(100),
enterpriseValue INTEGER,
enterpriseValueOverEBIT INTEGER,
enterpriseValueOverEBITDA INTEGER,
payoutRatio INTEGER,
priceToBookValue INTEGER,
priceEarnings INTEGER,
priceToEarnings INTEGER,
priceToEarningsRatio INTEGER,
preferredDividendsIncomeStatementImpact INTEGER,
sharePriceAdjustedClose INTEGER,
priceSales INTEGER,
priceToSalesRatio INTEGER,
returnOnAverageAssets INTEGER,
returnOnAverageEquity INTEGER,
returnOnInvestedCapital INTEGER,
returnOnSales INTEGER,
shares INTEGER,
weightedAverageShares INTEGER,
weightedAverageSharesDiluted INTEGER,
salesPerShare INTEGER,
tangibleAssetsBookValuePerShare INTEGER,
FOREIGN KEY (id) 
    REFERENCES FSTime (id) 
        ON DELETE CASCADE 
        ON UPDATE NO ACTION
);