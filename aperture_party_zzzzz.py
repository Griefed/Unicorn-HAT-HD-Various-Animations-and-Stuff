#!/usr/bin/env python

from random import randrange
import colorsys
import time
import numpy
import unicornhathd
import math
import datetime
import itertools
from PIL import Image, ImageDraw, ImageFont
import pygame
from gpiozero import CPUTemperature

degree_sign = u'\N{DEGREE SIGN}'

print("Unicorn HAT HD: Various Animations")
print(" ")
print("Displays zZzZ during a certain time of the day.")
print("The Aperture Science logo from Portal, cycling through the HSV colour spectrum.")
print("Rainbow-Coloured scrolltext. Text can be customized.")
print("The Aperture Science logo from Portal, lit by an animated rainbow, with sound.")
print("A relaxing ingle, with sound")
print("Rainbow-Coloured CPU Temperature. Warns you if the temperature exceeds 55"+degree_sign+"C")
print("""
Press Ctrl+C to exit!
""")

def time_in_range(start, end, x):
	if start <= end:
		return start <= x <= end
	else:
		return start <= x or x <= end

zzzz = [[1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
	[0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
	[1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
	[0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0],
	[0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
	[0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1],
	[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
	[0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
	[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
	[1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
	[0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0],
	[0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0],
	[1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]]

aperture = [[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
         [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0],
         [0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0],
         [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
         [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
         [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
         [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
         [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
         [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
         [0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0],
         [0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0],
         [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]]

pygame.mixer.pre_init(44100, -16, 2, 2048) #Pre-Initialize pygame and mixer BEFORE any sound is loaded or played
pygame.init()

#Everything related to the rainbow text:
TEXT1 = 'Von der Erde bis zum Ende des Universums. Vom Ende des Universums bis zur Erde.' #Enter your text here!
FONT1 = ('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 12) #Which Font to use
width, height = unicornhathd.get_shape() #Also used by switch == 3
text1_x = 1
text1_y = 1
font_file1, font_size1 = FONT1
font1 = ImageFont.truetype(font_file1, font_size1)
text1_width, text1_height = font1.getsize(TEXT1)
text1_width += width + text1_x
image1 = Image.new('RGB', (text1_width, max(height, text1_height)), (0, 0, 0))
draw1 = ImageDraw.Draw(image1)
draw1.text((text1_x, text1_y), TEXT1, fill=(255, 255, 255), font=font1)

#Everything related to displaying the CPU Temperature
FONT2 = ('/usr/share/fonts/truetype/piboto/PibotoCondensed-Regular.ttf', 12)
text2_x = 0
text2_y = 0
font_file2, font_size2 = FONT2
font2 = ImageFont.truetype(font_file2, font_size2)
degree_sign = u'\N{DEGREE SIGN}'
HeatAlarm = pygame.mixer.Sound("/home/pi/Pimoroni/unicornhathd/examples/HeatAlarm.ogg")

#Which image to open in case switch == 3
img = Image.open('/home/pi/Pimoroni/unicornhathd/examples/fire_layer_1_flat.png')
fire = pygame.mixer.Sound("/home/pi/Pimoroni/unicornhathd/examples/fire.ogg")

#Everyhting related to the zzzz displayed only during certain times of a day:
start = datetime.time(22, 0, 0)	#Start time at which the zzzz will be displayed, in Hours, Minutes, Seconds. (24, 0, 0 does NOT work)
end = datetime.time(8, 0, 0)	#End time at which normal operation will be resumed, in Hours, Minues, Secons
zzzz = numpy.array(zzzz)
rising = range(1, 10, 1)
ba = range(10, 5, -1)
dum = range(5, 10, 1)
falling = range(10, 0, -1)
pattern = (rising, ba, dum, falling)
brightness_levels = list(itertools.chain.from_iterable(pattern))

#Everything relating to the Aperture Logo
step = 0
aperture = numpy.array(aperture)
still_alive_radio = pygame.mixer.Sound("/home/pi/Pimoroni/unicornhathd/examples/Still_Alive_Radio_Loop.ogg")

#For keeping track of how many times certain parts were executed. Uncomment wanted parts below.
zZzZ = 0	#For zzzz
ASScroll = 0	#For Aperture Science Logo HSV colour scroll
ASRainbow = 0	#For Aperture Science Logo Rainbow animation
RainbowText = 0 #For Rainbow coloured scrolltext
ShowImg = 0	#For displaying an img
cputemp = 0	#For displaying the CPU Temperature

try:
	while True:
		unicornhathd.rotation(0)
		unicornhathd.brightness(0.3)
		cpu = CPUTemperature()
		x = datetime.datetime.now().time()
		if time_in_range(start, end, x) and cpu.temperature < 55: #Only executed if the time is right AND the CPU Temperature is below 55 Degrees Celsius
			#zZzZ += 1 #Uncomment if you want to keep track of how many times this was executed
			unicornhathd.brightness(0.1)
			for level in brightness_levels:	#zzzz displayed during certain times of the day
				for x in range(16):
					for y in range(16):
						h = 0.5
						s = 1.0
						v = zzzz[x, y] * float(level) / 10
						r, g, b = colorsys.hsv_to_rgb(h, s, v)
						red = int(r * 255.0)
						green = int(g * 255.0)
						blue = int(b * 255.0)
						unicornhathd.set_pixel(x, y, red, green, blue)
					unicornhathd.show()
					time.sleep(0.005)
				time.sleep(0.8)

		else:
			switch = randrange(5)
			if cpu.temperature >= 55: #If the CPU Temperature exceeds 55 Degrees Celsius, go directly to the part where the temperature is displayed and the alarm sound is played.
				switch = 4
			else:
				if switch == 0:
					#ASScroll += 1 #Uncomment if you want to keep track of how many times this part was executed
					for hue in range(3600): #Aperture Logo which slowly scrolls through the hsv colourwheel
						for x in range(16):
							for y in range(16):
								h = hue/3600.0
								v = aperture[x, y]
								r, g, b = colorsys.hsv_to_rgb(h, 1, v)
								r *= 255.0
								g *= 255.0
								b *= 255.0
								unicornhathd.set_pixel(x, y, r, g, b)
						unicornhathd.show()
						#time.sleep(1)
						#if hue == 1337:
							#print("leet")
						#print(hue, "h is:", h)
				elif switch == 1:
					#RainbowText += 1 #Uncomment if you want to keep track of how many times this part was executed
					unicornhathd.rotation(270)
					unicornhathd.brightness(0.5)
					for prolong in range(3):
						for scroll in range(text1_width - width): #Rainbow coloured scrolltext. Check out TEXT & FONT under the arrays at the top if you want to customize.
							for x in range(width):
								hue = (x + scroll) / float(text1_width)
								br, bg, bb = [int(n * 255) for n in colorsys.hsv_to_rgb(hue, 1.0, 1.0)]
								for y in range(height):
									pixel = image1.getpixel((x + scroll, y))
									r, g, b = [float(n / 255.0) for n in pixel]
									r = int(br * r)
									g = int(bg * g)
									b = int(bb * b)
									unicornhathd.set_pixel(width - 1 - x, y, r, g, b)
							unicornhathd.show()
							time.sleep(0.05)
				elif switch == 2:
					#ASRainbow += 1 #Uncomment if you want to keep track of how many times this part was executed
					still_alive_radio.set_volume(0.1)
					still_alive_radio.play()
					for prolong in range(1200):	#Stay inside this loop for a little while
						step += 1		#Aperture Logo being 'lit' up by a rainbow.
						for x in range(0, 16):
							for y in range(0, 16):
								dx = 7
								dy = 7
								dx = (math.sin(step / 20.0) * 15.0) + 7.0
								dy = (math.cos(step / 15.0) * 15.0) + 7.0
								sc = (math.cos(step / 10.0) * 10.0) + 16.0
								h = math.sqrt(math.pow(x - dx, 2) + math.pow(y - dy, 2)) / sc
								v = aperture[x, y]
								r, g, b = colorsys.hsv_to_rgb(h, 1, v)
								r *= 255.0
								g *= 255.0
								b *= 255.0
								unicornhathd.set_pixel(x, y, r, g, b)
						unicornhathd.show()
						#time.sleep(1.0 / 60)
					still_alive_radio.stop()
				elif switch == 3:
					#ShowImg += 1 #Uncomment if you want to keep track of how many times this was executed
					for prolong in range(20): #Stay inside this loop for a little while
						fire.set_volume(0.1)
						fire.play()
						for o_x in range(int(img.size[0] / width)): #Display an image
							for o_y in range(int(img.size[1] / height)):
								valid = False
								for x in range(width):
									for y in range(height):
										pixel = img.getpixel(((o_x * width) + y, (o_y * height) + x))
										r, g, b = int(pixel[0]), int(pixel[1]), int(pixel[2])
										if r or g or b:
											valid = True
										unicornhathd.set_pixel(x, y, r, g, b,)
								if valid:
									unicornhathd.show()
									time.sleep(0.1)
						fire.stop()
					fire.stop()
				elif switch == 4:
					for prolong in range(20):
						#cputemp += 1 #Uncomment if you want to keep track of how many times this part was executed
						unicornhathd.rotation(270)
						cpu = CPUTemperature()
						TEXT2 = (str(int(cpu.temperature))+degree_sign)
						text2_width, text2_height = font2.getsize(TEXT2)
						text2_width += width + text2_x
						image2 = Image.new('RGB', (text2_width, max(height, text2_height)), (0, 0, 0))
						draw2 = ImageDraw.Draw(image2)
						draw2.text((text2_x, text2_y), TEXT2, fill=(255, 255, 255), font=font2)
						for scroll in range(text2_width - width + 90):
							for x in range(width):
								if cpu.temperature <= 55:
									hue = (x + scroll) / float(text2_width)
								else:
									hue = 0.0	#If the CPU Temperature exceeds 55Degree Celsius, make you notice
									HeatAlarm.set_volume(0.1)
									HeatAlarm.play()
								br, bg, bb = [int(n * 255) for n in colorsys.hsv_to_rgb(hue, 1.0, 1.0)]
								for y in range(height):
									pixel2 = image2.getpixel((x, y))
									r, g, b = [float(n / 255.0) for n in pixel2]
									r = int(br * r)
									g = int(bg * g)
									b = int(bb * b)
									unicornhathd.set_pixel(width -1 -x, y, r, g, b)
							unicornhathd.show()
							time.sleep(0.02)
					HeatAlarm.stop()
except KeyboardInterrupt:
	unicornhathd.off()
	#print()
	#print("Number of times each animation/display has been called")
	#print("zzzz: " + str(zZzZ))
	#print("Aperture Science HSV Scroll: " + str(ASScroll))
	#print("Aperture Science Rainbow Animation: " + str(ASRainbow))
	#print("Rainbow Scrolltext: " + str(RainbowText))
	#print("Show Image: " + str(ShowImg))
	#print("CPU Temperature: " + str(cputemp))
	#time.sleep(60)

