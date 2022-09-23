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
        email = request.POST['email']
        password = request.POST['password']
        db, cmd = PoolDict.ConnectionPool()
        q = "select * from employee where email='{}' and password='{}'".format(email, password)
        cmd.execute(q)
        result = cmd.fetchone()
        print(result)
        if(result):
            request.session['EMPLOYEE']=result
            #Total Products
            db, cmd = PoolDict.ConnectionPool()
            p = "select count(*) as n from products"
            cmd.execute(p)
            r1 = cmd.fetchone()
            #Total Purchases
            s = "select count(*) as n from finalproducts"
            cmd.execute(s)
            r2 = cmd.fetchone()
            #Total Issue
            t = "select count(*) as n from purchase"
            cmd.execute(t)
            r3 = cmd.fetchone()
            #Total Issues
            u = "select count(*) as n from issue"
            cmd.execute(u)
            r4 = cmd.fetchone()
            # Purchases
            db, cmd = Pool.ConnectionPool()
            pr = "select PP.*,(select C.categoryname from categories C where C.categoryid = PP.categoryid),(select S.subcategoryname from subcategory S where S.subcategoryid = PP.subcategoryid), (select P.productname from products P where P.productid = PP.productid), (select FP.finalproductname from finalproducts FP where FP.finalproductid = PP.finalproductid), (select S.firstname from suppliers S where S.supplierid = PP.supplierid) from purchase PP"
            cmd.execute(pr)
            rows = cmd.fetchall()
            # Issues
            ir = "select IP.*,(select C.categoryname from categories C where C.categoryid = IP.categoryid),(select S.subcategoryname from subcategory S where S.subcategoryid = IP.subcategoryid), (select P.productname from products P where P.productid = IP.productid), (select FP.finalproductname from finalproducts FP where FP.finalproductid = IP.finalproductid) from issue IP"
            cmd.execute(ir)
            irows = cmd.fetchall()
            print(irows)
            return render(request, 'EmployeeDashboard.html',{'result': result, 'r1': r1, 'r2': r2, 'r3': r3, 'r4': r4, 'rows': rows, 'irows': irows})
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
    result= request.session['EMPLOYEE']
    # Total Products
    db, cmd = PoolDict.ConnectionPool()
    p = "select count(*) as n from products"
    cmd.execute(p)
    r1 = cmd.fetchone()
    # Total Purchases
    s = "select count(*) as n from finalproducts"
    cmd.execute(s)
    r2 = cmd.fetchone()
    # Total Issue
    t = "select count(*) as n from purchase"
    cmd.execute(t)
    r3 = cmd.fetchone()
    # Total Issues
    u = "select count(*) as n from issue"
    cmd.execute(u)
    r4 = cmd.fetchone()
    # Purchases
    db, cmd = Pool.ConnectionPool()
    pr = "select PP.*,(select C.categoryname from categories C where C.categoryid = PP.categoryid),(select S.subcategoryname from subcategory S where S.subcategoryid = PP.subcategoryid), (select P.productname from products P where P.productid = PP.productid), (select FP.finalproductname from finalproducts FP where FP.finalproductid = PP.finalproductid), (select S.firstname from suppliers S where S.supplierid = PP.supplierid) from purchase PP"
    cmd.execute(pr)
    rows = cmd.fetchall()
    # Issues
    ir = "select IP.*,(select C.categoryname from categories C where C.categoryid = IP.categoryid),(select S.subcategoryname from subcategory S where S.subcategoryid = IP.subcategoryid), (select P.productname from products P where P.productid = IP.productid), (select FP.finalproductname from finalproducts FP where FP.finalproductid = IP.finalproductid) from issue IP"
    cmd.execute(ir)
    irows = cmd.fetchall()
    print(irows)
    return render(request, 'EmployeeDashboard.html',{'result': result, 'r1': r1, 'r2': r2, 'r3': r3, 'r4': r4, 'rows': rows, 'irows': irows})

@xframe_options_exempt
def EmployeeInterface(request):
    try:
        result=request.session['ADMIN']
        return render(request,'EmployeeInterface.html',{'result': result})

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

        #EmailService.SendHTMLMail(emailaddress,"Hi {} Your Login Password for Material Management is {} ".format(firstname,password))
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
        return render(request, 'DisplayAllEmployee.html', {'result':result,'rows':rows})

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
            p = "update employee set employeeid=employeeid-1 where employeeid>{}".format(empid)
            cmd.execute(p)
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
