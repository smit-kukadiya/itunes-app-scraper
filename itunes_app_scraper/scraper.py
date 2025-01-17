"""
iTunes App Store Scraper
"""
import requests
import json
import time
import re
import os
from datetime import datetime
from typing import List
from lxml import html

from urllib.parse import quote_plus
from itunes_app_scraper.util import AppStoreException, AppStoreCollections, AppStoreCategories, AppStoreMarkets, COUNTRIES

class Regex:
	STARS = re.compile(r"<span class=\"total\">[\s\S]*?</span>")


class AppStoreScraper:
	"""
	iTunes App Store scraper

	This class implements methods to retrieve information about iTunes App
	Store apps in various ways. The methods are fairly straightforward. Much
	has been adapted from the javascript-based app-store-scraper package, which
	can be found at https://github.com/facundoolano/app-store-scraper.
	"""

	def get_app_ids_for_query(self, term, num=50, page=1, country="us", lang="nl", timeout=2, headers={
                                                                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
                                                                    }):
		"""
		Retrieve suggested app IDs for search query

		:param str term:  Search query
		:param int num:  Amount of items to return per page, default 50
		:param int page:  Amount of pages to return
		:param str country:  Two-letter country code of store to search in,
		                     default 'us'
		:param str lang:  Language code to search with, default 'en'

		:return list:  List of App IDs returned for search query
		"""
		if term is None or term == "":
			raise AppStoreException("No term was given")

		url = "https://search.itunes.apple.com/WebObjects/MZStore.woa/wa/search?clientApplication=Software&media=software&term="
		url += quote_plus(term)

		amount = int(num) * int(page)

		country = self.get_store_id_for_country(country)
		headers = {
			"X-Apple-Store-Front": "%s,24 t:native" % country,
			"Accept-Language": lang
		}

		try:
			result = requests.get(url, headers=headers, timeout=timeout).json()
		except ConnectionError as ce:
			raise AppStoreException("Cannot connect to store: {0}".format(str(ce)))
		except json.JSONDecodeError:
			raise AppStoreException("Could not parse app store response")

		return [app["id"] for app in result["bubbles"][0]["results"][:amount]]

	def get_app_ids_for_collection(self, collection="", category="", num=50, country="us", lang=""):
		"""
		Retrieve app IDs in given App Store collection

		Collections are e.g. 'top free iOS apps'.

		:param str collection:  Collection ID. One of the values in
		                        `AppStoreCollections`.
		!!!DO NOT USE!!! :param int category:  Category ID. One of the values in
		                      AppStoreCategories. Can be left empty. !!!DO NOT USE!!!
		:param int num:  Amount of results to return. Defaults to 50.
		:param str country:  Two-letter country code for the store to search in.
		                     Defaults to 'us'.
		:param str lang: Dummy argument for compatibility. Unused.

		:return:  List of App IDs in collection.
		"""
		if not collection:
			collection = AppStoreCollections.TOP_FREE_IOS

		country = self.get_store_id_for_country(country)
		params = (collection, category, num, country)
		url = "http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/%s/%s/limit=%s/json?s=%s" % params

		try:
			result = requests.get(url).json()
		except json.JSONDecodeError:
			raise AppStoreException("Could not parse app store response")

		return [entry["id"]["attributes"]["im:id"] for entry in result["feed"]["entry"]]

	def get_app_ids_for_developer(self, developer_id, country="us", lang=""):
		"""
		Retrieve App IDs linked to given developer

		:param int developer_id:  Developer ID
		:param str country:  Two-letter country code for the store to search in.
		                     Defaults to 'us'.
		:param str lang: Dummy argument for compatibility. Unused.

		:return list:  List of App IDs linked to developer
		"""
		url = "https://itunes.apple.com/lookup?id=%s&country=%s&entity=software" % (developer_id, country)

		try:
			result = requests.get(url).json()
		except json.JSONDecodeError:
			raise AppStoreException("Could not parse app store response")

		if "results" in result:
			return [app["trackId"] for app in result["results"] if app["wrapperType"] == "software"]
		else:
			# probably an invalid developer ID
			return []

	def get_similar_app_ids_for_app(self, app_id, country="us", lang="en"):
		"""
		Retrieve list of App IDs of apps similar to given app

		This one is a bit special because the response is not JSON, but HTML.
		We extract a JSON blob from the HTML which contains the relevant App
		IDs.

		:param app_id:  App ID to find similar apps for
		:param str country:  Two-letter country code for the store to search in.
		                     Defaults to 'us'.
		:param str lang:  Language code to search with, default 'en'

		:return list:  List of similar app IDs
		"""
		url = "https://itunes.apple.com/us/app/app/id%s" % app_id

		country = self.get_store_id_for_country(country)
		headers = {
			"X-Apple-Store-Front": "%s,32" % country,
			"Accept-Language": lang
		}

		result = requests.get(url, headers=headers).text
		if "customersAlsoBoughtApps" not in result:
			return []

		blob = re.search(r"customersAlsoBoughtApps\":\s*(\[[^\]]+\])", result)
		if not blob:
			return []

		try:
			ids = json.loads(blob[1])
		except (json.JSONDecodeError, IndexError):
			return []

		return ids

	def get_app_details(self, app_id, country="us", lang="", add_ratings=True, flatten=True, sleep=None, force=False):
		"""
		Get app details for given app ID

		:param app_id:  App ID to retrieve details for. Can be either the
		                numerical trackID or the textual BundleID.
		:param str country:  Two-letter country code for the store to search in.
		                     Defaults to 'us'.
		:param str lang: Dummy argument for compatibility. Unused.
		:param bool flatten: The App Store response may by multi-dimensional.
		                     This makes it hard to transform into e.g. a CSV,
		                     so if this parameter is True (its default) the
		                     response is flattened and any non-scalar values
		                     are removed from the response.
		:param int sleep: Seconds to sleep before request to prevent being
						  temporary blocked if there are many requests in a
						  short time. Defaults to None.
		:param bool force:  by-passes the server side caching by adding a timestamp
		                    to the request (default is False)

		:return dict:  App details, as returned by the app store. The result is
		               not processed any further, unless `flatten` is True
		"""
		try:
			app_id = int(app_id)
			id_field = "id"
		except ValueError:
			id_field = "bundleId"

		if force:
			# this will by-pass the serverside caching
			import secrets
			timestamp = secrets.token_urlsafe(8)
			url = "https://itunes.apple.com/lookup?%s=%s&country=%s&entity=software&timestamp=%s" % (id_field, app_id, country, timestamp)
		else:
			url = "https://itunes.apple.com/lookup?%s=%s&country=%s&entity=software" % (id_field, app_id, country)

		try:
			if sleep is not None:
				time.sleep(sleep)
			result = requests.get(url).json()
		except Exception:
			try:
				# handle the retry here.
				# Take an extra sleep as back off and then retry the URL once.
				time.sleep(2)
				result = requests.get(url).json()
			except Exception:
				raise AppStoreException("Could not parse app store response for ID %s" % app_id)

		try:
			app = result["results"][0]
		except (KeyError, IndexError):
			raise AppStoreException("No app found with ID %s" % app_id)


		# 'flatten' app response
		# responses are at most two-dimensional (array within array), so simply
		# join any such values
		if flatten:
			for field in app:
				if isinstance(app[field], list):
					app[field] = ",".join(app[field])
				elif isinstance(app[field], dict):
					app[field] = ", ".join(["%s star: %s" % (key, value) for key,value in app[field].items()])

		if add_ratings:
			try:
				ratings = self.get_app_ratings(app_id, countries=[country])
				app['histogram'] = [value for key, value in ratings.items()]
			except AppStoreException:
				# Return some details
				self._log_error(country, 'Unable to collect ratings for %s' % str(app_id))
				app['histogram'] = None

		# url = f"https://apps.apple.com/{country}/app/id{app_id}"
		# options = {
		# 	'url': url,
		# }
		# response = requests.get(**options)
		# tree = html.fromstring(response.content)
		# summary = tree.xpath("//h2[@class='product-header__subtitle app-header__subtitle']/text()")[0].split("\n")[1].strip()
		# copyright = tree.xpath("//dd[@class='information-list__item__definition information-list__item__definition--copyright']/text()")[0]
		# iap = True if len(tree.xpath("//dt[normalize-space()='In-App Purchases']/text()")) > 0 else False
		# developer_website = tree.xpath("//a[@class='link']/@href")[0] ## require to modify
		# app['summary'] = summary
		# app['copyright'] = copyright
		# app['offersIAP'] = iap
		# app['developerWebsite'] = developer_website

		return app

	def get_multiple_app_details(self, app_ids, country="us", lang="", add_ratings=False, sleep=1, force=False):
		"""
		Get app details for a list of app IDs

		:param list app_id:  App IDs to retrieve details for
		:param str country:  Two-letter country code for the store to search in.
		                     Defaults to 'us'.
		:param str lang: Dummy argument for compatibility. Unused.
		:param int sleep: Seconds to sleep before request to prevent being
						  temporary blocked if there are many requests in a
						  short time. Defaults to 1.
		:param bool force:  by-passes the server side caching by adding a timestamp
		                    to the request (default is False)

		:return generator:  A list (via a generator) of app details
		"""
		for app_id in app_ids:
			try:
				yield self.get_app_details(app_id, country=country, lang=lang, add_ratings=add_ratings, sleep=sleep, force=force)
			except AppStoreException as ase:
				self._log_error(country, str(ase))
				continue

	def get_store_id_for_country(self, country="us"):
		"""
		Get store ID for country code

		:param str country:  Two-letter country code
		:param str country:  Two-letter country code for the store to search in.
		                     Defaults to 'us'.
		"""
		country = country.upper()

		if hasattr(AppStoreMarkets, country):
			return getattr(AppStoreMarkets, country)
		else:
			raise AppStoreException("Country code not found for {0}".format(country))

	def get_app_ratings(self, app_id, countries=None, sleep=1):
		"""
		Get app ratings for given app ID

		:param app_id:  App ID to retrieve details for. Can be either the
		                numerical trackID or the textual BundleID.
		:countries:     List of countries (lowercase, 2 letter code) or single country (e.g. 'de')
		                to generate the rating for
		                if left empty, it defaults to mostly european countries (see below)
		:param int sleep: Seconds to sleep before request to prevent being
						  temporary blocked if there are many requests in a
						  short time. Defaults to 1.

		:return dict:  App ratings, as scraped from the app store.
		"""
		dataset = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 }
		if countries is None:
			countries = COUNTRIES
		elif isinstance(countries, str): # only a string provided
			countries = [countries]
		else:
			countries = countries

		for country in countries:
			url = "https://itunes.apple.com/%s/customer-reviews/id%s?displayable-kind=11" % (country, app_id)
			store_id = self.get_store_id_for_country(country)
			headers = { 'X-Apple-Store-Front': '%s,12 t:native' % store_id }

			try:
				if sleep is not None:
					time.sleep(sleep)
				result = requests.get(url, headers=headers).text
			except Exception:
				try:
					# handle the retry here.
					# Take an extra sleep as back off and then retry the URL once.
					time.sleep(2)
					result = requests.get(url, headers=headers).text
				except Exception:
					raise AppStoreException("Could not parse app store rating response for ID %s" % app_id)

			ratings = self._parse_rating(result)

			if ratings is not None:
				dataset[1] = dataset[1] + ratings[1]
				dataset[2] = dataset[2] + ratings[2]
				dataset[3] = dataset[3] + ratings[3]
				dataset[4] = dataset[4] + ratings[4]
				dataset[5] = dataset[5] + ratings[5]

        # debug
		#,print("-----------------------")
		#,print('%d ratings' % (dataset[1] + dataset[2] + dataset[3] + dataset[4] + dataset[5]))
		#,print(dataset)

		return dataset
	
	def get_app_from_collection_category(self, collection: str, category: str, device: str = "iphone", country: str = 'us') -> List[str]:
		"""
		Get the app IDs from a collection and category
		:param str collection: the collection to get the apps, "top-free", "top-paid"
		:param str category: the category to get the apps from AppStoreCategories
		:param str device: the device to get the apps, "iphone", "ipad
		:param str country: the country to get the apps, two letter country code

		:returns List[str] appID: a list of app IDs
		"""

		if hasattr(AppStoreCategories, category):
			category_data = getattr(AppStoreCategories, category)

		url = f"https://apps.apple.com/{country}/charts/{device}/{category_data[0]}/{category_data[1]}?chart={collection}"
		
		options = {
			'url': url,
		}

		response = requests.get(**options)
		tree = html.fromstring(response.content)
		data = tree.xpath('//*[@id="charts-content-section"]/ol/li/a/@href')
		appIDs = [ url.split("/id")[-1] for url in data[:100] ]
		return appIDs
	
	def get_suggestion_from_query(self, query: str, country: str = 'us') -> List[str]:
		if hasattr(AppStoreMarkets, country):
			country = getattr(AppStoreMarkets, country)

		url = "https://search.itunes.apple.com/WebObjects/MZSearchHints.woa/wa/hints?clientApplication=Software&term=" + requests.utils.quote(query)

		headers = {
			'X-Apple-Store-Front': f"{country},29"
		}

		response = requests.get(url, headers=headers)
		response.raise_for_status()
		tree = html.fromstring(response.content)
		data = tree.xpath('//string/text()')
		
		#remove all links from list
		data = [x for x in data if not x.startswith("https://")]

		return data[1:]

	def _parse_rating(self, text):
		matches = Regex.STARS.findall(text)

		if len(matches) != 5:
			# raise AppStoreException("Cant get stars - expected 5 - but got %d" % len(matches))
			return None

		ratings = {}
		star = 5

		for match in matches:
			value = match
			value = value.replace("<span class=\"total\">", "")
			value = value.replace("</span>", "")
			ratings[star] = int(value)
			star = star - 1

		return ratings

	def _log_error(self, app_store_country, message):
		"""
		Write the error to a local file to capture the error.

		:param str app_store_country: the country for the app store
		:param str message: the error message to log
		"""
		log_dir = 'log/'
		if not os.path.isdir(log_dir):
			os.mkdir(log_dir)

		app_log = os.path.join(log_dir, "{0}_log.txt".format(app_store_country))
		errortime = datetime.now().strftime('%Y%m%d_%H:%M:%S - ')
		fh = open(app_log, "a")
		fh.write("%s %s \n" % (errortime,message))
		fh.close()
