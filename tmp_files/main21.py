from datetime import timedelta
import os

from functions import *
from Router import routes











imgurl = "./static/assets/5.webp"


app = Flask(__name__)
app.secret_key = "very secure key"

app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=1440)


def add_cache_headers(response):
    # Set cache control headers to prevent caching
    response.headers[
        "Cache-Control"
    ] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "-1"
    return response


socketio = SocketIO(app)



IST = pytz.timezone("Asia/Kolkata")
socketio = SocketIO(app)


# Register the after_request function for all routes

app.register_blueprint(routes)

@app.route("/Public")
def Public():
    return render_template("public.html")


@app.route("/Hub")
def Hub():
    return render_template("Hub.html")


@app.route("/", methods=["POST", "GET"])
def LogIn():
    art_info = getArt()
    message = request.args.get("message")
    username1 = request.args.get("username")
    if message == None:
        message = ""
    else:
        message = request.args.get("message")

    if username1 == None:
        username1 = ""
    else:
        username1 = request.args.get("username")

    if request.method == "POST":
        username = request.form["UsernameAtLogin"]
        password = request.form["PasswordAtLogin"]
        op = isPasswordOkay(username, password)
        if op != False:
            session["authenticated"] = op[1]

            session["shit"] = "real"

            return redirect("/Home")

            headers = {"Authorization": f"Bearer {op}"}

            # response = requests.get('/Home', headers=headers)

            # decoded_payload = jwt.decode(op, "kousic", algorithms=["HS256"])
            # print(decoded_payload)

            # return render_template(
            #     "LogIn.html", moon=moon, error=op, username=username1
            # )
        else:
            return render_template(
                "LogIn.html",
             
                error="Incorrect Password or Username",
                username=username1,
                art=art_info[0], artist=art_info[1]
            )  
    
    return render_template("LogIn.html", error=message, username=username1,art=art_info[0], artist=art_info[1])


@app.route("/SignUp", methods=["POST", "GET"])
def SignUp():
    if request.method == "POST":
        username = request.form["Username"]
        password = request.form["Password"]
        passwordre = request.form["ConfrimPassword"]
        InpData = InputValidation(username, password, passwordre)
        if isinstance(InpData, list):
            if send_sign_up_data_to_db(InpData[0], InpData[1]) == 200:
                csid = session.get('sid')
               # return render_template('SignUp.html', moon=moon, error=csid, Username=username, name="SignUp")
                op12 = isPasswordOkay(InpData[0], password)
                if op12 != False:
                    session["authenticated"] = op12[1]
                    session["new"] = "true"
                    print("=====================================INSession======================================")
                    print(session.get("authenticated"))
                    print("=====================================INSession======================================")
                    return redirect("/Home")
               
                # return render_template("interests-display.html", id=csid, Username=InpData[0])

                
                # return redirect(
                #     url_for(
                #         "LogIn",
                #         message="Now Please Login to your Account",
                #         username=username,
                #     )
                # )
                # return render_template('SignUp.html', moon=moon, error="Success", Username=username, name="SignUp")
            else:
                return render_template(
                    "SignUp.html",
                  
                    error="Some error occured",
                    Username=username,
                    name="SignUp",
                )

        else:
            return render_template(
                "SignUp.html",
        
                error=InpData,
                Username=username,
                name="SignUp",
            )
    art_info = getArt()


    return render_template("SignUp.html", art=art_info[0], artist=art_info[1])







# Your route to handle the selected interests
@app.route('/dump_selected_interests', methods=['POST'])
def update_interests11():
    if request.method == 'POST':
        data = request.json  # Assuming you're sending JSON data
        selected_interests = data.get('selectedInterests', [])
        sid =  data.get('sid')
       
        with open(f"./user-json/{sid}.json", 'r') as json_file:
            existing_data = json.load(json_file)

        # Update the JSON data with selected interests
        existing_data['Interests'] = selected_interests

        # Write back the updated data to the JSON file
        with open(f'./user-json/{sid}.json', 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)


        return jsonify({'redirect': '/Home'})

    # Return an appropriate response in case of other methods or failures
    return "Invalid request"



with open('./server-json/user.json') as f:
    usernames_data = json.load(f)
    taken_usernames = usernames_data['usernames']

@app.route('/check_username', methods=['GET'])
def check_username():
    username = request.args.get('username')
    if username is not None:
   
        username = username.lower()
        print(username)
        if username in taken_usernames:
            print("F")
            return jsonify({'available': False})

        else:
            print("T")

            return jsonify({'available': True})
    else:
        return jsonify({'available': False})



@app.route("/test")
def wel1():
    return render_template("interests-display.html")


# ==============================From Here On The Real Magic Starts====================#Complicated shit#


A1 = "https://firebasestorage.googleapis.com/v0/b/kr-cdn.appspot.com/o/1.webp?alt=media&token=7101fb13-bbba-4f43-bb2b-c4616bdd1453"
A2 = "https://firebasestorage.googleapis.com/v0/b/kr-cdn.appspot.com/o/2.webp?alt=media&token=56e09231-fb3d-4b90-bd7a-d39d79a8b49e"
A3 = "https://firebasestorage.googleapis.com/v0/b/kr-cdn.appspot.com/o/3.webp?alt=media&token=0b06f523-ad8e-4531-aeb8-925f67154ce2"
A4 = "https://firebasestorage.googleapis.com/v0/b/kr-cdn.appspot.com/o/4.webp?alt=media&token=4eda5ac1-2b1b-48e0-975d-37fe17f53f1e"
A5 = "https://firebasestorage.googleapis.com/v0/b/kr-cdn.appspot.com/o/5.webp?alt=media&token=437034c1-eddf-4b85-96af-f4a74ef83a7e"
A6 = "https://firebasestorage.googleapis.com/v0/b/kr-cdn.appspot.com/o/6.webp?alt=media&token=10153472-3c88-4bfd-848f-04997eeb41ca"
A7 = "https://firebasestorage.googleapis.com/v0/b/kr-cdn.appspot.com/o/7.webp?alt=media&token=41f6e68f-ef36-430d-8a73-417550d81e18"
A8 = "https://firebasestorage.googleapis.com/v0/b/kr-cdn.appspot.com/o/8.webp?alt=media&token=9c25ac77-a08f-497d-a132-b0e610b67f8c"
A9 = "https://firebasestorage.googleapis.com/v0/b/kr-cdn.appspot.com/o/9.webp?alt=media&token=a307e12b-76c2-4d3a-9010-ffbf9b2aa8f2"
A10 = "https://firebasestorage.googleapis.com/v0/b/kr-cdn.appspot.com/o/10.webp?alt=media&token=4c026fad-e8b7-4f23-a957-3104dd32a897"
A11 = "https://firebasestorage.googleapis.com/v0/b/kr-cdn.appspot.com/o/11.webp?alt=media&token=c034277e-7051-4bac-b08d-44561234b866"
A12 = "https://firebasestorage.googleapis.com/v0/b/kr-cdn.appspot.com/o/12.webp?alt=media&token=a833bc2c-94b0-4d92-a65a-63ce88cb8ab4"
A13 = "https://firebasestorage.googleapis.com/v0/b/kr-cdn.appspot.com/o/13.webp?alt=media&token=557dcc9d-944e-4717-9855-6189528e465e"
A14 = "https://firebasestorage.googleapis.com/v0/b/kr-cdn.appspot.com/o/14.webp?alt=media&token=83fba94d-a619-4411-a419-b758c841802f"
A15 = "https://firebasestorage.googleapis.com/v0/b/kr-cdn.appspot.com/o/15.webp?alt=media&token=37b07c90-fc61-4059-8943-ff670ee0672b"


@app.route("/Home", methods=["GET"])
@require_token
def Home():
    csid = session.get('sid')
    acc_status = session.get["new"]
    if acc_status == "true":
        return render_template("interests-display.html", id=csid, Username=InpData[0])

    return render_template("AfterLoginHome.html",
                            
                            img = "./static/assets/5.webp",

                        #    imgurl1 = A1,
                        #    imgurl2 = A2,
                        #    imgurl3 = A3,
                        #    imgurl4 = A4,
                        #    imgurl5 = A5,
                        #    imgurl6 = A6,
                        #    imgurl7 = A7,
                        #    imgurl8 = A8,
                        #    imgurl9 = A9,
                        #    imgurl10 = A10,



                           
                           )



@app.route("/get/interests")
def get_interests():
    # Specify the path to your local JSON file
    json_file_path = "./json/interests.json"

    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as json_file:
            interests_data = json.load(json_file)
    else:
        # Handle error when the file does not exist or cannot be read
        interests_data = {"interests": []}

    return jsonify(interests_data)


@app.route("/get/intropara")
def intropara():
    # Specify the path to your local JSON file
    json_file_path = "./json/intro.json"

    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as json_file:
            intro_data = json.load(json_file)
    else:
        # Handle error when the file does not exist or cannot be read
        intro_data = {"description": []}

    return jsonify(intro_data)


@socketio.on("message")
def message(data):
    message_text = data["data"]

    datetime_now = datetime.now(IST)

    # Format the datetime as desired: date:monthname:year and 12-hr time format
    formatted_date = datetime_now.strftime("%d %B %Y")
    formatted_time = datetime_now.strftime("%I:%M %p")
    final_time = formatted_date + " - " + formatted_time
    content = {
        "message": message_text,
        "datetime": formatted_date + " - " + formatted_time,
    }
    print(content)
    socketio.emit("message", content)

    # with mysql.cursor() as cursor:
    #     cursor.execute("INSERT INTO messages (message, datetime) VALUES (%s, %s)", (message_text, final_time))
    #     mysql.commit()


# @app.route("/history")
# def get_chat_history():
#     with mysql.cursor() as cursor:
#         cursor.execute("SELECT message, datetime FROM messages ORDER BY id DESC LIMIT 100")
#         rows = cursor.fetchall()
#         print(jsonify({"messages": [{"message": row[0], "datetime": row[1]} for row in rows]}))
#     return jsonify({"messages": [{"message": row[0], "datetime": row[1]} for row in rows]})





##=========================ROUTER========================##


    
    
##=========================ROUTER========================##





app.after_request(add_cache_headers)
if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0")
