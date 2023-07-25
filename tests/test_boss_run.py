import pandas as pd
import numpy as np
from boss.bo.bo_main import BOMain

df = pd.read_csv('../data/data.csv', sep=';', index_col='ID')
X = df.loc[:, ['P-factor', 'temperature']].to_numpy()
Y = -df.loc[:, 'lignin yield'].to_numpy()

bounds = [[500, 2500], [180, 210]]


def dummy():
    pass


# BOMain object for the first objective
bo = BOMain(
    f=dummy,
    bounds=bounds,
    yrange=[np.min(Y), np.max(Y)],
    initpts=0,
    iterpts=0,
    noise=1e-2,
)
res = bo.run(X, Y)

print(f'Predicted max. {-res.select("mu_glmin", -1)}')
print(f'Predicted max. loc {res.select("x_glmin", -1)}')


