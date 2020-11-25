from flask import Flask, render_template, request,Response, flash
from client import Client
from CNS import Answer,Message
import pandas as pd


import toml
conf = toml.load("setup.toml")
server_config = conf.get("database")
records = server_config.get("records")

# ---------------------------------------------

Dict_record = {"phone_number":records[0],
               "email_institute":records[1],
               "email_personal":records[2],
               "section":records[3]}

# ------------------------------------------------

c = Client("setup.toml")
app = Flask(__name__)
app.config['SECRET_KEY'] = '21a00ee024ebe902cf1848208f5c1a29'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
df=pd.DataFrame()


def Process_msg(msg: Message, required_fields):
    arr = []
    j=0
    for answer in msg.answers:
        if(answer.status_code == 0):
            arr.append({"No records Found for this user":""})
        else:
            ret_records = answer.records
            field_name = required_fields[j]
            d1 = [[field_name[i],ret_records[i]] for i in range(len(ret_records))]
            d = dict(d1)
            arr.append(d)
        j+=1
    return arr



@app.route('/')
def student():
   return render_template('lol.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      number=int(result['number'])
      names=[]
      required_fields=[]
      for i in range(1,number+1):
         names.append(result['textbox'+str(i)])
         required_fields.append(result.getlist('interest'+str(i)))
      print(names,required_fields)
      for required_field in required_fields:
          if(len(required_field)==0):
            flash('Please select atleast one field !!', 'danger')
            return render_template("lol.html")
      for i in range(len(required_fields)):
        required_fields[i] = list(map(Dict_record.get,required_fields[i]))
      qry_lst = [[names[i],required_fields[i]] for i in range(number)]
      c.make_qrymsg(qry_lst)
      c.send_qry()
      d = c.rcv_msg()
      d = Message.decode(d)

      p_msg = Process_msg(d, required_fields)

      global df
      df=pd.DataFrame(p_msg,index=names)
      return render_template("result.html",output=dict(zip(names,p_msg)))

@app.route('/download')
def download():
    global df
    #print(df.index)
    return Response(
       df.to_csv(),
       mimetype="text/csv",
       headers={"Content-disposition":
       "attachment; filename=filename.csv"})


if __name__ == '__main__':
   app.run(debug = True)