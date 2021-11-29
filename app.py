from flask import *
import random,string,requests
import pandas as pd
import os


app = Flask(__name__)

username = "annorboadu"
apiKey = "ad43cb64139370fa55479c9446b08c8b"
From = "NARMGH"
url = "https://sms.dtechghana.com/api/v1/messages"
headers = {'Content-Type': 'application/json', 'Host': 'sms.dtechghana.com'}



@app.route('/home', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        if request.form['prime'] == 'signin':
            # Sign-in Functionality
            #print(myquery)
            df= pd.read_csv('database.csv')

            #print(df['Userid'])
            #print(request.form['pass'])

            if request.form['userid'] in df['Userid'].values:
                #print('fsakfna')
                dff= df[df['Userid'] == request.form['userid']]
                if len(dff) > 0:
                    count= 1
                else:
                    count= 0
                print(type(dff.values))
                print(dff.values)

                if dff['Password'].values == request.form['pass']:
                    userdata= dict(zip(df.columns.values, dff.values[0]))
                    return render_template('signedin.html',Userdata=userdata,count= count)

            return render_template('signedin.html')
        elif request.form['prime'] == 'signup':
            # Signup Functionality
            return render_template('signup.html')

        elif request.form['prime'] == 'sub':
            #Pushing to MongoDB Feature starts here
            try:
                payingmember= request.form['paying_member']
            #default
            except:
                payingmember= "No"
            password= ''.join(random.sample((string.ascii_lowercase + string.digits), 6))
            user_json= {
            'Paying_member': payingmember,
            'Surname': request.form['surname'],
            'FirstName': request.form['firstname'],
            'Middlename': request.form['middlename'],
            'Userid': 'NARMGH21/'+ str(1000),
            'Password': password,
            'Dob': request.form['dob'],
            'Gender': request.form['gender'],
            'Contact_no': request.form['contactno'],
            'Ghana_Card_no': request.form['cardno'],
            'Home_address': request.form['homeaddress'],
            'Regions': request.form['regions'],
            'District': request.form['district'],
            'Place_of_work': request.form['placeofwork'],
            'Rank': request.form['rank'],
            'Staffid': request.form['staffid'],
            'Pin': request.form['pin'],
            'Qualification': request.form['qualification']
            }
            df_user = pd.DataFrame([user_json])
            #print(df_user)
            df_user.to_csv('database.csv', mode='a', index= False,header=False)

            #Send sms to the Number
            To = request.form['contactno']
            mesg= "Dear "+ request.form['firstname'] +'\n'+ 'Your Registration has been received at NARMGH'+'\n'+'secretariat.'+\
                  '\n'+'\n' + 'Login details of NARMGH are'+ '\n' +'\n'+ 'UserID: '+ 'NARMGH21/'+ str(1000) + '\n'+ \
                  'Password: ' + password +'\n' + '\n' +'The information submitted is highly protected'+'\n' + 'Thank you.'

            payload = json.dumps({'to': To, 'from': From, 'content': mesg})
            response = requests.post(url, data=payload, headers=headers, auth=(username, apiKey))
            return render_template('registered.html')
    else:
        return render_template('homepage.html')

    return render_template('homepage.html')

if __name__ == '__main__':
    app.run()
