"""

    Streamlit webserver-based Recommender Engine.

    Author: Explore Data Science Academy.

    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within the root of this repository for guidance on how to use
    this script correctly.

    NB: !! Do not remove/modify the code delimited by dashes !!

    This application is intended to be partly marked in an automated manner.
    Altering delimited code may result in a mark of 0.
    ---------------------------------------------------------------------

    Description: This file is used to launch a minimal streamlit web
	application. You are expected to extend certain aspects of this script
    and its dependencies as part of your predict project.

	For further help with the Streamlit framework, see:

	https://docs.streamlit.io/en/latest/

"""
# Streamlit dependencies
import streamlit as st

# Data handling dependencies
import pandas as pd
import numpy as np

# Custom Libraries
from surprise import SVD
from utils.data_loader import load_movie_titles
from utils.eda import get_movie_names
from recommenders.collaborative_based import collab_model
from recommenders.content_based import content_model
from utils.eda import unique_genre

# Data Loading
title_list = load_movie_titles('Movie-Recommender-System/resources/data/content_data.csv')
movie = pd.read_csv('Movie-Recommender-System/resources/data/movies.csv')
genre_data = pd.read_csv('Movie-Recommender-System/resources/data/for_genres.csv')
genre_list = unique_genre(genre_data)
years = genre_data.year.unique()


# App declaration


def main():
    # DO NOT REMOVE the 'Recommender System' option below, however,
    # you are welcome to add more options to enrich your app.
    page_options = ["Landing Page", "About The Data", "Select Movie By Genre and Year",
                    "Visuals", "Recommender System", "Solution Overview"]

    # -------------------------------------------------------------------
    # ----------- !! THIS CODE MUST NOT BE ALTERED !! -------------------
    # -------------------------------------------------------------------
    page_selection = st.sidebar.selectbox("Choose Option", page_options)
    if page_selection == "Recommender System":
        # Header contents
        st.write('# Movie Recommender Engine')
        st.image('Movie-Recommender-System/resources/imgs/Image_header.png', use_column_width=True)
        # Recommender System algorithm selection
        sys = st.radio("Select an algorithm",
                       ('Content Based Filtering',
                        'Collaborative Based Filtering'))

        # User-based preferences
        st.write('### Enter Your Three Favorite Movies')
        movie_1 = st.selectbox('First Option', title_list[:5000])
        movie_2 = st.selectbox('Second Option', title_list[5000:10000])
        movie_3 = st.selectbox('Third Option', title_list[10000:])
        fav_movies = [movie_1, movie_2, movie_3]

        # Perform top-10 movie recommendation generation
        if sys == 'Content Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = content_model(movie_list=fav_movies,
                                                            top_n=10)
                    st.title("We think you'll like:")
                    for i, j in enumerate(top_recommendations):
                        st.subheader(str(i + 1) + '. ' + j)
                except:
                    st.error("Oops! Looks like this algorithm doesn't work.\
                              We'll need to fix it!")

        if sys == 'Collaborative Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = collab_model(movie_list=fav_movies,
                                                           top_n=10)
                    st.title("We think you'll like:")
                    for i, j in enumerate(top_recommendations):
                        st.subheader(str(i + 1) + '. ' + j)
                except:
                    st.error("Oops! Looks like this algorithm doesn't work.\
                              We'll need to fix it!")

    # -------------------------------------------------------------------
    # ------------- SAFE FOR ALTERING/EXTENSION -------------------
    if page_selection == "Solution Overview":
        st.title("Solution Overview")

        file = 'Movie-Recommender-System/resources/markdown/solution_overview.txt'
        with open(file, 'r') as f:
            text = f.read()

        st.markdown("<h3 style='text-align: center;'>Thought process</h3>", unsafe_allow_html=True)
        st.markdown(f"<p align='justify'>{text}</p>", unsafe_allow_html=True)

    if page_selection == "About The Data":
        st.title("About The Project")

        file = 'Movie-Recommender-System/resources/markdown/about_project.txt'
        with open(file, 'r') as f:
            text = f.read()

        st.markdown("<h3 style='text-align: center;'></h3>", unsafe_allow_html=True)
        st.markdown(f"<p align='justify'>{text}</p>", unsafe_allow_html=True)

        if st.checkbox("Rating"):
            st.subheader("Movie Ratings Table")
            st.image('Movie-Recommender-System/resources/imgs/train.png')

        if st.checkbox("Movies"):
            st.subheader("Movies Table")
            st.image('Movie-Recommender-System/resources/imgs/movie.png', use_column_width=True)

        if st.checkbox("Genome Score"):
            st.subheader("Scores Table")
            st.image('Movie-Recommender-System/resources/imgs/genome_scores.png')

        if st.checkbox("Genome Tags"):
            st.subheader("Score Tag Mappings")
            st.image('Movie-Recommender-System/resources/imgs/genome_tags.png')

        if st.checkbox("IMDB"):
            st.subheader("IMDB Movies")
            st.image('Movie-Recommender-System/resources/imgs/imdb.png')

        if st.checkbox("Links"):
            st.subheader("IMDB and TMDB maps")
            st.image('Movie-Recommender-System/resources/imgs/links.png', use_column_width=True)

        if st.checkbox("Tags"):
            st.subheader("User Assigned Tags")
            st.image('Movie-Recommender-System/resources/imgs/tags.png', use_column_width=True)

    if page_selection == "Select Movie By Genre and Year":
        choices = ['By Genre', 'By Release Year']

        st.title("How Would You Like to Select a Movie")
        selecter = st.radio('', choices)

        if selecter == 'By Genre':
            st.header("View Movies By Genres")

            st.write('To show The movies available by their genre type\
                please use the dropdown below to specify the movie\
                    type you would love to watch.')
            selector = st.selectbox('Select Genre', genre_list)
            if st.button("Show Movies"):
                result_list = get_movie_names(movie, selector)

                st.subheader("These are The Movies That have {} as part of it's Genres".format(selector))
                for i, j in enumerate(result_list):
                    st.write(str(i + 1) + '. ' + j)

        if selecter == 'By Release Year':
            st.header("View Movies By Release Year")

            st.write('Select the year from the select box\
                to see the movies released in that year')
            selector = st.selectbox('Select Genre', years)
            if st.button("Show Movies"):
                result_list = genre_data[genre_data['year'] == selector]['title'].to_list()
                st.subheader("These are The Movies That were released in {}".format(selector))
                for i, j in enumerate(result_list):
                    st.write(str(i + 1) + '. ' + j)

    if page_selection == "Visuals":
        st.title("Exploring The Data with Plots and visuals")

        if st.checkbox("Ratings Proportions"):
            st.subheader("Proportion of Ratings in Dataset")
            st.image('Movie-Recommender-System/resources/imgs/eda/rating_proportion.png')

        if st.checkbox("Movies Budget Ranking"):
            st.subheader("Budget Rankings")
            st.image('Movie-Recommender-System/resources/imgs/eda/budget.png')

        if st.checkbox("Genres in the Dataset"):
            st.subheader("Genres")
            st.image('Movie-Recommender-System/resources/imgs/eda/genres_distribution.png')

    html_template = """
    <div style="background-color:orange;padding:5px;border-radius:500px;margin:5px;">
    <h1 style="color:black;text-align:center;">SIMUCC ANALYTICS</h1>
    <h2 style="color:blue;text-align:center;">Movie Recommender System</h2>
    </div>
    """

    if page_selection == "Landing Page":
        st.markdown(html_template, unsafe_allow_html=True)
        st.write('   ')
        st.image('Movie-Recommender-System/resources/imgs/landing_page.png', use_column_width=True)


if __name__ == '__main__':
    main()
