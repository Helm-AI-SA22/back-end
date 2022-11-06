SCOPUS_SITE = 'https://api.elsevier.com/content/search/scopus'
SCOPUS_API_KEY = '3e68f6817fc5ecd448df31067d4bd08a'
SCOPUS_COUNT = 10
SCOPUS_HEADERS = 'apiKey=' + SCOPUS_API_KEY + '&httpAccept=application/json&view=COMPLETE' + '&count=' + str(SCOPUS_COUNT)

IEEE_API_KEY = '5tn9eufwb5f2j8wm3ed9esaj'
IEEE_SITE = 'https://ieeexploreapi.ieee.org/api/v1/search/articles'
IEEE_HEADERS = 'apikey=' + IEEE_API_KEY

AI_URL_DEPLOY = "helmai"
AI_PORT_DEPLOY = 5000

AI_URL = "http://helmai"
AI_PORT = 5000
