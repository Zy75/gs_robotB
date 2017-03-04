import serial
from datetime import datetime

ser = serial.Serial('/dev/ttyUSB0', 38400)

sp2 = [0] * 16

error1 = 0
error2 = 0

while True:
    try:
        dat1 = ser.readline()

        sp1 = dat1.split(',')

        for num in range(9):
          sp2[num] = int(sp1[num])

        ii = sp2[6]

        i_delta = sp2[8]

        if i_delta != 1:
           error1 += 1

        t_delta = sp2[7]
        
        if t_delta > 105:
           error2 += 1

        print "%6d  %6d  %6d  %6d  %6d  %6d  seq=%4d   tdt=%5d   idt=%4d     err=%d,  %d" %( sp2[0],sp2[1],sp2[2],sp2[3],sp2[4],sp2[5], ii,t_delta, i_delta, error1,error2)

        ser.write(sp1[6] + ':' + sp1[9] + '\n')
        
    except KeyboardInterrupt:
        break

ser.close()
