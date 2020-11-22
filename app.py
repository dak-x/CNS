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
      required_fields=[]
      
      for i in range(1,number+1):
         names.append(result['textbox'+str(i)])
         required_fields.append(result.getlist('interest'+str(i)))
         
      return render_template("result.html",result = result,names=names,required_fields=required_fields)

if __name__ == '__main__':
   app.run(debug = True)