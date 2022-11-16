from utils.utils import error_log

def rank(documents, sort_key):

	if not sort_key in ["publicationDate", "citationCount", "tfidf"]:
		error_log("Only 'publicationDate', 'tfidf' and 'citationCount' can be used as sorting keys")
	
	return sorted(documents, key = lambda x: -int(x[sort_key]))
