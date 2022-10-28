The YaMDb project collects user reviews of works. 
With this project, you can:
- send text reviews for the works 
- rate the work
- comment on other users' reviews
- get a list of all works, categories, genres, comments, reviews
***
### Technologies
Yatube API uses open-source technologies:
- Python 3.7 https://www.python.org/downloads/release/python-379 
- Django REST framework 3.12 https://www.django-rest-framework.org/community/3.12-announcement 
- Simple JWT-authentication with implementation via confirmation code https://django-rest-framework-simplejwt.readthedocs.io/en/latest 
***
### Installation
- Clone the project
``
git clone 
``` 
- Install and activate the virtual environment
- Install requirements from the file requirements.txt
``
pip install -r requirements.txt
`` 
- In the file folder manage.py run the command:
`` python
Query examples and result
```
GET http://127.0.0.1:8000/api/v1/categories /
[
{
"quantity": 2,
"next": null,
"previous": null,
"results": [
{
"name": "Title",
"slug": "Title"
},
{
"name": "Music",
"slug": "music"
},
{
"name": "Movie",
"slug": "movie"
}
]
}
]


GET http://127.0.0.1:8000/api/v1/genres/?search=Rock
[
{
"quantity": 2,
"next": null,
"previous": null,
"results": [
{
"title": "Metal",
"slug": "metal"
}
]
}
]
``

