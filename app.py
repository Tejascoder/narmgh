from flask import *
import random,string,requests
import pandas as pd
import os
from creds import admin
app = Flask(__name__)
us,pw= admin()
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
                #print(type(dff.values))
                #print(dff.values)
                if dff['Password'].values == request.form['pass']:
                    userdata= dict(zip(df.columns.values, dff.values[0]))
                    del userdata['Password']
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
            df = pd.read_csv('database.csv')
            last_row= df.iloc[-1:]
            #print(last_row)
            id= int( str(last_row['Userid'].values[0]).split('/')[1] ) + 1
            password= ''.join(random.sample((string.ascii_lowercase + string.digits), 6))
            if request.form['middlename']:
                midname= request.form['middlename']
            else:
                midname = ' '
            user_json= {
            'Paying_member': payingmember,
            'Surname': request.form['surname'],
            'FirstName': request.form['firstname'],
            'Middlename': midname,
            'Userid': 'NARMGH21/'+ str(id),
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
            print(df_user)
            df_user.to_csv('database.csv', mode='a', index= False,header=False)

            #Send sms to the Number
            To = '233' + request.form['contactno'][1:]
            mesg= "Dear "+ request.form['firstname'] +'\n'+ 'Your Registration has been received at NARMGH'+'\n'+'secretariat.'+\
                  '\n'+'\n' + 'Login details of NARMGH are'+ '\n' +'\n'+ 'UserID: '+ 'NARMGH21/'+ str(id) + '\n'+ \
                  'Password: ' + password +'\n' + '\n' +'The information submitted is highly protected'+'\n' + 'Thank you.'

            payload = json.dumps({'to': To, 'from': From, 'content': mesg})
            response = requests.post(url, data=payload, headers=headers, auth=(username, apiKey))
            return render_template('registered.html')
    else:
        return render_template('homepage.html')

    return render_template('homepage.html')

@app.route('/admin', methods= ['GET','POST'])
def view_tables():
    df = pd.read_csv('database.csv')[1:]
    #print(df)
    count_regions= df.groupby(['Regions'])['Regions'].count()
    regions= list(count_regions.index.values)

    count= list(count_regions.values)
    counts= [int(i) for i in count]

    #Contains regional count
    #regional_counts= dict(zip(regions, counts))
    col= df.columns.values
    all_datas = df.values.tolist()
    if request.method == 'POST':
        #Check for the Admin User and Pass
        if request.form['adminid'] == us and request.form['adminpass'] == pw:
            #Enter into Admin Panel
            userids= df['Userid'].values.tolist()
            print(userids)
            return render_template('admininterface.html',all_datas=all_datas, cnt=len(df),regions=regions,counts=counts,col= col,userids=userids)

        else:
            return "Sorry.Please contact Adminstrator"
    else:
        return render_template('admin.html')

@app.route('/adminChanges', methods=['GET', 'POST'])
def admin_resub():
    if request.method == 'POST':
        if request.form['prime'] == 'resub':
            df = pd.read_csv('database.csv')[1:]
            all_datas = df.values.tolist()
            #Grouping by regions vs count graph
            count_regions = df.groupby(['Regions'])['Regions'].count()
            regions = list(count_regions.index.values)

            count = list(count_regions.values)
            counts = [int(i) for i in count]
            #Updating functionality goes here
            Uid= request.form['userId']

            #Contains Index of UID
            index= df.index[df['Userid'] == Uid].values[0]
            selcted_Pass= df.loc[index]['Password']
            print(selcted_Pass)

            try:
                payingmember= request.form['paying_member']
            #default
            except:
                payingmember= "No"

            if request.form['middlename']:
                midname= request.form['middlename']
            else:
                midname = ' '
            user_json = {
                'Paying_member': payingmember,
                'Surname': request.form['surname'],
                'FirstName': request.form['firstname'],
                'Middlename':midname,
                'Userid': Uid,
                'Password': selcted_Pass,
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
            print('DONE')
            df.loc[index, list(df.columns.values)] = list(user_json.values())
            #df now has updated ignoring the first row
            df_copy = pd.read_csv('database.csv')
            #print(df_copy.iloc[0])
            first_dummy= list(df_copy.iloc[0].values)
            final= [first_dummy] + df.values.tolist()
            print(final)
            df_final = pd.DataFrame(final, columns= list(df.columns.values))
            print(df_final)
            df_final.to_csv('database.csv',index= False)
            df = pd.read_csv('database.csv')[1:]
            all_datas = df.values.tolist()
            return render_template('admininterface.html', all_datas=all_datas,regions=regions,counts=counts, cnt=len(df), col=df.columns.values)

    else:
        df = pd.read_csv('database.csv')[1:]
        all_datas = df.values.tolist()
        return render_template('admininterface.html',all_datas=all_datas, cnt=len(df), col= df.columns.values)

@app.route('/printuser', methods=['GET', 'POST'])
def print_user():
    df = pd.read_csv('database.csv')
    col =list(df.columns.values)
    #View feature having data in array
    return render_template('printuser.html', col=col)



if __name__ == '__main__':
    app.run()
