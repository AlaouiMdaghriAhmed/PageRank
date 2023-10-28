#!/usr/bin/python
from org.apache.pig.scripting import Pig
import time

# Original code by Pascal MOLLI
# https://github.com/momo54/large_scale_data_management/blob/main/dataproc.py

INIT = Pig.compile("""
links = LOAD '$input' using PigStorage(' ') as (url:chararray, p:chararray, link:chararray);
distinct_links = DISTINCT links; --Needed to obtain equivalent result as PySpark with distinct, PySpark line 79

grouped_links = GROUP distinct_links by url;                                                                                  
ranked_links = foreach grouped_links generate group as url, 1 as pagerank, distinct_links.link as links;                                 
STORE ranked_links into '$docs_in';
""")

PIG_UPDATE = """
-- PR(A) = (1-d) + d (PR(T1)/C(T1) + ... + PR(Tn)/C(Tn))
previous_pagerank = 
    LOAD '$docs_in' 
    USING PigStorage('\t') 
    AS ( url: chararray, pagerank: double, links:{ link: ( url: chararray ) } );

outbound_pagerank =  
    FOREACH previous_pagerank 
    GENERATE 
        pagerank / COUNT ( links ) AS pagerank, 
        FLATTEN ( links ) AS to_url;

new_pagerank = 
    FOREACH 
        ( COGROUP outbound_pagerank BY to_url, previous_pagerank BY url INNER )
    GENERATE 
        group AS url, 
        ( 1 - $d ) + $d * SUM ( outbound_pagerank.pagerank ) AS pagerank, 
        FLATTEN ( previous_pagerank.links ) AS links;

STORE new_pagerank 
    INTO '$docs_out' 
    USING PigStorage('\t');

"""
UPDATE = Pig.compile(PIG_UPDATE)

PIG_STORE_MAX = """

--Needed to preserve pageranks of TO_URL lost during inner co-grouping
ranks = 
    FOREACH (GROUP outbound_pagerank by to_url)
    GENERATE 
        group, 
        ( 1 - $d ) + $d * SUM ( outbound_pagerank.pagerank ) AS pagerank;

max_pagerank = foreach (group ranks all) {
        ordered = order ranks by pagerank DESC; 
        limited = limit ordered 10; --only keeping top 10 pagerank
        generate flatten(limited);
}

max_pagerank = foreach max_pagerank generate $0,$1;

STORE max_pagerank 
    INTO '$out_top_pagerank' 
    USING PigStorage('\t');
"""
## read the last pagerank
UPDATE_AND_STORE_MAX = Pig.compile(PIG_UPDATE+PIG_STORE_MAX)

gs_bucket = "gs://pyspark_pig"
time_tag = time.strftime("%Y%m%d-%H%M%S")

params = { 'd': '0.85', 'input': 'gs://public_lddm_data/page_links_en.nt.bz2', \
           'docs_in': gs_bucket+'/tmp_pagerank_pig_'+time_tag, \
           'compute_max': True, 'out_top_pagerank': gs_bucket+'/top_pagerank_'+time_tag }
stats = INIT.bind(params).runSingle()
if not stats.isSuccessful():
	raise 'failed initialization'

iterations = 3
for i in range(iterations):
  	out = gs_bucket+"/out_pagerank_pig_" + str(i + 1) +"_"+time_tag
  	params["docs_out"] = out
  	Pig.fs("rmr " + out)
  	if (params["compute_max"] and (i+1)==iterations):
   		stats = UPDATE_AND_STORE_MAX.bind(params).runSingle()
  	else:
   		stats = UPDATE.bind(params).runSingle()		   
  	if not stats.isSuccessful():
   		raise 'failed'
  	params["docs_in"] = out
