#!/usr/bin/env python3
# Author by 0xrohadi
# Kabupaten Sleman, Yogyakarta, Indonesia

'''
Python to fuzzing admin panel login with threading is so fast ;)
'''

# standard Python libraries
import requests
import threading
import argparse
import sys
import time

threadLock = threading.Lock()
threads = []

class MyThread(threading.Thread):
    
    def __init__(self, url, wordlist):
        threading.Thread.__init__(self)
        self.url = url
        self.wordlist = wordlist
    
    def run(self):
        do_fuzzing(self.url, self.wordlist)


def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-u',
        '--url',
        required = True,
        help = 'Your target to fuzzing'
    )
    parser.add_argument(
        '-w',
        '--wordlist',
        required = True,
        help = 'Your wordlist ext .text'
    )
    args = parser.parse_args()
    
    return args
    
def get_time():
    t = time.strftime('[%m-%d-%Y : %H:%M:%S]')
    return t

def banner():
    display = '''\033[96m
 _____             _            _____   _       _     
|   __|_ _ ___ ___|_|___ ___   |  _  |_| |_____|_|___ 
|   __| | |- _|- _| |   | . |  |     | . |     | |   |
|__|  |___|___|___|_|_|_|_  |  |__|__|___|_|_|_|_|_|_|
                        |___|
~ Codename: 0xrohadi
~ Let\'s Do Fuzzing Admin Login ;)\033[0m
    '''
    print(display)
    
def my_headers():
    # change user-agent here with your user-agent you want
    headers = {
        'User-Agent': 'Bot Python Hahaha',
        'DNT': '1'
    }
    
    return headers

def convert(url):
    if url.startswith('http://www.'):
        return 'http://' + url[len('http://www.'):] + '/'
    if url.startswith('www.'):
        return 'http://' + url[len('www.'):] + '/'
    if not url.endswith('/'):
        return 'http://' + url + '/'
    if not url.startswith('http://'):
        return 'http://' + url 
        
    return url

def do_fuzzing(url, wordlist):
    headers = my_headers()
    url = convert(url)
    host = url + wordlist
    try:
        res = requests.get(host, headers = headers)
        if (res.status_code == 200):
            threadLock.acquire()
            print('\033[92m[+]\033[0m Found: {:<7} | Check: {:<0}'.format(res.status_code, host))
            threadLock.release()
        else:
            threadLock.acquire()
            print('\033[91m[-]\033[0m Not Found: {0} | {1}'.format(res.status_code, host))
            threadLock.release()
    except Exception as e:
        print(e)
        sys.exit()
        
def main():
    args = parser()
    time = get_time()
    if args.url is None:
        print('Usage: python3 adminfinder.py -u target -w wordlist.txt')
        sys.exit()
    else:
        banner()
        print('Starting at: {0}\n'.format(time))
        words = [w.strip() for w in open(args.wordlist, 'r').readlines()]
        for x in words:
            t = MyThread(args.url, x)
            threads.append(t)
            t.daemon = True
            t.start()
        
        for i in threads:
            i.join()
        print('\nDon\'t forget follow me on Twitter: @0xrohadi, Thank You!')


if __name__ == '__main__':
    main()