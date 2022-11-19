import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from utils.scopus_api import make_scopus_request
from utils.ieee_api import make_ieee_request
from utils.arxiv_api import make_arxiv_request
from utils.utils import debug_log
from utils.AI_request import make_post_request_to_AI
from utils.ranking import rank
from utils.constants import NUMBER_RETURN_PAPERS


def add_topic_paper(topics, papers, doi):
    for paper in papers:
        if paper["id"] == str(doi):
            paper["topics"] = topics

    return papers


def prune_topics(topics, threshold=0.1):
    cleaned_topics = list()

    for topic in topics:
        if topic["affinity"] >= threshold:
            cleaned_topics.append(topic)

    return cleaned_topics


def process_ai_result(ai_result, list_papers):
    documents_result_ai = ai_result.pop("documents")

    for doc in documents_result_ai:
        doi = doc["id"]
        list_papers = add_topic_paper(prune_topics(doc["topics"]), list_papers, doi)

    return list_papers


def format_data_ai(list_papers, key_doi, key_abstract):
    return_list = list()
    
    for paper in list_papers:
        if not paper[key_abstract] is None:

            formatted_paper = dict()

            formatted_paper[key_doi] = paper[key_doi]
            formatted_paper[key_abstract] = paper[key_abstract]

            return_list.append(formatted_paper)
    
    return return_list


def remove_duplicated(results, key):
    memo = set()
    transformed_results = list()
    
    for res in results:
        if not res[key] in memo:
            transformed_results.append(res)
            memo.add(res[key])
        else:
            for doc in transformed_results:
                if doc["id"] == res[key]:
                    doc["source"] += res["source"]


    return transformed_results


def mapping_feature_names(results, start_features, end_features, source):

    transformed_results = list()

    for res in results:
        transformed_results.append({end_features[i]: res[k] for i, k in enumerate(start_features)})
    for doc in transformed_results:
        doc["source"] = [source]

    return transformed_results


def aggregator(ieee_results, scopus_results, arxiv_results):

    with open("aggregation_features.json") as f:
        aggregation_features = json.load(f)

    ieee_transformed_results = mapping_feature_names(ieee_results, aggregation_features["ieee"], aggregation_features["aggregated"], "ieee")
    scopus_transformed_results = mapping_feature_names(scopus_results, aggregation_features["scopus"], aggregation_features["aggregated"], "scopus")
    arxiv_transformed_results = mapping_feature_names(arxiv_results, aggregation_features["arxiv"], aggregation_features["aggregated"], "arxiv")

    results = ieee_transformed_results + scopus_transformed_results + arxiv_transformed_results

    # remove duplicate
    transformed_results = remove_duplicated(results, aggregation_features["aggregated_key"])

    return transformed_results


def format_data_rank(papers, id_feature, title_feature, abstract_feature):
    return_papers = list()

    for paper in papers:
        return_papers.append({
            "id": paper[id_feature], 
            "text" : paper[title_feature] + paper[abstract_feature]
            })
    
    return return_papers


def build_regex(query):

    regex = r"(?u)"

    for keyword in query:
        regex = regex + r"\b" + keyword + r"\b|" # Select the keywords
    
    regex += r"\b\w\w+\b" # Select all single words
    
    return regex


def apply_query_rank(papers, keywords):
    # papers list of of dict {"id": _, "text": _}
    title_abstract_list = list()

    for paper in papers:
        title_abstract_list.append(paper["text"])

    # Inserisci query tra i doc
    title_abstract_list.insert(0, ' '.join(keywords))

    # Calcola tf-idf (with stopword elimination and custom regex to select multi word keywords)
    tfidf = TfidfVectorizer(token_pattern=build_regex(keywords), stop_words='english')

    tfidf_matrix = tfidf.fit_transform(title_abstract_list)

    # Prendi tf-idf corrispondente alla query (prima row)
    tfidf_query = tfidf_matrix[0]

    # Calcola similarity tra tfidf di tutti i doc e tf-idf della query
    pairwise_similarity = tfidf_matrix * tfidf_query.T

    # setta similarity della query con se stessa a 0
    pairwise_similarity[0] = 0

    # converti a array
    np_similarity = pairwise_similarity.toarray()
    np_similarity = np.reshape(np_similarity, ((len(np_similarity))))

    return_dict = dict()

    for tfidf, paper in zip(np_similarity[1:], papers):
        return_dict[paper["id"]] = tfidf

    return return_dict


def process_rank_result(rank_result, list_papers, id_feature):
    # apply tf-idf to the list of papers and sort them
    list_papers.sort(key=lambda paper : rank_result[paper[id_feature]], reverse=True)

    return list_papers


def execute_aggregation_topic_modeling(keywords, topic_modeling):
    
    ieee_results = make_ieee_request(keywords)


    debug_log("ieee done")

    scopus_results = make_scopus_request(keywords)

    debug_log("scopus done")

    arxiv_results = make_arxiv_request(keywords)

    debug_log("arxiv done")

    aggregated_results = aggregator(ieee_results, scopus_results, arxiv_results)
    
    debug_log("aggregation done")

    # take simple subset, to be fast
    # aggregated_results = aggregated_results[:200]

    with open("aggregation_features.json") as f:
        aggregation_features = json.load(f)

    # apply filtering
    # apply ranking, parallelizable wrt call AI module
    data_to_rank = format_data_rank(aggregated_results, aggregation_features["aggregated_key"], aggregation_features["aggregated_title"], aggregation_features["aggregated_abstract"])

    debug_log("formatted to rank done")

    rank_result = apply_query_rank(data_to_rank, keywords)

    debug_log("rank done")

    # call AI module
    data_to_ai = format_data_ai(aggregated_results, aggregation_features["aggregated_key"], aggregation_features["aggregated_abstract"])

    debug_log("formatted to ai done")

    ai_result = make_post_request_to_AI(data_to_ai, topic_modeling)

    debug_log("ai done")

    processed_result = process_ai_result(ai_result, aggregated_results)

    debug_log("processed ai results done")

    processed_result = process_rank_result(rank_result, processed_result, aggregation_features["aggregated_key"])

    debug_log("processed rank results done")

    return {"documents" : processed_result[:NUMBER_RETURN_PAPERS]}