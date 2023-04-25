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

#### Step 1 - Download the Script:

To use the init.py script, the user needs to download it first. They can download the script from GitHub using the following command on the terminal:

```plaintext
git clone https://github.com/DARCOS-DZ/el-moadin-pi
```

This command downloads the script to the current working directory.

After the download process, the user needs to navigate to the downloaded folder using the following command:

```plaintext
cd el-moadin-pi/
```

#### Step 2 - Start init.py:

To start the init.py script, the user needs to run the following command on the terminal:

```plaintext
python3 init.py
```

This command runs the script and prompts the user to input some required data for the configuration of the app.

```plaintext
 _____ _  ___  ___                _ _        ______ _
|  ___| | |  \/  |               | (_)       | ___ (_)
| |__ | | | .  . | ___   __ _  __| |_ _ __   | |_/ /_
|  __|| | | |\/| |/ _ \ / _` |/ _` | | '_ \  |  __/| |
| |___| | | |  | | (_) | (_| | (_| | | | | | | |   | |
\____/|_| \_|  |_/\___/ \__,_|\__,_|_|_| |_| \_|   |_|

App for controlling mosques speakers with a mobile app with a cloud MQTT broker"""

Before you start make sure you have this informations :

- Mosque name
- The offset time of the mosque
- The home assistant address
- The home assistant token
- The home assistant entity_id of the switch

Do you have these informations [y/n] :
```

Type "y" if you have the informations.

#### Step 3 - Input Data:

After running the script, the user will see a logo and a message explaining the required data. The user needs to input the data as prompted by the script.

*   Mosque Name: The user needs to input the name of the mosque.

```plaintext
what is the name of this mosque ? : mosque_name
```

*   Offset Time: The user needs to input the offset time of the mosque in minutes. They can get this value from the prayer timetable of the mosque.

```plaintext
what is the offset time of this mosque ? : 1
```

*   Home Assistant Address: The user needs to input the address of the Home Assistant instance they want to use to control the app.

```plaintext
what is the homeassistant address of this mosque ? : http://localhost:8123
```

*   Home Assistant Token: The user needs to input the authentication token of the Home Assistant instance they want to use to control the app. They can get this value from the user profile section of the Home Assistant web interface.

```plaintext
what is the home assistant token of this mosque ? : abcdefghijklmnopqrstuvwxyz0123456789
```

*   Home Assistant Entity ID of the Switch: The user needs to input the entity ID of the Home Assistant switch they want to use to control the app. They can get this value from the entity registry section of the Home Assistant web interface.

```plaintext
what is the entity id of the switch of this mosque ? : switch.mosque_speaker
```

#### Step 4 - Installation Completed:

After the user inputs all the required data, the script will start installing the necessary dependencies and configuring the app. The user will see some output on the terminal indicating the progress of the installation process. If the installation process completes without errors, the user will see the following output:

```plaintext
Startup configuration is done
```

This output indicates that the installation process is complete, and the user can now use the app to control the mosque speakers.


## License

[![MIT License](https://img.shields.io/badge/MIT-Licence-green.svg)](https://choosealicense.com/licenses/mit/)
