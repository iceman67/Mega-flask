from flask import Flask
import DS1820
app = Flask(__name__)
 
@app.route("/")
def hello():
    dev = DS1820()
    L = dev.get_temp_list()
    temp_str = ','.join(str(x) for x in L)
    return temp_str
 
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8000)
