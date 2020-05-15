deflateBR
=========

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

[![PyPI version fury.io](https://badge.fury.io/py/deflateBR.svg)](https://pypi.python.org/pypi/deflateBR/)
[![Build Status Azure](https://dev.azure.com/neylsoncrepalde/deflateBR/_apis/build/status/neylsoncrepalde.deflatebr?branchName=master)](https://dev.azure.com/neylsoncrepalde/deflateBR/_build/latest?definitionId=1&branchName=master)
[![Build Status Travis](https://travis-ci.org/neylsoncrepalde/deflatebr.svg?branch=master)](https://travis-ci.org/neylsoncrepalde/deflatebr?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/neylsoncrepalde/deflatebr/badge.svg?branch=master)](https://coveralls.io/github/neylsoncrepalde/deflatebr?branch=master)
[![Documentation Status](https://readthedocs.org/projects/deflatebr/badge/?version=latest)](https://deflatebr.readthedocs.io/en/latest/?badge=latest)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/3f38c77f8e5c4d02bbb8befd3cdb9489)](https://www.codacy.com/manual/neylsoncrepalde/deflatebr?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=neylsoncrepalde/deflatebr&amp;utm_campaign=Badge_Grade)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/deflateBR.svg)](https://pypi.python.org/pypi/deflateBR/)
[![PyPI status](https://img.shields.io/pypi/status/deflateBR.svg)](https://pypi.python.org/pypi/deflateBR/)
[![PyPi downloads](https://pypip.in/d/deflateBR/badge.png)](https://crate.io/packages/deflateBR/)
[![GitHub issues](https://img.shields.io/github/issues/neylsoncrepalde/deflatebr.svg)](https://GitHub.com/neylsoncrepalde/deflateBR/issues/)
[![GitHub issues-closed](https://img.shields.io/github/issues-closed/neylsoncrepalde/deflatebr.svg)](https://GitHub.com/neylsoncrepalde/deflatebr/issues?q=is%3Aissue+is%3Aclosed)



`deflateBR` is a `Python` package used to deflate nominal Brazilian Reais
using several popular price indexes. It is a reimplementation of the great
[deflateBR R package](https://cran.r-project.org/web/packages/deflateBR/index.html) 
by [Fernando Meireles](https://twitter.com/meirelesff).

Installation
------------

```bash
pip install deflateBR
```

Examples
--------

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


To display a **progress bar**, set `progress_bar=True`. If you are running on a jupyter notebook or a jupyter lab, set also `on_jupyter=True` to have a nice HTML progress bar: 

```python
dbr.deflate(nominal_values=df.nom_values, nominal_dates=df.dates, 
            real_date='2020-01', progress_bar=True, on_jupyter=False)
```
    100%|██████████████████████████████| 6/6 [00:00<00:00, 3006.67it/s] 
    array([1084.40219182, 1192.842411  , 1247.06252059, 1053.40923236,
       1264.09107883, 1316.76154045])


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
