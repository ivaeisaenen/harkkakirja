# harkkakirja

# Training log web application

User can create account and make training notes for example gym training.

Training log can be pricate or public.


# Välipalautus 3

## DONE

1. Now you can make new user accounts and log in 

2. Add trainings and view trainings

3. Reorganized whole code to separate python files

4. Changed html so that text is inside header or paragraph tags

5. Timestamps for user and trainings works now

## TODO

-Set trainings visible / hidden based user preference

-Remove trainings

-Some security issues like CSRF haavoittuvuus lisäämällä:

--session["csrf_token"] = secrets.token_hex(16)

--<input type="hidden" name="csrf_token" value="{{ session.csrf_token }}">

--if session["csrf_token"] != request.form["csrf_token"]:

[Harkkakirja Heroku application](https://harkkakirja.herokuapp.com/)

