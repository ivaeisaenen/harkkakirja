# harkkakirja

# Training log web application

User can create account and make training notes for example gym training.

Training log can be pricate or public.

Other user can view public logs and comment also.

Maybe follows and notifications if there is time for that kind of stuff

# Välipalautus 2

## DONE

1. Now you can make new user accounts and log in 

2. Add trainings and view trainings

## TODO

-Maybe short trainings by date

-Set trainings visible / hidden based user preference

-Search other people trainings

-Remove trainings

-Maybe if time add ability to follow someone and see their newest trainings in front page "feed"

-Maybe also if there is time some front page features shown in index.html like see top trending trainings (based on views/followers)

-Some security issues like CSRF haavoittuvuus lisäämällä:

--session["csrf_token"] = secrets.token_hex(16)

--<input type="hidden" name="csrf_token" value="{{ session.csrf_token }}">

--if session["csrf_token"] != request.form["csrf_token"]:

[Harkkakirja Heroku application](https://harkkakirja.herokuapp.com/)

