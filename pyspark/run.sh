#!/bin/bash

## copy data
gsutil cp small_page_links.nt gs://pyspark_pig/

## copy PySpark code
gsutil cp pagerank.py gs://pyspark_pig/

## create the cluster 2 workers
gcloud dataproc clusters create cluster-a35a --enable-component-gateway --region europe-west1 --zone europe-west1-c --master-machine-type n1-standard-4 --master-boot-disk-size 500 --num-workers 2 --worker-machine-type n2-standard-2 --worker-boot-disk-size 500 --image-version 2.0-debian10 --project sage-archway-348614

## run
## (suppose that out directory is empty !!)
gcloud dataproc jobs submit pyspark --region europe-west1 --cluster cluster-a35a gs://pyspark_pig/pagerank.py -- gs://public_lddm_data/page_links_en.nt.bz2 3


## access results
gsutil cat gs://pyspark_pig/pyspark_result_*
gsutil cat gs://pyspark_pig/top_pagerank_*

## delete cluster...
gcloud dataproc clusters delete cluster-a35a --region europe-west1
