deflateBR
=========

[![Build Status](https://travis-ci.org/neylsoncrepalde/deflatebr.svg?branch=master)](https://travis-ci.org/neylsoncrepalde/deflatebr?branch=master)
[![codecov](https://codecov.io/gh/neylsoncrepalde/deflatebr/branch/master/graph/badge.svg)](https://codecov.io/gh/neylsoncrepalde/deflatebr)



`deflateBR` is a `Python` package used to deflate nominal Brazilian Reais
using several popular price indexes. It is a reimplementation of the great
[`deflateBR` `R` package](https://cran.r-project.org/web/packages/deflateBR/index.html) 
by [Fernando Meireles](https://twitter.com/meirelesff).

Installation
============

```bash
pip install deflateBR
```

Examples
========

The `deflateBR`’s main function, `deflate`, requires three arguments to
work: an `int` of `float` vector of nominal Reais (`nominal_values`); a `str` or `datetime` vector of corresponding dates (`nominal_dates`); and a reference month in the `YYYY-MM` format (`real_date`), used to deflate the values. An
example:

To deflate BRL R$100,00 (one hundred brazilian reais) in January 2015,
simply do

```python
import deflatebr as dbr

dbr.deflate(nominal_values=100, nominal_dates='2015-01-01', 
            real_date='2020-01')
```
    array([131.32029183])

To deflate a bigger series, do

```python
import pandas as pd

df = pd.DataFrame({'nom_values':[100,200,300,400],
                    'dates':['2015-01-01', '2015-02-01',
                            '2015-10-01', '2015-12-01']})
df
```
       nom_values       dates
    0         100  2015-01-01
    1         200  2015-02-01
    2         300  2015-10-01
    3         400  2015-12-01

```python
dbr.deflate(nominal_values=df.nom_values, nominal_dates=df.dates, 
            real_date='2020-01')
```
    array([131.32029183, 259.42387232, 365.99132289, 479.18030761])


Behind the scenes, `deflateBR` requests data from
[IPEADATA](http://www.ipeadata.gov.br/)’s API on one these five
Brazilian price indexes:
[IPCA](https://ww2.ibge.gov.br/english/estatistica/indicadores/precos/inpc_ipca/defaultinpc.shtm)
and
[INPC](https://ww2.ibge.gov.br/english/estatistica/indicadores/precos/inpc_ipca/defaultinpc.shtm),
maintained by [IBGE](https://ww2.ibge.gov.br/home/); and
[IGP-M](http://portalibre.fgv.br/main.jsp?lumChannelId=402880811D8E34B9011D92B6160B0D7D),
[IGP-DI](http://portalibre.fgv.br/main.jsp?lumChannelId=402880811D8E34B9011D92B6160B0D7D),
and
[IPC](http://portalibre.fgv.br/main.jsp?lumChannelId=402880811D8E34B9011D92B7350710C7)
maintained by
[FGV/IBRE](http://portalibre.fgv.br/main.jsp?lumChannelId=402880811D8E2C4C011D8E33F5700158).
To select one of the available price indexes, just provide one of the
following options to the `index =` argument: `ipca`, `igpm`, `igpdi`,
`ipc`, and `inpc`. In the following, the INPC index is used.

```python
dbr.deflate(nominal_values=100, nominal_dates='2015-01-01', 
            real_date='2020-01', index='inpc')
```
    array([131.06584509])


Methodology
-----------

Following standard practice, seconded by the [Brazilian Central
Bank](https://www3.bcb.gov.br/CALCIDADAO/publico/metodologiaCorrigirIndice.do?method=metodologiaCorrigirIndice),
the `deflateBR` adjusts for inflation by multiplying nominal Reais by
the ratio between the original and the reference price indexes. For
example, to adjust 100 reais of January 2018, with IPCA index of
4916.46, to August 2018, with IPCA of 5056.56 in the previous month, we
first calculate the ratio between the two indexes (e.g., 5056.56 /
4916.46 = 1.028496) and then multiply this value by 100 (e.g., 102.84
adjusted Reais). The `deflate` function gives exactly the same result:

```python
dbr.deflate(100,"2018-01-01", "2018-08", "ipca")
```
    array([102.84961131])

Authors
------

[Neylson Crepalde](https://www.neylsoncrepalde.com) & 
[Fernando Meireles](http://fmeireles.com)
