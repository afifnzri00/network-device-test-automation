import requests
from requests.exceptions import RequestException, ConnectionError
import json

# def change_first_ip(first_ip,url1, payload1, url2, payload2, cookies):

def change_first_ip(first_ip):

    new_ip = str (first_ip)

    username = "admin"
    password = "admin"



    base_url3 = "http://192.168.0."
    api_endpoint3 = "/api/auth"

    # url1 = "http://192.168.0.100/api/login"
    url1 = "http://192.168.0.100/api/auth"
    url2 = "http://192.168.0.100/api/save/network"
    url3 = base_url3 + new_ip + api_endpoint3
    # url3 = "http://192.168.0."+ new_ip

    # session_cookie = ""

    # cookies = {"session": ""}
    payload1 = {"username": username,"password": password}
    

    dataPort = "3000"
    gw = "192.168.0.1"
    ip = "192.168.0."+ new_ip
    sn = "255.255.255.0"

    payload2 = {"dataPort": dataPort,"gw": gw,"ip": ip,"sn": sn}


    try:
        response1 = requests.post(url1, data=payload1, timeout=5)
        response1.raise_for_status() 
        response_text = response1.text.replace('\\', '\\\\')  # escape the '\' in the server response to avoid errors
        data1 = json.loads(response_text)
        print("authtoken OKAY")
        authtoken = data1["authtoken"]
        headers = {"authtoken": authtoken}
        try:
            response2 = requests.post(url2, data=payload2, headers=headers, timeout= 5)
            response2.raise_for_status()
            print("change IP OKAY")
            try:
                response3 = requests.post(url3,data=payload1,timeout= 5)
                response3.raise_for_status()
                print("new IP OKAY")
                return True
            except requests.exceptions.RequestException as e:
                print(f"new ip error: {e}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"change ip error: {e}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"authtoken error: {e}")
        return False



    # with requests.Session() as session:
    #     try:
    #         response1 = session.post(url1, data=payload1, timeout=5)
    #         if response1.status_code == 200:
    #             response_text = response1.text.replace('\\', '\\\\')  # escape the '\' in the server response to avoid errors
    #             data1 = json.loads(response_text)
    #             # data1 = response1.json()
    #             print("Authorization OKAY")
    #             authtoken = data1["authtoken"]
    #             headers = {"authtoken": authtoken}
    #             response2 = session.post(url2, data=payload2, headers=headers, timeout= 5)
    #             if response2.status_code == 200:
    #                 print("Change IP OKAY")
    #                 response3 = session.post(url3,data=payload1,timeout= 5)
    #                 if response3.status_code == 200:
    #                     print("New IP auhtorization OKAY")
    #                     return True
    #                 else:
    #                     print(f"Error in request to {url3}: {response3.text}")
    #                     print("NOT OKAY3")
    #                     return False
    #             else:
    #                 print(f"Error in request to {url2}: {response2.text}")
    #                 print("NOT OKAY2")
    #                 return False
    #         else:
    #             print(f"Error in request to {url1}: {response1.text}")
    #             print("NOT OKAY1")
    #             return False
    #     except requests.exceptions.RequestException as e:
    #         print(f"RequestException: {e}")
    #         return False









   # try:
    #     response1 = requests.post(url1, data=payload1, cookies=cookies)
    #     response1.raise_for_status()
    #     print(f'reponse1: {response1}')
    #     try:
    #         response2 = requests.post(url2, data=payload2, cookies=cookies)
    #         response2.raise_for_status()
    #         print(f"reponse2: {response2}")
    #         return True
    #     except requests.exceptions.RequestException as e:
    #             print(f"Error in request to {url2}: {e}")
    #             return False

    # except requests.exceptions.RequestException as e:
    #     print(f"Error in request to {url1}: {e}")
    #     return False




# def changeip_main():
#     first_ip = 101
#     change_first_ip(first_ip)

# if __name__ == "__main__":
#     changeip_main()