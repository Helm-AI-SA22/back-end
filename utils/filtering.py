import pandas as pd
from utils.utils import add_topic_ratio


UNION = 'union'
INTERSECTION = 'intersection'
MODE = 'mode'
ID = 'id'
TOPICS = 'topics'

# mode = 'union' --> OR
# mode = 'intersection' --> AND
def topic_filtering(data_df, topic_dict):
    # OR case
    if topic_dict[MODE] == UNION:
        for i, row in data_df.iterrows():
            drop = True
            for topic in row.topics:
                if topic[ID] in topic_dict[TOPICS]:
                    drop = False
                    break

            if drop:
                data_df.drop(i, inplace=True)  

    # AND case
    elif topic_dict[MODE] == INTERSECTION:
        for i, row in data_df.iterrows():
            for topic in topic_dict[TOPICS]:
                if topic not in [t[ID] for t in row.topics]:
                    data_df.drop(i, inplace=True)  
                    break
                
    return data_df


MIN = 'min'
MAX = 'max'
YEAR = 'year'
PUB_DATE = 'publicationDate'

def date_filtering(data_df, crit):
    # add data_df['year'] column finding 4 digits string in data_df['publicationDate']
    data_df[YEAR] = data_df[PUB_DATE].str.extract('(\d{4})', expand=True).astype(int)
    data_df = data_df[data_df[YEAR] >= crit[MIN]]

    if crit[MAX] != -1:
        data_df = data_df[data_df[YEAR] <= crit[MAX]]

    # drop data_df['year'] column
    data_df.drop(YEAR, axis=1, inplace=True)

    return data_df


AUTHORS = 'authors'

def author_filtering(data_df, crit):
    # drop rows of data_df where crit_string is not in data_df['authors']
    data_df[AUTHORS] = data_df[AUTHORS].str.lower()
    for author in crit:
        print(author)
        data_df = data_df[data_df[AUTHORS].str.contains(author.lower())]

    data_df[AUTHORS] = data_df[AUTHORS].str.title()
    return data_df


CIT_COUNT = 'citationCount'

def citation_filtering(data_df, crit):
    data_df = data_df[data_df[CIT_COUNT] >= crit[MIN]]
    
    if crit[MAX] != -1:
        data_df = data_df[data_df[CIT_COUNT] <= crit[MAX]]

    return data_df

#FILTER FOR PREPRINT DOCUMENT
# null = all documents
# 0 = arxiv (only)
# 1 = non-arxiv only
def arxiv_filtering(data_df, crit):
    if (crit == 1):
        data_df = data_df[data_df[CIT_COUNT] == -1]
    else:
        data_df = data_df[data_df[CIT_COUNT] >= -1]

    return data_df


OPEN_ACCESS = 'openaccess'

#Take documents with 'openaccess' = 'availability' (null for both)
#   null = all documents
#   0 = free access (only)
#   1 = pay access (only)
def availability_filtering(data_df, flag):
    data_df = data_df[data_df[OPEN_ACCESS] == flag]
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
