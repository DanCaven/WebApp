from flask import Flask, session, redirect, url_for, escape, request, render_template, jsonify
import requests
import os
import json

data = {"dan":{"pass":"asdf","classes":["CMSCI 123", "CMSCI 425"]},"hannah":{"pass":"love","classes":["Genetics", "Bio"]}}

app = Flask(__name__)
def updateInfo(user):
    url = "https://globalagendaapi.herokuapp.com/api/getuser"
    querystring = {"user":user}
    response = requests.request("GET", url, params=querystring).text
    response = json.loads(response)
    session["user"] = response

@app.route("/test")
def test():
    return "hello world"

@app.route("/login", methods=["GET","POST"])
def login():
    if "log" in request.args:
        info = (request.form)
        user = info['user']
        url = "https://globalagendaapi.herokuapp.com/api/login"
        querystring = {"user":info["user"],"pass":info["pass"]}
        #print(querystring)
        response = requests.request("GET", url, params=querystring).text
        response = json.loads(response)
        if response["user"] == info["user"]:
            #print("in authenticated")
            session["user"] = response
            return redirect(url_for('profile', username = response["user"]))
    return render_template("login.html")

@app.route("/profile")
def profile():
    info = (request.args)
    user = info.get('username')
    updateInfo(user)
    return render_template("profile.html", user=session["user"]["user"], classes=session['user']["classes"])

@app.route("/classes", methods=["GET","POST"])
def classes():
    #print(request.args)
    if "code" in request.args:
        url = "https://globalagendaapi.herokuapp.com/api/AddClass"
        user = (session["user"]["user"])
        querystring = {"user":user,"code":request.args.get("code").lower()}
        response = requests.request("GET", url, params=querystring).text
        updateInfo(user)
    clss = request.args.get("clss")
    url = "https://globalagendaapi.herokuapp.com/api/Agenda/get/class"
    querystring = {"name":str(clss)}
    packet = requests.get(url, params=querystring)
    packet = packet.json()
    if packet != "empty set":
        #print(packet)
        packet = dict(packet)
        #print(packet)
        return render_template("classes.html",clss=clss, packet=packet,classes=session['user']["classes"], user = session["user"]["user"])
    return render_template("search.html", flag =True,user = session["user"]["user"])



@app.route("/search")
def search():
    return render_template("search.html",flag=False,user=session["user"]["user"])

@app.route("/upload")
def upload():
    if "prof" in request.args:
        info = request.args
        code = info.get("code")
        prof = info.get("prof")
        name = info.get("name")
        time = info.get("time")
        url = "https://globalagendaapi.herokuapp.com/api/Agenda/upload/class"
        querystring = {"code":code,"prof":prof,"time":time,"name":name}
        response = requests.request("GET", url, params=querystring)
        #print(response)
        return render_template("upload.html",user=session["user"]["user"])
    elif "due"  in request.args:
        info = request.args
        code = info.get("code")
        name = info.get("name")
        due = info.get("due")
        points = info.get("points")
        topics = info.get("topics")
        url = "https://globalagendaapi.herokuapp.com/api/Agenda/upload/assignments"
        querystring = {"code":code,"due":due,"points":points,"name":name,"topics":topics}
        response = requests.request("GET", url, params=querystring)
        return render_template("upload.html",user=session["user"]["user"])
    else:
        return render_template("upload.html",user=session["user"]["user"])

@app.route("/assignment")
def asignment():
    clss = request.args.get("clss")
    asignment = request.args.get("assignment")
    url = "https://globalagendaapi.herokuapp.com/api/Agenda/get/assignment"
    querystring = {"code":clss,"name":assingment}
    packet = requests.request("GET", url, params=querystring).json()
    #packet = packet.json()
    ##print(packet)
    return packet

@app.route("/flag")
def flag():
    info = request.args
    code = info.get("code")
    flag = info.get("flag")
    name = info.get("name")
    url = "https://globalagendaapi.herokuapp.com/api/Agenda/flag"
    querystring = {"code":code,"flag":flag,"name":name}
    response = requests.request("GET", url,params=querystring)
    return redirect(url_for('classes', clss = code))

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
