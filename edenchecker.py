import requests
import os

edenred_username = os.getenv('EDENRED_USERNAME')
edenred_password = os.getenv('EDENRED_PASSWORD')

# Abort if we don't have settings done properly
if edenred_username is None or edenred_password is None:
    print("Environment variables for EDENRED_USERNAME and EDENRED_PASSWORD have not been set.")
    sys.exit(1) 

edenred_signin_url = 'https://api.myedenred.fi/signin'
post_data = {"username":edenred_username,"password":edenred_password}  
headers = {'Content-Type': 'application/json'}
benefits_status_url = 'https://api.myedenred.fi/users/me/user-benefits'


with requests.Session() as session:
    login_edenred = session.post(edenred_signin_url, json=post_data, headers=headers)
    
    if login_edenred.status_code == 200:
        get_response = session.get(benefits_status_url)
        if get_response.status_code == 200:           
            try:
                data = get_response.json()
                if 'benefits' in data:
                    print("Edenred balance results:")
                    for entry in data['benefits']:
                        walletType = entry.get('walletType', 'No walletType found')
                        balance = entry.get('balance', 'No balance found')
                        # Hacky way to identify and name proper benefits
                        if walletType == "main":
                            walletType = "Lunch"
                        if walletType == "wellness":
                            walletType = "Wellness"
                        balance = str(balance / 100) + "€"
                        print(f"{walletType} - Balance: {balance}")
                else:
                    print("No benefits found...")
            except ValueError as e:
                print("Invalid JSON response:", e)
        else:
            print(f"Getting benefit information failed with HTTP statuscode: {get_response.status_code}")
    else:
        print(f"Logging in failed with HTTP statuscode: {login_edenred.status_code}")
