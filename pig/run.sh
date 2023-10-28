#!/bin/bash

## En local ->
## pig -x local -
## pig -embedded jython dataproc.py

## copy data
gsutil cp small_page_links.nt gs://pyspark_pig/

## copy PySpark code
gsutil cp dataproc.py gs://pyspark_pig/

## Clean out directory
gsutil rm -rf gs://pyspark_pig/out

## create the cluster 2 workers
gcloud dataproc clusters create cluster-a35a --enable-component-gateway --region europe-west1 --zone europe-west1-c --master-machine-type n2-standard-2 --master-boot-disk-size 500 --num-workers 2 --worker-machine-type n1-standard-4 --worker-boot-disk-size 500 --image-version 2.0-debian10 --project sage-archway-348614

## run
## (suppose that out directory is empty !!)
gcloud dataproc jobs submit pig --region europe-west1 --cluster cluster-a35a -f gs://pyspark_pig/dataproc.py

## access results
gsutil cat gs://pyspark_pig/out*

## delete cluster...
gcloud dataproc clusters delete cluster-a35a --region europe-west1
