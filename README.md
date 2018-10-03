# Paytm-api-for-django
High performance Paytm Gateway api for Django. Just plug and play app. good luck.

## Features

### Requirements
Python 3+
Django 2+

### Installation
**Step 1** : clone this repo and paste it in your project directory
**Step 2** : open **settings.py** file of your project and add **paytm** to **INSTALLED_APPS** paste the below settings

```python
# settings.py

INSTALLED_APPS = [
    .
    .
    .
    'paytm',
]

# other settings...

PAYTM_STAGING_URL = 'https://securegw-stage.paytm.in'
PAYTM_PRODUCTION_URL = 'https://securegw.paytm.in'

HOSTNAME = '127.0.0.1:8000'

if DEBUG:
    PAYTM_URL = PAYTM_STAGING_URL
else:
    PAYTM_URL = PAYTM_PRODUCTION_URL

PAYTM_MERCHANT_KEY = 'XXXXXXXXXXXX' # replace with original merchangt key
PAYTM_GATEWAY_SETTINGS = {
    'MID':'XXXXXXXXXXXXXXXXXXXX', # replace with original merchangt id or MID
    'INDUSTRY_TYPE_ID':'Retail',
    'WEBSITE':'APPSTAGING', # WEBSTAGING for websites -->> change this with production variables
    'CHANNEL_ID':'WAP', #WEB for websites
    'CALLBACK_URL':f'http://{HOSTNAME}/paytm/payment_response/', } # https:// if you are on production server

PAYTM_SAVE_SUCCESS_TRANSECTIONS_ONLY = True  # if this is true paytm will save only successful transection else it willsave all transections
```
**Step 3** : Run **migrations and migrate** after that Replace "XXXXX..." above with respective **merchant key** and **MID**

**Step 4** : open urls.py and add
```python
#urls.py

urlpatterns = [
  #other urls ...
  path('paytm/', include('paytm.urls'))
]
```

**Step 5** : Setup complete and you are good to go

## Test your api

 - run the server and go to **http://127.0.0.1:8000/paytm/test/**
 
 ![](https://lh5.googleusercontent.com/aLLJJWemvZr-KaOtQhz-yxMx55Cvx0f2uCRZJdGpedPwk0BUshaitkPGKd6JifD7gd8FBf3BDYU6YQCoqm93=w1920-h976)
 
 - Fill the details and test your api
 
 
## URLS
    ### To request for payment
    url: https://{HOST}/paytm/payment_response/ 
    method: POST
    minimum requirements = ['ORDER_ID', 'TXN_AMOUNT', 'CUST_ID'] send these fields
    NOTE: This api is also optimized for PAYMENT_MODE_ONLY field for more info go through paytm gateway docs below
    
    
    ### To check status of transection
    url: https://{HOST}/paytm/status/
    method: POST
    minimum requirements = ['ORDER_ID'] send these fields
    
    for all the available fields go through
    PAYTM Gateway Documentation
    https://business.paytm.com/developers-api/integration/payment-gateway/documentation


# NOTES 
- Every api need the **user to be logged** in So if you dont want it to check for logged in just remove LoginRequiredMixin from views.py in paytm folder
- All the response are in json format
- Apis are checked and highly optimized for performance
- This package also include **Refund API** But Paytm suggest not to use apis for this use **PAYTM DASHBOARD**
- you will need to install **pycrypto** for paytm to work.  
    ```sh
    pip install pycrypto
    ```
    if above give error, i included pre-compiled wheel file
    
    ```sh
    pip install pycrypto-2.6.1-cp36-cp36m-win_amd64.whl
    ```
    this will solve the problem for windows users too.

### Any problem? raise an issue

# LICENCE
 - MIT
