# -*- coding: utf-8 -*-
#!/usr/bin/env python
from __future__ import print_function
import argparse
import sys
import serial
import binascii
import time

###############################################################################
class LoRa_RN2483():
  def __init__(self, port):
    self.port = port
    self.serial = None

  def send_data(self, data):
    if self.serial:
      print(">> ", data)
      self.serial.write(data)
      self.rcv_data()
      return True

  def rcv_data(self):
    if self.serial:
      x = self.serial.readall()
      if len(x):
        print("<< ", x)
        return x

  def info(self):
    self.send_data('sys get ver\r\n'.encode('utf-8'))
    self.send_data('sys get hweui\r\n'.encode('utf-8'))
    self.send_data('sys get vdd\r\n'.encode('utf-8'))

    # Radio parameters
    self.send_data('radio get mod\r\n'.encode('utf-8'))
    self.send_data('radio get freq\r\n'.encode('utf-8'))
    self.send_data('radio get pwr\r\n'.encode('utf-8'))
    self.send_data('radio get sf\r\n'.encode('utf-8'))
    self.send_data('radio get rxbw\r\n'.encode('utf-8'))
    self.send_data('radio get prlen\r\n'.encode('utf-8'))
    self.send_data('radio get crc\r\n'.encode('utf-8'))
    self.send_data('radio get iqi\r\n'.encode('utf-8'))
    self.send_data('radio get cr\r\n'.encode('utf-8'))
    self.send_data('radio get wdt\r\n'.encode('utf-8'))
    self.send_data('radio get sync\r\n'.encode('utf-8'))
    self.send_data('radio get bw\r\n'.encode('utf-8'))
    
  def config(self):
    self.send_data('mac pause\r\n'.encode('utf-8'))
    self.send_data('radio set mod lora\r\n'.encode('utf-8'))
    self.send_data('radio set freq 868100000\r\n'.encode('utf-8'))
    self.send_data('radio set pwr 15\r\n'.encode('utf-8'))
    self.send_data('radio set sf sf12\r\n'.encode('utf-8'))
    self.send_data('radio set rxbw 125\r\n'.encode('utf-8'))
    self.send_data('radio set prlen 8\r\n'.encode('utf-8'))
    self.send_data('radio set crc on\r\n'.encode('utf-8'))
    self.send_data('radio set iqi off\r\n'.encode('utf-8'))
    self.send_data('radio set cr 4/5\r\n'.encode('utf-8'))
    self.send_data('radio set wdt 0\r\n'.encode('utf-8'))     
    self.send_data('radio set sync 34\r\n'.encode('utf-8'))   
    self.send_data('radio set bw 125\r\n'.encode('utf-8'))

  def reset(self):
    self.send_data('sys reset\r\n'.encode('utf-8'))
    
  def factoryReset(self):
    self.send_data('sys factoryRESET\r\n'.encode('utf-8'))
    time.sleep(5)
    self.rcv_data()

  def tx(self, data):
    self.send_data('mac pause\r\n'.encode('utf-8'))
    self.send_data(('radio tx ' + data + '\r\n').encode('utf-8'))

  def rx(self):
    self.send_data('mac pause\r\n'.encode('utf-8'))
    self.send_data('radio rx 0\r\n'.encode('utf-8'))
    while 1:
      # print('.', end='', flush=True)
      x = self.rcv_data()
      if x:
        if x.decode('utf-8').find('radio_rx') != -1:
          self.tx(binascii.hexlify('NRBSPONG'.encode('utf-8')).decode())
          self.send_data('mac pause\r\n'.encode('utf-8'))
          self.send_data('radio rx 0\r\n'.encode('utf-8'))

  def open(self):
    self.serial = serial.Serial(
        port=self.port,
        baudrate=57600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
      )
    return self.serial

  def close(self):
    if self.serial:
      self.serial.close()
      self.serial = None

supported_operations = ['info', 'config', 'reset', 'factory', 'tx', 'rx']

###############################################################################
def parseArgs(argv):
  parser = argparse.ArgumentParser()

  op = ''
  for o in supported_operations:
    if len(op):
      op = op + ', '
    op = op + o
  op = 'One out of these operations: ' + op

  parser.add_argument('-o', '--operation', required=True, help=op)
  parser.add_argument('-p', '--port', required=True, help="USB/serial com port: Linux: /dev/ttyUSB0..., Windows: com1, com2...")
  
  return parser.parse_args(argv)

###############################################################################
def main(argv=sys.argv[1:]):
  args = parseArgs(argv)
  
  operations = args.operation.lower().replace(';', ' ').replace(',', ' ').split()

  lora = LoRa_RN2483(args.port)

  try:
    if lora.open():
      for o in operations:
        print("Operation: ", o)

        if o == "info":
          lora.info()
        elif o == "config":
          lora.config()
        elif o == "reset":
          lora.reset()
        elif o == "factory":
          lora.factoryReset()
        elif o == "tx":
          # for _ in range(255):
          lora.tx('Hello')

        elif o == "rx":
          lora.rx()
        else:
          print("Unknown operation!")
      
      lora.close()
  except Exception as e:
    print("Exception:", e)
  finally:
    lora.close()

def crc16_update(crc, a):
  crc ^= a

  i = 0
  while i < 8:
    if crc & 1:
      crc = (crc >> 1) ^ 0xA001  
    else:
      crc = (crc >> 1)
    i += 1
  
  return crc;

	
if __name__ == "__main__":
  main()

  