# El Moadin Pi
A Raspberry pi client to control the mosque speakers via an MQTT broker, a REST API and a Flutter application

## Features

- Auto schedule call to prayer.
- Receiving & publishing custom call to prayer audio recorded files.
- Receiving & publishing prayer events (audio records to put before or after a prayer).
- Receiving & publishing live recorded audio events.

## Tech

El Moadin Pi uses a number of open source projects to work properly:

- [Django](https://www.djangoproject.com/)
- [Paho MQTT](https://www.eclipse.org/paho/)
- [PM2](https://www.npmjs.com/package/pm2)
- [Pygame](https://www.pygame.org/news)
- [Django Crontab](https://github.com/kraiz/django-crontab)
- [Django 4 Background Tasks](https://github.com/meneses-pt/django-background-tasks)
- [Background](https://github.com/kennethreitz/background)
- [Django constance](https://github.com/jazzband/django-constance/blob/master/docs/index.rst)

## Installation

For a quick install, use the init.py script on a fresh Raspberry Pi.

First download the source code.

```sh
git clone https://github.com/DARCOS-DZ/el-moadin-pi
```

The cd to the repo.

```sh
cd el-moadin-pi/
```

Start the installation with:

```sh
python3 init.py
```

```sh
 _____ _  ___  ___                _ _        ______ _
|  ___| | |  \/  |               | (_)       | ___ (_)
| |__ | | | .  . | ___   __ _  __| |_ _ __   | |_/ /_
|  __|| | | |\/| |/ _ \ / _` |/ _` | | '_ \  |  __/| |
| |___| | | |  | | (_) | (_| | (_| | | | | | | |   | |
\____/|_| \_|  |_/\___/ \__,_|\__,_|_|_| |_| \_|   |_|

App for controlling mosques speakers with a mobile app with a cloud MQTT broker

Before you start make sure you have this informations :

- Mosque name
- The offset time of the mosque

Do you have these informations [y/n] :

```
Type "y" if you have the informations.

```sh
Please answer to the following questions to init your Raspberry pi

what is the name of this mosque ? : Mosque name

what is the offset time of this mosque ? : 1
```
Put the required information and the script will automatically install OS dependencies, create virtual environment, install python dependencies, set the mosque name, set the offset time, migrate the database, start pm2 process, set pm2 startup settings for auto start when the raspberry pie is rebooted.

## License

[![MIT License](https://img.shields.io/badge/MIT-Licence-green.svg)](https://choosealicense.com/licenses/mit/)
