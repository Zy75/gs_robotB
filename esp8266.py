import time
import socket

error1 = 0
seq_old = 0
seq_delta = 0
dat_i = [0] * 12
t_old = 0
t_delta = 0

host = "192.168.8.19"
port = 4000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((host, port))

while True:

  time.sleep(0.02)

  pload = client.recv(1024)

  data = pload.split()

  for k in range(9):
    dat_i[k] = int(data[k])

  seq = dat_i[6]

  seq_delta = seq - seq_old

  if seq_delta <= 0:
    seq_delta += 256

  if seq_delta != 1:
     error1 += 1
    
  seq_old = seq

  t_delta = dat_i[8]
   
  print "%6d %6d %6d %6d %6d %6d   seq=%3d   %d err= %d,  t_delta=%4d" % (dat_i[0],dat_i[1],dat_i[2],dat_i[3],dat_i[4],dat_i[5],seq,seq_delta,error1,t_delta)


  client.send("zyx\r")

