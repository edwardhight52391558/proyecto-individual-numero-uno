import pandas as pd

df_platform = pd.read_csv('platform.csv')

df_ml = pd.read_csv('ml.csv')

rating_promedio_ml = df_ml[['movieId','rating']].groupby('movieId').mean()
rating_promedio_ml['id'] = rating_promedio_ml.index


