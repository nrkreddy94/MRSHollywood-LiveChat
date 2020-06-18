#!/usr/bin/env python
# coding: utf-8

# import libraries
import pandas as pd
import pickle
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('LiveChat.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

movie_reviews=pd.read_csv("move_review_final_dataset.csv",compression="gzip")
logger.info('success!! Loading move_review_final_dataset.csv')

movie_name_index_df=pd.read_csv("movie_user_rating_index.csv",encoding ='utf-8',compression='gzip')
logger.info('success!! Loading movie_user_rating_index.csv')

movie_user_rating_df=pd.read_csv("movie_user_rating_pivottable.csv", encoding ='utf-8',compression='gzip')
#movie_user_rating_df=pd.read_csv("movie_user_rating_pivottable_test.csv", encoding ='utf-8',compression='gzip')
logger.info('success!! Loading movie_user_rating_pivottable.csv')

# We trained this model with cosine simility for movie recommendation system
model_knn = pickle.load( open( "collaborativeFiltering_model.pkl", "rb" ) )
logger.info('success!! Loading collaborativeFiltering_model.pkl')

# We trained this model with Navie Bayes - Multinomial 
# get moive name index which is used in model_knn
model_classifier = pickle.load( open( "collaborativeFiltering_NLP_model.pkl", "rb" ) )
logger.info('success!! Loading collaborativeFiltering_NLP_model.pkl')

#To get correct movie name, if user enter movie name mis order used in model_classifier
vectorizer = pickle.load(open("collaborativeFiltering_NLP_vectorizer.pkl", 'rb')) 
logger.info('success!! Loading collaborativeFiltering_NLP_vectorizer.pkl')

# pass movie name and get movie index which can be used in recommendation modelmodel_knn
def getMovieIndex(name):
    logger.info('getMovieIndex: name ={0}'.format(name))
    name=name.strip().lower()
    firstValue="10 cloverfield lane".lower()
    test_vector= vectorizer.transform([name])
    predicted = model_classifier.predict(test_vector)
    
    available =   name in firstValue
    # return -1 for unavailable movies
    if((predicted[0] == 0) & (~available)):
        logger.info('getMovieIndex: index ={0}'.format(-1))
        return -1
    else:
        logger.info('getMovieIndex: index ={0}'.format(predicted[0]))
        return predicted[0]


# pass movie index and numb of movies recommendations 
def getRecomendedMoviesByIndex(queryIndex,numOfMoives=5):
    logger.info('getRecomendedMoviesByIndex: queryIndex ={0} and numOfMovies={1}'.format(queryIndex,numOfMoives))
    distances, indices = model_knn.kneighbors(movie_user_rating_df.iloc[queryIndex,:].values
                                              .reshape(1,-1), n_neighbors = numOfMoives)
    logger.info('getRecomendedMoviesByIndex: distances ={0}'.format(distances))
    logger.info('getRecomendedMoviesByIndex: indices ={0}'.format(indices))
    return distances,indices


# pass movie index and number of movie recommendations 
def recommendedMovies(name,numOfMoives=5):
    logger.info('recommendedMovies: name ={0} and numOfMovies={1}'.format(name,numOfMoives))
    movieList=list()
    try:
        query_index=getMovieIndex(name)
        if(query_index == -1):
             return movieList
        distances, indices =getRecomendedMoviesByIndex(query_index,numOfMoives)
        for i in range(0, len(distances.flatten())):
           # print(movie_name_index_df.title[indices.flatten()[i]],distances.flatten()[i])
            movieList.append(movie_name_index_df.title[indices.flatten()[i]])
        logger.info('recommendedMovies: movieList ={0}'.format(movieList))
        return movieList
    except:
         logger.info('recommendedMovies: movieList ={0}'.format(movieList))
         return movieList


# pass movie name and get movie details
def movieDetailsWithTitle(title):
    logger.info('movieDetailsWithTitle: title ={0}'.format(title))
    title=title.strip().lower()
    details = movie_reviews[movie_reviews["title"] == title]
    if(details.empty):
         details = movie_reviews[movie_reviews["title"].str.contains(title)]
    logger.info('movieDetailsWithTitle: details ={0}'.format(details))
    return details


def listToDataFrame(mvList):
    columns=["movieId","title","genres","year","tmdLink","total_rating","0.5","1.0","1.5","2.0","2.5","3.0","3.5","4.0","4.5","5.0","avg_rating"]
    movieList=list()
    for i, val in enumerate(mvList): 
        for rows in movieDetailsWithTitle(val).itertuples(): 
            movieList.append([rows.movieId, rows.title, rows.genres, rows.year,rows.tmdLink, rows.total_rating,
                                 rows._7,rows._8, rows._9, rows._10,rows._11,
                                 rows._12,rows._13,rows._14,rows._15,rows._16,rows.avg_rating])
    movies_df=pd.DataFrame(movieList,columns=columns)
    movies_df.sort_values(by="year", axis=0, ascending=False, inplace=True, kind='quicksort', na_position='last')
    return movies_df.reset_index(drop=True)
            

# find number of best movies
def findBestMovie(numberOfMovies=5):
    logger.info('findBestMovie: numberOfMovies ={0}'.format(numberOfMovies))
    most_popular_movie=movie_reviews["total_rating"].max()
    bestMovie=movie_reviews.query("total_rating == @most_popular_movie")
    name=bestMovie.iloc[0].title
    #name="10 You Things  About I "
    mvList=recommendedMovies(name,numberOfMovies)
    logger.info('findBestMovie: mvList ={0}'.format(mvList))
    return listToDataFrame(mvList)

# Get number of best movies with respect to given year
def findBestMovieWithYear(year,numberOfMovies=5):
    logger.info('findBestMovieWithYear:year={0}, numberOfMovies ={1}'.format(year,numberOfMovies))
    most_popular_movies_year=movie_reviews[movie_reviews["year"]==year].sort_values(by="total_rating", axis=0, ascending=False, inplace=False, kind='quicksort', na_position='last')
    return most_popular_movies_year.iloc[:numberOfMovies]


# Get number of best movies with respect to given genres
def findBestMovieWithGenres(genres,numberOfMovies=5):
    logger.info('findBestMovieWithGenres:genres={0}, numberOfMovies ={1}'.format(genres,numberOfMovies))
    genres= genres.replace("and",",")
    most_popular_movies_genres=  movie_reviews.query("genres == @genres").sort_values(by="total_rating", axis=0, ascending=False, inplace=False, kind='quicksort', na_position='last')
    return most_popular_movies_genres.iloc[:numberOfMovies]


# Get number of best movies with respect to genres and year
def findBestMovieWithGenresWithYear(genres,year,numberOfMovies=5):
    logger.info('findBestMovieWithGenresWithYear:genres={0}, year={1},numberOfMovies ={2}'.format(genres,year,numberOfMovies))
    genres= genres.replace("and",",")
    most_popular_movies_genres_year=movie_reviews.query("genres == @genres & year == @year").sort_values(by="total_rating", axis=0, ascending=False, inplace=False, kind='quicksort', na_position='last')
    return most_popular_movies_genres_year.iloc[:numberOfMovies]


# find number of similar (cosine similarity) movies with respect to given movie
def findSimilarMovies(name,numberOfMovies=5):
    logger.info('findSimilarMovies:name={0}, numberOfMovies ={1}'.format(name,numberOfMovies))
    mvList=recommendedMovies(name,numberOfMovies+1)
    return listToDataFrame(mvList)


#findBestMovie(2)
#findBestMovieWithYear(2018,2)

# resturn datafram as json
#json=findBestMovie(2).to_json(orient = "records")
#json

#findBestMovieWithGenres("action and adventure",2)
#findBestMovieWithGenresWithYear("comedy",2013,3)
#movieDetailsWithTitle("anchorman")

#findSimilarMovies("avengers",5)




























