from flask import Flask,render_template,redirect,request,render_template_string,url_for
import random,string,json
app=Flask(__name__)
data={}

def shortner(longurl):
    data=json.loads(open('/etc/secrets/data','r').read())
    shorturl=""
    chars=string.ascii_letters + string.digits
    for _ in range(6):
        shorturl+=random.choice(chars)
    if shorturl in data.keys():
        shortner(longurl)
    else:
        data[shorturl]=longurl
        with open('/etc/secrets/data','w') as file:
            file.write(str(data).replace("'",'"'))
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
    data=json.loads(open('/etc/secrets/data','r').read())
    if shorturl in data:
        return redirect(data[shorturl])
    else:
        return render_template_string('PageNotFound {{ errorCode }}', errorCode='404'), 404
    
    
@app.route('/add-custom-url', methods=["POST", "GET"])
def add_custom():
    data=json.loads(open('/etc/secrets/data','r').read())
    if request.method=="POST":
        longurl=request.form['url']
        custom=request.form['custom']
        if custom in data.keys():
            return render_template('custom.html',info="Custom Link Already Exists Try Using Another Keyword")
        else:
            data[custom]=longurl
            shortnedlink=request.url_root+custom
            with open('/etc/secrets/data','w') as file:
                file.write(str(data).replace("'",'"'))
            return render_template('custom.html',result=shortnedlink,info="URL Successfully Generated")
    else:
        return render_template('custom.html')
if __name__=='__main__':
    app.run(debug=True)