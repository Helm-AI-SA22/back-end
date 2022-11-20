import re
from utils.utils import error_log

def rank(documents, criteria="tfidf", ascending=True):

	if not criteria in ["publicationDate", "citationCount", "tfidf"]:
		error_log("Only 'publicationDate', 'tfidf' and 'citationCount' can be used as sorting keys")
	
	if criteria == "tfidf":
		return sorted(documents, key = lambda x: -float(x[criteria]), reverse=ascending)
	elif criteria == "citationCount":
		return sorted(documents, key = lambda x: -int(x[criteria]), reverse=ascending)
	elif criteria == "publicationDate":
		return sorted(documents, key = lambda x: -(int(re.findall(r"(\d{4})", x["publicationDate"])[0])), reverse=ascending)
