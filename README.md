# Unicorn HAT HD: Various Animations, Displays and Text
Python Script for Pimoroni's Unicorn HAT HD

### Randomly display/shows one of the following:

1. Displays zzzZ during a certain time of the day. Sleep-Mode, if you will.

2. Displays the Aperture Science Logo, from the videogame Portal, cycling through the HSV colour spectrum.

3. Rainbow-coloured scrolltext.

4. Displays the Aperture Science Logo, from the videogame Portal, in animated rainbow colours, with sound.

5. A relaxing ingle, with sound.

6. CPU Temperature in °C, rainbow coloured unless temperatures exceed 55°C. Should the temperature rise above 55°C, it's displayed in red and an alarm sound is played.

### NOTICE:

### You need to provide HeatAlarm.off, fire.ogg, Still_Alive_Radio.ogg YOURSELF!


Should you want to customize the rainbow coloured text, check out TEXT1 and change it to your heart's desire. Also check out FONT1 if you want to change the font used.

Also has some variables built-in, in case you want to keep track of how many times certain parts of this script have been called. Simply look for any line with a "#Uncomment if you want to keep track of how many times this part was executed" and uncomment it, as well as the corresponding lines at the very bottom of the script, which will print them when you exit.


If you can't start the script, remember to 
```bash
sudo chmod +x aperture_party_zzzzz.py```
