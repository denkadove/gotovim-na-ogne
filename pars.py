import requests
import time
import os
import random
from bs4 import BeautifulSoup
import threading


def get_url():
    f = open('urls.txt', 'r')
    urls = f.readlines()
    f.close()
    urls = [line.rstrip() for line in urls]
    return urls


def get_proxy_list():
    f = open('proxy.txt', 'r')
    proxy_list = f.readlines()
    proxy_list = [line.rstrip() for line in proxy_list]
    f.close()
    return proxy_list


def clear_urls():
    f = open('404.txt', 'r', encoding='utf-8')
    links = f.readlines()
    f.close()
    u = open('urls.txt', 'r', encoding='utf-8')
    urls = u.readlines()
    u.close()
    links = [line.rstrip() for line in links]
    for i in range(len(links)):
        links[i] = links[i][:links[i].find("|") - 1]

    return links


def get_page(url):
    # for url in urls:
    p = {"http": proxy_list[random.randint(0, len(proxy_list) - 1)]}
    response = requests.get(url, proxies=p, headers={
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})

    soup = BeautifulSoup(response.text, 'html.parser')
    code = response.status_code
    file_name = str(code) + '.txt'

    if response.status_code == 200:
        name = soup.find('h1').text
        try:
            price = soup.select('.values_wrapper > .price_value')[0].text
        except Exception:
            price = 0
        print(name, '=>', price)
        f = open('prices.txt', 'a', encoding='utf-8')
        to_file = str(name) + ' => ' + str(price) + '\n'
        f.write(to_file)
        f.close()

    else:
        try:
            f = open(file_name, 'a', encoding='utf-8')
        except:
            f = open(file_name, 'w', encoding='utf-8')
        to_file = str(url) + ' | Ответ сервера: ' + str(code) + ' ошибка!' + '\n'
        f.write(to_file)
        print('Ответ сервера:', code, ' ошибка!')
        f.close()
    # time.sleep(0.5)


urls = get_url()
proxy_list = get_proxy_list()


def main():
    f = open('prices.txt', 'w', encoding='utf-8')
    f.close()
    threads = []
    global_start_time = time.time()
    # get_page(urls)
    for url in urls:
        threads.append(threading.Thread(target=get_page, args=(url,)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print('Данные сохранены в файле prices.txt')
    print('Общее время работы (сек): {s:0.4f}'.format(s=time.time() - global_start_time))
    os.system('pause')
    # links = clear_urls()
    # print(links)


if __name__ == '__main__':
    main()
