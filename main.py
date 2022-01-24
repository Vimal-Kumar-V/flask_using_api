from flask import Flask,request
from flask_pymongo import MongoClient
from bson.objectid import ObjectId
import json

app=Flask(__name__)
mongo=MongoClient(host="localhost",port=27017)


db=mongo.api_tasks
def dictify(query):
    ans={}
    query = str(query)
    query = query[2:-1]

    query = query.split("&")
    for q in query:
        q = q.split("=")
        q[0]=q[0].strip()
        q[1]=q[1].strip()
        ans[q[0]] = q[1]
    return ans

@app.route("/",methods=["POST","GET"])
def home():
    if request.method=="POST":

        task_id=request.args.get('task_id')
        task_name=request.args.get('task_name')
        date_of_creation=request.args.get('created_date')
        date_of_completion=request.args.get('completed_date')
        status=request.args.get('status')
        task={"task_id":task_id,"task_name":task_name,"date_of_creation":date_of_creation,"date_of_completion":date_of_completion,"status":status}
        db.api_tasks.insert_one(task)
        return "Success"

    else:
        tasks=list(db.api_tasks.find())
        return str(tasks)
@app.route('/update/<id>',methods=['GET',"POST"])
def update(id):
    if request.method=="POST":
        update_id=ObjectId(id)
        updated_string=dictify(request.query_string)
        db.api_tasks.update({"_id":update_id},{"$set":updated_string})
        return "success"
@app.route('/delete/<id>',methods=['POST'])
def delete(id):
    delete_id=ObjectId(id)
    db.api_tasks.remove({"_id":delete_id})
    return "success"
@app.route('/search',methods=['POST','GET'])
def search():
    if request.method=="POST":
        string_search=dict(dictify(request.query_string))

        result=list(db.api_tasks.find(string_search,{"_id":0}))
        return str(result)






if __name__=="__main__":
    app.run(debug=True)
