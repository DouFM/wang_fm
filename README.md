# wang_fm

Refactor of [pmiao_fm](https://github.com/dccrazyboy/miao_fm)

## Depends

#### Software
1. Python 2.7.5
2. mongodb 2.4.8

#### Python Packages
1. Flask==0.10.1
2. Flask-RESTful==0.2.8
3. Flask-Script==0.6.6
4. mongoengine==0.8.6
5. requests==2.1.0
6. APScheduler==2.1.1

## Install
    # You need to install Python, pip, virtualenv, MongoDB first.
    virtualenv doufm
    cd doufm
    git clone https://github.com/DouFM/wang_fm
    pip install -r wang_fm/requirements.txt
    . bin/activate
    cd wang_fm
    python manager.py setup
    python manager.py auto_update  # Download demo music, this needs to be stopped manually
    python manager.py runserver

## Test
use [nose](https://nose.readthedocs.org/en/latest/) to test all.

run `nosetests -vv`

## manager.py

    usage: manager.py [-h]
                      {shell,enable_channel,update_channel_num,setup,runserver,channels,auto_update,tasks,disable_channel}
                      ...

#### Examples

1. use `./manager.py setup` to setup db.
2. use `./manager.py runserver` to run server. (This needs to keep running)
3. use `./manager.py tasks [-h] hour` to run tasks. (This needs to keep running)
