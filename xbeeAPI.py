from xbee import XBee,ZigBee
import serial
import struct
import math

ser = serial.Serial('/dev/ttyUSB0', 38400)
xbee = ZigBee(ser,escaped=True)

dest = '\x00\x13\xA2\x00\x40\xE7\x42\x09'

error1 = 0
error2 = 0

def motor_cmd(ax,ay,az,gx,gy,gz,seq):
    
    return math.sin( 2.0 * math.pi * float(seq) / 256.0 )
    

while True:
    try:
        
        while True:
            response = xbee.wait_read_frame()
            if response['id'] == 'rx':
               break

        ax = struct.unpack('h',response['rf_data'][0:2])[0]
        ay = struct.unpack('h',response['rf_data'][2:4])[0]
        az = struct.unpack('h',response['rf_data'][4:6])[0]
        gx = struct.unpack('h',response['rf_data'][6:8])[0]
        gy = struct.unpack('h',response['rf_data'][8:10])[0]
        gz = struct.unpack('h',response['rf_data'][10:12])[0]
        
        t_delta = struct.unpack('h',response['rf_data'][14:16])[0]

        print "%6d %6d %6d %6d %6d %6d" % (ax,ay,az,gx,gy,gz),

	seqnum = struct.unpack('B',response['rf_data'][12])[0]
	seq_delta = struct.unpack('B',response['rf_data'][13])[0]
       
#        dat = struct.pack('fB', motor_cmd(ax,ay,az,gx,gy,gz,seqnum), seqnum )
        dat = struct.pack('fB', 0.0, seqnum )

        xbee.tx(dest_addr='\xFF\xFE', dest_addr_long=dest, data=dat)

        if seq_delta != 1:
           error1 += 1
       
        if t_delta > 74:
           error2 += 1
           prev_td = t_delta
        print "%5d %5d %6d     error=%3d   %3d   prev_td=%5d" % (seqnum,seq_delta,t_delta,error1,error2,prev_td)

    except KeyboardInterrupt:
        break

ser.close()
