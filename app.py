
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

from flask import Flask, request
from flask_restful import Api, Resource
from flask_restplus import reqparse
import json
import logging
from flask_restful_swagger import swagger

from LiveChat import findBestMovie
from LiveChat import findBestMovieWithYear
from LiveChat import findBestMovieWithGenres
from LiveChat import findBestMovieWithGenresWithYear
from LiveChat import movieDetailsWithTitle
from LiveChat import findSimilarMovies


app = Flask(__name__)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

api = swagger.docs(Api(app),apiVersion = "1.0",
                   api_spec_url="/docs",
                   produces=["application/json"], 
                   basePath="http://localhost:5003",
                   resourcePath="/",
                   description="Live Chat API calls")

parser = reqparse.RequestParser()
parser.add_argument('year', type=int,required=False, help='please enter year to get movie list')
parser.add_argument('genres', type=str,required=False, help='please enter genres to get movie list')
parser.add_argument('title', type=str,required=False, help='please enter title to get movie deatils')
parser.add_argument('numOfMovies', type=int,required=False, help='please enter number of movies you want')
              
class BestMovie(Resource): 
        def __init__(self):
            self.__numOfMovies=parser.parse_args().get("numOfMovies")
     
        @swagger.model
        @swagger.operation(
            notes="Get number of best movies from 2013 to 2018",
            parameters=[
                    {
                    	"name": "numOfMovies",
                    	"description": "please enter number of movies you want",
                    	"required": True,
                    	"allowMultiple": False,
                    	"dataType": "int",
                    	"paramType": "query"
                    }
                    ],
          
            responseMessages=[
                    	{
                    	"code": 201,
                    	"message": "Created. The URL of the created blueprint should be in the Location header"
                    	},
                    	{
                    	"code": 405,
                    	"message": "Invalid input"
                    	}
                    ]
                )
        def get(self):    
            logger.info('RemoteAddress={0} - BestMovie: numOfMovies = {1}'.format(request.remote_addr,self.__numOfMovies))                 
            bestMovie=findBestMovie(self.__numOfMovies)
            response=json.JSONDecoder().decode(bestMovie.to_json(orient = "records"))
            logger.info('BestMovie: List = {0}'.format(response))
            return response
    

             
class BestMovieWithYear(Resource): 
    def __init__(self):
        self.__year=parser.parse_args().get("year")
        self.__numOfMovies=parser.parse_args().get("numOfMovies")
     
    @swagger.model
    @swagger.operation(
            notes='Get best movie with respect to year',
            parameters=[
                    {
                    	"name": "year",
                    	"description": "Provide an year to get movie list",
                    	"required": True,
                    	"allowMultiple": False,
                    	"dataType": "int",
                    	"paramType": "query"
                    },
                      {
                    	"name": "numOfMovies",
                    	"description": "please enter number of movies you want",
                    	"required": True,
                    	"allowMultiple": False,
                    	"dataType": "int",
                    	"paramType": "query"
                    }
                    ],
          
            responseMessages=[
                    	{
                    	"code": 201,
                    	"message": "Created. The URL of the created blueprint should be in the Location header"
                    	},
                    	{
                    	"code": 405,
                    	"message": "Invalid input"
                    	}
                    ]
                )
    def get(self): 
        logger.info('RemoteAddress={0} - BestMovieWithYear:year={1},numOfMovies = {2}'.format(request.remote_addr,self.__year,self.__numOfMovies))                     
        bestMovie=findBestMovieWithYear(self.__year,self.__numOfMovies)
        response=json.JSONDecoder().decode(bestMovie.to_json(orient = "records"))
        logger.info('BestMovieWithYear: List = {0}'.format(response))
        return response

          
class BestMovieWithGenres(Resource): 
     def __init__(self):
        self.__genres=parser.parse_args().get("genres")
        self.__numOfMovies=parser.parse_args().get("numOfMovies")
        
     @swagger.model
     @swagger.operation(
            notes="Get best movie with Genres",
            parameters=[
                    {
                    	"name": "genres",
                    	"description": "Provide a genres to get movie list",
                    	"required": True,
                    	"allowMultiple": False,
                    	"dataType": "string",
                    	"paramType": "query"
                    },
                      {
                    	"name": "numOfMovies",
                    	"description": "please enter number of movies you want",
                    	"required": True,
                    	"allowMultiple": False,
                    	"dataType": "int",
                    	"paramType": "query"
                    }
                    ],
          
            responseMessages=[
                    	{
                    	"code": 201,
                    	"message": "Created. The URL of the created blueprint should be in the Location header"
                    	},
                    	{
                    	"code": 405,
                    	"message": "Invalid input"
                    	}
                    ]
                )
     def get(self):  
            logger.info('RemoteAddress={0} - BestMovieWithGenres:genres={1},numOfMovies = {2}'.format(request.remote_addr,self.__genres,self.__numOfMovies))                     
            bestMovie=findBestMovieWithGenres(self.__genres,self.__numOfMovies)
            response=json.JSONDecoder().decode(bestMovie.to_json(orient = "records"))
            logger.info('BestMovieWithGenres: List = {0}'.format(response))
            return response

               
class BestMovieWithGenresAndYear(Resource): 
     def __init__(self):
        self.__genres=parser.parse_args().get("genres")
        self.__year=parser.parse_args().get("year")
        self.__numOfMovies=parser.parse_args().get("numOfMovies")
         
     @swagger.model
     @swagger.operation(
            notes="Get best movie with Genres and Year",
            parameters=[
                    {
                    	"name": "genres",
                    	"description": "Provide a genres to get movie list",
                    	"required": True,
                    	"allowMultiple": False,
                    	"dataType": "string",
                    	"paramType": "query"
                    },
                       {
                    	"name": "year",
                    	"description": "Provide an year to get movie list",
                    	"required": True,
                    	"allowMultiple": False,
                    	"dataType": "int",
                    	"paramType": "query"
                    },
                       {
                    	"name": "numOfMovies",
                    	"description": "please enter number of movies you want",
                    	"required": True,
                    	"allowMultiple": False,
                    	"dataType": "int",
                    	"paramType": "query"
                    }
                    ],
          
            responseMessages=[
                    	{
                    	"code": 201,
                    	"message": "Created. The URL of the created blueprint should be in the Location header"
                    	},
                    	{
                    	"code": 405,
                    	"message": "Invalid input"
                    	}
                    ]
                )

     def get(self): 
            logger.info('RemoteAddress={0} - BestMovieWithGenresAndYear:genres={1},year={2},numOfMovies = {3}'.format(request.remote_addr,self.__genres,self.__year,self.__numOfMovies))              
            bestMovie=findBestMovieWithGenresWithYear(self.__genres,self.__year,self.__numOfMovies)
            response=json.JSONDecoder().decode(bestMovie.to_json(orient = "records"))
            logger.info('BestMovieWithGenresAndYear: List = {0}'.format(response))
            return response

                 
class BovieDetailsWithTitle(Resource): 
    def __init__(self):
        self.__title=parser.parse_args().get("title")
        print("title=",self.__title)
        
    @swagger.model
    @swagger.operation(
            notes="Get movie detail by passing title",
            parameters=[
                    {
                    	"name": "title",
                    	"description": "Provide a title to get movie list",
                    	"required": True,
                    	"allowMultiple": False,
                    	"dataType": "string",
                    	"paramType": "query"
                    }
                    ],
          
            responseMessages=[
                    	{
                    	"code": 201,
                    	"message": "Created. The URL of the created blueprint should be in the Location header"
                    	},
                    	{
                    	"code": 405,
                    	"message": "Invalid input"
                    	}
                    ]
                )
    def get(self):   
            logger.info('RemoteAddress={0} - BovieDetailsWithTitle:title={1}'.format(request.remote_addr,self.__title)) 
            bestMovie=movieDetailsWithTitle(self.__title)
            response=json.JSONDecoder().decode(bestMovie.to_json(orient = "records"))
            logger.info('BovieDetailsWithTitle: List = {0}'.format(response))
            return response

                 
class SimilarMoviesWithTitle(Resource): 
    def __init__(self):
        self.__title=parser.parse_args().get("title")
        self.__numOfMovies=parser.parse_args().get("numOfMovies")
        #print("title=",self.__title)
        
    @swagger.model
    @swagger.operation(
            notes="Get similar movies by passing title",
            parameters=[
                    {
                    	"name": "title",
                    	"description": "Provide a title to get similar movies list",
                    	"required": True,
                    	"allowMultiple": False,
                    	"dataType": "string",
                    	"paramType": "query"
                    },
                      {
                    	"name": "numOfMovies",
                    	"description": "please enter number of movies you want",
                    	"required": True,
                    	"allowMultiple": False,
                    	"dataType": "int",
                    	"paramType": "query"
                    }
                    ],
          
            responseMessages=[
                    	{
                    	"code": 201,
                    	"message": "Created. The URL of the created blueprint should be in the Location header"
                    	},
                    	{
                    	"code": 405,
                    	"message": "Invalid input"
                    	}
                    ]
                )
    def get(self):   
            logger.info('RemoteAddress={0} - SimilarMoviesWithTitle:title={1},numOfMovies = {2}'.format(request.remote_addr,self.__title,self.__numOfMovies)) 
            bestMovie=findSimilarMovies(self.__title,self.__numOfMovies)
            response=json.JSONDecoder().decode(bestMovie.to_json(orient = "records"))
            logger.info('SimilarMoviesWithTitle: List = {0}'.format(response))
            return response
        
api.add_resource(BestMovie, "/bestMovie")
api.add_resource(BestMovieWithYear, "/bestMovieWithYear")
api.add_resource(BestMovieWithGenres, "/bestMovieWithGenres")
api.add_resource(BestMovieWithGenresAndYear, "/bestMovieWithGenresAndYear")
api.add_resource(BovieDetailsWithTitle, "/movieDetailsWithTitle")
api.add_resource(SimilarMoviesWithTitle, "/similarMoviesWithTitle")

if __name__ == '__main__':
   #app.run(debug=True,port=5003)
    app.run(port=5003)


#findBestMovie(2)
#findBestMovieWithYear(2018,2)

# resturn datafram as json
#json=findBestMovie(2).to_json(orient = "records")
#json

#findBestMovieWithGenres("action and adventure",2)
#findBestMovieWithGenresWithYear("comedy",2013,3)
#movieDetailsWithTitle("anchorman")

#findSimilarMovies("avengers",5)