import os
import requests
import urllib
import json
import datetime
import pandas as pd

def pretty_print_request(req):
  """
  At this point it is completely built and ready
  to be fired; it is "prepared".

  However pay attention at the formatting used in 
  this function because it is programmed to be pretty 
  printed and may differ from the actual request.
  """
  print('{}\n{}\r\n{}\r\n\r\n{}'.format(
    '-----------START-----------',
    req.method + ' ' + req.url,
    '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
    req.body,
  ))


def call_endpoint(uri, method,  deserialize_response=None, verbose=False, *, params=None, body=None):
  """
  Calls a HTTP REST endpoint with the given message body (json) and optionally deserializes the result.
  
  Parameters
  ----------
  uri : string
      Base HTTP/HTTPS URI .
  
  method : string
          The name (and signature if GET) of the REST method.
  
  deserialize_response : (optional) string
                        Can be 'json' if desired return value in desrialized json or None for returning the raw response content.
  
  params : (optional) Dictionary of parameters for GET method
  
  body : (optional) The json body of the POST method
  """
  endpoint = uri + method
  if body:
    resp = requests.post(endpoint, json=body)
  elif params:
    resp = requests.get(endpoint, params=urllib.parse.urlencode(params, quote_via=urllib.parse.quote, safe='+'))
  else:
    resp = requests.get(endpoint)
  
  if verbose:
    pretty_print_request(resp.request)
  
  assert resp.status_code == 200, endpoint + " failed with status: " + str(resp.status_code)
  
  if deserialize_response == "json":
    return json.loads(resp.content.decode('utf-8'))
  else:
    return resp.content

class OpenFdaManager:

  def __init__(self):
    # Note: There are noisy dates in the system so let's just look at the last 10 years
    end_dt     = datetime.now()
    end_date   = end_dt.strftime('%Y%m%d')
    start_date = f'{end_dt.year - 10}{end_dt.month}{end_dt.day}'
    self.date_range = f'[{start_date}+TO+{end_date}]'
    
    self.key = 't3q7Qu8xU4PFs5l8A7f8wZHVejkUu8g0zXguh7yC'
    self.uri = 'https://api.fda.gov/'
    self.method = 'drug/event.json'

    self.s = {
      'p': {
        'r': 'patient.reaction.reactionmeddrapt',
        'ro': 'patient.reaction.reactionoutcome'
      },
      'd': {
        'mn': 'patient.drug.openfda.manufacturer_name',
        'bn': 'patient.drug.openfda.brand_name',
        'bne': 'patient.drug.openfda.brand_name.exact',
        'gn': 'patient.drug.openfda.generic_name'
      },
      'rd': 'receivedate',
      'c': 'occurcountry',
      '&': '+AND+'
    }

  def get_adverse_report_counts_for(self, company_name=None, verbose=False):
    """
    Get the number of adverse events reported for a given company or all
    adverse events if no company is provided.
    
    Arguments
    ---------
    company_name : (Optional) string
    """
    params = {
      'api_key' : self.key,
      'search'  : self.s['rd']+f':{self.date_range}',
      'sort'    : self.s['rd']+':asc',
      'count'   : self.s['rd']
    }

    if company_name is not None:
      params['search'] = params['search']+self.s['&']+self.s['d']['mn']+f':"{company_name}"'
    
    resp = call_endpoint(self.uri, self.method, deserialize_response='json', verbose=verbose, params=params)
    return resp['results']

  def get_top_countries_for(self, company_name, limit, verbose=False):
    """
    Get top countries reporting adverse events for given company.
    
    Arguments
    ---------
    company_name : string
    
    limit : int
          Number of top countries to return
    """
    params = {
      'api_key' : self.key,
      'search'  : (self.s['rd']+f':{self.date_range}'
                  +self.s['&']+self.s['d']['mn']+f':"{company_name}"'),
      'count'   : self.s['c']+'.exact',
      'sort'    : self.s['c']+'.exact:desc',
      'limit'   : limit
    }

    resp = call_endpoint(self.uri, self.method, deserialize_response='json', verbose=verbose, params=params)
    return resp['results']
  
  def get_top_generic_drugs_for(self, company_name, countries, limit, verbose=False):
    """
    Get top generic drug adverse reactions for given company and a list
    of countries
    
    Arguments
    ---------
    company_name : string
    
    countries : Array of string
              A array containing alpha2 codes for countries
    
    limit : int
          Number of top generic drugs to return per country
    
    Returns
    -------
    Dictionary of objects
    Key   : country code
    Value : array of dictionary of type: { 'term': generic drug, 'count': count }
    """
    result = {}
    for country in countries:
      params = {
        'api_key' : self.key,
        'search'  : (self.s['rd']+f':{self.date_range}'
                    +self.s['&']+self.s['d']['mn']+f':"{company_name}"'
                    +self.s['&']+self.s['c']+f'.exact:"{country}"'),
        'count'   : self.s['d']['gn']+'.exact',
        'sort'    : self.s['d']['gn']+'.exact:desc',
        'limit'   : limit
      }
      resp = call_endpoint(self.uri, self.method, deserialize_response='json', verbose=verbose, params=params)
      result[country] = resp['results']
    return result
  
  def get_top_patient_reactions_for(self, company_name, drug, countries, limit, verbose=False):
    """
    Get top patient adverse reactions for given company, drug and a list
    of countries
    
    Arguments
    ---------
    company_name : string
    
    drug : string
    
    countries : Array of string
              A array containing alpha2 codes for countries
    
    limit : int
          Number of top drug adverse reactions to return per country
    
    Returns
    -------
    Dictionary of objects
    Key   : country code
    Value : array of dictionary of type: { 'term': adverse reaction, 'count': count }
    """
    result = {}
    for country in countries:
      params = {
        'api_key' : self.key,
        'search'  : (self.s['rd']+f':{self.date_range}'
                    +self.s['&']+self.s['d']['mn']+f':"{company_name}"'
                    +self.s['&']+self.s['c']+f'.exact:"{country}"'
                    +self.s['&']+self.s['d']['gn']+f'.exact:"{drug}"'),
        'count'   : self.s['p']['r']+'.exact',
        'sort'    : self.s['p']['r']+'.exact:desc',
        'limit'   : limit
      }
      resp = call_endpoint(self.uri, self.method, deserialize_response='json', verbose=verbose, params=params)
      result[country] = resp['results']
    return result
