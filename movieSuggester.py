import requests
import random
import pandas as pd
import sqlalchemy as db
import os

# tmdbKey = os.environ.get('TMDB_KEY')
# omdbKey = os.environ.get('OMDB_KEY')

tmdbKey = "37909ab2a58f4d635646887a974c77a1"
omdbKey = "44a1fd91"


def getMovies(genre="", userRating="", streamingServices=[]):
    try:

        if streamingServices != []:
            selectedSS = random.choice(streamingServices)
        else:
            selectedSS = ""

        url = "https://api.themoviedb.org/3/discover/movie?api_key=" \
              + tmdbKey + "&language=en-US&sort_by=popularity.desc&" \
                          "include_adult=false&include_video=false&page=1&" \
                          "vote_count.gte=20&vote_average.gte=" + \
              str(userRating) + "&with_genres=" + str(genre) + \
              "&with_watch_providers=" + str(selectedSS) + \
              "&watch_region=US"

        response = requests.get(url)
        response = response.json()
        totalPages = response['total_pages']

        if totalPages > 500:
            totalPages = 500

        randomPage = random.randint(1, totalPages)

        url = "https://api.themoviedb.org/3/discover/movie?api_key=" \
              + tmdbKey + "&language=en-US&sort_by=popularity.desc&" \
                          "include_adult=false&include_video=false&page=" \
              + str(randomPage) + "&vote_count.gte=20&vote_average.gte=" \
              + str(userRating) + "&with_genres=" + str(genre) + \
              "&with_watch_providers=" + \
              str(selectedSS) + "&watch_region=US"

        response = requests.get(url)
        response = response.json()

        return response
    except ValueError:
        print("No movie found.")
        return -1


def selectMovie(movies):
    try:
        if movies == -1:
            return -1
        movieNumber = random.randint(0, len(movies["results"]) - 1)
        selectedMovie = movies["results"][movieNumber]

        movieTitle = selectedMovie["title"]
        movieYear = selectedMovie["release_date"][:4]


        url = "http://www.omdbapi.com/?apikey=" + omdbKey + "&t=" + \
              movieTitle.replace(" ", "+") + "&y=" + str(movieYear) + \
              "&plot=full"

        response = requests.get(url)
        response = response.json()

        
        return response
            
    except KeyError:
        print("No movie found.")
        return -1

def getMovieTitle(movie):
    if movie == -1:
        return "No Movie"
    else:
        try:
            return movie["Title"]
        except:
            return "No Movie"


def getHTML(movie):
    if movie == -1:
        return "<h1 class='nomovie'> No Movie Found </h1>" +\
            "<h5> (try using different inputs) </h5>"
    else:
        try:
            ratingSub = ""

            for rating in movie["Ratings"]:
            
                ratingSub += "" + \
                    "<div class='singleRating'>" + \
                        "<p class='source'>" + rating["Source"] + "</p>" + \
                        "<p class='value'>" + rating["Value"] + "</p>" + \
                    "</div>"

            ratings = "<div class='ratings'>" + ratingSub + "</div>"

            myHTML = "" + \
                "<div class='topCorner'>" + \
                    "<h1 class='title'>" + movie["Title"] + "</h1>"  + \
                    " <h4 class='yrr'>" + movie["Year"] + " · " + movie["Rated"] + " · " + movie["Runtime"] + \
                "</div>" + \
                "<div class='moviePoster'><img src='" + movie["Poster"] + "' class='img'> </div>" + \
                "<div class='movieInfo'>" + \
                    "<p class='genreStyle>" + movie["Genre"] + "</p>" + \
                    "<p class='plot'>" + movie["Plot"] + "</p>" + \
                    "<p class='director'>" + "Director: " + movie["Director"] + "</p>" + \
                    "<p class='writers'>" + "Writer: " + movie["Writer"] + "</p>" + \
                    "<p class='actors'>" + "Actors: " + movie["Actors"] + "</p>" + \
                    "<p class='language'>" + "Language: " + movie["Language"] + "</p>" + \
                "</div>"

            myHTML = myHTML + ratings

            return myHTML
        except:
            return "<h1 class='nomovie'> No Movie Found </h1>" +\
            "<h5> (try using different inputs) </h5>"



def createRecommendationsDatabase(movie):
    try:
        movieID = movie["id"]

        url = "https://api.themoviedb.org/3/movie/" + str(movieID) + \
          "/recommendations?api_key=" + tmdbKey + "&language=en-US&page=1"

        response = requests.get(url)
        response = response.json()

        df = pd.DataFrame.from_dict(response)

        response = response["results"]

        df = pd.DataFrame.from_dict(response)

        df1 = df[['title', 'release_date', 'vote_average', 'overview']]

        engine = db.create_engine('sqlite:///data_base_name.db')
        df1.to_sql('similarMovies', con=engine, if_exists='replace',
                   index=False)
        query_result = engine.execute("SELECT * FROM similarMovies LIMIT 10;"
                                      ).fetchall()
        print()
        print("Here is a table of similar movies: ")
        print(pd.DataFrame(query_result))
    except ValueError:
        print()
        print("We could not find any similar movies.")

