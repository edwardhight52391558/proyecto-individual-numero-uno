from fastapi import FastAPI
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

app_movies = FastAPI(title= 'PELICULAS en NETFLIX, PRIME VIDEO, DISNEY PLUS, HULU',
            description= 'DATABASE para consultas de peliculas',
            version= '1.0.1')

r_movies = pd.read_csv('rating_movies.csv')
df_rp = pd.read_csv('rating_p.csv')
df_rp = df_rp.set_index('movieId')
df_platform = pd.read_csv('platform.csv')

df_N = df_platform[df_platform['platform']=='netflix']
df_D = df_platform[df_platform['platform']=='disney']
df_A = df_platform[df_platform['platform']=='amazon']
df_H = df_platform[df_platform['platform']=='hulu']

@app_movies.get('/get_max_duration/{year}/{platform}/{duration_type}')
def get_max_duration(year: int,platform: str, duration_type: str):
    if platform == 'netflix':
        index_pelicula = df_N[(df_N['release_year']==year)&(df_N['duration_type']==duration_type)&(df_N['type']=='movie')][['duration_int']].idxmax(axis= 0)[0]
        pelicula = df_N.loc[index_pelicula, 'title']
    if platform == 'amazon':
        index_pelicula = df_A[(df_A['release_year']==year)&(df_A['duration_type']==duration_type)&(df_A['type']=='movie')][['duration_int']].idxmax(axis= 0)[0]
        pelicula = df_A.loc[index_pelicula, 'title']
    if platform == 'hulu':
        index_pelicula = df_H[(df_N['release_year']==year)&(df_H['duration_type']==duration_type)&(df_H['type']=='movie')][['duration_int']].idxmax(axis= 0)[0]
        pelicula = df_H.loc[index_pelicula, 'title']
    if platform == 'disney':
        index_pelicula = df_D[(df_D['release_year']==year)&(df_D['duration_type']==duration_type)&(df_D['type']=='movie')][['duration_int']].idxmax(axis= 0)[0]  
        pelicula = df_D.loc[index_pelicula, 'title']
    return 'pelicula : ' + pelicula

@app_movies.get('/get_score_count/{platform}/{scored}/{year}')
def get_score_count(platform: str,scored: float, year: int):
    if platform == 'disney':
        lista_id = df_D[(df_D['release_year']==year)&(df_D['type']=='movie')]['id']
    if platform == 'amazon':
        lista_id = df_A[(df_A['release_year']==year)&(df_A['type']=='movie')]['id']
    if platform == 'hulu':
        lista_id = df_H[(df_H['release_year']==year)&(df_H['type']=='movie')]['id']
    if platform == 'netflix':
        lista_id = df_N[(df_N['release_year']==year)&(df_N['type']=='movie')]['id']
    count = 0
    for x in lista_id:     
        if df_rp.loc[x, 'rating'] >scored:
            count += 1 
    return count

@app_movies.get('/get_count_platform/{platform}')
def get_count_platform(platform: str):
    if platform == 'netflix':
        return 6131
    if platform == 'hulu':
        return 1484
    if platform == 'amazon':
        return 7814
    if platform == 'disney':
        return 1052
    
@app_movies.get('/get_actor/{platform}/{year}')
def get_actor(platform: str,year: int):
    if platform == 'netflix':
        df_N['actores'] = df_N.cast.str.split(',', expand = False)
        actores = df_N[df_N['release_year']==year]['actores']
    if platform == 'amazon':
        df_A['actores'] = df_A.cast.str.split(',', expand = False)
        actores = df_A[df_A['release_year']==year]['actores']
    if platform == 'hulu':
        df_H['actores'] = df_H.cast.str.split(',', expand = False)
        actores = df_H[df_H['release_year']==year]['actores']
    if platform == 'disney':
        df_D['actores'] = df_D.cast.str.split(',', expand = False)
        actores = df_D[df_D['release_year']==year]['actores']
    actor = []
    for i in actores:
        for k in i: actor.append(k)
    actor = pd.DataFrame(actor)
    return actor.value_counts().index[0][0].strip()

@app_movies.get('/prod_per_county/{tipo}/{pais}/{year}')
def prod_per_county(tipo: str, pais: str, year: int):
    count = df_platform[(df_platform['type']==tipo)&(df_platform['country']==pais)&(df_platform['release_year']==year)]['id'].count()
    return int(count)

@app_movies.get('/get_contents/{rating}')
def get_contents(rating: str):
    r = df_platform[df_platform['rating']==rating]['id'].count()
    return int(r)

@app_movies.get('/get_recomendacion_movies/{rating}/{duracion}/{year}/{platform}')
def get_recomendacion_movies(rating: float, duracion: int, year: int, platform: str):
    if platform=='amazon': plataforma = 1
    if platform=='netflix': plataforma = 4
    if platform=='hulu': plataforma = 3
    if platform=='disney': plataforma = 2
    year = year - 1930
    X = r_movies[['duration_int','rating','release_year','platform']]
    y = r_movies['indice']

    peliculas = []
    for k in [1,50,100,200,3000]:
        knn = KNeighborsClassifier(n_neighbors=k)

        knn.fit(X, y)

        new_point = [(duracion, rating, year,plataforma)]

        prediction = knn.predict(new_point)

        peliculas.append(r_movies.loc[prediction[0], 'title'])

    return peliculas

        
