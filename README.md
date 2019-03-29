# Top 10 Music Chart Worldwide

This application allows list out the latest top 10 songs worldwide just by keying-in the country code of your choice.
Eg. Type-in UK for United Kingdom, US for United States of America, AU for Australia, NZ for New Zealand, FR for France, IT for Italy and etc.

To check out the top 10 songs worldwide just type-in WX.

Besides that, you are also able to compare 2 country charts side-by-side. Just key-in the url as follows:
/?countryA=XX&countryB=YY [where XX is the code for the 1st country and YY is the code for the second country]


## Getting Started

The steps in the first part of this guide will allow you to run the project on your local machine for development and testing, while the steps in the second part will allow you to deploy the application on a live system.


### Prerequisites

The requirements.txt file contains all the packages & modules needed for this app, namely:

```
pip>=9.0.1
Flask==0.12.2
requests
requests_cache
pprint
config
cassandra-driver
```


### PART 1. Development

Steps to get a development environment running for the application are as follows:

1.	Download the musicapp.zip folder (as attached) and unzip it.

2.	Open a terminal and change into the directory of the musicapp folder.

     $ cd Desktop/musicapp

3.	Create a virtual environment with your preferred name.

     $ python3 -m venv flask_venv

     [Note that: the virtual environment here is named flask_venv]

4.	Activate the virtual environment.

     $ source flask_venv/bin/activate

5.	Recursively (-r) installs or updates (-U) the “requirement” packages (modules) that have been specified in the requirements.txt file.

     $ python -m pip install -U -r requirements.txt

6.	Once completed, the app can be run as follows:

     $ python musicapp.py

7.	Right click on the running URL on the terminal upon successful development to open the app.

    eg http://127.0.0.1:8080/


### PART 2. Deployment

Steps to deploy the application within a cloud environment in Google Cloud Platform (GCP) using Cassandra are as follows:

1.	Download the music.zip folder (as attached) and unzip it.

2. "Activate google shell" from the top right corner of GCP Console to open an interactive shell terminal in our browser.

3. Create a subdirectory on the google shell terminal and enter it:

    $ mkdir music && cd music

4. Create a requirements.txt file, a Dockerfile and a python file (for the app) with the nano command and copy the contents.

    $ nano requirements.txt
    $ nano Dockerfile
    $ nano musicapp.py

5. Create Database from CSV file:

  a.3 files under Cassandra Services to be executed are:

    1. cassandra-peer-service.yml: Headless service to get the IP addresses of the Cassandra Nodes
    2. cassandra-replication-controller.yml: Replication Controller
    3. cassandra-service.yml: Service

  b. Check if the container is running correctly

    $ kubectl get pods -l name=cassandra

  c. Copy the test CSV into cassandra pod (to ease the process and save time)

    $ docker cp madb.csv cassandra-{POD NUMBER}:/https://raw.githubusercontent.com/wanargh/musicapp/master/madb.csv/madb.csv

  d. Choose a cassandra pod created and execute the following cqlsh (CQL shell) command line in the chosen pod to add a new keyspace, table and copy the data.

  $ kubectl exec- it cassandra-{POD NUMBER} cqlsh

    cqlsh> CREATE KEYSPACE madb WITH REPLICATION = {'class':'SimpleStrategy','replication_factor':1};
    cqlsh> CREATE TABLE madb.stats (commontrack_id float PRIMARY KEY, track_id float,track_name text,artist_id float, artist_name text, album_id float, album_name text);
    cqlsh> COPY madb.stats (commontrack_id, track_id,track_name,artist_id,artist_name, album_id, album_name) FROM '/home/madb.csv' WITH DELIMITER=','AND HEADER=TRUE;


6. Prepare for cluster deployment

  a. Build docker image and check if it has been created

    $ docker build -t gcr.io/${PROJECT_ID}/musicapp:v1 .
    $ docker images

  b. Push docker image to the Google Cloud Repository, gcr private repository:

    $ docker push gcr.io/${PROJECT_ID}/musicapp:v1

 7. Deploy application

  a. Deploy the application (listening to port 8080) with a deployment name "music-web" and check if the pods has been created

    $ kubectl run web --image=gcr.io/${PROJECT_ID}/musicapp:v1 --port 8080
    $ kubectl get pods

  b. Create a "service" resource (which provides networking and IP support to the application's pods) to expose the cluster to internet

    $ kubectl expose deployment music-web --type=LoadBalancer --port 80 --target-port 8080
    $ kubectl expose deployment web --type=NodePort --target-port 8080


  c. Deploy the Ingress resource: a Kubernetes resource that contains rules and configuration for routing external HTTP(S) traffic to internal services (ie. directs traffic traffic to web service and create HTTP(S) Load Balancer route all external HTTP traffic -port 80 to the web NodePort Service exposed)

   $ wget -O basic.ingress.yaml https://cloud.google.com/kubernetes-engine/docs/tutorials/http-balancer/basic-ingress.yaml
   $ kubectl apply -f basic.ingress.yaml

  d. Get the external IP address assigned to the deployment

    $ kubectl get service


## Build with
1. Cassandra: http://cassandra.apache.org/doc/latest/ - database
2. Flask: http://flask.pocoo.org/docs/1.0/ - web framework
3. MusixMatch: http://musixmatch.com - source of top 10 songs APIs
4. Kubernetes: https://kubernetes.io/docs/home/) - distributed web service


# Author

Zawanah Zianah Zaharen (https://github.com/wanargh)
