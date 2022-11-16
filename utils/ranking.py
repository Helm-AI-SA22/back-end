from utils.utils import error_log

def rank(documents, sort_key):

	if not sort_key in ["publicationDate", "citationCount"]:
		error_log("Only 'publicationDate' and 'citationCount' can be used as sorting keys")
	
	return sorted(documents, key = lambda x: -int(x[sort_key]))