import pandas as pd 
import numpy as np 
import ast, re 
  
movies  = pd.read_csv('data/tmdb_5000_movies.csv') 
credits = pd.read_csv('data/tmdb_5000_credits.csv.gz') 
  
print('Movies shape :', movies.shape) 
print('Credits shape:', credits.shape) 
print(movies.columns.tolist())
rint(movies.isnull().sum()) 
