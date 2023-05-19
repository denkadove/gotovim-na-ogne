import time
import os
from queue import Queue
from bs4 import BeautifulSoup

class LenGasParser:

    def __init__(self):
        self.data = self.get_url()

    def get_url(self):
        f = open('urls.txt', 'r')
        urls = f.readlines()
        f.close()
        urls = [line.rstrip() for line in urls]
        return urls    

def main():
    print(LenGasParser.get_url)     

if __name__ == "__main__":
    main()

