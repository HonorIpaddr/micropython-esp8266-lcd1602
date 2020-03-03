from time import sleep_ms,ticks_ms
from machine import I2C,Pin
from esp8266_i2c_lcd import I2cLcd
from dht import DHT11



DEFAULT_I2C_ADDR = 0x27

i2c = I2C(scl = Pin(5),sda= Pin(4),freq=400000)
lcd = I2cLcd(i2c,DEFAULT_I2C_ADDR,2,16)
dht11 = DHT11(Pin(2))

lcd.clear()
lcd.move_to(0,0)
lcd.putstr('booting.')
count = 6
while count>0:
	
	sleep_ms(500)
	lcd.putstr('.')
	count = count-1


def dump_dht11():
	dht11.measure()
	text= "T:%d oC\nH:%d /100 RH"%(dht11.temperature(),dht11.humidity())
 	lcd.clear()
	lcd.move_to(0,0)
	lcd.putstr(text)


while True:
	dump_dht11()
	sleep_ms(15000)

 
