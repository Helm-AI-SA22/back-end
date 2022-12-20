import pandas as pd
from utils.utils import add_topic_ratio

MIN = 'min'
MAX = 'max'

UNION = 'union'
INTERSECTION = 'intersection'


# mode = 'union' --> OR
# mode = 'intersection' --> AND
def topic_filtering(data_df, topic_dict):
    # OR case
    if topic_dict["mode"] == UNION:
        for i, row in data_df.iterrows():
            drop = True
            for topic in row.topics:
                if topic['id'] in topic_dict["topics"]:
                    drop = False
                    break

            if drop:
                data_df.drop(i, inplace=True)  

    # AND case
    elif topic_dict["mode"] == INTERSECTION:
        for i, row in data_df.iterrows():
            for topic in topic_dict["topics"]:
                if topic not in [t['id'] for t in row.topics]:
                    data_df.drop(i, inplace=True)  
                    break
                
    return data_df


def date_filtering(data_df, crit):
    # add data_df['year'] column finding 4 digits string in data_df['publicationDate']
    data_df['year'] = data_df['publicationDate'].str.extract('(\d{4})', expand=True).astype(int)
    data_df = data_df[data_df['year'] >= crit[MIN]]

    if crit[MAX] != -1:
        data_df = data_df[data_df['year'] <= crit[MAX]]

    # drop data_df['year'] column
    data_df.drop('year', axis=1, inplace=True)

    return data_df


def author_filtering(data_df, crit):
    # drop rows of data_df where crit_string is not in data_df['authors']
    data_df['authors']=data_df['authors'].str.lower()
    for author in crit:
        print(author)
        data_df = data_df[data_df['authors'].str.contains(author.lower())]
    data_df['authors']=data_df['authors'].str.title()
    return data_df


def citation_filtering(data_df, crit):
    data_df = data_df[data_df['citationCount'] >= crit[MIN]]
    
    if crit[MAX] != -1:
        data_df = data_df[data_df['citationCount'] <= crit[MAX]]

    return data_df

#FILTER FOR PREPRINT DOCUMENT
# null = all documents
# 0 = arxiv (only)
# 1 = non-arxiv only
def arxiv_filtering(data_df, crit):
    if (crit == 1):
        data_df = data_df[data_df['citationCount'] == -1]
    else:
        data_df = data_df[data_df['citationCount'] >= -1]

    return data_df

#Take documents with 'openaccess' = 'availability' (null for both)
#   null = all documents
#   0 = free access (only)
#   1 = pay access (only)
def availability_filtering(data_df, flag):
    data_df = data_df[data_df['openaccess'] == flag]
    return data_df


filtering_functions = {
    "topic": topic_filtering,
    "date": date_filtering,
    "authors": author_filtering,
    "citationCount": citation_filtering,
    "availability": availability_filtering,
    "arxiv": arxiv_filtering
}


def filtering(data_dict):
    criteria = data_dict["criteria"]

    # convert data_dict[ "documents" ] to dataframe
    data_df = pd.DataFrame(data_dict["documents"])

    # print(data_df.info())
    
    for key in criteria:
        # print(f"key: {key}; criteria: {criteria[key]}")
        if (criteria[key] is not None):
            data_df = filtering_functions[key](data_df, criteria[key])
    
    # convert data_df to dictionary
    documents = data_df.to_dict(orient='records')
    
    # drop criteria from data_dict
    data_dict.pop("criteria")
    data_dict["documents"] = documents
    
    data_dict = add_topic_ratio(data_dict)

    return data_dict
