# HackPy
Hackpy is a Django-based web application that clones the functionality of Hacker News by periodically crawling data from the Hacker News website. The app includes user registration, login, link submission, voting, and a comments system with nested replies.

## Features

- Periodically crawls Hacker News to fetch the latest 30 news items and displays them on the homepage.
- Allows user registration and login.
- Users can post links through a simple form.
- Users can upvote or downvote any link posted on the website.
- The UI and data formatting resemble Hacker News, including humanized dates and displaying points and total comments.
- Clicking on the comments link opens a page showing both crawled comments and a form to add more comments, including nested replies.
- Supports markdown for posting comments.
- News is paginated and ordered similarly to Hacker News.
- Includes a search function for news, which can be implemented using Elasticsearch or full-text search in Postgres.
# Tech/framework used
- [Python](https://www.python.org/)
- [Django Rest Framework](https://www.django-rest-framework.org/)

# Installation
- Clone the code
- Install the requirements using pip install requirements.txt
- Run 'python3 manage.py runserver'

