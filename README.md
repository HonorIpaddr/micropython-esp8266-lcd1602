# 主题
 
 2020-03-03 分享：esp8266 通过i2c 模块驱动 1602 LCD
## 交流群
QQ: 2551950052

## 特别感谢

这次分享中参考了 https://github.com/dhylands/python_lcd 

感谢大佬分享代码，这样我就不用自己封装lcd显示相关方法，降低学习成本。

## Tips:
1. webrepl 默认是不开启的，所以每次reset后都要手动开启，方法参考步骤9
2. 稳定版默认不开启debug模式
3. 千万别接错线
4. dh11 精度比较低，但是做个室内温度计够用了
5. micropython 加载python程序的过程，上电启动-->boot.py-->main.py ,所以，我们可以把程序固化在main.py中

## 准备：
1. esp8266开发板（nodemcu)
2. 数据线（旧款的andord手机数据线）usb-TypeA ---- usb-microB
3. dht11 传感器，
   ```
   Pin1 -- VDD(3.3v or 5v) --esp8266_3.3v
        |
        5k 电阻
        |
   Pin2 -- data -- esp8266_gipo2
   Pin3 -- 空
   Pin4 -- GND -- esp8266_gnd
   ```
4. 串口驱动，linux系统自带，windows 需要对应安装pl2302或ch340, 具体看板子上的串口芯片
5. 1602 LCD 
6. 1602 LCD I2C 模块
   pin 1-16 对应连接
   pin vcc -- vcc
   pin GND -- GND
   pin sda -- gpio4(nodemcu_d2)
   pin scl -- gpio5(nodemcu_d1)
7. python3 任意版
8. 配置pip 使用清华镜像 
   ```
   pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
   ```
9. esptool
10. python_lcd库 https://github.com/dhylands/python_lcd.git
11. webrepl-cli 用于上传文件到esp8266的文件系统中
12. linux上位机（我用树莓派作为是上位机），windows和linux的主机都没问题，只要成功驱动usb转串口芯片就可以。

## 过程

1. 为esp8266 刷入最新的micropython 固件
  * 下载最新的固件，比如我分享是最新稳定版本[20191220 v1.12](https://micropython.org/resources/firmware/esp8266-20191220-v1.12.bin)
  * 下载地址https://micropython.org/dowload#esp8266
2. 安装esptool
  ```
  pip install esptool
  ```
3. 下载大神封装好的lcd库

  ```
  git clone https://github.com/dhylands/python_lcd.git

  ```
4. 下载webrepl-cli 
  ```
  git clone https://github.com/micropython/webrepl.git
  ```
5. 擦除esp8266片上系统
  ```
  esptool.py -p /dev/ttyUSB0 earse_flash
  ```
6. 刷入固件
  ```
  esptool.py -p /dev/ttyUSB0 -b 115200 -c esp8266 write_flash --flash_size=detect 0 esp8266-20191220-v1.12.bin
  ```
7. 串口进入交互界面
  ```
  minicom -D /dev/ttyUSB0
  ```
8. 连接wifi（esp8266 只支持2.4G)
  ```
  from network import WLAN,STA_IF
  sta_if = WLAN(STA_IF)
  sta_if.active(True)
  sta_if.connect('ssid','password')
  sta_if.ifconfig()
  sta_if.isconnected()
  ```
9. 开启webrepl,方便上传代码文件
  ```
  import webrep_setup
  import webrep 
  webrepl.start(password="123") # 设置临时密码
  ```
10. 上传文件， ip地址在第9步中，sta_if.ifconfig() 可以查到
```
webrepl_cli.py -p 123 ./main.py 192.168.7.174:/
webrepl_cli.py -p 123 ./python_lcd/lcd/esp8266_i2c_lcd.py 192.168.7.174:/
webrepl_cli.py -p 123 ./python_lcd/lcd/i2c_lcd.py 192.168.7.174:/
```
11. 通过 板子reset 按钮重启确保加载 main.py


