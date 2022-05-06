import psutil, time, yaml, pathlib  # https://pypi.org/project/PyYAML/
from phue import Bridge #https://github.com/studioimaginaire/phue
from datetime import datetime



def log(text):
    dt_string = datetime.now().strftime("%Y/%m/%d/, %H:%M:%S ")
    with open("log.txt", "a+") as file: #open's the file to allow it to be written to
        file.write(dt_string + " -- " + text + "\n")# writes to log new startup, includes date/time

log("Startup")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~VERYIFY IF CONFIG FILE EXISTS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if pathlib.Path("config.txt").is_file():
    pass
else:
    with open("config.txt", "w") as file: # Open the file as read
        print("Cannot find file")
        log("Unable to find config file")
        pass
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~LOAD CONFIG~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
with open("config.txt") as file: # Open the file as read
    config_file = yaml.load(file, Loader=yaml.FullLoader) # Set the contents to = tmp_current_dictionary

for key, value in config_file.items():
    if key == "battery_max_charge":
        if value == None:
            battery_max_charge = 80
        else:
            battery_max_charge = value
    if key == "battery_min_charge":
        if value == None:
            battery_min_charge = 50
        else:
            battery_min_charge = value
    if key == "hue_bridge": 
        if value == None:
            hue_bridge = None
            print("No Hue Bridge configured")
            log("No Hue Bridge configured")
        else:
            hue_bridge = value 
    if key == "hue_plug":
        if value == None:
            hue_plug = None
            print("No Hue Plug configured")
            log("No Hue Plug configured")
        else:
            hue_plug = value

log("battery_max_charge = " + str(battery_max_charge))
log("battery_min_charge = " + str(battery_min_charge))
log("hue_bridge = " + str(hue_bridge))
log("hue_plug = " + str(hue_plug))
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~CONNECT TO HUE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
hue_bridge = Bridge(hue_bridge)

hue_bridge.connect()
dict = hue_bridge.get_api()

hue_array = []

#This code can be used to find which device you wish to control
for item in dict:
    if item == "lights":
        for device in dict[item]: 
            #print(device)#Here we print what is the ID of the light/plug
            for data in dict[item][device]:
                if data == "name":
                    #print(dict[item][device][data])# Here we print the name of the light/plug
                    #print("\n")
                    hue_array.append((device,dict[item][device][data]))

with open("hue.txt", "w") as file: #open's the file to allow it to be written to
    for item in hue_array:
        file.write(str(item) + "\n")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Get Charge Status~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def check_charge_status():
    #This function gets whether the device is plugged in and what battery percentage
    global battery, plugged, percent
    battery = psutil.sensors_battery()
    plugged = battery.power_plugged
    percent = str(battery.percent)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
while True:

    check_charge_status()

    #Here we detect if the laptop is setup to charge
    if plugged == True:
        hue_bridge.set_light(hue_plug,'on', True)# We set the defualt mode of the hue plug to on

        #If so shoud charging be stopped
        if battery.percent >= battery_max_charge:

            print("charged too much!")
            #shut off charging
            hue_bridge.set_light(hue_plug,'on', False)
            while battery.percent > battery_min_charge:
                check_charge_status()
                print(percent)               

                time.sleep(60)





    time.sleep(60)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~