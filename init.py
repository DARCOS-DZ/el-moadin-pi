import subprocess
import time

class bcolors:
    OKGREEN = '\033[1;32m'
    FAIL = '\033[1;31m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    CYAN = '\033[1;36m'
    WHITE = '\033[1;37m'

logo = """
 _____ _  ___  ___                _ _        ______ _
|  ___| | |  \/  |               | (_)       | ___ (_)
| |__ | | | .  . | ___   __ _  __| |_ _ __   | |_/ /_
|  __|| | | |\/| |/ _ \ / _` |/ _` | | '_ \  |  __/| |
| |___| | | |  | | (_) | (_| | (_| | | | | | | |   | |
\____/|_| \_|  |_/\___/ \__,_|\__,_|_|_| |_| \_|   |_|

App for controlling mosques speakers with a mobile app with a cloud MQTT broker"""

message = """
Before you start make sure you have this informations :

- Mosque name
- The offset time of the mosque
- The home assistant address
- The home assistant token
- The home assistant entity_id of the switch
""" # + - Mqtt broker ip address
# - Local HomeAssistant ip address
# """

print(bcolors.BOLD + bcolors.CYAN  + logo + bcolors.ENDC)
time.sleep(1)
print(bcolors.BOLD + bcolors.CYAN + message + bcolors.ENDC)


os_dependencies = ["virtualenv", "libsdl2-dev", "libsdl2-mixer-2.0-0", "libsdl2-image-2.0-0", "libsdl2-ttf-2.0-0", "npm"]

def os_installer(dependencies):
    for app in dependencies:
        print("\n" +bcolors.BOLD + bcolors.CYAN + f"Installing {app} ..." + bcolors.ENDC + "\n")
        command = "sudo apt install {} -y".format(str(app))
        subprocess.call(command, shell=True)
        print("\n" +bcolors.BOLD + bcolors.OKGREEN + f"{app} installed successfully" + bcolors.ENDC + "\n")
        time.sleep(1)
    command = "mkdir media ; mkdir media/prayer_event ; mkdir media/prayer_audio ; mkdir media/live_event ;".format(str(app))
    subprocess.call(command, shell=True)

def pm2_installer():
    print("\n" +bcolors.BOLD + bcolors.CYAN + "Installing PM2 ..." + bcolors.ENDC + "\n")
    command = "sudo npm install pm2 -g"
    subprocess.call(command, shell=True)
    print("\n" +bcolors.BOLD + bcolors.OKGREEN + "PM2 installed successfully" + bcolors.ENDC + "\n")
    time.sleep(1)

def env_init():
    command = "bash create_virtualenv.sh"
    subprocess.call(command, shell=True)

def pm2_services():
    command = 'pm2 start run_production.sh'
    subprocess.call(command, shell=True)
    command = 'pm2 start run_process_tasks.sh'
    subprocess.call(command, shell=True)

home_assistant_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIyZDg5NWQ1YjFlMzM0NTM0OTA3MTc1Y2I1Njc3Yjc3MCIsImlhdCI6MTY3NDQ4MDE1OCwiZXhwIjoxOTg5ODQwMTU4fQ.aIIt-N9wtMfUTw9petvp0Ve84VsFBZ72RPweQjX9XBw"
# set the default address
def set_config(mosque, offset_time, home_assistant_address="http://localhost:8123", home_assistant_token=home_assistant_token, entity_id="switch.plug_zigbee2_switch"):  #, broker_ip=None, home_assistant=None):
    command = f'''source env/bin/activate ;
    ./manage.py constance set mosque "{mosque}";
    ./manage.py constance set offset_time {offset_time};
    ./manage.py constance set home_assistant_address {home_assistant_address};
    ./manage.py constance set home_assistant_token {home_assistant_token};
    ./manage.py constance set entity_id {entity_id};
    '''
    subprocess.call(command, shell=True, executable='/bin/bash')
    # if broker_ip != None :
    #     command = f'''source env/bin/activate ;
    #     ./manage.py constance set broker_ip "{broker_ip}";
    #     '''
    #     subprocess.call(command, shell=True, executable='/bin/bash')
    # if home_assistant != None :
    #     command = 'pm2 startup'
    #     subprocess.call(command, shell=True, executable='/bin/bash')

def pm2_startup_conf():
    process = subprocess.Popen(
        "pm2 startup",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
        encoding='utf-8',
        errors='replace',
    )
    while True:
        realtime_output = process.stdout.readline()
        print(realtime_output)
        if realtime_output == '' and process.poll() is not None:
            break
        if realtime_output:
            output = realtime_output.strip()
            if "sudo" in output :
                command = output
                subprocess.call(command, shell=True, executable='/bin/bash')
                subprocess.call("pm2 save", shell=True, executable='/bin/bash')
                break

def migrate():
    command = "source env/bin/activate ; ./manage.py migrate"
    subprocess.call(command, shell=True, executable='/bin/bash')

answer = None

while answer not in ("y", "n"):
    answer = input(bcolors.BOLD + bcolors.WHITE + "Do you have these informations [y/n] : " + bcolors.ENDC)
    if answer.lower() == "y":

        print("\n" + bcolors.BOLD + bcolors.CYAN + "Please answer to the following questions to init your Raspberry pi" + bcolors.ENDC)
        mosque = input(bcolors.BOLD + bcolors.WHITE + "\nwhat is the name of this mosque ? : " + bcolors.ENDC)
        offset_time = int(input(bcolors.BOLD + bcolors.WHITE + "\nwhat is the offset time of this mosque ? : "+ bcolors.ENDC))
        home_assistant_address = input(bcolors.BOLD + bcolors.WHITE + "\nwhat is the homeassistant address of this mosque ? : "+ bcolors.ENDC)
        home_assistant_token = input(bcolors.BOLD + bcolors.WHITE + "\nwhat is the home assistant token of this mosque ? : "+ bcolors.ENDC)
        entity_id = input(bcolors.BOLD + bcolors.WHITE + "\nwhat is the entity id of the switch of this mosque ? : "+ bcolors.ENDC)
        # broker_ip = input(bcolors.BOLD + bcolors.WHITE + "\nwhat is the broker address ? : " + bcolors.ENDC)
        # home_assistant = input(bcolors.BOLD + bcolors.WHITE + "\nwhat is the HomeAssistant address ? : " + bcolors.ENDC)

        try:
            print("\n" + bcolors.BOLD + bcolors.CYAN + "We will install the os dependencies, enter your sudo password" + bcolors.ENDC)
            os_installer(dependencies=os_dependencies)
        except Exception as e:
            print("\n" + bcolors.BOLD + bcolors.FAIL + "Dependencies error" + bcolors.ENDC + "\n")
            break
        try:
            pm2_installer()
        except Exception as e:
            print("\n" + bcolors.BOLD + bcolors.FAIL + "PM2 Installation error" + bcolors.ENDC + "\n")
            break
        try:
            print("\n" + bcolors.BOLD + bcolors.CYAN + "Creating virtual environement & installing pip dependencies ..." + bcolors.ENDC)
            env_init()
            print("\n" +bcolors.BOLD + bcolors.OKGREEN + "Virtual environement & installing pip dependencies are installed successfully" + bcolors.ENDC + "\n")
        except Exception as e:
            print("\n" + bcolors.BOLD + bcolors.FAIL + "Virtual environement Installation error" + bcolors.ENDC + "\n")
            break
        try:
            print("\n" + bcolors.BOLD + bcolors.CYAN + "Migrating the database ..." + bcolors.ENDC)
            migrate()
            print("\n" +bcolors.BOLD + bcolors.OKGREEN + "Database migrated successfully" + bcolors.ENDC + "\n")
        except Exception as e:
            print("\n" + bcolors.BOLD + bcolors.FAIL + "Database migration error" + bcolors.ENDC + "\n")
            break
        try:
            print("\n" + bcolors.BOLD + bcolors.CYAN + "Starting pm2 jobs ..." + bcolors.ENDC)
            pm2_services()
            print("\n" +bcolors.BOLD + bcolors.OKGREEN + "pm2 jobs started successfully" + bcolors.ENDC + "\n")
        except Exception as e:
            print("\n" + bcolors.BOLD + bcolors.FAIL + "pm2 jobs error" + bcolors.ENDC + "\n")
            break
        try:
            print("\n" + bcolors.BOLD + bcolors.CYAN + "Updating the settings ..." + bcolors.ENDC)
            set_config(mosque=mosque, offset_time=offset_time, home_assistant_address=home_assistant_address, home_assistant_token=home_assistant_token, entity_id=entity_id)
            print("\n" +bcolors.BOLD + bcolors.OKGREEN + "Settings updated successfully" + bcolors.ENDC + "\n")
        except Exception as e:
            print("\n" + bcolors.BOLD + bcolors.FAIL + "Updating settings error" + bcolors.ENDC + "\n")
            break
        try:
            print("\n" + bcolors.BOLD + bcolors.CYAN + "Creating pm2 startup conf ..." + bcolors.ENDC)
            pm2_startup_conf()
            print("\n" +bcolors.BOLD + bcolors.OKGREEN + "Startup configuration is done" + bcolors.ENDC + "\n")
            break
        except Exception as e:
            print("\n" + bcolors.BOLD + bcolors.FAIL + "Startup configuration error" + bcolors.ENDC + "\n")
            break

    elif answer.lower() == "n":
        break
    else:
        print("\n" + bcolors.BOLD + bcolors.FAIL + "Please enter y or n." + bcolors.ENDC + "\n")
