"""
App Store Scraper utility classes
"""
import json

class AppStoreUtils:
	"""
	Helper class to access the names of the other classes
	"""
	@staticmethod
	def get_entries(clazz_name):
		"""
		Get the members and their names from the function

		:param object clazz_name: the class object be called. 
		:returns object method_names: a JSON representation of the names.
		"""
		methods  = {}
		for collection in dir(clazz_name):
			if not collection.startswith('__'):
				methods[str(collection)] = getattr(clazz_name, str(collection))
		return methods

class AppStoreCollections:
	"""
	App store collection IDs

	Borrowed from https://github.com/facundoolano/app-store-scraper. These are
	the various collections displayed in the app store, usually on the front
	page.
	"""
	TOP_MAC = 'topmacapps' # Not working
	TOP_FREE_MAC = 'topfreemacapps'
	TOP_GROSSING_MAC = 'topgrossingmacapps' # Not working
	TOP_PAID_MAC = 'toppaidmacapps' # Not working
	NEW_IOS = 'newapplications'
	NEW_FREE_IOS = 'newfreeapplications'
	NEW_PAID_IOS = 'newpaidapplications'
	TOP_FREE_IOS = 'topfreeapplications'
	TOP_FREE_IPAD = 'topfreeipadapplications'
	TOP_GROSSING_IOS = 'topgrossingapplications'
	TOP_GROSSING_IPAD = 'topgrossingipadapplications'
	TOP_PAID_IOS = 'toppaidapplications'
	TOP_PAID_IPAD = 'toppaidipadapplications'

class AppStoreCategories:
	"""
	App Store category IDs

	Borrowed from https://github.com/facundoolano/app-store-scraper. These are
	the app's categories.
	"""
	
	APPLE_BOOKS = ["books-apps", 6018]
	APPLE_BUSINESS = ["business-apps", 6000]
	APPLE_CATALOGS = 6022
	APPLE_DEVELOPER_TOOLS = ["developer-tools-apps", 6026]
	APPLE_EDUCATION = ["education-apps", 6017]
	APPLE_ENTERTAINMENT = ["entertainment-apps", 6016]
	APPLE_FINANCE = ["finance-apps", 6015]
	APPLE_FOOD_AND_DRINK = ["food-drink-apps", 6023]
	APPLE_GAMES_FREE = ['top-free-games', 6014]
	APPLE_GAMES_PAID = ['top-paid-games', 6014]
	APPLE_GAMES_ACTION = ["action-games", 7001]
	APPLE_GAMES_ADVENTURE = ["adventure-games", 7002]
	APPLE_GAMES_ARCADE = 7003
	APPLE_GAMES_BOARD = ["board-games", 7004]
	APPLE_GAMES_CARD = ["card-games", 7005]
	APPLE_GAMES_CASINO = ["casino-games", 7006]
	APPLE_GAMES_CASUAL = ["casual-games", 7003]
	APPLE_GAMES_DICE = 7007
	APPLE_GAMES_EDUCATIONAL = 7008
	APPLE_GAMES_FAMILY = ["family-games", 7009]
	APPLE_GAMES_MUSIC = ["music-games", 7011]
	APPLE_GAMES_PUZZLE = ["puzzle-games", 7012]
	APPLE_GAMES_RACING = ["racing-games", 7013]
	APPLE_GAMES_ROLE_PLAYING = ["role-playing-games", 7014]
	APPLE_GAMES_SIMULATION = ["simulation-games", 7015]
	APPLE_GAMES_SPORTS = ["sports-games", 7016]
	APPLE_GAMES_STRATEGY = ["strategy-games", 7017]
	APPLE_GAMES_TRIVIA = ["trivia-games", 7018]
	APPLE_GAMES_WORD = ["word-games", 7019]
	APPLE_GRAPHICS_AND_DESIGN = ["graphics-design-apps", 6027]
	APPLE_HEALTH_AND_FITNESS = ["health-fitness-apps", 6013]
	APPLE_LIFESTYLE = ["lifestyle-apps", 6012]
	APPLE_MAGAZINES_AND_NEWSPAPERS = ["magazines-newspapers-apps", 6021]
	APPLE_MAGAZINES_ARTS = 13007
	APPLE_MAGAZINES_AUTOMOTIVE = 13006
	APPLE_MAGAZINES_WEDDINGS = 13008
	APPLE_MAGAZINES_BUSINESS = 13009
	APPLE_MAGAZINES_CHILDREN = 13010
	APPLE_MAGAZINES_COMPUTER = 13011
	APPLE_MAGAZINES_FOOD = 13012
	APPLE_MAGAZINES_CRAFTS = 13013
	APPLE_MAGAZINES_ELECTRONICS = 13014
	APPLE_MAGAZINES_ENTERTAINMENT = 13015
	APPLE_MAGAZINES_FASHION = 13002
	APPLE_MAGAZINES_HEALTH = 13017
	APPLE_MAGAZINES_HISTORY = 13018
	APPLE_MAGAZINES_HOME = 13003
	APPLE_MAGAZINES_LITERARY = 13019
	APPLE_MAGAZINES_MEN = 13020
	APPLE_MAGAZINES_MOVIES_AND_MUSIC = 13021
	APPLE_MAGAZINES_POLITICS = 13001
	APPLE_MAGAZINES_OUTDOORS = 13004
	APPLE_MAGAZINES_FAMILY = 13023
	APPLE_MAGAZINES_PETS = 13024
	APPLE_MAGAZINES_PROFESSIONAL = 13025
	APPLE_MAGAZINES_REGIONAL = 13026
	APPLE_MAGAZINES_SCIENCE = 13027
	APPLE_MAGAZINES_SPORTS = 13005
	APPLE_MAGAZINES_TEENS = 13028
	APPLE_MAGAZINES_TRAVEL = 13029
	APPLE_MAGAZINES_WOMEN = 13030
	APPLE_MEDICAL = ["medical-apps", 6020]
	APPLE_MUSIC = ["music-apps", 6011]
	APPLE_NAVIGATION = ["navigation-apps", 6010]
	APPLE_NEWS = ["news-apps", 6009]
	APPLE_PHOTO_AND_VIDEO = ["photo-video-apps", 6008]
	APPLE_PRODUCTIVITY = ["productivity-apps", 6007]
	APPLE_REFERENCE = ["reference-apps", 6006]
	APPLE_SHOPPING = ["shopping-apps", 6024]
	APPLE_SOCIAL_NETWORKING = ["social-networking-apps", 6005]
	APPLE_SPORTS = ["sports-apps", 6004]
	APPLE_TRAVEL = ["travel-apps", 6003]
	APPLE_UTILITIES = ["utilities-apps", 6002]
	APPLE_WEATHER = ["weather-apps", 6001]


class AppStoreMarkets:
	"""
	App Store store IDs per country

	Borrowed from https://github.com/facundoolano/app-store-scraper.
	"""
	DZ = 143563
	AO = 143564
	AI = 143538
	AR = 143505
	AM = 143524
	AU = 143460
	AT = 143445
	AZ = 143568
	BH = 143559
	BB = 143541
	BY = 143565
	BE = 143446
	BZ = 143555
	BM = 143542
	BO = 143556
	BW = 143525
	BR = 143503
	VG = 143543
	BN = 143560
	BG = 143526
	CA = 143455
	KY = 143544
	CL = 143483
	CN = 143465
	CO = 143501
	CR = 143495
	HR = 143494
	CY = 143557
	CZ = 143489
	DK = 143458
	DM = 143545
	EC = 143509
	EG = 143516
	SV = 143506
	EE = 143518
	FI = 143447
	FR = 143442
	DE = 143443
	GB = 143444
	GH = 143573
	GR = 143448
	GD = 143546
	GT = 143504
	GY = 143553
	HN = 143510
	HK = 143463
	HU = 143482
	IS = 143558
	IN = 143467
	ID = 143476
	IE = 143449
	IL = 143491
	IT = 143450
	JM = 143511
	JP = 143462
	JO = 143528
	KE = 143529
	KW = 143493
	LV = 143519
	LB = 143497
	LT = 143520
	LU = 143451
	MO = 143515
	MK = 143530
	MG = 143531
	MY = 143473
	ML = 143532
	MT = 143521
	MU = 143533
	MX = 143468
	MS = 143547
	NP = 143484
	NL = 143452
	NZ = 143461
	NI = 143512
	NE = 143534
	NG = 143561
	NO = 143457
	OM = 143562
	PK = 143477
	PA = 143485
	PY = 143513
	PE = 143507
	PH = 143474
	PL = 143478
	PT = 143453
	QA = 143498
	RO = 143487
	RU = 143469
	SA = 143479
	SN = 143535
	SG = 143464
	SK = 143496
	SI = 143499
	ZA = 143472
	ES = 143454
	LK = 143486
	SR = 143554
	SE = 143456
	CH = 143459
	TW = 143470
	TZ = 143572
	TH = 143475
	TN = 143536
	TR = 143480
	UG = 143537
	UA = 143492
	AE = 143481
	US = 143441
	UY = 143514
	UZ = 143566
	VE = 143502
	VN = 143471
	YE = 143571


class AppStoreException(Exception):
	"""
	Thrown when an error occurs in the App Store scraper
	"""
	pass


COUNTRIES = [
    # 'ad', # Andorra
    'at', # Austria
    'be', # Belgium
    'ca', # Canada
    'ch', # Switzerland
    'cy', # Cyprus
    'cz', # Czechia
    'de', # Germany
    'dk', # Denmark
    'ee', # Estonia
    'es', # Spain
    'fi', # Finland
    'fr', # France
    'gb', # Great Britain
    # 'gi', # Gibraltar
    'gr', # Greece
    'hr', # Hungary
    'ie', # Ireland
    # 'im', # Isle of Man
    'is', # Iceland
    'it', # Italy
    'lu', # Luxembourg
    'lv', # Latvia
    # 'mc', # Monaco
    # 'me', # Montenegro
    'mt', # Malta
    'nl', # Netherlands
    'no', # Norway
    'pl', # Poland
    'pt', # Portugal
    'ro', # Romania
    # 'rs', # Serbia
    'se', # Sweden
    'si', # Slovenia
    'sk', # Slovakia
    'sr', # ???
    'tr', # Turkey
    'ua', # Ukraine
    'us', # United States of America
]
