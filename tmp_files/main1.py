from flask import Flask, render_template, request, session, jsonify
from flask_socketio import SocketIO
import MySQLdb
from datetime import datetime
import pytz
  


app = Flask(__name__)

app.config["SECRET_KEY"] = "your_secret_key_here"
#app.config["MYSQL_HOST"] = "mysql-202fbrdp-k.alwaysdata.net"
#app.config["MYSQL_USER"] = "322595"
#app.config["MYSQL_PASSWORD"] = "kousicreddy2211"
#app.config["MYSQL_DB"] = "202fbrdp-k_chatrtc"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "chatrtc"
###################################################################################\
name = "202FBRDP"
A1="https://firebasestorage.googleapis.com/v0/b/kr-cdn.appspot.com/o/1.webp?alt=media&token=7101fb13-bbba-4f43-bb2b-c4616bdd1453"
A2="https://firebasestorage.googleapis.com/v0/b/kr-cdn.appspot.com/o/2.webp?alt=media&token=56e09231-fb3d-4b90-bd7a-d39d79a8b49e"
A3="https://firebasestorage.googleapis.com/v0/b/kr-cdn.appspot.com/o/3.webp?alt=media&token=0b06f523-ad8e-4531-aeb8-925f67154ce2"
A4="https://firebasestorage.googleapis.com/v0/b/kr-cdn.appspot.com/o/4.webp?alt=media&token=4eda5ac1-2b1b-48e0-975d-37fe17f53f1e"
A5="https://firebasestorage.googleapis.com/v0/b/kr-cdn.appspot.com/o/5.webp?alt=media&token=437034c1-eddf-4b85-96af-f4a74ef83a7e"
A6="https://firebasestorage.googleapis.com/v0/b/kr-cdn.appspot.com/o/6.webp?alt=media&token=10153472-3c88-4bfd-848f-04997eeb41ca"
A7="https://firebasestorage.googleapis.com/v0/b/kr-cdn.appspot.com/o/7.webp?alt=media&token=41f6e68f-ef36-430d-8a73-417550d81e18"
A8="https://firebasestorage.googleapis.com/v0/b/kr-cdn.appspot.com/o/8.webp?alt=media&token=9c25ac77-a08f-497d-a132-b0e610b67f8c"
A9="https://firebasestorage.googleapis.com/v0/b/kr-cdn.appspot.com/o/9.webp?alt=media&token=a307e12b-76c2-4d3a-9010-ffbf9b2aa8f2"
A10="https://firebasestorage.googleapis.com/v0/b/kr-cdn.appspot.com/o/10.webp?alt=media&token=4c026fad-e8b7-4f23-a957-3104dd32a897"
A11="https://firebasestorage.googleapis.com/v0/b/kr-cdn.appspot.com/o/11.webp?alt=media&token=c034277e-7051-4bac-b08d-44561234b866"
A12="https://firebasestorage.googleapis.com/v0/b/kr-cdn.appspot.com/o/12.webp?alt=media&token=a833bc2c-94b0-4d92-a65a-63ce88cb8ab4"
A13="https://firebasestorage.googleapis.com/v0/b/kr-cdn.appspot.com/o/13.webp?alt=media&token=557dcc9d-944e-4717-9855-6189528e465e"
A14="https://firebasestorage.googleapis.com/v0/b/kr-cdn.appspot.com/o/14.webp?alt=media&token=83fba94d-a619-4411-a419-b758c841802f"
A15="https://firebasestorage.googleapis.com/v0/b/kr-cdn.appspot.com/o/15.webp?alt=media&token=37b07c90-fc61-4059-8943-ff670ee0672b"
###################################################################################
IST = pytz.timezone('Asia/Kolkata')
socketio = SocketIO(app)
mysql = MySQLdb.connect(
    host=app.config["MYSQL_HOST"],
    user=app.config["MYSQL_USER"],
    passwd=app.config["MYSQL_PASSWORD"],
    db=app.config["MYSQL_DB"]
)

# Create the 'messages' table if it doesn't exist
with mysql.cursor() as cursor:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            message TEXT,
            profile VARCHAR(20),
            datetime VARCHAR(45)
        )
    """)
    mysql.commit()

@app.route("/", methods=["POST", "GET"])
def home():
    session.clear()
    return render_template("public.html",name=name,
                        
                    A1=A1,
                    A2=A2,
                    A3=A3,
                    A4=A4,
                    A5=A5,
                    A6=A6,
                    A7=A7,
                    A8=A8,
                    A9=A9,
                    A10=A10,
                    A11=A11,
                    A12=A12,
                    A13=A13,
                    A14=A14,
                    A15=A15)
def finalimg(Img):
    if Img == "A1":
        return A1
    elif Img == "A2":
        return A2
    elif Img == "A3":
        return A3
    elif Img == "A4":
        return A4
    elif Img == "A5":
        return A5
    elif Img == "A6":
        return A6
    elif Img == "A7":
        return A7
    elif Img == "A8":
        return A8
    elif Img == "A9":
        return A9
    elif Img == "A10":
        return A10
    elif Img == "A11":
        return A11
    elif Img == "A12":
        return A12
    elif Img == "A13":
        return A13
    elif Img == "A14":
        return A14
    elif Img == "A15":
        return A15
   

@socketio.on("message")
def message(data):
    message_text = data["data"]
    message_profile = finalimg(data["Image"])


    datetime_now = datetime.now(IST)

    # Format the datetime as desired: date:monthname:year and 12-hr time format
    formatted_date = datetime_now.strftime("%d %B %Y")
    formatted_time = datetime_now.strftime("%I:%M %p")
    final_time = formatted_date + " - " + formatted_time
    content = {
        "message": message_text,
        "Img" : message_profile,
        "datetime":formatted_date + " - " + formatted_time
    }
    print(content)
    socketio.emit("message", content)

    with mysql.cursor() as cursor:
        cursor.execute("INSERT INTO messages (message, datetime, profile) VALUES (%s, %s, %s)", (message_text, final_time, data["Image"]))
        mysql.commit()

    

@app.route("/history")
def get_chat_history():
    with mysql.cursor() as cursor:
        cursor.execute("SELECT message, datetime, profile FROM messages ORDER BY id DESC LIMIT 100")
        rows = cursor.fetchall()
        print(jsonify({"messages": [{"message": row[0], "datetime": row[1],"profile":finalimg(row[2])} for row in rows]}))
    return jsonify({"messages": [{"message": row[0], "datetime": row[1],"profile":finalimg(row[2])} for row in rows]})

if __name__ == "__main__":
    socketio.run(app, debug=True)
