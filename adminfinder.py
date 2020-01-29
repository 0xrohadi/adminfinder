#!/usr/bin/env python3

# let's import whatever, we need from standard library
import requests, argparse, sys, time
from concurrent.futures import ThreadPoolExecutor


# i need colors to make it better
R = '\33[91m'
G = '\33[92m'
Y = '\33[93m'
C = '\33[96m'
B = '\33[94m'
P = '\33[95m'
D = '\33[90m'
E = '\33[0m'

# processing commandline arguments
ap = argparse.ArgumentParser(prog='adminfinder.py', description='Multiple admin panel finder scan written Python')
ap.add_argument('-u', '--url', required=True, help='Set target url/website')
ap.add_argument('-w', '--wordlist', required=True, help='Wordlist to use, default wordlist.txt')
ap.add_argument('-t', '--thread', required=True, help='Number of threads to use, up tou you')

args = vars(ap.parse_args())

# single user agent
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'

# time
def local_time():
    t = time.localtime()
    current_time = time.strftime('%H:%M:%S', t)
    return current_time
    
# let's check the robots.txt file
def check_robots():
    url = args['url']
    if not url.startswith('http://'):
        url = 'http://'+url
    if not url.endswith('/'):
        url = url+'/'
    headers = {'User-Agent': user_agent}
    host = url+'robots.txt'
    try:
        req = requests.get(host, headers=headers).status_code
        if req == 200:
            print('{g}[+] Yeah robots.txt found{e}'.format(g=G, e=E))
        else:
            print('{r}[-] Can\'t not found robots.txt{e}'.format(r=R, e=E))
    except requests.exceptions.ConnectionError as e:
        print('{r}[!] Connection error{e}'.format(r=R, e=E))
    except Exception as e:
        print('{r}[!] Something error {}{e}'.format(e, r=R, e=E))

# if you find it will display the status response varies
def admin(url, pass_list):
    url = args['url']
    if not url.startswith('http://'):
        url = 'http://'+url
    if not url.endswith('/'):
        url = url+'/'
    headers = {'User-Agent': user_agent}
    host = url+pass_list
    try:
        req = requests.get(host, headers=headers).status_code
        if req == 200:
            print('{e}|   {g}{:<20}{e} | {g}{:<55}{e}'.format(req, host, g=G, e=E))
        else:
            print('{e}|   {r}{:<20}{e} | {r}{:<55}{e}'.format(req, host, r=R, e=E))
    except requests.exceptions.ConnectionError as e:
        print('{r}[!] Your\'e connection internet slow down :({e}'.format(r=R, e=E))
    except Exception as e:
        print('{r}[!] Something error {}{e}'.format(e, r=R, e=E))

# requesting immediate processing with the thread
def admin_scan(url):
    try:
        password = args['wordlist']
        with ThreadPoolExecutor(max_workers=int(args['thread'])) as executor:
            with open(password, 'r') as password_list:
                for pass_list in password_list:
                    pass_list = pass_list.replace('\n', '') 
                    executor.submit(admin, url, pass_list)
    except FileNotFound as e:
        print('{r}[!] File does\'t not exist, check again{e}'.format(r=R, e=E))
    except KeyboardInterrupt as e:
        print('{r}[!] CTRL+C detected{e}'.format(r=R, e=E))
    except Exception as e:
        print('{r}[!] Something error {}{e}'.format(e, r=R, e=E)) 
                
# just a fancy ass banner, you like it bro :)
def banner_display():
    # original ascii, i found on google seaech engine
    p = '''{y}
                     /|               /\\
                /^^^/ |^\\Z           /  |
               |         \\Z         /   |
               / {r}@{y}        \\Z       /   / \\_______
  (  \\      _ /            \\Z     /   /         /
(     ---- /{r}G{y}       |\\      |Z   /   /         /
 (  / ---- \\    /---'/\\     |Z  /   /         /
            \\/--'   /--/   /Z  /             /
             |     /--/   |Z  /            / \\_______
            /     /--/    |Z  \\           /         /
         --/     /--/     \\Z   |         /         /
          /     /--/       \\Z  /                  /
               |--|         \\Z/                  /
               |---|        /              /----'{g}
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  {g}• {r}ADMIN FINDER SCANN PYTHON
  {g}• {r}Codename By {c}0xrohadi{r} 
  {g}• {r}Blog: https://maqlo-heker.blogspot.com {g}
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
               {y} \\---|                     /^^^^^^^^^^^^\\Z
                 \\-/                                    \\Z
                  /     /        |                       \\Z
              \\---'    |\\________|      |_______          |Z
            \\--'     /\\/ \\|_|_|_||      |_|_|_|_|\\_       |Z
             '------'            /     /  /      |_       /Z
                             \\---'    |  / ```````      /Z
                           \\--'     /\\/  \\ ____________/Z
                            '------'      \\{e}
    '''.format(r=R, g=G, c=C, e=E, y=Y)
    print(p)

# create the play function
def main():
    try:
        if len(sys.argv) < 2:
            print(parser.usage())
        else:
            banner_display()
            url = args['url']
            print('{e}[{c}#{e}] Start on {g}{}{e}'.format(local_time(), e=E, c=C, g=G))
            print('{e}[{c}#{e}] Checking for robots file in {g}{}{e}'.format(url, e=E, c=C, g=G))
            check_robots()
            time.sleep(2)
            print('{e}[{c}#{e}] Website to scan: {g}{}\n{e}'.format(url, e=E, g=G, c=C))
            time.sleep(2)
            print('{e}[{c}•{e}] {:<20} {e}[{c}•{e}] {:<55}{e}'.format('STATUS', 'URL', c=C, e=E))
            admin_scan(url)
            print('\n{e}[{c}#{e}] Scan is completed on {g}{}{e}'.format(local_time(), e=E, g=G, c=C))
            time.sleep(2)
            print('{e}[{c}#{e}] Have fun using this tools :D'.format(e=E, c=C))
    except KeyboardInterrupt as e:
        print('{r}[!] CTRL+C detected{e}'.format(e=E, r=R))
    except Exception as e:
        print('{r}[!] Something error {}{e}'.format(e, e=E, r=R))
 
# call to start
if __name__ == '__main__':
    main()