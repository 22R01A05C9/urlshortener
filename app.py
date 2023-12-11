from flask import Flask,render_template,redirect,request,render_template_string,url_for
import random,string,requests
app=Flask(__name__)


def shortner():
    shorturl=""
    chars=string.ascii_letters + string.digits
    for _ in range(6):
        shorturl+=random.choice(chars)
    return shorturl
        
@app.route('/', methods=["POST", "GET"])
def main():
    try:
        if request.method=="POST":
            longurl=request.form['url']
            while(1):
                shorturl=shortner()
                response=requests.post(url='https://storedataalsolens.pythonanywhere.com/save_data',data={'short':shorturl,'url':longurl})
                if response.status_code==200:
                    break
            shortnedlink=request.url_root+shorturl
            return render_template('index.html',result=shortnedlink,info="URL Successfully Generated")
        else:
            return render_template('index.html')
    except:
        return render_template('index.html',info="Some Unknown Error occured")

@app.route('/<shorturl>')
def redirect_function(shorturl):
    try:
        response=requests.post(url='https://storedataalsolens.pythonanywhere.com/get_data',data={'short':shorturl})
        if response.status_code==200:
            return redirect(str(response.text))
        else:
            return render_template_string('PageNotFound {{ errorCode }}', errorCode='404'), 404
    except:
        return "some error occured"
    
    
@app.route('/add-custom-url', methods=["POST", "GET"])
def add_custom():
    if request.method=="POST":
        try:
            longurl=request.form['url']
            custom=request.form['custom']
            response=requests.post(url='https://storedataalsolens.pythonanywhere.com/save_data',data={'short':custom,'url':longurl})
            if response.status_code==200:
                shortnedlink=request.url_root+custom
                return render_template('custom.html',result=shortnedlink,info="URL Successfully Generated")
            elif response.status_code==203:
                return render_template('custom.html',info="Custom Link Already Exists Try Using Another Keyword")     
        except:
            return render_template('custom.html',info="Some Unknown Error occured")
    else:
        return render_template('custom.html')
if __name__=='__main__':
    app.run(debug=True)