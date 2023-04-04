#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal=Animal.query.filter(Animal.id==id).first()
    if not animal:
        rb='<h1>404 Animal not found</h1>'
        r=make_response(r, 404)
        return r
    
    rb=f'''<ul>Name: {animal.name}</ul>
            <ul>Species: {animal.species}</ul>
            <ul>Zookeeper: {animal.zookeeper.name}</ul>
            <ul>Enclosure: {animal.enclosure.environment}</ul>'''
    r=make_response(rb, 200)
    return r

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    keeper=Zookeeper.query.filter(Zookeeper.id==id).first()
    if not keeper:
        rb='<h1>404 Zookeeper not found</h1>'
        r=make_response(rb, 404)
        return r
    
    rb=f"""<ul>Name: {keeper.name}</ul>
        <ul>Birthday: {keeper.birthday}</ul>"""
    
    animals=[animal for animal in keeper.animals]
    if not animals:
        rb+=f'<ul>{keeper.name} doesn\'t have any animals'
    else:
        for a in animals:
            rb+=f"<ul>Animal: {a.name} the {a.species}</ul>"

    
    r=make_response(rb,200)
    return r

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    encl=Enclosure.query.filter(Enclosure.id==id).first()
    if not encl:
        rb=f'404 Enclosure not found'
        r=make_response(rb,404)
        return r
    rb=f'''<ul>Environment: {encl.environment}</ul>
        <ul>Open to Visitors: {bool(encl.open_to_visitors)}</ul>'''
    
    animals=[animal for animal in encl.animals]
    if not animals:
        rb+=f'<ul>This enclosure doesn\'t have any animals'
    else:
        for a in animals:
            rb+=f"<ul>Animal: {a.name} the {a.species}</ul>"
    
    r=make_response(rb, 200)
    return r


if __name__ == '__main__':
    app.run(port=5555, debug=True)
