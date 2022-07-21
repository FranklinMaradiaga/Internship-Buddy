import requests
import random
import pandas as pd
import sqlalchemy as db
import os

# tmdbKey = os.environ.get('TMDB_KEY')
# omdbKey = os.environ.get('OMDB_KEY')

tmdbKey = "37909ab2a58f4d635646887a974c77a1"
omdbKey = "44a1fd91"


def getMovies(genre="", userRating="", streamingServices=""):
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
        print("No movies found.")
        return -1


def displayMovie(movie):
    movieTitle = movie["title"]
    movieYear = movie["release_date"][:4]

    try:
        url = "http://www.omdbapi.com/?apikey=" + omdbKey + "&t=" + \
              movieTitle.replace(" ", "+") + "&y=" + str(movieYear) + \
              "&plot=short"

        response = requests.get(url)
        response = response.json()

        title = response["Title"]

        print()
        print("Here is some information about the movie we selected for you:")
        print("Title: " + title)
        print("Year: " + response["Year"])
        print("Rated: " + response["Rated"])
        print("Runtime: " + response["Runtime"])
        print("Genre: " + response["Genre"])
        print("Director: " + response["Director"])
        print("Writer: " + response["Writer"])
        print("Language: " + response["Language"])
        print("Plot: " + response["Plot"])
        print("Ratings: ")
        for rating in response["Ratings"]:
            print("   Source: " + rating["Source"])
            print("   Value: " + rating["Value"])
    except KeyError:
        return -1


def createRecommendationsDatabase(movie):
    movieID = movie["id"]

    url = "https://api.themoviedb.org/3/movie/" + str(movieID) + \
          "/recommendations?api_key=" + tmdbKey + "&language=en-US&page=1"

    response = requests.get(url)
    response = response.json()

    df = pd.DataFrame.from_dict(response)

    try:
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


def runProgram():
    genre = getGenre()
    userRating = getUserRating()
    streamingServices = getStreamingServices()

    endProgram = ""

    while endProgram.lower() != "no":
        movies = getMovies(genre, userRating, streamingServices)
        if movies == -1:
            break
        movieNumber = random.randint(0, len(movies["results"]) - 1)
        selectedMovie = movies["results"][movieNumber]

        while displayMovie(selectedMovie) == -1:
            movies = getMovies(genre, userRating, streamingServices)
            movieNumber = random.randint(0, len(movies["results"]) - 1)
            selectedMovie = movies["results"][movieNumber]

        createRecommendationsDatabase(selectedMovie)
        print()

        endProgram = input("Would you like to search for a new movie? "
                           "Type 'yes' or 'no'. Type 'new' to enter "
                           "new inputs: ")

        while (endProgram.lower() != 'yes' and endProgram.lower() != 'no' and
               endProgram.lower() != 'new'):
            endProgram = input("Invalid input. Type yes, no, or new: ")

        if endProgram.lower() == 'new':
            break

    if endProgram.lower() == 'new' or movies == -1:
        runProgram()


# runProgram()