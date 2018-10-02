# Paytm-api-for-django
High performance with just plug and play feature. just put the app, tweak some settings and you are ready to go. good luck.

## Features

### Requirements
Python 3+
Django 2+

### Installation
step 1: clone this repo and paste it in your project directory
step 2: open **settings.py** file of your project and add **paytm** to **INSTALLED_APPS** paste the below settings

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
    'CALLBACK_URL':f'http://{HOSTNAME}/paytm/payment_response/',
```
step 3: Replace "XXXXX..." above with respective **merchant key** and **MID**

step 4: open urls.py and add
```python
#urls.py

urlpatterns = [
  #other urls ...
  path('paytm/', include('paytm.urls'))
]
```

step 4: Setup complete and you are good to go

### Test your api

 - run the server and go to **http://127.0.0.1:8000/paytm/test/**
 
 ![alt text](https://lh5.googleusercontent.com/DFC9npQY45EVMrEEekFEj6AgcfZJ7Sec1Omd-OoGNUz49sp__ZL9kHyccKBBcj_0ZrZoXP20541jBqiFSeKI=w1920-h976)
 
 - fill the details and test your api
 
 
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
- All the response are in json format
- Apis are checked and highly optimized for performance
- This package also include **Refund API** But Paytm suggest not to use apis for this use **PAYTM DASHBOARD**


### Any problem? raise an issue

# LICENCE
 - MIT
