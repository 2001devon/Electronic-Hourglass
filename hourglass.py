import machine
from machine import Pin, ADC, PWM
import utime
from speaker import beep_the_speaker
from accel import get_accel_state, AccelState
from LCD import LCD
red = Pin(14, Pin.OUT, Pin.PULL_UP)
green = Pin(15, Pin.OUT, Pin.PULL_UP)
paused_button = False
button = Pin(13, Pin.IN, Pin.PULL_UP)
def button_handler(pin):
 global paused_button
 paused_button = not paused_button
button_pin = 13 
button = Pin(button_pin, Pin.IN, Pin.PULL_UP)
button.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)
# -----------------------------------------
# LCD Instantiation
# -----------------------------------------
# add this code to the beginning of your main file to instantiate the LCD
# GPIO 
lcd = LCD(enable_pin=8, # Enable Pin, int
 reg_select_pin=7, # Register Select, int
 #data_pins=[12, 11, 10, 9] # Data Pin numbers for the upper nibble. list[int]
 data_pins=[9, 10, 11, 12] # Data Pin numbers for the upper nibble. list[int]
 )
lcd.init()
lcd.clear()
#lcd.print ("howdy")
#utime.sleep(2)
#lcd.home()
# -----------------------------------------
# LCD Class:
# -----------------------------------------
def red_on():
 red.value(1)
def green_on():
 green.value(1)
def green_off():
 green.value(0)
def red_off():
 red.value(0)
def display_time(time):
 lcd.clear()
 lcd.go_to (0,0)
 lcd.print ("Time remains = ")
 lcd.go_to (0,1)
 lcd.print ("{:02}:{:02}".format(time//60,time%60))
 
def read_button():
 if button.value() == 0: # Button pressed
 utime.sleep_ms(10) # Debounce time
 if button.value() == 0: # Check if button is still pressed
 return True
 return False
 
def blink():
 green_on()
 red_off()
 utime.sleep_ms(30)
 green_off()
 red_on()
 utime.sleep_ms(30)
def hourglass():
 #I only need these three varibles to define the state of the system
 time_remaining = 60
 paused_button = False
 paused_accel = False
 accel_state = get_accel_state()
 previous_accel_state = accel_state
 
 while True:
 if get_accel_state() != AccelState.SIDE: 
 accel_state = get_accel_state()
 
 #if button is pressed to pause or if accelemeter is on its side- it should enter this paused stateis
 if read_button() == True:
 paused_button = True
 if get_accel_state() == AccelState.SIDE: 
 paused_accel = True
 
 # while we are paused blink the leds
 while read_button():
 blink()
 print ("button")
 if read_button():
 paused_button = False
 
 
 while paused_accel:
 blink()
 if get_accel_state() != AccelState.SIDE:
 paused_accel = False
 accel_state = get_accel_state()
 
 
 if time_remaining > 0: 
 time_remaining -= 1
 green_on()
 red_off()
 
 if time_remaining == 0:
 beep_the_speaker()
 red_on()
 green_off()
 lcd.print ("Time is up")
 
 if accel_state != previous_accel_state:
 beep_the_speaker()
 #adjust time remaining
 display_time(time_remaining)
 time_remaining = 60 - time_remaining
 
 
 previous_accel_state = accel_state 
 display_time(time_remaining)
 utime.sleep(1)
 
if __name__=="__main__":
 hourglass()
