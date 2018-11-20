from flask import Flask
from flask_restplus import Resource, Api
import pandas as pd

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

if __name__=='__main__':
    app.run(debug=True)