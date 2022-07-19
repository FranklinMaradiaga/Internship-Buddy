import requests
import random
import pandas as pd
import sqlalchemy as db

tmdbKey = ""
omdbKey = ""

print()
print("This program recommends a movie based on your preferences!")
print()


def getGenre():
    url = "https://api.themoviedb.org/3/genre/movie/list?api_key=" \
          + tmdbKey + "&language=en-US"
    response = requests.get(url)
    response = response.json()

    genreList = [genre['name'] for genre in response['genres']]
    idList = [genre['id'] for genre in response['genres']]

    genreOrNo = input("Would you like to specify a genre for the movie "
                      "suggestion? (yes or no): ")

    if genreOrNo.lower() == "yes":
        print("Here are the genres available:")
        print(genreList)

        userGenre = input("Enter a genre: ").lower().capitalize()

        while userGenre not in genreList:
            userGenre = input("Invalid input. Enter a genre listed "
                              "above: ").lower().capitalize()

        return idList[genreList.index(userGenre)]

    elif genreOrNo.lower() == "no":
        return ""
    else:
        print("Invalid input. Type 'yes' or 'no'")
        return getGenre()


def getUserRating():
    ratingOrNO = input("Would you like to specify a minimum user rating? "
                       "(yes or no): ")

    if ratingOrNO.lower() == "yes":
        print("User ratings range from 0 to 10. For reference, most popular "
              "movies have an average user rating between 6 and 8")
        userRating = input("Enter a minimum user rating: ")
        return checkUserRating(userRating)
    elif ratingOrNO.lower() == "no":
        return ""
    else:
        print("Invalid input. Type 'yes' or 'no'")
        return getUserRating()


def checkUserRating(rating):
    try:
        userRating = float(rating)
        while userRating < 0 or userRating > 10:
            userRating = float(input("Invalid input. Enter an number between 0"
                                     " and 10: "))
        return userRating
    except ValueError:
        print("Error: input should be a number.", end=" ")
        rating = input("Enter a minimum user rating: ")
        return checkUserRating(rating)


def getStreamingServices():
    streamingServices = ["Netflix", "Amazon Prime Video", "Hulu",
                         "Paramount Plus", "HBO max", "Peacock", "ShowMax",
                         "Apple Tv Plus", "Crunchyroll", "Disney Plus",
                         "HBO Go", "The Roku Channel", "Discovery Plus",
                         "Showtime", "Apple iTunes", "Netflix Kids",
                         "Youtube Premium", "Google Play Movies"]

    idList = [8, 9, 15, 531, 384, 386, 55, 350, 283, 390, 31, 207, 510, 37, 2,
              175, 188, 3]

    serviceOrNo = input("Would you like to specify a streaming service? "
                        "(yes or no): ")

    if serviceOrNo.lower() == "yes":
        print("Here are the streaming services available:")
        print(streamingServices)

        userSS = input(
            "Enter the streaming services you have (separate them with "
            "a comma and a space ', '): ").strip().split(", ")

        userSS = [service.lower() for service in userSS]
        streamingServices = [service.lower() for service in streamingServices]

        validInput = True

        for service in userSS:
            if service not in streamingServices:
                validInput = False

        while not validInput:
            validInput = True
            userSS = input(
                "Enter the streaming services you have (separate them "
                "with a comma and a space ', '): ").strip().split(", ")

            userSS = [service.lower() for service in userSS]
            for service in userSS:
                if service not in streamingServices:
                    validInput = False

        return [idList[streamingServices.index(service)] for service in userSS]

    elif serviceOrNo.lower() == "no":
        return ""

    else:
        print("Invalid input. Type 'yes' or 'no'")
        return getStreamingServices()


def getMovies(genre="", userRating="", streamingServices=""):
    try:

        if streamingServices != "":
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


runProgram()
