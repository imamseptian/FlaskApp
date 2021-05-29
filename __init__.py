from enum import unique
from flask import Flask, render_template,request,redirect,url_for,flash,jsonify
#from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
import flask_sqlalchemy
import pandas as pd
import pymysql


app = Flask(__name__)
app.secret_key = "Secret Key"

# Google Cloud SQL (change this accordingly)
USERNAME ="imamseptian"
PASSWORD ="imamseptian1234"
PUBLIC_IP_ADDRESS ="34.126.174.105"
DBNAME ="rating_db"
PROJECT_ID ="groovy-analyst-314808"
INSTANCE_NAME ="groovy-analyst-314808:asia-southeast1:collectrating"

  
# configuration
app.config["SECRET_KEY"] = "xxxxxxx"
#app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql + mysqldb://imamseptian:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket =/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+pymysql://{USERNAME}:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}"
#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql + mysqlconnector://{USERNAME}:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}"
#app.config["SQLALCHEMY_DATABASE_URI"]= "mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>"
# app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql + mysqldb://{USERNAME}:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket =/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/cobarating'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255),unique=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255),unique=True)
    password = db.Column(db.String(255))

    def __init__(self,username, name,email,password):
        self.username=username
        self.name=name
        self.email=email
        self.password=password

class Foods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_code = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(255))
    category = db.Column(db.String(255))
    type = db.Column(db.String(255))
    calories = db.Column(db.Float)
    protein = db.Column(db.Float)
    carbs = db.Column(db.Float)
    fat = db.Column(db.Float)
    fiber = db.Column(db.Float)
    sugar = db.Column(db.Float)
    vitamin_a = db.Column(db.Float)
    vitamin_b6 = db.Column(db.Float)
    vitamin_b12 = db.Column(db.Float)
    vitamin_c = db.Column(db.Float)
    vitamin_d = db.Column(db.Float)
    vitamin_e = db.Column(db.Float)


    def __init__(self,food_code, name,category,type,calories,protein,carbs,fat,fiber,sugar,vitamin_a,vitamin_b6,vitamin_b12,vitamin_c,vitamin_d,vitamin_e):
        self.food_code=food_code
        self.name=name
        self.category=category
        self.type=type
        self.calories=calories
        self.protein=protein
        self.carbs=carbs
        self.fat=fat
        self.fiber=fiber
        self.sugar=sugar
        self.vitamin_a=vitamin_a
        self.vitamin_b6=vitamin_b6
        self.vitamin_b12=vitamin_b12
        self.vitamin_c=vitamin_c
        self.vitamin_d=vitamin_d
        self.vitamin_e=vitamin_e

class Ratings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    food_id = db.Column(db.Integer)
    food_code = db.Column(db.Integer)
    rating = db.Column(db.Integer)


    def __init__(self,user_id, food_id,food_code,rating):
        self.user_id=user_id
        self.food_id=food_id
        self.food_code=food_code
        self.rating=rating
     
@app.route('/')
def Index():
    #return "Hellow Flask Application"
     all_data = Users.query.all()


     return render_template("index.html",user_data=all_data)


@app.route('/convert_food')
def convert_food():
    # return "Hellow Flask Application"
    food_df = pd.read_csv('Healthy FnB.csv')
    for index, row in food_df.iterrows():
        my_data = Foods(row['Food code'],row['Food'], row['Category'],row['Type'],row['Calories (kcal/100g)'],row['Protein (g)'],row['Carbohydrate (g)'],row['Fat (g)'],row['Fiber (g)'],row['Sugars (g)'],row['Vitamin A (mcg)'],row['Vitamin B-6 (mg)'],row['Vitamin B-12 (mcg)'],row['Vitamin C (mg)'],row['Vitamin D (mcg)'],row['Vitamin E (mg)'])
        db.session.add(my_data)
        db.session.commit()

    return redirect(url_for('Index'))

@app.route('/',methods = ['POST'])
def insert():
    if request.method == "POST":
        username = 'username72'
        name = request.form['name']
        email = 'username72@ayohealthy.id'
        password = 'qwerty123'

        my_data = Users(username, name,email,password)
        db.session.add(my_data)
        db.session.commit()
        my_data = Users.query.get(my_data.id) 
        my_data.username = ('username'+str(my_data.id))
        my_data.email = ('username'+str(my_data.id)+'@ayohealthy.id')
        db.session.commit()

        flash("User Inserted Successfully")

        return redirect(url_for('Index'))

@app.route('/userfood/<id>')
def foodtable(id):
    user_data = Users.query.get(id)
    food_data = Foods.query.all()
    
    rating_data = db.session.query(Ratings,Foods).join(Ratings,Ratings.food_id == Foods.id).filter(Ratings.user_id == id)
    rated_food = []
    for rating,food in rating_data:
        rated_food.append(rating.food_id)

    food_data = db.session.query(Foods).filter(Foods.id.notin_(rated_food)) 
    # return "Hellow Flask Application"
    return render_template("food_list.html",user_data=user_data, food_data=food_data,rating_data=rating_data)


@app.route('/cobajson')
def ayaya():
    # dataku = Foods.query.join(Ratings,Ratings.food_id == Foods.id)
    dataku = db.session.query(Ratings,Foods).join(Ratings,Ratings.food_id == Foods.id).filter(Ratings.user_id == 5)
    # dataku = Users.query.all()
    # print(dataku)
    coba_join = []
    content={}
    for rating,food in dataku:
        
        # content = {'id':foods.id,'bruh':22}
        content = {'id':rating.id,'food_code':food.food_code,'name':food.name,'category':food.category,'calories':food.calories,'carbs':food.carbs,'protein':food.protein,'fat':food.fat,'fiber':food.fiber}
        coba_join.append(content)
        content={}
    people = [{'name': 'Alice', 'birth-year': 1986},
          {'name': 'Bob', 'birth-year': 1985}]
    rated = db.session.query(Ratings).filter(Ratings.user_id==1).all()
    print(len(rated))
    return jsonify(people) 
    

@app.route('/rate',methods=['GET','POST'])
def giverate():
    if request.method == "POST":
        
        user_id = request.form['user_id']
        food_id = request.form['food_id']
        food_code = request.form['food_code']
        rating = request.form['rating']
        
        my_data = Ratings(user_id, food_id,food_code,rating)
        db.session.add(my_data)
        db.session.commit()

        return redirect(url_for('foodtable',id=user_id))

@app.route('/editrating',methods=['GET','POST'])
def editrating():
    if request.method == "POST":
        
        if request.method == 'POST':
            my_data = Ratings.query.get(request.form.get('id'))

            my_data.rating = request.form['rating']
            # my_data.email = request.form['email']
            # my_data.phone = request.form['phone']

            db.session.commit()
            flash("User Updated Successfully")
            
            return redirect(url_for('foodtable',id=my_data.user_id))

            

@app.route('/update',methods=['GET','POST'])
def update():
    if request.method == 'POST':
        my_data = Users.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        # my_data.email = request.form['email']
        # my_data.phone = request.form['phone']

        db.session.commit()
        flash("User Updated Successfully")
        
        return redirect(url_for('Index'))


@app.route('/delete/<id>/',methods=['GET','POST'])
def delete(id):
    my_data = Users.query.get(id)
    rated = db.session.query(Ratings).filter(Ratings.user_id==id).all()
    if(len(rated)>0):
        flash("Users with rating cannot be deleted")
        return redirect(url_for('Index'))
    else:

        db.session.delete(my_data)
        db.session.commit()
        flash("Users Deleted Successfully")

        return redirect(url_for('Index'))

@app.route('/deleterating/<userid>/<ratingid>/',methods=['GET','POST'])
def detele_rating(userid,ratingid):
    my_rating = Ratings.query.get(ratingid)
    
    db.session.delete(my_rating)
    db.session.commit()

    return redirect(url_for('foodtable',id=userid))
        
if __name__ == "__main__":
    app.run(debug=True)

