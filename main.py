from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)


class Product(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    data_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.id


@app.route('/delete/<int:id>')
def delete(id):
    item_to_delete = Product.query.get_or_404(id)

    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect('/market')
    except:

        return 'There was a problem deleted that friend'


@app.route('/')
@app.route('/market', methods=['POST', 'GET'])
def market_page():
    title = 'My products list'

    if request.method == 'POST':
        item_name = request.form['name']
        item_price = request.form['price']
        new_item = Product(name=item_name, price=item_price)

        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect('/market')
        except:
            return 'There was an error adding your friend'
    else:
        items = Product.query.order_by(Product.data_created)
        return render_template('market.html', title=title, items=items)


@app.route('/search', methods=['GET', 'POST'])
def search_page():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search = '%{0}%'.format(search_value)
        results = Product.query.filter(Product.name.like(search)).all()
        return render_template('search.html', items=results,
                               pageTitle='Mike\'s Friends',
                               legend='Search Results')
    else:
        return render_template('search.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
