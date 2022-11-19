from keys import SCOPUS_API_KEY, IEEE_API_KEY

SCOPUS_SITE = 'https://api.elsevier.com/content/search/scopus'
SCOPUS_COUNT = 25
SCOPUS_MAX_COUNT = 25
SCOPUS_HEADERS = 'apiKey=' + SCOPUS_API_KEY + '&httpAccept=application/json&view=COMPLETE' + '&count=' + str(SCOPUS_COUNT)

IEEE_SITE = 'https://ieeexploreapi.ieee.org/api/v1/search/articles'
IEEE_HEADERS = 'apikey=' + IEEE_API_KEY

ARXIV_SITE = "http://export.arxiv.org/api/query"
ARXIV_MAX_RESULTS = 20

AI_URL_DEPLOY = "helmai"
AI_PORT_DEPLOY = 5000

AI_URL = "http://172.17.0.3"
AI_PORT = 5000

STARTING_STRING_SCOPUS = "KEY%28"
ENDING_STRING_SCOPUS = "%29"

SPACE_IEEE = "%20"
QUOTES_IEEE = "%22"

NUMBER_RETURN_PAPERS = 100