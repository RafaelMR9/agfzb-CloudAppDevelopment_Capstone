import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    api_key = kwargs.get("api_key")
    try:
        if api_key:
            # Basic authentication GET
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', api_key))
        else:
            # no authentication GET
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    response = requests.post(url, params=kwargs, json=json_payload)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # For each dealer object
        for dealer in json_result:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)
    return results

def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    if kwargs.get("id"):
        json_result = get_request(url, id=kwargs.get("id"))
    else:
        json_result = get_request(url)
    if json_result:
        for review in json_result:
            review_obj = DealerReview(dealership=review["dealership"], name=review["name"], purchase=review["purchase"], review=review["review"])
            if "dealership" in review: review_obj.id = review["dealership"]
            if "purchase_date" in review: review_obj.purchase_date = review["purchase_date"]
            if "car_make" in review: review_obj.car_make = review["car_make"]
            if "car_model" in review: review_obj.car_model = review["car_model"]
            if "car_year" in review: review_obj.car_year = review["car_year"]
            
            sentiment = analyze_review_sentiments(review_obj.review)
            review_obj.sentiment = sentiment
            results.append(review_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_by_id_from_cf(url, dealerId):
    json_result = get_request(url, id=dealerId)
    if json_result:
        dealer_obj = CarDealer(address=json_result[0]["address"], city=json_result[0]["city"], full_name=json_result[0]["full_name"],
                                id=json_result[0]["id"], lat=json_result[0]["lat"], long=json_result[0]["long"],
                                short_name=json_result[0]["short_name"],
                                st=json_result[0]["st"], zip=json_result[0]["zip"])
    return dealer_obj

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/6ef1463a-b0e7-47a0-aaf4-df512b1fb08e"
    api_key = "0DMaeS3NFFEOI_3xt1BMJgrp62jSwlIXau8N1fX4E5xT"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze( text=text+"hello hello hello",features=Features(sentiment=SentimentOptions(targets=[text+"hello hello hello"]))).get_result()
    label=json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']
    return(label)


