import requests

def post_data(url,data):
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl91dWlkIjoiIiwiZW50aXR5X3V1aWQiOiIxOTIwIiwiZW50aXR5X3R5cGUiOiJ1c2VyIiwiZW50aXR5X3JlZl91dWlkIjoiN2U4ZDFkNTctYmZlNC00Nzc1LTgyYmQtOTJhNjcxZWZjMTBjIiwiZW50aXR5X25hbWUiOiIiLCJzYWx0IjoiZWU2Njg2Y2EifQ.dTPyqwgeHNolCCQRdeffXK--gAxyvQwagDExWRYHdH4"
    headers={'Authorization': token}
    try:
        x = requests.get(url, json=data, headers=headers)
        print(x)
        if x.status_code == 200:
            return True
        return False
    except:
        print("Some problems occured during sending the data")