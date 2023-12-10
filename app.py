from flask import Flask,render_template,redirect,request,render_template_string
import random,string
app=Flask(__name__)
data={}

def shortner(longurl):
    shorturl=""
    chars=string.ascii_letters + string.digits
    for _ in range(6):
        shorturl+=random.choice(chars)
    if shorturl in data.keys():
        shortner(longurl)
    else:
        data[shorturl]=longurl
    return shorturl
        
@app.route('/', methods=["POST", "GET"])
def main():
    if request.method=="POST":
        longurl=request.form['url']
        shorturl=shortner(longurl)
        shortnedlink=request.url_root+shorturl
        return render_template('index.html',result=shortnedlink,info="URL Successfully Generated")
    else:
        return render_template('index.html')

@app.route('/<shorturl>')
def redirect_function(shorturl):
    if shorturl in data:
        return redirect(data[shorturl])
    else:
        return render_template_string('PageNotFound {{ errorCode }}', errorCode='404'), 404
    
if __name__=='__main__':
    app.run()