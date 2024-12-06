# Challenge Name: Elf In The Matrix
## Category
- Web Exploitation

## Description
There has been rumors that the LED Matrix hides some secrets, can you find thenm?
## Difficulty and Flags
- Flag 1 Easy FLAG{Wobots_UwU}
- Flag 2 Medium FLAG{Br3aking_&_Elfering}
- Flag 3 Hard FLAG{h4xx0r_0n_s4nt4s_n4ughty_l1st}
- Flag 4 Hard FLAG{h4xxor_owns_Xmas}


## Hint(s)
- Flag 1: check the robots assembly line.
- Flag 2: how do blind people read? mayne the source code will tell you 
- Flag 2: did you check the response of the request?
- Flag 3: Dont pop a shell, be smart about it and find another way in.
- Flag 3: ${Have you heard of environemental variables?}
- Flag 4: Did you do your local enumeration?

## Setup

#### Debian Machine
- ssh to the machine from the internet (15x.x.x.x Ip address) with root
- login to the user elfie with the following command: su elfie : message Calderon for password 
- run the following command: sudo wg-quick up elfinthematrix
    - YOU WILL LOSE THE CONECTION. DONT PANIC.
- now ssh back to the server with the following: ssh elfie@10.8.0.8  : message Calderon for password 
- cd to /home/elfie/LightControllerCTFChallenge
- run the following command: source ./venv/bin/activate
- finaly run the following command: python3 app.py &
- you will see and output like this 
```
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://10.137.0.6:8080
Press CTRL+C to quit


``` 
- If not then call Calderon 

#### Raspberry Pi 
- Calderon will handle this part


## Walkthrough
1. go to robots.txt to get the first flag
2. go to /login and look at the soiurce code for some braile, then enter the credentials. then click generate otp and look ath the respose of the request. the ot is there. just copy and paste and click login 
3. Intercept the request post request when ou send it to the pi and replace it wirh something like this 
 ```pixel_art.json;cat${IFS}${PATH:0:1}home${PATH:0:1}elfie${PATH:0:1}.ssh${PATH:0:1}id_rsa" solution````
4. Leak the ssh key and login to the server
5. do sudo -l and see you can use sudo less without a password
6. Run less and pop a sudo shell 
7. Profit 

