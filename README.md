# LaptopPower
 
This Project aims to preserve battery life of Laptops that are allways plugged in.

Using the Philiips hue smart plug, this client connects to the hue api to disable or enable power to the device when between set battery percentages.


Firstly navigate to the directory where you have downloaded the files, unzip them if necesery, then in CLI (being sure that the directory is where you downloaded the files)
Run: pip install -r requirements.txt

Then configure the IP address of your hue bridge in the config.txt, being sure to save the file.

To use, press the button on your hue bridge then within 30 seconds run the client.py

In Hue.txt you will see a list of the ID's and names of your Hue devices.

Locate the device you wish to use, then copy the ID to the config.txt and overwrite the value of hue_plug 

