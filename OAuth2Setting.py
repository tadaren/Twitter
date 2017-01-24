# -*- coding:utf-8 -*-

import base64
import urllib.parse
import urllib.request
import json

class OAuth2:

	def __init__(self, api_key, api_secret):
		self.bearer_token = get_bearer_token(api_key, api_secret)

	def access(self, url, params):
		req = urllib.request.Request(url+'?'+urllib.parse.urlencode(params))
		req.add_header('Authorization', 'Bearer ' + self.bearer_token)

		response = urllib.request.urlopen(req)
		json_response = json.loads(response.read().decode('utf-8'))

		return json_response

	def get_user_timeline(self, screen_name, count):
		url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'

		params = {'screen_name': screen_name, 'count': count}

		return self.access(url, params)

	def get_trends(self, place, exclude='hashtags'):
		url = 'https://api.twitter/com/1.1/trends/place.json'

		params = {'id': place, 'exclude': exclude}

		return self.access(url, params)

	def search_tweets(self, q, count, geocode=None, lang=None, locale=None, result_type=None, until=None, since_id=None, max_id=None, include_entities=None, callback=None):
		url = 'https://api.twitter.com/1.1/search/tweets.json'

		params = {'q': q, 'count': count}
		if geocode is not None:
			params.update({'geocode': geocode})
		if lang is not None:
			params.update({'lang': lang})
		if locale is not None:
			params.update({'locale': locale})
		if result_type is not None:
			params.update({'result_type': result_type})
		if until is not None:
			params.update({'until': until})
		if since_id is not None:
			params.update({'since_id': since_id})
		if max_id is not None:
			params.update({'max_id': max_id})
		if include_entities is not None:
			params.update({'include_entities': include_entities})
		if callback is not None:
			params.update({'callback': callback})

		return self.access(url, params)


def get_bearer_token(api_key, api_secret):
	url = 'https://api.twitter.com/oauth2/token'

	token_credential = urllib.parse.quote(api_key) + ':' + urllib.parse.quote(api_secret)
	credential = 'Basic ' + base64.b64encode(bytes(token_credential, "utf-8")).decode("utf-8")
	params = {'grant_type': 'client_credentials'}
	data = urllib.parse.urlencode(params).encode('ascii')

	req = urllib.request.Request(url)
	req.add_header('Authorization', credential)
	req.add_header('Content-Type', 'application/x-www-form-urlencoded;charset=UTF-8')

	response = urllib.request.urlopen(req, data)
	print(response.status)
	json_response = json.loads(response.read().decode('utf-8'))
	access_token = json_response['access_token']
	return access_token
