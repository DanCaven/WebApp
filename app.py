from flask import Flask, session, redirect, url_for, escape, request, render_template, jsonify
import requests


data = {"dan":{"pass":"asdf","classes":["CMSCI 123", "CMSCI 425"]},"hannah":{"pass":"love","classes":["Genetics", "Bio"]}}

app = Flask(__name__)

@app.route("/test")
def test():
    return "hello world"

@app.route("/login", methods=["GET","POST"])
def login():
    if "log" in request.args:
        info = (request.form)
        user = info['user']
        url = "http://localhost:5000/login"
        querystring = {"user":"dan","pass":"asdf"}
        response = requests.request("GET", url, params=querystring)
        r = jsonify(response.text)
        if "verified" in response.text:
            session["user"] = user
            return redirect(url_for('profile', username = user))
    return render_template("login.html")

@app.route("/profile")
def profile():
    user = session['user']
    return render_template("profile.html", user=user, classes=data[user]['classes'])

@app.route("/classes")
def classes():
    clss = request.args.get("clss")
    url = "http://localhost:5000/api/Agenda/get/class"
    querystring = {"name":str(clss)}
    print(querystring)
    packet = requests.get(url, params=querystring)
    packet = packet.json()
    if packet != "empty set":
        print(packet)
        packet = dict(packet)
        print(packet)
        return render_template("classes.html",clss=clss, packet=packet)
    return render_template("search.html", flag =True)



@app.route("/search")
def search():
    return render_template("search.html",flag=False)

@app.route("/upload")
def upload():
    if "prof" in request.args:
        info = request.args
        code = info.get("code")
        prof = info.get("prof")
        name = info.get("name")
        time = info.get("time")
        url = "http://localhost:5000/api/Agenda/upload/class"
        querystring = {"code":code,"prof":prof,"time":time,"name":name}
        response = requests.request("GET", url, params=querystring)
        print(response)
        return render_template("upload.html")
    elif "due"  in request.args:
        info = request.args
        code = info.get("code")
        name = info.get("name")
        due = info.get("due")
        points = info.get("points")
        topics = info.get("topics")
        url = "http://localhost:5000/api/Agenda/upload/assignments"
        querystring = {"code":code,"due":due,"points":points,"name":name,"topics":topics}
        response = requests.request("GET", url, params=querystring)
        return render_template("upload.html")
    else:
        return render_template("upload.html")

@app.route("/assignment")
def asignment():
    clss = request.args.get("clss")
    asignment = request.args.get("assignment")
    url = "http://localhost:5000/api/Agenda/get/assignment"
    querystring = {"code":clss,"name":assingment}
    packet = requests.request("GET", url, params=querystring).json()
    #packet = packet.json()
    #print(packet)
    return packet

@app.route("/flag")
def flag():
    info = request.args
    code = info.get("code")
    flag = info.get("flag")
    name = info.get("name")
    url = "http://localhost:5000/api/Agenda/flag"
    querystring = {"code":code,"flag":flag,"name":name}
    response = requests.request("GET", url,params=querystring)
    return redirect(url_for('classes', clss = code))

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
