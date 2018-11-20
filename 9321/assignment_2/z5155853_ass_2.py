from flask import Flask, request
from flask_restplus import Resource, Api, fields, reqparse
import json
import urllib.request
import pymongo
import datetime
import xml.etree.ElementTree as ET
import requests
from bson import json_util

client = pymongo.MongoClient( 'mongodb://Felix:felix123@ds229290.mlab.com:29290/worldbank_data' )
db = client.worldbank_data
app = Flask(__name__)
api = Api(app)
indicator_type=api.model('indicators',{'indicator_id': fields.String})
@api.route('/indicators')
class indicators(Resource):
    @api.expect(indicator_type)
    @api.response( 201, 'create indicator' )
    @api.response( 200, 'found indicator' )
    @api.response( 404, 'not exist ' )
    def post(self):
        indicator=request.json['indicator_id']
        for collection in db.collection_names(include_system_collections=False):
            for data in db[collection].find():
                if 'indicator' in data:
                    indicators_json.append((data['indicator'],collection))
        for i in indicators_json:
            if indicator == i[0]:
                return {"location" : "/indicators/{}".format(i[1])},200
        if indicator not in indicator_list:
            return {'message':"the input indicator id doesn't exist in the data source"},404
        data_entry = []
        r = requests.get( "http://api.worldbank.org/v2/countries/all/indicators/{}?date=2012:2017&format=json&page=1".format(indicator) )
        indicator_data = r.json()

        for i in range(len(indicator_data[1])):
            data_format={ "country": "{}".format(indicator_data[1][i]['country']['value']),
                          "date": "{}".format(indicator_data[1][i]['date']),
                          "value": indicator_data[1][i]['value']
                          }
            data_entry.append(data_format)
        r1 = requests.get("http://api.worldbank.org/v2/countries/all/indicators/{}?date=2012:2017&format=json&page=2".format(indicator ) )
        indicator_data1 = r1.json()
        for i in range( len( indicator_data1[1] ) ):
            data_format1 = {"country": "{}".format( indicator_data1[1][i]['country']['value'] ),
                           "date": "{}".format( indicator_data1[1][i]['date'] ),
                           "value": indicator_data1[1][i]['value']
                           }
            data_entry.append( data_format1 )

        index=[]
        for collection in db.collection_names( include_system_collections=False ):
            if collection[:9]=='indicator':
                index.append(int(collection[10:]))
        if index==[]:
            indicator_id=1
        else:
            indicator_id=max(index)+1
        creation_time = '{}'.format( datetime.datetime.utcnow() )
        result_format = {"collection_id": "indicator-{}".format(indicator_id),
                         "indicator": "{}".format(indicator),
                         "indicator_value": "{}".format(indicator_data[1][0]['indicator']['value']),
                         "creation_time": creation_time,
                         "entries": data_entry
                         }


        db["indicator-{}".format(indicator_id)].insert( result_format )

        return {
            "location" : "/indicators/indicator-{}".format(indicator_id),
            "collection_id" : "indicator-{}".format(indicator_id),
            "creation_time": creation_time,
            "indicator" : "{}".format(indicator)
        },201

    @api.response( 200, 'ok' )
    @api.response( 404, 'not found' )
    def get(self):
        result_set=[]
        for collection in db.collection_names(include_system_collections=False):
            if collection[:9] == 'indicator':
                for data in db[collection].find():
                    collection_abstract={ "location" : "/indicators/{}".format(data['collection_id']),
                                          "collection_id" : "{}".format(data['collection_id']),
                                          "creation_time": data['creation_time'],
                                          "indicator" : data['indicator']
                                          }
                    result_set.append(collection_abstract)
        if result_set==[]:
            return {'message': 'not found'},404
        return result_set,200

@api.route('/indicators/<string:collection_id>')
class indicator_set(Resource):
    @api.response( 200, 'ok' )
    @api.response( 404, 'not exist' )
    def get(self,collection_id):
        if collection_id not in db.collection_names( include_system_collections=False ):
            api.abort(404,"not exist")
        for data in db[collection_id].find({}, {'_id': False}):
            data_sanitized = json.loads( json_util.dumps( data ) )
            return data_sanitized,200
    @api.response( 200, 'delete ok' )
    @api.response( 404, 'not exist' )
    def delete(self,collection_id):
        if collection_id not in db.collection_names( include_system_collections=False ):
            api.abort(404,"not exist")
        db.drop_collection( '{}'.format(collection_id) )
        return { "message" :"Collection = {} is removed from the database!".format(collection_id)},200

@api.route('/indicators/<string:collection_id>/<string:year>/<string:country>')
class indicator_value(Resource):
    @api.response( 200, 'ok' )
    @api.response( 404, 'not exist' )
    def get(self,collection_id,year,country):
        for data in db[collection_id].find( {} ):
            indicator_id=data['indicator']
            data_sanitized = json.loads( json_util.dumps( data['entries'] ) )
            for i in data_sanitized:
                if i['country']==country and i['date']==year:
                    if i['value']:
                        return { "collection_id": collection_id,
                                 "indicator" : indicator_id,
                                 "country": country,
                                 "year": year,
                                 "value": i['value']
                                 }, 200
                if i==data_sanitized[-1]:
                    return {'message': 'in {},economic indicator value is '
                                       'not existed for given year if {} and a country of {} '.format(collection_id,year,country)},404

parser=reqparse.RequestParser()
parser.add_argument('query')
@api.route('/indicators/<string:collection_id>/<string:year>')
class top_bottom_value(Resource):
    @api.expect( parser, validate=True )
    @api.response( 200, 'ok' )
    @api.response( 404, 'not exist' )
    @api.response( 400, 'invalid query' )
    def get(self,collection_id,year):
        agrs = parser.parse_args()
        value=[]
        for data in db[collection_id].find( {} ):
            data_sanitized = json.loads( json_util.dumps( data['entries'] ) )
            for i in data_sanitized:
                if i['date']==year:
                    if i['value']==None:
                        i['value'] = -1
                    value.append(i)
        newlist = sorted( value, key=lambda k: k['value'] ,reverse=True)
        if newlist==[]:
            return {'message': 'not exist'},404
        for data in db[collection_id].find( {} ):
            if not agrs.get( 'query' ):
                return {"indicator": '{}'.format( data["indicator"] ),
                        "indicator_value": '{}'.format( data["indicator_value"] ),
                        "entries": newlist
                        }, 200
            elif agrs.get( 'query' ) and len(agrs.get( 'query' ))>3 and agrs.get( 'query' )[:3]=='top':
                N = int( agrs.get( 'query' )[3:] )
                if N > 100 or N < 1:
                    return {'message': ' {} can be not an integer value between 1 and 100'.format( N )}
                return { "indicator": '{}'.format(data["indicator"]),
                         "indicator_value": '{}'.format(data["indicator_value"]),
                         "entries" : newlist[:N]
                         },200
            elif agrs.get( 'query' ) and len(agrs.get( 'query' ))>5 and agrs.get( 'query' )[:6]=='bottom':
                N = int( agrs.get( 'query' )[6:] )
                if N > 100 or N < 1:
                    return {'message': ' {} can be not an integer value between 1 and 100'.format( N )}
                return { "indicator": '{}'.format(data["indicator"]),
                         "indicator_value": '{}'.format(data["indicator_value"]),
                         "entries" : newlist[-N:]
                         },200
            else:
                return {'message': 'invalid query'}, 400
if __name__=='__main__':
    indicator_list=[]
    url = urllib.request.urlopen( "http://api.worldbank.org/v2/indicators?per_page=10000" )
    url1 = urllib.request.urlopen( "http://api.worldbank.org/v2/indicators?per_page=10000&page=2" )
    tree = ET.parse( url )
    tree1 = ET.parse( url1 )
    root = tree.getroot()
    root1 = tree1.getroot()
    for elem in root:
        indicator_list.append(elem.get( 'id' ))
    for elem1 in root1:
        indicator_list.append(elem1.get( 'id' ))
    indicators_json = []
    app.run(debug=True)