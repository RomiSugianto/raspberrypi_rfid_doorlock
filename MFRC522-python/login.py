#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522
import time
import signal
import pymysql
con = pymysql.connect(db="absen", user="user", passwd="user",host="10.10.0.163",port=3306,autocommit=True)

print ("connect successful!!")

# Card Register
# userid = ['383132523085','737457602814']


GPIO.setwarnings(False)

reader = SimpleMFRC522.SimpleMFRC522()

continue_reading = True

def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    con.close()
    GPIO.cleanup()

signal.signal(signal.SIGINT, end_read)

while continue_reading:
    id, text = reader.read()
    tempname=str(text)
    tempid=str(id)
    cur = con.cursor()
    sql_select_query = """select nama from siswa where card = %s"""
    cur.execute(sql_select_query, (tempid, ))
    rows_count = cur.execute(sql_select_query, (tempid, ))
    card = cur.fetchone()
    name = card[0]

    if rows_count > 0:
        print("cid recognized")
        print(id)
        print("welcome ",name)
        time.sleep(2)
    else:
        print("\r\nunrecognized id detected")
        print(id)
        print("unrecognized")
        time.sleep(2)