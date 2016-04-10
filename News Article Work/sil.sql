CREATE TABLE ArticleMetaData(
article_hash_url VARCHAR(100) NOT NULL,
title TEXT,
publish_date DATE,
onlytext LONGTEXT,
source_id INT,
source_url VARCHAR(200),
exact_url VARCHAR(200),
opinion_section ENUM('yes','no'),
search_text_hash VARCHAR(100),
word_count INT,
analysis_date DATE,
document_sentiment ENUM('positive','negative','neutral'),
pos_on_page INT,
page_number INT,
score FLOAT,
anger FLOAT,
disgust FLOAT,
fear FLOAT,
joy FLOAT,
sadness FLOAT,
PRIMARY KEY (article_hash_url)
);

CREATE TABLE ArticleAuthor(
article_id VARCHAR(100),
author TEXT,
id INT NOT NULL AUTO_INCREMENT,
PRIMARY KEY(id),
FOREIGN KEY (article_id) REFERENCES ArticleMetaData(article_hash_url)
);

CREATE TABLE AlchemyTaxonomy(
article_id VARCHAR(100),
id INT NOT NULL  AUTO_INCREMENT,
taxonomy_label TEXT,
score FLOAT,
confident ENUM('yes','no','NA'),
PRIMARY KEY(id),
FOREIGN KEY (article_id) REFERENCES ArticleMetaData(article_hash_url)
);

CREATE TABLE AlchemyEntity(
article_id VARCHAR(100),
id INT NOT NULL AUTO_INCREMENT,
entity TEXT,
relevance FLOAT,
sentiment ENUM('positive','negative','neutral'),
type TEXT,
dbpedia VARCHAR(200),
PRIMARY KEY(id),
FOREIGN KEY (article_id) REFERENCES ArticleMetaData(article_hash_url)
);

CREATE TABLE AlchemyKeyword(
article_id VARCHAR(100),
id INT NOT NULL AUTO_INCREMENT,
keyword TEXT,
relevance FLOAT,
sentiment ENUM('positive','negative','neutral'),
PRIMARY KEY(id),
FOREIGN KEY (article_id) REFERENCES ArticleMetaData(article_hash_url)
);

CREATE TABLE NewsSource(
id INT NOT NULL AUTO_INCREMENT,
name TEXT,
url VARCHAR(200),
PRIMARY KEY(id)
);

CREATE INDEX pub_date_index ON ArticleMetaData(publish_date);
CREATE INDEX ana_date_index ON ArticleMetaData(analysis_date);
