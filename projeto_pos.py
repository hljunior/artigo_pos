#!/usr/bin/env python
import os
import commands
#Define biblioteca da GPIO
import RPi.GPIO as GPIO
#Define biblioteca de tempo
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14,GPIO.OUT)

GPIO.output(14,GPIO.HIGH)

ip_roteador = '192.168.1.1'
host = '200.192.232.8'
comunidade_snmp = 'public'
timeout = '256'
erro_ideal = []
erro = []
time.sleep(180)
timeout = os.system("snmpwalk -v2c -c " + comunidade_snmp + " " + ip_roteador + " 1.3.6.1.2.1.2.2.1.14")
if timeout != 0:
    GPIO.output(14,GPIO.LOW) 
    time.sleep(20)
    GPIO.output(14,GPIO.HIGH) 
    time.sleep(180)

timeout = os.system("snmpwalk -v2c -c " + comunidade_snmp + " " + ip_roteador + " 1.3.6.1.2.1.2.2.1.14")
if timeout == 0:
    quantidade_interfaces = len(commands.getoutput("snmpwalk -v2c -c " + comunidade_snmp + " " + ip_roteador + " 1.3.6.1.2.1.2.2.1.14 | cut -d ':' -f 2 | awk '{print $NF}' | tr -d '\n'"))

else:
    quantidade_interfaces = 6

for n in range(0,quantidade_interfaces): erro_ideal.append(0)

#Inicia loop permanente 
while(1):
    perda = int(commands.getoutput("sudo nping -c 100 --tcp -p 53 " + host + "| grep 'Lost' | cut -d '.' -f 1 | awk -F '(' '{print $NF}'"))
    print 'perda = ', perda
    
    timeout = os.system("snmpwalk -v2c -c " + comunidade_snmp + " " + ip_roteador + " 1.3.6.1.2.1.2.2.1.14")
    erro = erro_ideal[:]
    erro_1 = erro_ideal[:]
    erro_2 = erro_ideal[:]
    if timeout == 0:
        erro_1 = commands.getoutput("snmpwalk -v2c -c " + comunidade_snmp + " " + ip_roteador + " 1.3.6.1.2.1.2.2.1.14 | cut -d ':' -f 2 | awk '{print $NF}' | tr -d '\n'")
        print 'erro_1 = ', erro_1
        time.sleep(5)	
        erro_2 = commands.getoutput("snmpwalk -v2c -c " + comunidade_snmp + " " + ip_roteador + " 1.3.6.1.2.1.2.2.1.14 | cut -d ':' -f 2 | awk '{print $NF}' | tr -d '\n'")         
        print 'erro_2 = ', erro_2
    
    for i in range(quantidade_interfaces): erro[i] = int( erro_2[i] ) - int( erro_1[i] ) 
    print 'erro = ', erro 
    if perda>3 or erro != erro_ideal:
        print 'rebooting'
        #Desliga o Roteador
        GPIO.output(14,GPIO.LOW)
        time.sleep(180)
        #Liga o Roteador
        GPIO.output(14,GPIO.HIGH)
        #Aguarda vinte minutos e reinicia os testes 
        time.sleep(1200)
    else:
        print 'perda =', perda
        print 'sem erros nas interfaces'
        if timeout != 0:
            print 'perda de gerencia SNMP' 
