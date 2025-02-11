from flask import Flask, render_template, request, jsonify
import mysql.connector
import spacy
import datetime

app = Flask(__name__)

# to load the spaCy English language model
nlp = spacy.load("en_core_web_sm")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_schedule", methods=["POST"])
def get_schedule():
    user_input = request.form["user_input"].lower()
    response = generate_response(user_input)
    return jsonify({"response": response})

def generate_response(user_input):
    # 1- to check for greetings 
    greetings = ["hi", "hello", "hey"]
    if any(greeting in user_input.lower() for greeting in greetings):
        return "Hello! How can I help you with your schedule?"

    # 2- to check for "today" 
    if "today" in user_input:
        today = datetime.datetime.now().strftime("%A").lower()
        print(f"Today's day: {today}")  
        return get_day_schedule(today)

    # 3. to check for "help" 
    if "help" in user_input:
        return "You can ask me about your schedule for a specific day (e.g., 'What's my schedule on Monday?') or for today (e.g., 'What's my schedule today?')."

    doc = nlp(user_input)  # to process user input with spaCy

    # 4. to extract day of the week
    days_of_week = []  # to initialize the list
    for entity in doc.ents:
        if entity.label_ == "DATE":
            days_of_week.append(entity.text.lower()) 

    if days_of_week:
        response = ""
        for day in days_of_week:
            response += get_day_schedule(day) + "<br>" 
        return response

    #... (yha or bhi conditins Add kr skte hai for other intents/entities)...

    # default response if no intent/entity is recognized
    return "I am not sure I understand. Please try asking about your schedule, like 'What's my schedule on Monday?'"

def get_day_schedule(day):
    try:
        mydb = mysql.connector.connect(
          host="localhost",  
          user="root",  
          password="root",  
          database="college_routine_chatbot"  
        )
        
        mycursor = mydb.cursor()
        sql = "SELECT DISTINCT time, subject, location FROM cse2_class_schedule WHERE day = %s"  # Added DISTINCT
        val = (day,)
        print(f"Querying schedule for day: {day}")  # debug print
        mycursor.execute(sql, val)

        myresult = mycursor.fetchall()

        if myresult:
            response = f"Here's your schedule for {day.capitalize()}:<br>"
            for row in myresult:
                response += f"- {row[0]}: {row[1]} ({row[2]})<br>"  
            return response
        else:
            return f"It looks like you don't have any classes scheduled for {day.capitalize()}." #agr database me koi class nhi hai to ye response aayega
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Sorry, there was an error fetching your schedule. Please try again later."
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()

if __name__ == "__main__":
    app.run(debug=True)