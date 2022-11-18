from utils.utils import error_log

def rank(documents, sort_key):

	if not sort_key in ["publicationDate", "citationCount", "tfidf"]:
		error_log("Only 'publicationDate', 'tfidf' and 'citationCount' can be used as sorting keys")
	
	if sort_key == "tfidf":
		return sorted(documents, key = lambda x: -float(x[sort_key]))
	elif sort_key == "citationCount":
		return sorted(documents, key = lambda x: -int(x[sort_key]))
	elif sort_key == "publicationDate":
		return sorted(documents, key = lambda x: -(int(re.findall(r"(\d{4})", x["publicationDate"])[0])))
