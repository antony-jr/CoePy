#!/usr/bin/python3
import requests
import base64
import sys

if __name__ == "__main__":
    print("CoePy GC , CoePy Get Captcha.")
    print("Copyright (C) 2018 Antony Jr.\n")

    if len(sys.argv) < 2:
        print("Usage: {} [NUMBER OF CAPTCHA'S TO RETRIVE AND SAVE] [IMAGE FILE(s) PREFIX]".format(sys.argv[0]))
        sys.exit(0)
        
    NumberOfCapcha = 0
    Template = str(sys.argv[2])
    try:
        NumberOfCapcha = int(sys.argv[1])
    except:
        NumberOfCapcha = None
        
    if NumberOfCapcha is None or NumberOfCapcha < 0:
        print("ERROR: Please mention a positive integer as the number of capcha's.")
        sys.exit(-1)
        
    s = requests.Session()
    for i in range(0 , NumberOfCapcha):
        print("[*] Requesting Host...")
        indexContent = str(s.get("http://coe1.annauniv.edu/home/index.php").content)
        print("[+] Retrived Data from Host...")

        indexContent = ((indexContent.split("login_stu"))[2]).split()
        for j in indexContent:
            if "base64" in j:
                recapcha = ((j.split("base64,"))[1]).split('"')[0]
                print("[+] Writing Captcha Image to '{}{}.png'...".format(Template , i))
                with open('{}{}.png'.format(Template , i) , 'wb') as fp:
                    fp.write(base64.b64decode(recapcha))
            break
