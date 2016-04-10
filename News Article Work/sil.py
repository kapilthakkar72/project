from alchemyapi import AlchemyAPI
from client import DiffbotClient
from config import API_TOKEN
import MySQLdb
import time
import json
import pandas as pd
import time
import datetime
##Globals##
####Urls
csv_file = 'output.csv'
df_urls = pd.read_csv(csv_file)

####Alchemy object
alchemyapi = AlchemyAPI()

####Diffbot object
diffbot = DiffbotClient()
token = API_TOKEN
api = "article"

####MySQLdb cursor
db = MySQLdb.connect(host="localhost",user="root",passwd="yoyo",db="sil_new",charset="utf8")
cursor = db.cursor()
####Article Globals
meta_author = ''#to be used in set_author table
meta_text = '' #to be used with alchemy

def set_meta_table(article_hash,opinion_section,source_id,search_text_hash,exact_url,page_number,pos_on_page):
    
    print('')
    print "## running diffbot!"
    response = diffbot.request(exact_url,token,api,timeout=50000)
    #print type(response)

    print "## diffbot parsing done!"
    onlytext,author = '',''
    if 'objects' in response.keys():
        parsed_objects = response['objects']
    else:
        print "Cannot parse for - {}".format(exact_url)
        return onlytext,author

    for p in parsed_objects:
        title = p['title']
        onlytext = p['text']
        html = p['html']
        if 'author' in p.keys():
            author = p['author'] #how multiple authors represented???
        publish_date = p['date']


    word_count = len(onlytext.strip().split())
    analysis_date = time.asctime(time.localtime(time.time()))

    print "## Running alchemyapi"  
    response = alchemyapi.sentiment('text',onlytext)
    if response['status'] == "OK":
        document_sentiment =  response['docSentiment']['type']
        print "##Document Sentiment - {}".format(document_sentiment)
        score = 0.0
        if 'score' in response['docSentiment']:
            score = response['docSentiment']['score']
            print "##Score - {}".format(score)

        source_url = exact_url #Why need this field???
        analysis_fmt = "%a %b %d %H:%M:%S %Y"
        publish_fmt = "%a, %d %b %Y %H:%M:%S %Z"
        analysis_datetime = datetime.datetime.strptime(analysis_date,analysis_fmt)
        publish_datetime =  datetime.datetime.strptime(publish_date,publish_fmt)


        sql_query = "insert into ArticleMetaData( \
                    article_hash_url , title, publish_date,\
                    onlytext, source_id, source_url, exact_url, \
                    opinion_section,search_text_hash, word_count, \
                    analysis_date, document_sentiment,pos_on_page,\
                    page_number, score) values " 

        query_fmt ="(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        query = sql_query + query_fmt
        t = (article_hash_url,title,publish_datetime,\
                onlytext,source_id, source_url, exact_url, opinion_section,\
                search_text_hash,word_count,analysis_datetime, \
                document_sentiment,pos_on_page,page_number,score)
        print "##Printing query -"
        print query%t

        try:
            print " "
            print "## Writing to DB----"
            cursor.execute(query,(article_hash_url,title,publish_datetime,\
                    onlytext,source_id, source_url, exact_url, opinion_section,\
                    search_text_hash,word_count,analysis_datetime, \
                    document_sentiment,pos_on_page,page_number,score))
            db.commit()
            print "## DB Write success!! "
        except Exception,e:
            print "## DB write failed!!"
            print repr(e)
            db.rollback()
            exit(5)

    else:
        print('Error in sentiment call: ', response['statusInfo'])
        exit(10)


    return onlytext,author


def set_entity_table(article_id,demo_text):
    
    print('')
    print "**setting entity table**"
    response = alchemyapi.entities('text', demo_text, {'sentiment': 1})
    if response['status'] == 'OK':

        print('## Entities ##')
        for entity in response['entities']:
            print('article_id:',article_id)
            text = entity['text'].encode('utf-8')
            print('text: ', text)
            e_type = entity['type']
            print('type: ', e_type)
            relevance = entity['relevance']
            print('relevance: ',relevance )
            sentiment_type = entity['sentiment']['type']
            print('sentiment: ', sentiment_type)
            sentiment_score =0.0
            if 'score' in entity['sentiment']:
                sentiment_score = entity['sentiment']['score']
                print('sentiment score: ' + sentiment_score)
            dbpedia = ''
            if 'disambiguated' in entity.keys():
                dbpedia = entity['disambiguated']['dbpedia']
            print('')

            sql_query = "insert into AlchemyEntity( \
                    article_id , entity, relevance,\
                    sentiment, type, dbpedia) values " 

            query_fmt ="(%s,%s,%s,%s,%s,%s)"
            query = sql_query + query_fmt
            try:
                print "## Writing to DB----"
                cursor.execute(query,(article_id,text,relevance,sentiment_type,\
                                e_type,dbpedia))
                db.commit()
                print "## DB Write success!! "
            except Exception,e:
                print "## DB write failed!!"
                print repr(e)
                db.rollback()
                exit(4)
    else:
        print('Error in entity extraction call: ', response['statusInfo'])

    return


def set_keyword_table(article_id,demo_text):
    
    print('')
    print "**setting keyword table**"
    response = alchemyapi.keywords('text', demo_text, {'sentiment': 1})
    if response['status'] == 'OK':

        print('## Keywords ##')
        for keyword in response['keywords']:
            print('article_id:',article_id)
            text = keyword['text'].encode('utf-8')
            print('text: ', text)
            relevance = keyword['relevance']
            print('relevance: ',relevance )
            sentiment_type = keyword['sentiment']['type']
            print('sentiment: ', sentiment_type)
            sentiment_score =0.0
            if 'score' in keyword['sentiment']:
                sentiment_score = keyword['sentiment']['score']
                print('sentiment score: ' + sentiment_score)
            print('')

            sql_query = "insert into AlchemyKeyword( \
                    article_id , keyword, relevance,\
                    sentiment) values " 

            query_fmt ="(%s,%s,%s,%s)"
            query = sql_query + query_fmt
            try:
                print "## Writing to DB----"
                cursor.execute(query,(article_id,text,relevance,sentiment_type))
                db.commit()
                print "## DB Write success!! "
            except Exception,e:
                print "## DB write failed!!"
                print repr(e)
                db.rollback()
                exit(3)
    else:
        print('Error in keyword extraction call: ', response['statusInfo'])

    return

def set_taxonomy_table(article_id,demo_text):
    
    print('')
    print "**setting taxonomy table**"
    response = alchemyapi.taxonomy('text', demo_text)
    if response['status'] == 'OK':

        print('## Taxonomy ##')
        for category in response['taxonomy']:
            print('article_id:',article_id)
            taxonomy_label = category['label']
            print('label: ', taxonomy_label)
            score = category['score']
            print('score: ',score )
            confident = ''
            if 'confident' in category.keys():
                confident = category['confident']
                print('confident:',confident)

            print('')

            sql_query = "insert into AlchemyTaxonomy( \
                    article_id , taxonomy_label, score, confident) values " 

            query_fmt ="(%s,%s,%s,%s)"
            query = sql_query + query_fmt
            try:
                print "## Writing to DB----"
                cursor.execute(query,(article_id,taxonomy_label, score,confident))
                db.commit()
                print "## DB Write success!! "
            except Exception,e:
                print "## DB write failed!!"
                print repr(e)
                db.rollback()
                exit(2)
    else:
        print('Error in taxonomy call: ', response['statusInfo'])

    return

def set_author_table(article_id,author):
    
    print('')
    print "**setting author table**"

    print('## Author ##')
    print('article_id:',article_id)
    print('author:',author)
    print('')

    sql_query = "insert into ArticleAuthor( \
            article_id , author) values " 

    query_fmt ="(%s,%s)"
    query = sql_query + query_fmt
    try:
        print "## Writing to DB----"
        cursor.execute(query,(article_id,author))
        db.commit()
        print "## DB Write success!! "
    except Exception,e:
        print "## DB write failed!!"
        print repr(e)
        db.rollback()
        exit(1)

    return

if __name__ == "__main__":

        for i,r in df_urls.iterrows():
            ####Taken from csv
            print "processing Index: {} of 621".format(r['index'])
            article_hash_url = r['article_hash_url']
            page_number = r['page_number']
            pos_on_page = r['pos_on_page']
            page_number = r['page_number']
            opinion_section = r['opinion_section']
            source_id = r['source_id']
            search_text_hash = 'npa'
            exact_url = r['exact_url']
            print ("Print exact_url:",exact_url)
            #### Taken from csv

            meta_text,meta_author = set_meta_table(article_hash_url,opinion_section,source_id,search_text_hash,exact_url,page_number,pos_on_page)
            if meta_text == '':
                print "No parsed content from diffbot! Moving to next record. Index: {}".format(r['index'])
                exit(1)
            #set_entity_table(article_hash_url,meta_text)
            #set_keyword_table(article_hash_url,meta_text)
            #set_taxonomy_table(article_hash_url,meta_text)
            #set_author_table(article_hash_url,meta_author)

	db.close()
