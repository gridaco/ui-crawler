import csv
import os.path
import time
from pathlib import Path
import warnings
from selenium import webdriver

filename = os.path.join(str(Path.cwd()), 'top500.domains.05.18.csv')



def read_top_500():
    with open(filename, newline='\n') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        rows = [x for x in reader]
        rows = rows[1:]
        urls = ["http://"+x[1] for x in rows]
        return urls

def parse_domain(url):
    # http://facebook.com/
    url = url.replace("http://", "").replace("https://", "").replace(".", "_").replace("/", "")
    return url


def take_screenshots():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920x1080")

    driver = webdriver.Chrome(options=options)

    urls = read_top_500()
    print("TOTAL URLS", len(urls))
    count = len(urls)
    i = 0
    for url in urls:
        try:
            print("Took Screenshot at %s, %s done.. %s left.." % (url, str(i), str(count-i)))
            driver.get(url)
            driver.implicitly_wait(10)
            ss_dir = os.path.join(str(Path.cwd()), 'screenshots', parse_domain(url)+".png")
            print(ss_dir)
            driver.save_screenshot(ss_dir)
        except Exception as e:
            driver.quit()
            driver = webdriver.Chrome(options=options)
            warnings.warn(e)
            time.sleep(1)

        i += 1
    driver.quit()


if __name__ == '__main__':
    take_screenshots()
