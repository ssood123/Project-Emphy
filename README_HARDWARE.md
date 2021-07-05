# Emphy Overview
The hardware for Emphy consists of three different components:
1. The OpenBot car
2. Raspberry pi
3. Leash. 

## OpenBot Car
The hardware design for our final prototype was taken directly from the [OpenBot GitHub](https://github.com/intel-isl/OpenBot/tree/master). This design includes 4 different 3D printed parts for the chassis as shown below. The cad designs and STL files for 3D printing can be found on the OpenBot Github under [body](https://github.com/intel-isl/OpenBot/tree/master/body). While we stuck with the basic design, it can be edited to include space to place a raspberry pi and its power source within the insides of the chassis as well as a mounting point for the leash. 
The design for OpenBot is shown below. It consists on 3D printed parts and off the shelf hardware and electronics which can all be bought online. The complete list of parts required for this car can be found [here](https://github.com/intel-isl/OpenBot/tree/master/body). 

![Assembly](/Images/assembly.gif)

The wiring and components images for the car below are taken from the OpenBot github.

<img src="https://github.com/ssood123/Senior-Design-Project/blob/main/Images/wiring_diagram.png" width=800>
<img src="https://github.com/BostonUniversitySeniorDesign/21-07-Emphy/blob/main/Images/diy_parts.jpg" width=400, align=left>
<img src="https://github.com/BostonUniversitySeniorDesign/21-07-Emphy/blob/main/Images/chassis_motors_pcb.jpg" width=400>

When assembling this robot ourselves using an arduino nano and not a custom pcb, the complexity of the internal wiring and the assembeled OpenBot is shown below. This still requires the leash and Raspberry pi to be added which are discussed later.

<img src="https://github.com/BostonUniversitySeniorDesign/21-07-Emphy/blob/main/Images/internal_wiring.jpg" width=600>
<img src="https://github.com/BostonUniversitySeniorDesign/21-07-Emphy/blob/main/Images/OpenBot.jpeg" width=400, align=left>
<img src="https://github.com/BostonUniversitySeniorDesign/21-07-Emphy/blob/main/Images/OpenBot2.jpg" width=400>

## Raspberry Pi 4B
To control the OpenBot robot, we use a raspberry pi 4B which can communicate with the OpenBot application. There are no special instructions needed for the raspberry pi setup and previous version of raspberry pi with Wifi capabilites should be capable of running the [Emphy.py](https://github.com/BostonUniversitySeniorDesign/21-07-Emphy/blob/main/Emphy-OpenBot/Emphy.py) python script on them. The leash is connected to the raspberry pi through hardware pins and a USB headset which acts as a speaker and mic is connected to the Raspberry pi. The assembly of the leash is described below while the Headset can be any regular [headset](https://www.bestbuy.com/site/insignia-on-ear-analog-mono-headset-black/5648055.p?skuId=5648055&ref=212&loc=1&extStoreId=255&ref=212&loc=1&gclid=Cj0KCQjw1a6EBhC0ARIsAOiTkrFK7XOMFXgLlLK9GqeRjYn7O9K_r8CUJ2avU9n8J9X4e5O-lFOnPGkaAkSpEALw_wcB&gclsrc=aw.ds). The headset needs to be correctly set up which is described in the software readme file and in the future, can possibly be replaced with a bluetooth headset. The raspberry pi is attached to the car body as shown below. Changes to the 3D printed body can allow for the Pi and the battery pack to be stored within the body.

<img src="https://github.com/BostonUniversitySeniorDesign/21-07-Emphy/blob/main/Images/latest1.jpg" width=400, align=left>
<img src="https://github.com/BostonUniversitySeniorDesign/21-07-Emphy/blob/main/Images/latest2.jpg" width=400>
<img src="https://github.com/BostonUniversitySeniorDesign/21-07-Emphy/blob/main/Images/OpenBot3.jpeg" width=400, align=left>
<img src="https://github.com/BostonUniversitySeniorDesign/21-07-Emphy/blob/main/Images/latest4.jpg" width=400>

### Leash Box
The purpose of the leash is to establish a way for the user to communicate with Emphy as well as a way for the car to communicate back to the user, through haptic feedback implemented on the leash as well as audio output through the Headset. The leash consists of two vibration motors on the left and right of the leash to indicate where the car will turn. There are also two buttons on the top of the leash, one to pause the robot in its track and the other to stop the robot from continuing on the current path and to ask the user again for a new destination. These components are then connected to the raspberry pi over a long wire which also acts as a leash for the user to hold. The 3D printed box acts as a handle for the user.
The CAD files inside LeashBox folder is for the box attached to the leash. They are in stl format and can be used to 3D printed the box. The box’s dimension is 12x6x3 cm. The lid has two identical parts. On the lid there are two holes for the buttons and four holes on the corner which are placed for the screws to connect the lid and the box body. The box has two holes on the sides for vibration motor and a hole on the front for the wire to go through.
The CAD is done using onShape.

<img src="https://github.com/BostonUniversitySeniorDesign/21-07-Emphy/blob/main/Images/leash.jpeg" width=400>
<img src="https://github.com/BostonUniversitySeniorDesign/21-07-Emphy/blob/main/Images/Leash_diagram.png" width=400>
