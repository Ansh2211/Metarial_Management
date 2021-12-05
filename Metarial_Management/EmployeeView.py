from django.shortcuts import render
from . import Pool
from . import PoolDict
import uuid
import random
import os
from . import SendSms
from . import EmailService
from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt
def EmployeeLogin(request):
    try:
        result = request.session['EMPLOYEE']
        return render(request, 'EmployeeDashboard.html', {'result': result})
    except Exception as e:
        return render(request, 'EmployeeLogin.html')

@xframe_options_exempt
def CheckEmployeeLogin(request):
    try:
        email = request.GET['email']
        password = request.GET['password']
        db, cmd = PoolDict.ConnectionPool()
        q = "select * from employee where email='{}' and password='{}'".format(email, password)
        cmd.execute(q)
        result = cmd.fetchone()
        print(result)
        if(result):
            request.session['EMPLOYEE']=result
            return render(request, 'EmployeeDashboard.html', {'result': result})
        else:
            return render(request, 'EmployeeLogin.html', {'result': result,'msg':'Invalid Email/Password'})
        db.close()
        return render(request, 'EmployeeDashboard.html', {'result': result})
    except Exception as e:
        return render(request, 'EmployeeLogin.html', {'result': {},'msg':'Server Error '})

@xframe_options_exempt
def EmployeeLogout(request):
    del request.session['EMPLOYEE']
    return render(request,'EmployeeLogin.html')

@xframe_options_exempt
def EmployeeDashboard(request):
  return render(request,"EmployeeDashboard.html")

@xframe_options_exempt
def EmployeeInterface(request):
    try:
        result=request.session['ADMIN']
        return render(request,'EmployeeInterface.html')

    except Exception as e:
        return render(request, 'AdminLogin.html')

@xframe_options_exempt
def EmployeeSubmit(request):
    try:
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        gender=request.POST['gender']
        birthdate=request.POST['birthdate']
        paddress=request.POST['paddress']
        states=request.POST['states']
        city=request.POST['city']
        caddress=request.POST['caddress']
        emailaddress=request.POST['emailaddress']
        mobilenumber=request.POST['mobilenumber']
        designation=request.POST['designation']

        picture=request.FILES['picture']
        filename=str(uuid.uuid4())+picture.name[picture.name.rfind('.'):]
        password="".join(random.sample(['1','5','a','x','@','#','66','r'],k=6))
        q="insert into employee(firstname, lastname, gender, dob, paddress, stateid, cityid, caddress, email, mobileno, designation, picture, password)values('{}','{}','{}','{}','{}',{},{},'{}','{}','{}','{}','{}','{}')".format(firstname,lastname,gender,birthdate,paddress,states,city,caddress,emailaddress,mobilenumber,designation,filename,password)
        db,cmd=Pool.ConnectionPool()
        cmd.execute(q)
        db.commit()
        F=open("D:/Metarial_Management/assets/"+filename,"wb")
        for chunk in picture.chunks():
            F.write(chunk)
        F.close()
        db.close()

        #result = SendSms.SendMessage("Hi {} Your Login Password for Material Management is {} ".format(firstname,password),mobilenumber)

        #EmailService.SendMail(emailaddress,"Hi {} Your Login Password for Material Management is {} ".format(firstname,password))

        EmailService.SendHTMLMail(emailaddress,"Hi {} Your Login Password for Material Management is {} ".format(firstname,password))
        #print(result.json())
        return render(request, 'EmployeeInterface.html',{'msg':'Record Submitted Successfully'})


    except Exception as e:
        print("Error:",e)
        return render(request, 'EmployeeInterface.html',{'msg':'Failed To Submit Record'})

@xframe_options_exempt
def DisplayAll(request):
    try:
        db, cmd = Pool.ConnectionPool()
        q="select E.*,(select C.cityname from cities C where C.cityid=E.cityid),(select S.statename from states S where S.stateid=E.stateid) from employee E"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        result = request.session['ADMIN']
        return render(request, 'DisplayAllEmployee.html', {'rows':rows})

    except Exception as e:
        return render(request, 'AdminLogin.html', {'rows': []})

@xframe_options_exempt
def DisplayByID(request):
    empid=request.GET['empid']
    try:
        db, cmd = Pool.ConnectionPool()
        q="select E.*,(select C.cityname from cities C where C.cityid=E.cityid),(select S.statename from states S where S.stateid=E.stateid) from employee E where employeeid={}".format(empid)
        cmd.execute(q)
        row=cmd.fetchone()
        db.close()
        return render(request, 'DisplayEmployeeByID.html', {'row': row})

    except Exception as e:
        return render(request, 'DisplayEmployeeByID.html', {'rows': []})

@xframe_options_exempt
def EditDeleteRecord(request):
    btn=request.GET['btn']
    empid=request.GET['empid']
    if(btn=="Edit"):
        firstname = request.GET['firstname']
        lastname = request.GET['lastname']
        gender = request.GET['gender']
        birthdate = request.GET['birthdate']
        paddress = request.GET['paddress']
        states = request.GET['states']
        city = request.GET['city']
        caddress = request.GET['caddress']
        emailaddress = request.GET['emailaddress']
        mobilenumber = request.GET['mobilenumber']
        designation = request.GET['designation']
        try:
            db, cmd = Pool.ConnectionPool()
            q = "update employee set firstname='{}', lastname='{}', gender='{}', dob='{}', paddress='{}', stateid={}, cityid={}, caddress='{}', email='{}', mobileno='{}', designation='{}' where employeeid={}".format(firstname, lastname, gender, birthdate, paddress, states, city, caddress, emailaddress, mobilenumber,designation,empid)
            cmd.execute(q)
            db.commit()
            db.close()
            return DisplayAll(request)

        except Exception as e:
            return DisplayAll(request)

    elif(btn=="Delete"):
        try:
            db, cmd = Pool.ConnectionPool()
            q = "delete from employee where employeeid={}".format(empid)
            cmd.execute(q)
            db.commit()
            db.close()
            return DisplayAll(request)

        except Exception as e:
            print(e)
            return DisplayAll(request)


@xframe_options_exempt
def EditEmployeePicture(request):
    try:
        empid = request.GET['empid']
        firstname = request.GET['firstname']
        lastname = request.GET['lastname']
        picture = request.GET['picture']
        row=[empid,firstname,lastname,picture]
        return render(request, 'EditEmployeePicture.html', {'row': row})

    except Exception as e:
        return render(request, 'EditEmployeePicture.html', {'row': []})

@xframe_options_exempt
def SaveEditPicture(request):
    try:
        empid=request.POST['empid']
        oldpicture=request.POST['oldpicture']
        picture=request.FILES['picture']
        filename=str(uuid.uuid4())+picture.name[picture.name.rfind('.'):]
        q="update employee set picture='{}' where employeeid={}".format(filename,empid)
        db,cmd=Pool.ConnectionPool()
        cmd.execute(q)
        db.commit()
        F=open("D:/Metarial_Management/assets/"+filename,"wb")
        for chunk in picture.chunks():
            F.write(chunk)
        F.close()
        db.close()
        os.remove('D:/Metarial_Management/assets/'+ oldpicture)
        return DisplayAll(request)

    except Exception as e:
        return DisplayAll(request)
