#!/usr/bin/env python3

from flask import Flask, jsonify, session
from flask_migrate import Migrate
from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.before_first_request
def seed_data():
    if not Article.query.first():
        article1 = Article(title="First Article", content="This is the first article.", author="Author One")
        article2 = Article(title="Second Article", content="This is the second article.", author="Author Two")
        db.session.add_all([article1, article2])
        db.session.commit()

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles/<int:id>')
def show_article(id):
    session['page_views'] = session.get('page_views', 0)
    session['page_views'] += 1

    if session['page_views'] > 3:
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

    article = db.session.get(Article, id)
    
    if article:
        # Create a preview of the first 50 characters of the content
        preview = article.content[:50] + "..." if len(article.content) > 50 else article.content

        # Calculate the minutes_to_read based on word count (assuming 200 words per minute)
        words = len(article.content.split())
        minutes_to_read = max(1, words // 200)  # Minimum of 1 minute

        return jsonify({
            'id': article.id,
            'title': article.title,
            'content': article.content,
            'author': article.author,
            'preview': preview,
            'minutes_to_read': minutes_to_read
        }), 200
    else:
        return jsonify({'message': 'Article not found'}), 404

if __name__ == '__main__':
    app.run(port=5555)
