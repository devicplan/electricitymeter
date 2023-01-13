# Electricity-Meter-Viewer V0.99.20
# Micropython with Raspberry Pico W
# 10.01.2023 jd@icplan.de
# backup.py - (impulse, impulse_d, impulse_m, impulse_y, sowi, zimp, par1, par2, 24*twohour, 24*twohour_t, another 2 * (24+31+24 values)) = 214 values separated as string semicolon
# Autobackup every hour

import network, socket, time, ntptime, utime, machine, os

led = machine.Pin("LED",machine.Pin.OUT)
led.off()
time.sleep(2)

ssid = 'Your_WLAN_Name'
password = 'Your_WLAN_Password'
pulse_per_kwh = 500

start_backup = 0                                                                   # start backup over http://x.x.x.x/backup
start_sbackup = 0                                                                  # start special backup over http://x.x.x.x/sbackup
impulse = 0                                                                        # pulse counter light pulses 5 min
impulse_d = 0                                                                      # pulse counter light pulses 1 h
impulse_m = 0                                                                      # pulse counter light pulses 24 hours
impulse_y = 0                                                                      # pulse counter light pulses 31 days
sowi = 2                                                                           # summertime = 2 wintertime = 1
zimp = 0                                                                           # Pulses per 1 KWh (unused)
par1 = 0                                                                           # free unused
par2 = 0                                                                           # free unused

twohour = [0] * 24                                                                 # data values of the last 2 hours
twohour_t = [0] * 24                                                               # time values
twohourd = ""                                                                      # string data values
twohourd_t = ""                                                                    # string time values
twohour_avr = 0                                                                    # average

oneday = [0] * 24                                                                  # data values of the last 24 hours
oneday_t = [0] * 24
onedayd = ""
onedayd_t = ""
oneday_avr = 0

month = [0] * 31                                                                   # data values of the last 31 days 0-0 o'clock
month_t = [0] * 31
monthd = ""
monthd_t = ""
month_avr = 0

twoyear = [0] * 24                                                                 # data values of the last 24 months
twoyear_t = [0] * 24
twoyeard = ""
twoyeard_t = ""
twoyear_avr = 0

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

html0 = """<!DOCTYPE html><html>
    <head> <title>Graphic Electricity Meter Viewer</title> </head>
    <body> <body bgcolor=A4C8F0><h1>Graphic Electricity Meter Viewer</h1>
    <table "width=400"><tr><td width="150">Software version</td><td>0.99.20 (10.01.2023)</td></tr><tr><td>Developed by</td><td>www.icplan.de</td></tr>
    <tr><td>current date and time</td><td>"""
html1 = """</td></tr></table><br><a href="https://quickchart.io/chart?c={type:'bar',data:{labels:["""
html2 = """],datasets:[{label:'Energy consumption in Wh - Average """
html3 = """ Wh',data:["""
html4 = """]}]}}">View and result of the last 2 hours</a><br><br><a href="https://quickchart.io/chart?c={type:'bar',data:{labels:["""
html5 = """]}]}}">View and result of the last 24 hours</a><br><br><a href="https://quickchart.io/chart?c={type:'bar',data:{labels:["""
html6 = """]}]}}">View and result of the last month</a><br><br><a href="https://quickchart.io/chart?c={type:'bar',data:{labels:["""
html7 = """]}]}}">View and result of the last 2 years</a><br><br><br><br>Other features<br><a href="backup">Create</a> backup<br><a href="sbackup">Create special</a> backup<br>
<a href="sommer">Set daylight</a> saving time<br>Set the <a href="winter">winter</a> time<br></body></html>"""

def backup_write():                                                                 # Create backup
    global impulse, impulse_d, impulse_m, impulse_y, sowi, zimp, par1, par2
    global twohour, twohour_t, oneday, oneday_t, month, month_t, twoyear, twoyear_t
    try:
        os.remove('backup.py')
    except OSError as error:
        print('backup.py - File does not exist')
    daten = [0] * 8
    daten[0] = impulse
    daten[1] = impulse_d
    daten[2] = impulse_m
    daten[3] = impulse_y
    daten[4] = sowi
    daten[5] = zimp
    daten[6] = par1
    daten[7] = par2
    daten = daten + twohour + twohour_t + oneday + oneday_t + month + month_t + twoyear + twoyear_t
    e = ''
    file = open('backup.py','w')
    for a in range (0,len(daten),1):
        e = e + str(daten[a])
        if(a < (len(daten)-1)): e = e +';'
    file.write(e)
    file.close()
    for a in range (0,3,1):
        led.on()                                                                    # led 3x short flash
        time.sleep(0.1)
        led.off()
        time.sleep(0.4)
    time.sleep(3)

def sbackup_write():                                                                # Create special backup
    global impulse, impulse_d, impulse_m, impulse_y, sowi, zimp, par1, par2
    global twohour, twohour_t, oneday, oneday_t, month, month_t, twoyear, twoyear_t
    try:
        os.remove('backup2.py')
    except OSError as error:
        print('backup2.py - File does not exist')
    daten = [0] * 8
    daten[0] = impulse
    daten[1] = impulse_d
    daten[2] = impulse_m
    daten[3] = impulse_y
    daten[4] = sowi
    daten[5] = zimp
    daten[6] = par1
    daten[7] = par2
    daten = daten + twohour + twohour_t + oneday + oneday_t + month + month_t + twoyear + twoyear_t
    e = ''
    file = open('backup2.py','w')
    for a in range (0,len(daten),1):
        e = e + str(daten[a])
        if(a < (len(daten)-1)): e = e +';'
    file.write(e)
    file.close()
    for a in range (0,6,1):
        led.on()                                                                    # led 6x short flash
        time.sleep(0.1)
        led.off()
        time.sleep(0.4)
    time.sleep(3)
    
def backup_read():                                                                 # read backup if file exists
    global impulse, impulse_d, impulse_m, impulse_y, sowi, zimp, par1, par2
    global twohour, twohour_t, oneday, oneday_t, month, month_t, twoyear, twoyear_t
    try:
        file = open('backup.py','r')
    except OSError as error:
        print('backup.py - File does not exist')
        return
    f = file.read()                                                                # file read
    file.close()
    e = f.split(';')                                                               # data cut
    impulse = float(e[0])
    impulse_d = float(e[1])
    impulse_m = float(e[2])
    impulse_y = float(e[3])
    sowi = float(e[4])                                                             # Summer / Wintertime
    zimp = float(e[5])                                                             # Pulses per 1 KWh
    par1 = float(e[6])
    par2 = float(e[7])
    x = 8
    for a in range (0,24,1):                                                       # last two hour readback
        twohour[a] = float(e[a+x])
        twohour_t[a] = e[a+x+24]
    for a in range (0,24,1):                                                       # last day readback
        oneday[a] = float(e[a+x+48])
        oneday_t[a] = e[a+x+72]
    for a in range (0,31,1):                                                       # last month readback
        month[a] = float(e[a+x+96])
        month_t[a] = e[a+x+127]
    for a in range (0,24,1):                                                       # last day readback
        twoyear[a] = float(e[a+x+158])
        twoyear_t[a] = e[a+x+182]
        
def pin_interrupt(Pin):                                                            # interrupt processing
    global impulse, pulse_per_kwh
    impulse += 1000 / pulse_per_kwh
    
Pin13 = machine.Pin(13,machine.Pin.IN)                                             # Pin13 count input to ground without pulup
#Pin13 = machine.Pin(13,machine.Pin.IN,machine.Pin.PULL_UP)                        # Pin13 count input to ground with pulup
Pin13.irq(trigger=machine.Pin.IRQ_RISING, handler=pin_interrupt)                   # works as interrupt

def update_link():                                                                 # update all links
    global twohour, twohour_t, twohourd, twohourd_t, oneday, oneday_t, onedayd, onedayd_t
    global month, month_t, monthd, monthd_t, impulse_m, twoyear, twoyear_t, twoyeard, twoyeard_t
    global twohour_avr, oneday_avr, month_avr, twoyear_avr
    twohourd = str(twohour[0])
    for a in range (1,24,1):
        twohourd = twohourd + "," + str(twohour[a])
    twohourd_t = str(twohour_t[0])
    for a in range (1,24,1):
        twohourd_t = twohourd_t + "," + str(twohour_t[a]) 
    onedayd = str(oneday[0])
    for a in range (1,24,1):
        onedayd = onedayd + "," + str(oneday[a])
    onedayd_t = str(oneday_t[0])
    for a in range (1,24,1):
        onedayd_t = onedayd_t + "," + str(oneday_t[a]) 
    monthd = str(month[0])
    for a in range (1,31,1):
        monthd = monthd + "," + str(month[a])
    monthd_t = str(month_t[0])
    for a in range (1,31,1):
        monthd_t = monthd_t + "," + str(month_t[a]) 
    twoyeard = str(twoyear[0])
    for a in range (1,24,1):
        twoyeard = twoyeard + "," + str(twoyear[a])
    twoyeard_t = str(twoyear_t[0])
    for a in range (1,24,1):
        twoyeard_t = twoyeard_t + "," + str(twoyear_t[a])        
    c = 0                                                                          # calculation average two hours
    for a in range (0,24,1):
        c = c + twohour[a]
    d = 0
    for a in range (0,24,1):                                                       # how many filled values are present?
        if(twohour[a]>1):
            d = d + 1
    if(d>0):
        twohour_avr = c / d
    c = 0                                                                          # calculation average one day
    for a in range (0,24,1):
        c = c + oneday[a]
    d = 0
    for a in range (0,24,1):                                                       # how many filled values are present?
        if(oneday[a]>1):
            d = d + 1
    if(d>0):
        oneday_avr = c / d
    c = 0                                                                          # calculation average one month
    for a in range (0,31,1):
        c = c + month[a]
    d = 0
    for a in range (0,31,1):                                                       # how many filled values are present?
        if(month[a]>1):
            d = d + 1
    if(d>0):
        month_avr = c / d
    c = 0                                                                          # calculation average two years
    for a in range (0,24,1):
        c = c + twoyear[a]
    d = 0
    for a in range (0,24,1):                                                       # how many filled values are present?
        if(twoyear[a]>1):
            d = d + 1
    if(d>0):
        twoyear_avr = c / d

def next5min():
    global twohour, twohour_t, twohourd, twohourd_t, impulse, impulse_d, impulse_m, impulse_y, ssid, password, twohour_avr
    impulse_d = impulse_d + impulse
    impulse_m = impulse_m + impulse
    impulse_y = impulse_y + impulse
    
    wlan.disconnect()                                                              # reconnect to wifi every 5 minutes
    led.on()
    time.sleep(1)
    wlan.connect(ssid, password)
    led.off()
    
    for a in range (1,24,1):                                                       # move dataset
        twohour[a-1] = twohour[a]    
    twohour[23] = impulse * 12                                                     # enter current pulses * 12
    for a in range (1,24,1):                                                       # move timings
        twohour_t[a-1] = twohour_t[a]
    b = ("'%02d:%02d'" % (time_a[3],time_a[4]))
    twohour_t[23] = b                                                              # enter current time
    impulse = 0

def nexthour():
    global oneday, oneday_t, onedayd, onedayd_t, impulse_d, oneday_avr
    for a in range (1,24,1):                                                       # move dataset
        oneday[a-1] = oneday[a]    
    oneday[23] = impulse_d                                                         # enter current impulses
    for a in range (1,24,1):                                                       # move timings
        oneday_t[a-1] = oneday_t[a]
    b = ("'%02d:%02d'" % (time_a[3],time_a[4]))
    oneday_t[23] = b                                                               # enter current time
    impulse_d = 0

def nextday():
    global month, month_t, monthd, monthd_t, impulse_m, month_avr, sowi, local_time_sec
    local_time_sec = utime.time() + int(sowi) * 3600 - (8 * 60 * 60)               # Yesterday's date 
    time_a = utime.localtime(local_time_sec)
    for a in range (1,31,1):                                                       # move dataset
        month[a-1] = month[a]    
    month[30] = impulse_m                                                          # enter current impulses
    for a in range (1,31,1):                                                       # move timings
        month_t[a-1] = month_t[a]
    b = ("'%02d.%02d.'" % (time_a[2],time_a[1]))                                   # day and month
    month_t[30] = b                                                                # enter current time
    impulse_m = 0
    local_time_sec = utime.time() + int(sowi) * 3600 

def nextmonth():
    global twoyear, twoyear_t, twoyeard, twoyeard_t, impulse_y, twoyear_avr, sowi, local_time_sec
    local_time_sec = utime.time() + int(sowi) * 3600 - (8 * 60 * 60)               # Yesterday's date 
    time_a = utime.localtime(local_time_sec)

    for a in range (1,24,1):                                                       # move dataset
        twoyear[a-1] = twoyear[a]    
    twoyear[23] = impulse_y / 30.5                                                 # enter current impulses / average
    for a in range (1,24,1):                                                       # move timings
        twoyear_t[a-1] = twoyear_t[a]
    b = ("'%02d.%04d'" % (time_a[1],time_a[0]))                                    # month and year
    twoyear_t[23] = b                                                              # enter current time
    impulse_y = 0
    local_time_sec = utime.time() + int(sowi) * 3600 

# Wait for connect or fail
max_wait = 30

while max_wait > 0:                                                                # wait 30 sec for wifi connect
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    led.on()
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
    led.off()

# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

ntptime.settime()                                                                  # load ntp time

s = socket.socket()
s.bind(addr)
s.settimeout(5)
s.listen(10)

print('listening on', addr)
backup_read()
update_link()

# Listen for connections
while True:
    local_time_sec = utime.time() + (int(sowi) * 3600)
#    local_time_sec = utime.time() + (int(sowi) * 3600) + ( 2 * 3600) + (27 * 60)
    time_a = utime.localtime(local_time_sec)
    print("%02d:%02d:%02d" % (time_a[3],time_a[4],time_a[5]))
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        cl_file = cl.makefile('rwb', 0)
        while True:
            line = cl_file.readline()
            lines = str(line)
            if((lines.find("/backup"))!=(-1)):
                start_backup = 1
            if((lines.find("/sbackup"))!=(-1)):
                start_sbackup = 1
            if((lines.find("/sommer"))!=(-1)):
                sowi = 2
            if((lines.find("/winter"))!=(-1)):
                sowi = 1
            if not line or line == b'\r\n':
                break

        thistime = ("%02d.%02d.%4d  %02d:%02d:%02d" % (time_a[2],time_a[1],time_a[0],time_a[3],time_a[4],time_a[5]))

        response = html0 + thistime + html1 + twohourd_t + html2 + str(twohour_avr) + html3 + twohourd + html4 + onedayd_t + html2 + str(oneday_avr) + html3 + onedayd + html5 + monthd_t + html2 + str(month_avr) + html3 + monthd + html6 + twoyeard_t + html2 + str(twoyear_avr) + html3 + twoyeard + html7
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()

    except OSError as e:
        if((e.args[0])==110):                                                     # error 110 = timeout socket
            pass
#           print('connection timeout')
        else:
            cl.close()
            print('connection closed')
            
    led.on()                                                                      # leds flash every 5 seconds for function control
    time.sleep(0.1)
    led.off()
    time.sleep(0.1)
    print(impulse, impulse_d, impulse_m, impulse_y)                               # print pulses
    
    if(time_a[5] < 10):
        if((time_a[4] % 5) == 0):                                                 # at 0, 5, 10, 15 ... 55 minutes one time start
            next5min()
            update_link()
            time.sleep(10 - time_a[5])
            print("%02d:%02d:%02d" % (time_a[3],time_a[4],time_a[5]))             # print time
            print("5 minutes ar over")
        if(time_a[4] == 0):                                                       # always start once at minute 0
            nexthour()
            update_link()
            backup_write()
            print("an hour is over")
        if((time_a[3] == 0)and(time_a[4] == 0)):                                  # always start once at hour 0
            time.sleep(15)
            nextday()
            update_link()
            ntptime.settime()                                                     # update time per ntp
            print("a day is over")
        if((time_a[2] == 1)and(time_a[3] == 0)and(time_a[4] == 0)):               # always start at day 1 once
            nextmonth()
            update_link()
            print("a month is over")
            
    if(start_backup == 1):                                                        # http://x.x.x.x/backup -> backup
        backup_write()
        print("create backup")
        start_backup = 0

    if(start_sbackup == 1):                                                       # http://x.x.x.x/sbackup -> backup
        sbackup_write()
        print("create special backup")
        start_sbackup = 0
