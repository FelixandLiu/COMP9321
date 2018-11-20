from flask import Flask, request, jsonify
from flask_restplus import Resource, Api, fields, inputs, reqparse
import pandas as pd
import json
app = Flask(__name__)
api = Api(app)

books_df = pd.read_csv('Books.csv')
columns_to_drop = ['Edition Statement',
                   'Corporate Author',
                   'Corporate Contributors',
                   'Former owner',
                   'Engraver',
                   'Contributors',
                   'Issuance type',
                   'Shelfmarks']
for i in range(len(columns_to_drop)):
    books_df.drop(columns=columns_to_drop[i], inplace=True)
books_df['Place of Publication']=books_df['Place of Publication'].apply(lambda x: 'London' if 'London' in x else x.replace('-', ' '))
books_df['Date of Publication'] = books_df['Date of Publication'].str.extract(r'^(\d{4})',expand=False)
books_df['Date of Publication']=pd.to_numeric(books_df['Date of Publication'])
pd.options.display.float_format = '{:,.0f}'.format
books_df['Date of Publication']=books_df['Date of Publication'].fillna(0)
books_df.set_index('Identifier',inplace=True)
for column in books_df:
    if ' ' in books_df[column]:
        books_df[column]=books_df[column].apply(lambda x: x.replace(' ', '_'))
book_fields=api.model('book',{'Identifier': fields.Integer,
                              'Place of Publication': fields.String,
                              'Date of Publication': fields.Integer,
                              'Publisher': fields.String,
                              'Title': fields.String,
                              'Author': fields.String,
                              'Flickr URL': fields.String})
@api.route('/books/<int:book_id>')
class Books(Resource):
    def get(self,book_id):
        if book_id not in books_df.index:
            api.abort( 404, "Book {} doesn't exist".format( book_id ) )
        a=dict(books_df.loc[book_id])
        return a
    def delete(self, book_id):
        if book_id not in books_df.index:
            api.abort(404,"Book {} doesn't exit".format(book_id))
        books_df.drop(book_id, axis=0, inplace=True)
        return {"message": "Book {} has been removed".format(book_id)},200

    @api.expect( book_fields )
    def put(self, book_id):
        if book_id not in books_df.index:
            api.abort(404,"Book {} doesn't exit".format(book_id))
        book=request.json
        if 'Identifier' in book and book_id !=book['Identifier']:
            return {'message': 'book{} not exist'.format(book_id)}
        for key in book:
            if key not in book_fields.keys():
                return {'message': 'book key{} is wrong'.format(key)}
            books_df.loc[book_id,key]=book[key]
        books_df.append(book, ignore_index=True)
        return {'message': 'book{} has been updated'.format(book_id)}
parser=reqparse.RequestParser()
parser.add_argument('order',choices=list(column for column in book_fields.keys()))
parser.add_argument('ascent',type=inputs.boolean)
@api.route('/books')
class total_books(Resource):
    @api.expect(parser,validate=True)
    def get(self):
        agrs = parser.parse_args()
        order_by = agrs.get('order')
        ascend = agrs.get('ascent')
        if order_by and ascend:
            books_df.sort_values(by=order_by,ascending=ascend,inplace=True)
        book_str = books_df.to_json( orient='index' )
        #return jsonify(book_str)

        
        book_list = json.load(book_str)
        ret=[]
        for i in book_list:
            book=book_list[i]
            book['Identifier']=int(i)
            ret.append(book)
        return ret


if __name__=='__main__':
    app.run(debug=True)