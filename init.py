import subprocess
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCMAGENTA = '\033[1;35m'
    OKGREEN = '\033[1;32m'
    WARNING = '\033[1;33m'
    FAIL = '\033[1;31m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
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
- Mqtt broker ip address
- Local HomeAssistant ip address
"""

print(bcolors.BOLD + bcolors.CYAN  + logo + bcolors.ENDC)
time.sleep(1)
print(bcolors.BOLD + bcolors.CYAN + message + bcolors.ENDC)


os_dependencies = ["virtualenv", "npm"]

def os_installer(dependencies):
    for app in dependencies:
        print("\n" +bcolors.BOLD + bcolors.CYAN + f"Installing {app} ..." + bcolors.ENDC + "\n")
        command = "sudo apt-get install {} -y".format(str(app))
        subprocess.call(command, shell=True)
        print("\n" +bcolors.BOLD + bcolors.OKGREEN + f"{app} installed successfully" + bcolors.ENDC + "\n")
        time.sleep(1)

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

def set_config(mosque, offset_time, broker_ip=None, home_assistant=None):
    command = f'''source env/bin/activate ;
    ./manage.py constance set mosque "{mosque}";
    ./manage.py constance set offset_time {offset_time};
    '''
    subprocess.call(command, shell=True, executable='/bin/bash')
    if broker_ip != None :
        command = f'''source env/bin/activate ;
        ./manage.py constance set broker_ip "{broker_ip}";
        '''
        subprocess.call(command, shell=True, executable='/bin/bash')
    if home_assistant != None :
        command = 'pm2 startup'
        subprocess.call(command, shell=True, executable='/bin/bash')

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


answer = None

while answer not in ("y", "n"):
    answer = input(bcolors.BOLD + bcolors.WHITE + "Do you have these informations [y/n] : " + bcolors.ENDC)
    if answer.lower() == "y":

        print("\n" + bcolors.BOLD + bcolors.CYAN + "Please answer to the following questions to init your Raspberry pi" + bcolors.ENDC)

        mosque = input(bcolors.BOLD + bcolors.WHITE + "\nwhat is the name of this mosque ? : " + bcolors.ENDC)
        offset_time = input(bcolors.BOLD + bcolors.WHITE + "\nwhat is the offset time of this mosque ? : "+ bcolors.ENDC)
        broker_ip = input(bcolors.BOLD + bcolors.WHITE + "\nwhat is the broker address ? : " + bcolors.ENDC)
        home_assistant = input(bcolors.BOLD + bcolors.WHITE + "\nwhat is the HomeAssistant address ? : " + bcolors.ENDC)

        print("\n" + bcolors.BOLD + bcolors.CYAN + "We will install the os dependencies, enter your sudo password" + bcolors.ENDC)
        os_installer(dependencies=os_dependencies)
        pm2_installer()
        env_init()
        pm2_services()
        set_config(mosque=mosque, offset_time=offset_time)
        pm2_startup_conf()
        break
    elif answer.lower() == "n":
        break
    else:
        print("\n" + bcolors.BOLD + bcolors.FAIL + "Please enter y or n." + bcolors.ENDC + "\n")
