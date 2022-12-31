def getserial():
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
          cpuserial = line[10:26]
    f.close()
    if cpuserial == "0000000000000000" :
      import random
      cpuserial = random.randint(100000,90000000)
    return cpuserial
