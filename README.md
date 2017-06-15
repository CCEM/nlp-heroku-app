# Reddex [![Build Status](https://travis-ci.org/CCEM/nlp-heroku-app.svg?branch=master)](https://travis-ci.org/CCEM/nlp-heroku-app)
A Chrome extension for evaluating the tone of Reddit comments.


This project identifies and evaluates reddit comments for tone (positivity, negativity, and objectivity). We do this in two parts: a Chrome browser extension and a web application. Our extension will allow the user the option of evaluating each comment when they visit a reddit comment thread by clicking on the extension icon. The tone is represented by highlighting the background color with red for negative comments, green for positive, and grey for neutral. Particularly positive comments are a deeper green while the particularly negative comments are more red. By right clicking on the icon the user can find a link back to our web application, where they can see further information about the history of the pages that have been evaluated. Behind the scenes, our extension was built in HTML, CSS and JavaScript which passes the information to a Python server and database that parses the page text and returns information on the language tone. We are using an NLTK library called Vader for these evaluations. Our web app was built using the Pyramid framework.

![img](http://i.imgur.com/BYsqRDA.png)

## Development setup

Clone the repository.
```sh
  - git clone https://github.com/CCEM/nlp-heroku-app.git
  -cd nlp-heroku-app
```

Create and activate virtual environment(optional)

Install required packages including those for testing.
```sh
  - pip install -e reddex/.[testing]
```

Install required lexicons for NLTK.
```sh
  - python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('subjectivity'); nltk.download('punkt')"
```
#### Testing

Assuming Postgres is installed, create the database.
```sh
createdb test_reddexdb
```

Change to working directory and run tests.
```sh
cd reddex
py.test reddex/tests.py --cov=reddex --cov-report term-missing
```


## Release History

* 0.1.0
    * The first proper release
    * CHANGE: Production Ready
* 0.0.1
    * Work in progress

## Meta

- W-Ely Paysinger – [https://github.com/W-Ely/github-link](https://github.com/W-Ely) – paysinger@gmail.com
- Morgan Nomura – [https://github.com/morganelle/github-link](https://github.com/morganelle) – morganelle@gmail.com
- Chris Hudson – [https://github.com/CaHudson94/github-link](https://github.com/CaHudson94) – c.ahudson84@gmail.com
- Carlos Cadena – [https://github.com/carloscadena/github-link](https://github.com/carloscadena) – cs.cadena@gmail.com

Distributed under the MIT license. See ``LICENSE`` for more information.

## Contributing

1. Fork it (<https://github.com/CCEM/nlp-heroku-app/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
