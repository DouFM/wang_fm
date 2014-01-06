# wang_fm

refactor of miao_fm

## Depends

### Software
1. Python 2.7.5
2. mongodb 2.4.8

### Python Packages
1. Flask==0.10.1
2. Flask-RESTful==0.2.8
3. Flask-Script==0.6.6
4. mongoengine==0.8.6
5. requests==2.1.0
6. APScheduler==2.1.1

## Test
use [nose](https://nose.readthedocs.org/en/latest/) to test all.

run `nosetests -vv`

## manager.py

1. use `./manager.py setup` to setup db.
2. use `./manager.py runserver` to run server.(this needs to keep running)
3. use `./manager.py tasks` to run tasks.(this needs to keep running)
