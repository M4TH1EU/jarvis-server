# Important : Thanks to @builderjer for their work on the "moviemaster" repo, the code below is based on their code as of Sep 2021.
# Source : https://github.com/builderjer/moviemaster

from datetime import datetime

import tmdbv3api
from lingua_franca.format import nice_date, nice_number

from jarvis.skills import Skill, SkillRegistering
from jarvis.skills.decorators import intent_file_handler
from jarvis.utils import config_utils, languages_utils

TMDB = tmdbv3api.TMDb()
MOVIE = tmdbv3api.Movie()


class MovieMaster(Skill, metaclass=SkillRegistering):

    def __init__(self, data=dict):
        super().__init__("MovieMaster", data)

    def on_load(self):
        """ This sets some variables that do not change during the execution of the script"""
        TMDB.api_key = config_utils.get_in_secret("TMDB_API_KEY")

        # Do a quick search to verify the api_key
        try:
            p = MOVIE.popular()
        except Exception:
            print("[WARN] Specified API KEY not valid, defaulting to generic one.")

        # Default key, might get deactivated at any time.
        TMDB.api_key = '6b064259b900f7d4fd32f3c74ac35207'

        # Set the language
        TMDB.language = languages_utils.get_language_only_country()

    @intent_file_handler("movie.description.intent", "MovieDescriptionIntent")
    def handle_movie_description(self, data):
        """ Gets the long version of the requested movie.
        """
        movie = data.get("movie")
        try:
            movie_details = MOVIE.details(MOVIE.search(movie)[:1][0].id)
            if movie_details.overview != "":
                self.speak_dialog("movie.description", {"movie": movie})
                self.speak(movie_details.overview)
            else:
                self.speak_dialog("no.info", {"movie": movie})

        # If the title can not be found, it creates an IndexError
        except IndexError:
            self.speak_dialog("no.info", {"movie": movie})

    @intent_file_handler("movie.information.intent", "MovieInformationIntent")
    def handle_movie_information(self, data):
        """ Gets the short version and adds the TagLine for good measure.
        """
        movie = data.get("movie")
        try:
            movieDetails = MOVIE.details(MOVIE.search(movie)[:1][0].id)
            self.speak_dialog("movie.info.response", {"movie": movieDetails.title, "year": nice_date(
                datetime.strptime(movieDetails.release_date.replace("-", " "), "%Y %m %d")),
                                                      "budget": nice_number(movieDetails.budget)})
            self.speak(movieDetails.tagline)

        # If the title can not be found, it creates an IndexError
        except IndexError:
            self.speak_dialog("no.info", {"movie": movie})

    @intent_file_handler("movie.year.intent", "MovieYearIntent")
    def handle_movie_year(self, data):
        """ Gets the year the movie was released.
        """
        movie = data.get("movie")
        try:
            movieDetails = MOVIE.details(MOVIE.search(movie)[:1][0].id)
            self.speak_dialog("movie.year", {"movie": movieDetails.title, "year": nice_date(
                datetime.strptime(movieDetails.release_date.replace("-", " "), "%Y %m %d"))})

        # If the title can not be found, it creates an IndexError
        except IndexError:
            self.speak_dialog("no.info", {"movie": movie})

    @intent_file_handler("movie.cast.intent", "MovieCastIntent")
    def handle_movie_cast(self, data):
        """ Gets the cast of the requested movie.

        """
        movie = data.get("movie")
        try:
            movieDetails = MOVIE.details(MOVIE.search(movie)[:1][0].id)
            cast = movieDetails.casts["cast"][:5]

            # Create a list to store the cast to be included in the dialog
            actorList = ""
            # Get the last actor in the list so that the dialog can say it properly
            lastInList = cast.pop()
            lastActor = " {} as {}".format(lastInList["name"], lastInList["character"])
            # Format the rest of the list for the dialog
            for person in cast:
                actor = " {} as {},".format(person["name"], person["character"])
                # Add the formated sentence to the actor list
                actorList = actorList + actor

            self.speak_dialog("movie.cast", {"movie": movie, "actorlist": actorList, "lastactor": lastActor})

        # If the title can not be found, it creates an IndexError
        except IndexError:
            self.speak_dialog("no.info", {"movie": movie})

    @intent_file_handler("movie.production.intent", "MovieProductionIntent")
    def handle_movie_production(self, data):
        """ Gets the production companies that made the movie.

        """
        movie = data.get("movie")
        try:
            movieDetails = MOVIE.details(MOVIE.search(movie)[:1][0].id)
            companyList = movieDetails.production_companies[:5]

            # If there is only one production company, say the dialog differently
            if len(companyList) == 1:
                self.speak_dialog("movie.production.single", {"movie": movie, "company": companyList[0]["name"]})
            # If there is more, get the last in the list and set up the dialog
            if len(companyList) > 1:
                companies = ""
                lastCompany = companyList.pop()["name"]
                for company in companyList:
                    companies = companies + company["name"] + ", "
                self.speak_dialog("movie.production.multiple",
                                  {"companies": companies, "movie": movie, "lastcompany": lastCompany})

        # If the title can not be found, it creates an IndexError
        except IndexError:
            self.speak_dialog("no.info", {"movie": movie})

    @intent_file_handler("movie.genres.intent", "MovieGenresIntent")
    def handle_movie_genre(self, data):
        """ Gets the genres the movie belongs to.

        """
        movie = data.get("movie")
        try:
            movieDetails = MOVIE.details(MOVIE.search(movie)[:1][0].id)
            genreList = movieDetails.genres[:5]
            # Set up dialog AGAIN just like above.  Is there a better way?
            if len(genreList) == 1:
                self.speak_dialog("movie.genre.single", {"movie": movie, "genre": genreList[0]["name"]})
            if len(genreList) > 1:
                genreDialog = ""
                lastGenre = genreList.pop()["name"]
                for genre in genreList:
                    genreDialog = genreDialog + genre["name"] + ", "
                self.speak_dialog("movie.genre.multiple", {"genrelist": genreDialog, "genrelistlast": lastGenre})

        # If the title can not be found, it creates an IndexError
        except IndexError:
            self.speak_dialog("no.info", {"movie": movie})

    @intent_file_handler("movie.runtime.intent", "MovieRuntimeIntent")
    def handle_movie_length(self, data):
        """ Gets the runtime of the searched movie.
        """
        movie = data.get("movie")
        try:
            movieDetails = MOVIE.details(MOVIE.search(movie)[:1][0].id)
            self.speak_dialog("movie.runtime", {"movie": movie, "runtime": movieDetails.runtime})

        # If the title can not be found, it creates an IndexError
        except IndexError:
            self.speak_dialog("no.info", {"movie": movie})

    @intent_file_handler("movie.recommendations.intent", "MovieRecommendationsIntent")
    def handle_movie_recommendations(self, data):
        """ Gets the top movies that are similar to the suggested movie.
        """
        try:
            movie = data.get("movie")
            # Create a list to store the dialog
            movieDialog = ""
            movieRecommendations = MOVIE.recommendations(MOVIE.search(movie)[:1][0].id)[:5]
            # Get the last movie
            lastMovie = movieRecommendations.pop()
            for film in movieRecommendations:
                if movieDialog == "":
                    movieDialog = film.title
                else:
                    movieDialog = movieDialog + ", " + film.title
            movieDialog = movieDialog + " and {}".format(lastMovie.title)
            self.speak_dialog("movie.recommendations", {"movielist": movieDialog, "movie": movie})

        # If the title can not be found, it creates an IndexError
        except IndexError:
            self.speak_dialog("no.info", {"movie": movie.title})

    @intent_file_handler("movie.popular.intent", "MoviePopularIntent")
    def handle_popular_movies(self, data):
        """ Gets the daily popular movies.

        The list changes daily, and are not just recent movies.

        """
        try:
            popularMovies = MOVIE.popular()[:5]
            # Lets see...I think we will set up the dialog again.
            lastMovie = popularMovies.pop()
            popularDialog = ""
            for movie in popularMovies:
                if popularDialog == "":
                    popularDialog = movie.title
                else:
                    popularDialog = popularDialog + ", " + movie.title
            popularDialog = popularDialog + " and {}".format(lastMovie.title)
            self.speak_dialog("movie.popular", {"popularlist": popularDialog})

        except:
            pass

    @intent_file_handler("movie.top.intent", "MovieTopIntent")
    def handle_top_movies(self, data):
        """ Gets the top rated movies of the day.
        The list changes daily, and are not just recent movies.

        """
        try:
            topMovies = MOVIE.top_rated()[:5]
            # Set up the dialog
            lastMovie = topMovies.pop()
            topDialog = ""
            for movie in topMovies:
                if topDialog == "":
                    topDialog = movie.title
                else:
                    topDialog = topDialog + ", {}".format(movie.title)
            topDialog = topDialog + " and {}".format(lastMovie.title)
            self.speak_dialog("movie.top", {"toplist": topDialog})

        except:
            pass


def create_skill(data):
    return MovieMaster(data)
