import pandas as pd 
import numpy as np 
import ast, re 
  
movies  = pd.read_csv('data/tmdb_5000_movies.csv') 
credits = pd.read_csv('data/tmdb_5000_credits.csv.gz') 
  
print('Movies shape :', movies.shape) 
print('Credits shape:', credits.shape) 
print(movies.columns.tolist())
print(movies.isnull().sum()) 

credits.rename(columns={'movie_id': 'id'}, inplace=True) 
df = movies.merge(credits, on='id') 
  
drop_cols = [ 
    'homepage', 'tagline', 'overview', 'status', 
    'original_title', 'spoken_languages', 
    'production_companies', 'production_countries' 
] 
df.drop(columns=drop_cols, inplace=True) 
print('After merge & drop:', df.shape)

df = df[(df['budget'] > 0) & (df['revenue'] > 0)] 
df.dropna(subset=['runtime', 'release_date'], inplace=True) 
print('After removing invalid rows:', df.shape) 

def parse_names(obj, key='name', limit=3): 
    try: 
        lst = ast.literal_eval(obj) 
        return [d[key] for d in lst[:limit]] 
    except: 
        return [] 
  
def get_director(crew_str): 
    try: 
        crew = ast.literal_eval(crew_str) 
        for p in crew: 
            if p['job'] == 'Director': 
                return p['name'] 
    except: 
        pass 
    return 'Unknown' 
  
df['genres']   = df['genres'].apply(parse_names) 
df['keywords'] = df['keywords'].apply(parse_names) 
df['cast']     = df['cast'].apply(parse_names) 
df['director'] = df['crew'].apply(get_director) 
df.drop(columns=['crew'], inplace=True) 

df['release_date']  = pd.to_datetime(df['release_date'], errors='coerce') 
df['release_year']  = df['release_date'].dt.year 
df['release_month'] = df['release_date'].dt.month 
df.drop(columns=['release_date'], inplace=True) 
  
for col in ['genres', 'keywords', 'cast']: 
    df[col] = df[col].apply( 
        lambda x: ','.join(x) if isinstance(x, list) else str(x)) 
  
df.to_csv('data/cleaned_movies.csv', index=False) 
print('Done! Shape:', df.shape) 
