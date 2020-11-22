from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def student():
   return render_template('lol.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      number=int(result['number'])
      names=[]
      required_fields=result.getlist('interest')
      # phone_number_bool=bool(result['phone_number']=='on')
      # email_personal_bool=bool(result['email_personal']=='on')
      # email_institute_bool=bool(result['email_institute']=='on')
      # section_bool=bool(result['section']=='on')

      for i in range(1,number+1):
         names.append(result['textbox'+str(i)])
         
      return render_template("result.html",result = result,names=names,required_fields=required_fields)

if __name__ == '__main__':
   app.run(debug = True)