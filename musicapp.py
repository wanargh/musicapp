from flask import Flask, render_template, request, jsonify #flask python microframework
import json #Python built-in module, no need to pip install
import requests #Python module that facilitates sending HTTP requests to REST APIs from app
import requests_cache #transparent persistent cache for requests module
from pprint import pprint
from cassandra.cluster import Cluster

requests_cache.install_cache('music_cache', backend='sqlite', expire_after=36000) #to cache previous requests on our server based on these configurations :filename/backend/expiration time in seconds

cluster = Cluster(['cassandra']) 
session = cluster.connect()
app = Flask(__name__,instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py') #in this order so that the variables from instance/config.py overrides values in config.py

music_url_template = 'https://api.musixmatch.com/ws/1.1/chart.tracks.get?apikey={API_KEY}&chart_name={chart_name}&page={page}&page_size={page_size}&country={country}&f_has_lyrics={f_has_lyrics}'
#source of API:www.musixmatch.com

@app.route('/404/')
def not_found():
    return render_template('404.html'),404

@app.route("/")
def home():
    countryA = request.args.get('countryA')
    top10dataA = get_top10dataA(countryA)
    countryB = request.args.get('countryB')
    top10dataB = get_top10dataB(countryB)
    return render_template("musichome.html",top10dataA=top10dataA,top10dataB=top10dataB)
    
@app.route('/top10dataA/<countryA>', methods=['GET']) #a decorator for the function below (dont skip line!)- function that should be called when a request on that path arrives
def get_top10dataj1(countryA): #GET: to retrieve info!
        #list of parameters to get the top 10 from countryA chart
        my_chart_name = request.args.get('chart_name','top')
        my_page = request.args.get('page','1')
        my_page_size = request.args.get('page_size','10')
        my_country = request.args.get('countryA','')
        my_has_lyrics = request.args.get('f_has_lyrics','1')

        #request template
        music_url = music_url_template.format(API_KEY=app.config['MY_API_KEY'],chart_name=my_chart_name,page=my_page,page_size=my_page_size,country=my_country,f_has_lyrics=my_has_lyrics )
        top10songs={}
        top10artists={}
        resp = requests.get(music_url)
        if resp.ok:
                top10dataA = resp.json()
        else:
                print(resp.reason)
        return jsonify(top10dataA)

@app.route('/top10dataA/', methods=['GET']) #a decorator for the function below (dont skip line!)- function that should be called when a request on that path arrives
def get_top10dataA(countryA): #GET: to retrieve info!
        #list of parameters to get the top 10 from countryA chart
        my_chart_name = request.args.get('chart_name','top')
        my_page = request.args.get('page','1')
        my_page_size = request.args.get('page_size','10')
        my_country = request.args.get('countryA','')
        my_has_lyrics = request.args.get('f_has_lyrics','1')

        #request template
        music_url = music_url_template.format(API_KEY=app.config['MY_API_KEY'],chart_name=my_chart_name,page=my_page,page_size=my_page_size,country=my_country,f_has_lyrics=my_has_lyrics )
        top10songs={}
        top10artists={}
        resp = requests.get(music_url)

        if resp.ok:
                top10data = resp.json() #chart function defined earlier return the (serialised) resource in JSON format
                top10songs['1st']= top10data['message']['body']['track_list'][0]['track']['track_name']
                top10songs['2nd']= top10data['message']['body']['track_list'][1]['track']['track_name']
                top10songs['3rd']= top10data['message']['body']['track_list'][2]['track']['track_name']
                top10songs['4th']= top10data['message']['body']['track_list'][3]['track']['track_name']
                top10songs['5th']= top10data['message']['body']['track_list'][4]['track']['track_name']
                top10songs['6th']= top10data['message']['body']['track_list'][5]['track']['track_name']
                top10songs['7th']= top10data['message']['body']['track_list'][6]['track']['track_name']
                top10songs['8th']= top10data['message']['body']['track_list'][7]['track']['track_name']
                top10songs['9th']= top10data['message']['body']['track_list'][8]['track']['track_name']
                top10songs['10th']= top10data['message']['body']['track_list'][9]['track']['track_name']

                top10artists['1st']= top10data['message']['body']['track_list'][0]['track']['artist_name']
                top10artists['2nd']= top10data['message']['body']['track_list'][1]['track']['artist_name']
                top10artists['3rd']= top10data['message']['body']['track_list'][2]['track']['artist_name']
                top10artists['4th']= top10data['message']['body']['track_list'][3]['track']['artist_name']
                top10artists['5th']= top10data['message']['body']['track_list'][4]['track']['artist_name']
                top10artists['6th']= top10data['message']['body']['track_list'][5]['track']['artist_name']
                top10artists['7th']= top10data['message']['body']['track_list'][6]['track']['artist_name']
                top10artists['8th']= top10data['message']['body']['track_list'][7]['track']['artist_name']
                top10artists['9th']= top10data['message']['body']['track_list'][8]['track']['artist_name']
                top10artists['10th']= top10data['message']['body']['track_list'][9]['track']['artist_name']
                top10dataA=(top10songs['1st'],top10artists['1st'],top10songs['2nd'],top10artists['2nd'],top10songs['3rd'],top10artists['3rd'],top10songs['4th'],top10artists['4th'],top10songs['5th'],top10artists['5th'],top10songs['6th'],top10artists['6th'],top10songs['7th'],top10artists['7th'],top10songs['8th'],top10artists['8th'],top10songs['9th'],top10artists['9th'],top10songs['10th'],top10artists['10th'])
        else:
                print(resp.reason)
        return (top10dataA)
        
@app.route('/top10dataB/<countryB>', methods=['GET']) #a decorator for the function below (dont skip line!)- function that should be called when a request on that path arrives
def get_top10dataj2(countryB): #GET: to retrieve info!
        #list of parameters to get the top 10 from countryA chart
        my_chart_name = request.args.get('chart_name','top')
        my_page = request.args.get('page','1')
        my_page_size = request.args.get('page_size','10')
        my_country = request.args.get('countryB','')
        my_has_lyrics = request.args.get('f_has_lyrics','1')

        #request template
        music_url = music_url_template.format(API_KEY=app.config['MY_API_KEY'],chart_name=my_chart_name,page=my_page,page_size=my_page_size,country=my_country,f_has_lyrics=my_has_lyrics )
        top10songs={}
        top10artists={}
        resp = requests.get(music_url)
        if resp.ok:
                top10dataB = resp.json()
        else:
                print(resp.reason)
        return jsonify(top10dataB)

@app.route('/top10dataB/', methods=['GET']) #a decorator for the function below (dont skip line!)- function that should be called when a request on that path arrives
def get_top10dataB(countryB): #GET: to retrieve info!
        #list of parameters to get the top 10 from countryB chart
        my_chart_name = request.args.get('chart_name','top')
        my_page = request.args.get('page','1')
        my_page_size = request.args.get('page_size','10')
        my_country = request.args.get('countryB','')
        my_has_lyrics = request.args.get('f_has_lyrics','1')

        #request template
        music_url = music_url_template.format(API_KEY=app.config['MY_API_KEY'],chart_name=my_chart_name,page=my_page,page_size=my_page_size,country=my_country,f_has_lyrics=my_has_lyrics )
        top10songsB={}
        top10artistsB={}
        resp = requests.get(music_url)

        if resp.ok:
                top10dataB = resp.json() #chart function defined earlier return the (serialised) resource in JSON format
                top10songsB['1st']= top10dataB['message']['body']['track_list'][0]['track']['track_name']
                top10songsB['2nd']= top10dataB['message']['body']['track_list'][1]['track']['track_name']
                top10songsB['3rd']= top10dataB['message']['body']['track_list'][2]['track']['track_name']
                top10songsB['4th']= top10dataB['message']['body']['track_list'][3]['track']['track_name']
                top10songsB['5th']= top10dataB['message']['body']['track_list'][4]['track']['track_name']
                top10songsB['6th']= top10dataB['message']['body']['track_list'][5]['track']['track_name']
                top10songsB['7th']= top10dataB['message']['body']['track_list'][6]['track']['track_name']
                top10songsB['8th']= top10dataB['message']['body']['track_list'][7]['track']['track_name']
                top10songsB['9th']= top10dataB['message']['body']['track_list'][8]['track']['track_name']
                top10songsB['10th']= top10dataB['message']['body']['track_list'][9]['track']['track_name']

                top10artistsB['1st']= top10dataB['message']['body']['track_list'][0]['track']['artist_name']
                top10artistsB['2nd']= top10dataB['message']['body']['track_list'][1]['track']['artist_name']
                top10artistsB['3rd']= top10dataB['message']['body']['track_list'][2]['track']['artist_name']
                top10artistsB['4th']= top10dataB['message']['body']['track_list'][3]['track']['artist_name']
                top10artistsB['5th']= top10dataB['message']['body']['track_list'][4]['track']['artist_name']
                top10artistsB['6th']= top10dataB['message']['body']['track_list'][5]['track']['artist_name']
                top10artistsB['7th']= top10dataB['message']['body']['track_list'][6]['track']['artist_name']
                top10artistsB['8th']= top10dataB['message']['body']['track_list'][7]['track']['artist_name']
                top10artistsB['9th']= top10dataB['message']['body']['track_list'][8]['track']['artist_name']
                top10artistsB['10th']= top10dataB['message']['body']['track_list'][9]['track']['artist_name']
                top10dataB=(top10songsB['1st'],top10artistsB['1st'],top10songsB['2nd'],top10artistsB['2nd'],top10songsB['3rd'],top10artistsB['3rd'],top10songsB['4th'],top10artistsB['4th'],top10songsB['5th'],top10artistsB['5th'],top10songsB['6th'],top10artistsB['6th'],top10songsB['7th'],top10artistsB['7th'],top10songsB['8th'],top10artistsB['8th'],top10songsB['9th'],top10artistsB['9th'],top10songsB['10th'],top10artistsB['10th'])
        else:
                print(resp.reason)
        return (top10dataB)

@app.route('/madb/<commontrack_id>', methods=['GET'])
def profile(commontrack_id):
    rows = session.execute( """Select * from madb.stats where commontrack_id = '{}'""".format(commontrack_id))
    for x in rows:
        return('<h1>{}  title is {} !</h1>'.format(commontrack_id,x.track_name))
    return('<h1>That track does not exist in the database!</h1>')

if __name__=="__main__": #to launch our app
        app.run(host='0.0.0.0',port=8080, debug=True)

