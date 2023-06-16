from flask import Flask, request, jsonify
from sendgrid import SendGridAPIClient
from services.database.database import App
from services.springer import start_scraping_thread
import dotenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])
sg = None
initialized = False

DATABASE_URL = "neo4j+s://874e6982.databases.neo4j.io:7687"
USER = "neo4j"
PASSWORD = "bfVN1NOoQbK9xp3Eu9G1Y3dYaFfpONP-5Iq6hyPgFmw"
SENDGRID_API_KEY = "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"

uri = DATABASE_URL
user = USER
password = PASSWORD
database = App(uri, user, password)


@app.before_request
def initialize():
    global initialized, sg
    if not initialized:
        app.logger.info("Starting scraping thread...")
        start_scraping_thread()
        sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)  # mail service
        initialized = True


@app.route('/registerUser', methods=['POST'])
def register_user():
    data = request.json
    email = data['email']
    print(email)
    # save it in database
    database.create_user(email, "sami")
    # create_user function
    return jsonify({"message": "User registered successfully"})


@app.route('/registerUserPreferences', methods=['POST'])
def register_user_preferences():
    data = request.json
    email = data['email']
    preferences = data['preferences']
    # percentage = 100 / len(preferences)
    # save it in database
    for preference in preferences:
        database.user_to_category(email,preference)
    # user_to_category function
    return jsonify({"message": "User preferences registered successfully"})


@app.route('/updatePreferences', methods=['POST'])
def update_preferences():
    data = request.json
    email = data['email']
    category_preferences = data['updated_preferences']
    database.delete_user_to_category(email)
    for update_preference in category_preferences:
        database.user_to_category(email,update_preference)
    # user_to_category update
    return jsonify({"message": "User preferences updated successfully"})


@app.route('/getTopArticles', methods=['GET'])
def get_top_articles():
    # data = get_articles_from_db()  # Retrieve data from the database
    data = database.get_blogs_by_likes()
    resp = []
    for article_data in data:
        link = article_data['link']
        title = article_data['title']
        category = database.get_category_by_blog(article_data['link'])
        author = article_data['author']
        summary = article_data['summary']
        time = article_data['read_time']
        id = article_data['id']
        # print(data)

        resp.append({
            "link": link,
            "title": title,
            "category": category,
            "author": author,
            "summary": summary,
            "time":time,
            "id": id
        })
    print(resp)
    return jsonify(resp)

@app.route('/getTopArticlesPerUser', methods=['GET'])
def get_top_articles_per_user():
    # data = get_articles_from_db()  # Retrieve data from the database
    args = request.args
    category = args['category']
    limit = int(args['limit'])
    data = database.get_blogs_by_category_and_limit(category,limit)
    resp = []

    for article_data in data:
        link = article_data['link']
        author = article_data['author']
        # article = read_article(link)
        # summary = summarize_article(article)
        resp.append({
            "link": link,
            "category": category,
            "author": author,
            # "summary": summary
        })

    return jsonify(resp)

@app.route('/getTopArticlesfor', methods=['GET'])
def get_top_articles_by_category():
    args = request.args
    category = args['category']
    print(category)
    data = database.get_blogs_by_likes_and_category(category)
    resp = []
    for article_data in data:
        link = article_data['link']
        category = database.get_category_by_blog(article_data['link'])
        author = article_data['author']
        # article = read_article(link)
        # summary = summarize_article(article)
        resp.append({
            "link": link,
            "category": category,
            "author": author,
            # "summary": summary
        })
    print(resp)
    return jsonify(resp)

@app.route('/addBookmark',methods=['GET'])
def addBookmark():
    args = request.args
    email = args.email
    link = args.link
    try:
        database.user_to_blog(email,link)
        return jsonify({"result":"success"}),200
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/getBookMarks', methods=['GET'])
def getBookMarks():
    try:
        user_email = request.args.get('email')
        if user_email is None:
            return jsonify(error='Email parameter is missing'), 400

        data = database.get_user_blogs(user_email)
        print(data)
        return jsonify(data=data), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/getArticle',methods=['GET'])    
def getArticle():
    try:
        article_id = request.args.get('article_id')
        # print(type(article_id))
        article_id = int(article_id)
        if article_id is None:
            return jsonify(error='ID parameter is missing'), 400
        data = database.get_blog_by_id(article_id)
        print(data)
        return jsonify(data=data), 200
    except Exception as e:
        return jsonify(error=str(e)), 500
    
# @app.route()

if __name__ == "__main__":
    database.create_user("test@mail", "sami")
    database.user_to_blog("test@mail","no one")
    database.user_to_blog("test@mail","https://link.springer.com/article/10.1007/s42757-022-0154-6")
    database.create_blog("Fuck off,it's a research paper","https://link.springer.com/content/pdf/10.1007/s42757-022-0154-6.pdf?pdf=button","Some Nerd","https://link.springer.com/content/pdf/10.1007/s42757-022-0154-6.pdf?pdf=button")
    database.get_blog_by_id(9)
    print("END............................")
    app.run(host='0.0.0.0', port=5000)
