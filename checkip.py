import requests
import json

connect_status = [False] * (40)  

url1 = "http://192.168.0.200/api/auth"
url2 = "http://192.168.0.200/api/clients"  # Replace with your desired URL


def check_ips_init():
    payload = {
        "username": "admin",
        "password": "admin"
        }
    
    try:
        response = requests.post(url1, data=payload,timeout = 3)
        response.raise_for_status() 
        response_text = response.text.replace('\\', '\\\\')  # escape the '\' in the server response to avoid errors
        data1 = json.loads(response_text)
        # data1 = response1.json()
        authtoken = data1["authtoken"]
        print(f"server authtoken{data1}")
        return authtoken

    except requests.RequestException as e:
        print(f"Error server authtoken request: {e}")
        # print(f"Error message: {response.text}")
        return False



def check_ips(server_auth_token):
    headers = {"authtoken":server_auth_token}
    try:
        response = requests.get(url2,headers=headers,timeout = 3)
        response.raise_for_status() 
        if response.status_code == 200:
            data = response.json()
            connected_ips = []
            for item in data:
                if item['connected'] == True:
                    connected_ips.append(item['ip'])
                    connected_ips.sort()
            for i in range(101,141):
                ip_to_check = f'192.168.0.{i}'    
                connect_status[i-101] =  ip_to_check in connected_ips
            return connect_status
        
    except requests.RequestException as e:
        print(f"Error check ip: {e}")
        return False




# ####################################################################
        # print (connected_ips)
        # return connected_ips

                # return connected_ips
                # connected_ips = []
                # connected_ips.append(item['ip'])
                # return connected_ips   

        # for ip in data:
        #     if ip.get("connected", True):
        #         connected_ips.append(ip.get("ip"))
        # connected_ips.sort()

        # print("")
        # print("Connected IP:")
        # for ip in connected_ips:
        #     print(ip)

# def check_ip_main():
    # check_ips_init()
    # check_login = check_ips_init()
    # while check_login:
    #     # check_ips()
    #     ayam = check_ips()
    #     print(ayam)
    # connect_status = [False] * (12)  

        # # for i in range(int(start_ip.split('.')[-1]), int(end_ip.split('.')[-1]) + 1):
        # print("")
        # for i in range(101,113):
        #     ip_to_check = f'192.168.0.{i}'
            
        #     connect_status[i-101] =  ip_to_check in ayam
        #     print (i,connect_status[i-101])
        #     # if ip_to_check in ayam:
        #     #     connect_status [i-100] = True
        #     #     print(f"IP {ip_to_check} is in the array.")
        #     # else:
        #     #     connect_status [i-100] = False
        #     #     print(f"IP {ip_to_check} is not in the array.")
    # return ayam
        
# if __name__ == "__main__":
#     check_ip_main()
    


# def check_ips_init():
#     payload = {
#         "username": "admin",
#         "password": "admin"
#         }
    
#     try:
#         response1 = requests.post(url1, data=payload,timeout = 3)
#         response1.raise_for_status() 
#         if response1.status_code == 200:
#             response_text = response1.text.replace('\\', '\\\\')  # escape the '\' in the server response to avoid errors
#             data1 = json.loads(response_text)
#             # data1 = response1.json()
#             authtoken = data1["authtoken"]
#             print(f"server authtoken{data1}")
#             return authtoken
#         else:
#             print(f"Unexpected status code: {response1.status_code}")
#             return False
#     except requests.RequestException as e:
#         print(f"Error during requests.post: {e}")
#         return False