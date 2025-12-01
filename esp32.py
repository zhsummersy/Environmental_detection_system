from machine import Pin, ADC,PWM,Timer
import time
import network
import urequests  
import json
from time import sleep_ms

serverip = 'http://192.168.123.2:8000'
url = '/upload'
postUrl = serverip + url
getUrl = serverip + '/getMax'
alertUrl = serverip + '/alert'
getZT = serverip + '/getZT'
headers = {'Content-Type': 'application/json'}


# 风机继电器
pin2 = machine.Pin(15, machine.Pin.OUT)
def Motor_start():
    pin2.value(1)

def Motor_stop():
    pin2.value(0)

def motorZT():
    response = urequests.get(getZT, headers=headers) 
    # 打印服务器的响应  
    print(response.text)
    if response.text == 'open':
        Motor_start()
    if response.text == 'close':
        Motor_stop()

# 报警LED
led = Pin(12,Pin.OUT)
def LedStart():
    led.value(1)
    time.sleep(0.5)
    led.value(0)
    led.value(1)
    time.sleep(0.5)
    led.value(0)
    
def LedStop():
    led.value(0)

# 蜂鸣器
class BUZZER:
    def __init__(self, sig_pin):
        self.pwm = PWM(Pin(sig_pin, Pin.OUT))

    def play(self, melodies, wait, duty):
        for note in melodies:
            print("note:{}".format(note))
            if note:
                self.pwm.freq(note)
            self.pwm.duty(duty)
            sleep_ms(wait)
        # 暂停PWM，将占空比设置为0
        self.pwm.duty(0)
E7 = 0
mario = [
    E7,E7,E7
]
buzzer = BUZZER(13)
def buzzerWork():
    buzzer.play(mario, 200, 512)
    sleep_ms(100)
    buzzer.play(mario, 200, 512)
    sleep_ms(100)
    buzzer.play(mario, 200, 512)
    buzzer.pwm.duty(0)
    
def buzzerStop():
    buzzer.pwm.duty(0)

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('Kee', '17368601723')
        i = 1
        while not wlan.isconnected():
            print("正在链接...{}".format(i))
            i += 1
            time.sleep(1)
    print('network config:', wlan.ifconfig())

height = 0.0
def waterHeight():
    global height
    ps2_y = ADC(Pin(39))
    ps2_y.atten(ADC.ATTN_11DB)  # 这里配置测量量程为3.3V
    p15 = Pin(15, Pin.IN)
    height = ps2_y.read()  # 0-4095
    height = height/1800
    print('height')
    print(height)
    # 循环检测


    
co = 0.0
def Co():
    global co
    ps2_y = ADC(Pin(33))
    ps2_y.atten(ADC.ATTN_11DB)  # 这里配置测量量程为3.3V
    co = ps2_y.read()  # 0-4095
    co = co/4095
    print('co')
    print(co)
    
h2s = 0.0
def H2s():
    global h2s
    ps2_y = ADC(Pin(32))
    ps2_y.atten(ADC.ATTN_11DB)  # 这里配置测量量程为3.3V
    h2s = ps2_y.read()  # 0-4095
    h2s = h2s/40950
    print('h2s')
    print(h2s)

ch4 = 0.0
def Ch4():
    global ch4
    adc = ADC(35)
    ch4 = adc.read()
    ch4 = ch4/40950
    print('ch4')
    print(ch4)

nh3 = 0.0
def Nh3():
    global nh3
    adc = ADC(34)
    nh3 = adc.read()
    nh3 = nh3/40950
    print('nh3')
    print(nh3)
    
def upload():
    data = {'co':co, 'h2s':h2s,'ch4':ch4,'nh3':nh3,'height':height}
    json_data = json.dumps(data) 
    print(json_data)
    response = urequests.post(postUrl, data=json_data, headers=headers) 
    # 打印服务器的响应  
    print(response.text)
    
tim_upload = Timer(10)
tim_upload.init(period=3000, mode=Timer.PERIODIC, callback=lambda t: upload())

# 获取最新的阈值
maxCo = 0.0
maxH2s = 0.0
maxCh4 = 0.0
maxNh3 = 0.0
maxHight = 0.0
def getmax():
    global maxCo,maxH2s,maxCh4,maxNh3,maxHight
    response = urequests.get(getUrl, headers=headers) 
    # 打印服务器的响应  
    rawJson = response.text
    #print(rawJson)
    data = json.loads(rawJson)
    maxCo = data[0]["threshold"]
    maxH2s = data[1]["threshold"]
    maxCh4 = data[2]["threshold"]
    maxNh3 = data[3]["threshold"]
    maxHight = data[4]["threshold"]

# 循环启动前的初始化
buzzerStop()
do_connect()
LedStop()
while True:
    # 获取最新的阈值
    getmax()
    # 获取最新的检测数据
    waterHeight()
    print('-------------')
    Co()
    print('-------------')
    H2s()
    print('-------------')
    Ch4()
    print('-------------')
    Nh3()
    # 判断是否报警
    if co >= float(maxCo):
        data = {"content":'warning! co!',"value":co}
        json_data = json.dumps(data) 
        response = urequests.post(alertUrl, data=json_data, headers=headers)
        print(response.text)
        print('co报警')
        LedStart()
        buzzerWork()
    elif h2s >= float(maxH2s):
        data = {"content":'warning! h2s!',"value":h2s}
        json_data = json.dumps(data) 
        response = urequests.post(alertUrl, data=json_data, headers=headers)
        print(response.text)
        print('h2s报警')
        LedStart()
        buzzerWork()
    elif ch4 >= float(maxCh4):
        data = {"content":'warning! ch4!',"value":ch4}
        json_data = json.dumps(data) 
        response = urequests.post(alertUrl, data=json_data, headers=headers)
        print(response.text)
        print('ch4报警')
        LedStart()
        buzzerWork()
    elif nh3 >= float(maxNh3):
        data = {"content":'warning! nh3!',"value":nh3}
        json_data = json.dumps(data) 
        response = urequests.post(alertUrl, data=json_data, headers=headers)
        print(response.text)
        print('nh3报警')
        LedStart()
        buzzerWork()
    elif height >= float(maxHight):
        data = {"content":'warning! height!',"value":height}
        json_data = json.dumps(data) 
        response = urequests.post(alertUrl, data=json_data, headers=headers)
        print(response.text)
        print('水位报警')
        LedStart()
        buzzerWork()
    else:
        print('无报警')
    time.sleep(1)
    
    



