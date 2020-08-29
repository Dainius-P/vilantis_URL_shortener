# Vilantis URL shortener
> Implement a URL shortening service using Django in compliance with the requirements below.

## About The Project

Implement a URL shortening service using Django in compliance with the requirements below. Use any additional software necessary. DO NOT use any 3rd-party URL shortening services, APIs or libraries. Format your code according to the PEP8 recommendations (you are free to choose your own favourite line length though). Document the options you've considered, their trade-offs and your decisions in the Readme file. Upload your solution to a public repo on GitHub and send us a link to it.

### Built With
* [Bootstrap](https://getbootstrap.com)
* [Django](https://www.djangoproject.com/)
* [React](https://reactjs.org/)

## Getting Started

### Running

1. `docker-compose build`
1. `docker-compose up`
1. There should now be two servers running:
  - [http://localhost:8000](http://localhost:8000) Django APP
  - [http://localhost:3000/](http://localhost:3000/) React app

To run in detach mode, execute `docker-compose up` command in two steps:
- `docker-compose up --detach backend`
- `docker-compose up --detach frontend`

### Create SuperUser
To create a super user, execute this command:
```docker-compose run backend python manage.py createsuperuser```

### Admin page
`http://localhost:8000/admin/`

## Tests

To execute tests, we must enter this command:
`python manage.py test`

Or using docker compose:
`docker-compose run backend python manage.py test`

## Considered options for the solution

To generate the short URL I had to generate a unique, short ID that would allow me to determine to which long url does it belong. First idea was to use Django **UUIDField**, but it generates a 32 element string which is too long for this solution, although it would be completely unique. Then I tried using the **uuid** package. I would get the hex value and get only the first 8 characters, but I noticed that it uses only numbers and lower case letters which would come to **36^8** unique values. This might be enough but we can do better. So I decided to generate my own uniuqe ID. I took all of the ascii letters (lower case and upper case), joined them by 10 digits and got **62^8** unique values. The short URL ID can be shorter by one or two elements, if there would not be a lot of trafic.