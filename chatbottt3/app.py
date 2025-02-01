from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_schedule", methods=["POST"])
def get_schedule():
    user_input = request.form["user_input"].lower()
    response = generate_response(user_input)
    return jsonify({"response": response})

def generate_response(user_input):
    if "schedule" in user_input:
        if "today" in user_input:
            import datetime
            today = datetime.datetime.now().strftime("%A").lower()
            return get_day_schedule(today)
        else:
            for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]: # include all days
                if day in user_input:
                    return get_day_schedule(day)
            return "Holiday!. Please specify a day like Monday, Tuesday, etc."

    elif "hello" in user_input or "hi" in user_input:
        return "Hello! How can I help you with your schedule?"

    elif "help" in user_input:
        return "You can ask me about your schedule for a specific day (e.g., 'What's my schedule on Monday?') or for today (e.g., 'What's my schedule today?')."

    else:
        return "I'm not sure I understand. Try asking about your schedule, like 'What's my schedule on Monday?'"

def get_day_schedule(day):
    try:
        mydb = mysql.connector.connect(
          host="localhost",  # our database server address
          user="root",  # our MySQL username
          password="root",  # our MySQL password
          database="college_routine_chatbot"  # name of our database
        )
        
        mycursor = mydb.cursor()
        sql = "SELECT time, subject, location FROM cse2_class_schedule WHERE day = %s"  # use correct table name
        val = (day,)
        mycursor.execute(sql, val)

        myresult = mycursor.fetchall()

        if myresult:
            response = f"Here's your schedule for {day.capitalize()}:<br>"
            for row in myresult:
                response += f"- {row[0]}: {row[1]} ({row[2]})<br>"
            return response
        else:
            return f"It looks like you don't have any classes scheduled for {day.capitalize()}."
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Sorry, there was an error fetching your schedule. Please try again later."
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()


if __name__ == "__main__":
    app.run(debug=True)