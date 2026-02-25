import threading
import requests
import json


url1 = "http://192.168.0.150/api/auth"
url2 = "http://192.168.0.150/api/startPaging" 
url3 = "http://192.168.0.150/api/endPaging"  

payload = {
    "username": "admin",
    "password": "admin"
    }

def hws_init():
    try:
        response = requests.post(url1, data=payload, timeout= 3)
        response.raise_for_status() 
        response_text = response.text.replace('\\', '\\\\')  # escape the '\' in the server response to avoid errors
        data1 = json.loads(response_text)
        # data1 = response1.json()
        authtoken = data1["authtoken"]
        print(f"paging authtoken{data1}")
        return authtoken

    except requests.RequestException as e:
        print(f"Error paging authtoken request: {e}")
        # print(f"Error message: {response.text}")
        return False
    

def HW_SEND_1(paging_auth_token):#send 1st packet data
    headers = {"authtoken": paging_auth_token}
    params = {"priority": "1", "zones": "","allcall":"true"}
    try:
        response = requests.get(url2,params=params,headers=headers)
        response.raise_for_status() 
        data = response.json()
        # print(f"StarPaging:{response}{json.dumps(data)}")
        return True
    
    except requests.RequestException as e:
        print(f"Error startpaging: {e}")
        print(f"Error message: {response.text}")
        return False

def threaded_timer(duration,paging_auth_token):
    timer_thread = threading.Timer(duration, timer_callback,args=[paging_auth_token])
    timer_thread.start()

def timer_callback(paging_auth_token):
    HW_SEND_2(paging_auth_token)

def HW_SEND_2(paging_auth_token):#send 2nd packet data
    headers = {"authtoken": paging_auth_token}
    try:
        response = requests.get(url3,headers=headers)
        response.raise_for_status() 
        if response.status_code == 200:
            # print(f"endpaging:{response}")
            return True
        
    except requests.RequestException as e:
        print(f"Error endpaging: {e}")
        print(f"Error message: {response.text}")
        return False
    
def hws_trigger(paging_auth_token):
    start_paging = HW_SEND_1(paging_auth_token)
    if start_paging == True:
        threaded_timer(10,paging_auth_token)
        return True




# if __name__ == "__main__":
#     paging_auth_token = hws_init()
#     hws_trigger(paging_auth_token)
#     # hws_main()
#     # hws_trigger()
    





# def hws_init():
#     try:
#         response1 = requests.post(url1, data=payload, timeout= 3)
#         response1.raise_for_status() 
#         if response1.status_code == 200:
#             response_text = response1.text.replace('\\', '\\\\')  # escape the '\' in the server response to avoid errors
#             data1 = json.loads(response_text)
#             # data1 = response1.json()
#             authtoken = data1["authtoken"]
#             print(f"paging authtoken{data1}")
#             return authtoken
#         else:
#             print(f"Unexpected status code: {response1.status_code}")
#             return False
#     except requests.RequestException as e:
#         print(f"Error during requests.post: {e}")
#         return False




# def HW_SEND_1(paging_auth_token):#send 1st packet data
#     headers = {"authtoken": paging_auth_token}
#     params = {"priority": "1", "zones": "","allcall":"true"}
#     try:
#         response = requests.get(url2,params=params,headers=headers)
#         response.raise_for_status() 
#         if response.status_code == 200:
#             data = response.json()
#             print(f"StarPaging:{response}{json.dumps(data)}")
#             return True
#         else:
#             data = response.json()
#             print(f"StarPaging:{response}{json.dumps(data)}")
#             return False

#     except requests.RequestException as e:
#         print(f"Error during requests.post: {e}")
#         return False






    # def HW_SEND_2(paging_auth_token):#send 2nd packet data
#     headers = {"authtoken": paging_auth_token}
#     try:
#         response = requests.get(url3,headers=headers)
#         response.raise_for_status() 
#         if response.status_code == 200:
#             print(f"EndPaging:{response}")
#             return True
#         else:
#             print(f"Unexpected status code: {response.status_code}")
#             return False

#     except requests.RequestException as e:
#         print(f"Error during requests.post: {e}")
#         return False