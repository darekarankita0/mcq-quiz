import os
from flask import Flask, session, render_template, url_for, redirect, request, flash
import uuid
from flask_session import Session
from copy import deepcopy
from datetime import datetime, date, time
from random import choice, shuffle
# Create a flask app and set its secret key
#app = Flask(__name__)
#app.secret_key = os.urandom(24)
#
app = Flask(__name__)
app.secret_key = str(uuid.uuid1())
print("Secret = {secret}.".format(secret=app.secret_key))
#SESSION_TYPE = "redis"
#PERMANENT_SESSION_LIFETIME = 1800

#app.config.update(SECRET_KEY=os.urandom(24))

#app.config.from_object(__name__)
#Session(app)
questions = {
'1': {'tip': 'Proximity Detection', 'answer': 'Proximity Detection','question': 'What is the use of the Ultrasonic Sensor?','options': ['Proximity Detection','Humidity Detection','Image Processing','GPS']},'4': {'tip': '4', 'answer': '4', 'question': "How many pins are present in the Ultrasonic Sensor",'options': ['1', '3', '2', '4']}, '2': {'tip': 'Digital', 'answer': 'Digital', 'question': 'What mode should we put the Arduino pin to, in order for object detection to work with the Ultrasonic Sensor?','options': ['Analog','Digital','PCM','TDM']},'6': {'tip': 'Damage is caused', 'answer': 'Damage is caused','question': 'What will happen if we supply a voltage of 25V to the Vcc of the Ultrasonic sensor?','options': ['Damage is caused','Sensor will work fine','Sensor will not respond for the time the voltage is applied','Sensor will function normally']}, '5': {'tip': 'Object is oscillating side by side', 'answer': "Object is oscillating side by side", 'question': 'If 1 means an object is detected and 0 meaning no object is detected, then considering the sensor is stationary, what can be said about the movement of the object if the output by the sensor is 1010101?', 'options': ['Object is stationary','Object is oscillating side by side','Object is continuously moving away','Object is continuously moving closer']},'3': {'tip': 'Sound', 'answer': 'Sound', 'question': 'What kind of waves does the Ultrasonic Sensor work on?', 'options': ['Gas','Heat','Light','Sound']},'7': {'tip': '15 mA', 'answer': '15 mA', 'question': 'What is the optimum current that is required to operate the Ultrasonic Sensor?', 'options': ['20 mA','15 mA','200 A','1 A']}
}
#
py_summary={}
py_summary["correct"]=[]
py_summary["wrong"]=[]
py_summary["curretq"]=1
score = len(py_summary["correct"])
py_summary["score"]=[]

#
app.nquestions=len(questions)
#
# options to the questions can be shuffled
#
# for item in questions.keys():
   # shuffle(questions[item]['options'])   
#
#

@app.route('/', methods=['GET', 'POST'])
def index():
#	
  if request.method == "POST":
    
    # The data has been submitted via POST request.
    #
    entered_answer = request.form.get('answer_python', '')
#   
    if not entered_answer:
      flash("Please choose an answer", "error") # Show error if no answer entered
    
    else:

      curr_answer=request.form['answer_python']
      correct_answer=questions[session.get("current_question")]["answer"]
# 
      if curr_answer == correct_answer[:len(curr_answer)]: 
        py_summary["correct"].append(int(session["current_question"]))
        score = len(py_summary["correct"])
        print(score)
        py_summary["score"]=score
#      
      else:
        py_summary["wrong"].append(int(session["current_question"]))
#		
      # set the current question to the next number when checked
      session["current_question"] = str(int(session["current_question"])+1)
      py_summary["curretq"]= max(int(session["current_question"]), py_summary["curretq"])	  
#   
      if session["current_question"] in questions:
        # If the question exists in the dictionary, redirect to the question
        #
        redirect(url_for('index'))
      
      else:
        # else redirect to the summary template as the quiz is complete.
        py_summary["wrong"]=list(set(py_summary["wrong"]))
        py_summary["correct"]=list(set(py_summary["correct"]))	
        score = len(py_summary["correct"])
        print(score)
        py_summary["score"]=score
        return render_template("end_miniquiz.html",summary=py_summary)
#  
  if "current_question" not in session:

    session["current_question"] = "1"
#  
  elif session["current_question"] not in questions:

    py_summary["wrong"]=list(set(py_summary["wrong"]))
    py_summary["correct"]=list(set(py_summary["correct"]))
    score = len(py_summary["correct"])
    print(score)
    py_summary["score"]=score
    print(py_summary["correct"])
    print(py_summary["wrong"])
    return render_template("end_miniquiz.html",summary=py_summary)
  
  # If the request is a GET request 
  currentN=int(session["current_question"])   
  currentQ =  questions[session["current_question"]]["question"]
  a1, a2, a3,a4 = questions[session["current_question"]]["options"] 
  # 
  return render_template('python_miniquiz.html',num=currentN,ntot=app.nquestions,question=currentQ,ans1=a1,ans2=a2,ans3=a3,ans4=a4)   
#
@app.route('/checkform_python',methods=['GET','POST'])
def check_answer():
    the_color1='Black';the_color2='Black';the_color3='Black';	
    the_color4='Black';the_color6='Black';
    the_check1='';the_check2='';the_check3='';the_check4='';
#
#    session["current_question"]=str(py_summary["curretq"])
    if "current_question" not in session:
        session["current_question"] = "1"		
    #
#	
    currentN = int(session["current_question"])   
    currentQ = questions[session["current_question"]]["question"]
    a1, a2, a3, a4 = questions[session["current_question"]]["options"] 
#
#
    curr_answer=request.form['answer_python']
    correct_answer=questions[session["current_question"]]["answer"]
    tip=questions[session["current_question"]]["tip"]
# track quiz check history
    f = open('mini_log.txt','a') #a is for append
    f.write('%s\n'%(datetime.now().strftime("%A, %d. %B %Y %I:%M%p")))		
    f.write('Current number: %s, '%(currentN))			
    f.write('Current question: %s\n'%(currentQ))	
    f.write('Correct answer: %s\n'%(correct_answer))
    f.write('Current selection: %s\n'%(curr_answer))	#	
    f.close()
#
    if curr_answer == correct_answer[:len(curr_answer)]: the_color6="Green"
    if curr_answer in a1[:len(curr_answer)]:
        if curr_answer in correct_answer[:len(curr_answer)]:
            the_color1="Green"
            the_check1=' - correct'
        else: 
            the_color1="Red"		
            the_check1=' - incorrect'		
#
    if curr_answer in a2[:len(curr_answer)]:
        if curr_answer in correct_answer[:len(curr_answer)]:
            the_color2="Green"
            the_check2='- correct'
        else: 
            the_color2="Red"			
            the_check2=' - incorrect'
#
    if curr_answer in a3[:len(curr_answer)]:
        if curr_answer in correct_answer[:len(curr_answer)]:
            the_color3="Green"
            the_check3=' - correct'
        else: 
            the_color3="Red"			
            the_check3=' - incorrect'
#			
    if curr_answer in a4[:len(curr_answer)]:
        if curr_answer in correct_answer[:len(curr_answer)]:
            the_color4="Green"
            the_check4=' - correct'
        else: 
            the_color4="Red"			
            the_check4=' - incorrect'
#
		
    return render_template('python_answer.html',num=currentN,ntot=app.nquestions,descript=tip,anscheck1=the_check1,anscheck2=the_check2,anscheck3=the_check3,anscheck4=the_check4,ans_color1=the_color1,ans_color2=the_color2,ans_color3=the_color3,ans_color4=the_color4,ans_color6=the_color6,question=currentQ,ans1=a1,ans2=a2,ans3=a3,ans4=a4)
# Runs the app using the web server on port 80, the standard HTTP port
if __name__ == '__main__':
	with app.test_request_context("/"):
		session["key"] = "value"
	#const PORT = process.env.PORT || '8080'
	#app=express();
	#app.set("port",PORT);
	#host="0.0.0.0"
	#port=33507
	app.run()
	#app.secret_key = 'super secret key'
	#app.config['SESSION_TYPE'] = 'filesystem'
	#sess.init_app(app)
	#app.debug=True
        # host="0.0.0.0",
        # port=33507
