from zapv2 import ZAPv2
import time


time.sleep(170)

target= 'http://192.168.0.100'
api_key = '123456'


zap = ZAPv2(apikey=api_key, proxies={'http':'http://localhost:8080', 'https':'http://localhost:8080'})

zap.urlopen(target)

zap.spider.scan(url=target, apikey=api_key)
time.sleep(5)

while (int(zap.spider.status()) < 100):
    print('Spider progress %: ' + zap.spider.status())
    time.sleep(5)


while (int(zap.pscan.records_to_scan) > 0):
    print('Pscan records: ' + zap.pscan.records_to_scan)
    time.sleep(5)

zap.ascan.scan(url=target, apikey=api_key)
time.sleep(5)


while (int(zap.ascan.status()) < 100):
    print('Ascan progress %: ' + zap.ascan.status())
    time.sleep(5)


with open ('./scratch/report.html' , 'w') as f:
    f.write(zap.core.htmlreport())


