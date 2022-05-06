import psutil, time, json
from phue import Bridge #https://github.com/studioimaginaire/phue


battery_max_charge = 80
battery_min_charge = 50
hue_bridge = "10.1.0.151"
hue_device = 14

b = Bridge(hue_bridge)

b.connect()
dict = b.get_api()


#This code can be used to find which device you wish to control
for item in dict:
    if item == "lights":
        for device in dict[item]: 
            print(device)#Here we print what is the ID of the light/plug
            for data in dict[item][device]:
                if data == "name":
                    print(dict[item][device][data])# Here we print the name of the light/plug
                    print("\n")
                    
b.set_light(hue_device,'on', True)


def check_charge_status():
    #This function gets whether the device is plugged in and what battery percentage
    global battery, plugged, percent
    battery = psutil.sensors_battery()
    plugged = battery.power_plugged
    percent = str(battery.percent)



while True:

    check_charge_status()

    #Here we detect if the laptop is setup to charge
    #if plugged == True:

        #If so shoud charging be stopped
    if battery.percent >= battery_max_charge:

        print("charged too much!")
        #shut off charging
        while battery.percent > battery_min_charge:
            check_charge_status()
            print(percent)
            time.sleep(60)





    time.sleep(60)
