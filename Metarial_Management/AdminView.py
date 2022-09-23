from django.shortcuts import render
from. import Pool
from . import PoolDict

def AdminLogin(request):
    try:
        result = request.session['ADMIN']
        return render(request, 'AdminDashBoard.html', {'result': result})
    except Exception as e:
        return render(request,'AdminLogin.html')

def CheckAdminLogin(request):
    try:
        emailid = request.POST['emailid']
        password = request.POST['password']
        db, cmd = PoolDict.ConnectionPool()
        q = "select * from Admins where emailid='{}' and password='{}'".format(emailid, password)
        cmd.execute(q)
        result = cmd.fetchone()
        print(result)
        if(result):
            request.session['ADMIN']=result
            #Total Employees
            db, cmd = PoolDict.ConnectionPool()
            p = "select count(*) as n from employee"
            cmd.execute(p)
            r1 = cmd.fetchone()
            #Total Categories
            s = "select count(*) as n from categories"
            cmd.execute(s)
            r2 = cmd.fetchone()
            #Total Products
            t = "select count(*) as n from finalproducts"
            cmd.execute(t)
            r3 = cmd.fetchone()
            u = "select count(*) as n from suppliers"
            cmd.execute(u)
            r4 = cmd.fetchone()
            #Purchases
            db, cmd = Pool.ConnectionPool()
            pr = "select PP.*,(select C.categoryname from categories C where C.categoryid = PP.categoryid),(select S.subcategoryname from subcategory S where S.subcategoryid = PP.subcategoryid), (select P.productname from products P where P.productid = PP.productid), (select FP.finalproductname from finalproducts FP where FP.finalproductid = PP.finalproductid), (select S.firstname from suppliers S where S.supplierid = PP.supplierid) from purchase PP"
            cmd.execute(pr)
            rows = cmd.fetchall()
            # Issues
            ir = "select IP.*,(select C.categoryname from categories C where C.categoryid = IP.categoryid),(select S.subcategoryname from subcategory S where S.subcategoryid = IP.subcategoryid), (select P.productname from products P where P.productid = IP.productid), (select FP.finalproductname from finalproducts FP where FP.finalproductid = IP.finalproductid) from issue IP"
            cmd.execute(ir)
            irows = cmd.fetchall()
            print(irows)
            return render(request, 'AdminDashboard.html',{'result': result, 'r1': r1, 'r2': r2, 'r3': r3, 'r4': r4, 'rows': rows, 'irows': irows})
        else:
            return render(request, 'AdminLogin.html', {'result': result,'msg':'Invalid Email/Password'})
        db.close()
        return render(request, 'AdminDashboard.html', {'result': result})
    except Exception as e:
        print(e)
        return render(request, 'AdminLogin.html', {'result': {},'msg':'Server Error '})

def AdminDashboard(request):
    db, cmd = PoolDict.ConnectionPool()
    result=request.session['ADMIN']
    # Total Employees
    db, cmd = PoolDict.ConnectionPool()
    p = "select count(*) as n from employee"
    cmd.execute(p)
    r1 = cmd.fetchone()
    # Total Categories
    s = "select count(*) as n from categories"
    cmd.execute(s)
    r2 = cmd.fetchone()
    # Total Products
    t = "select count(*) as n from finalproducts"
    cmd.execute(t)
    r3 = cmd.fetchone()
    u = "select count(*) as n from suppliers"
    cmd.execute(u)
    r4 = cmd.fetchone()
    # Purchases
    db, cmd = Pool.ConnectionPool()
    pr = "select PP.*,(select C.categoryname from categories C where C.categoryid = PP.categoryid),(select S.subcategoryname from subcategory S where S.subcategoryid = PP.subcategoryid), (select P.productname from products P where P.productid = PP.productid), (select FP.finalproductname from finalproducts FP where FP.finalproductid = PP.finalproductid), (select S.firstname from suppliers S where S.supplierid = PP.supplierid) from purchase PP"
    cmd.execute(pr)
    rows = cmd.fetchall()
    #Issues
    ir = "select IP.*,(select C.categoryname from categories C where C.categoryid = IP.categoryid),(select S.subcategoryname from subcategory S where S.subcategoryid = IP.subcategoryid), (select P.productname from products P where P.productid = IP.productid), (select FP.finalproductname from finalproducts FP where FP.finalproductid = IP.finalproductid) from issue IP"
    cmd.execute(ir)
    irows = cmd.fetchall()
    return render(request, 'AdminDashboard.html',{'result': result, 'r1': r1, 'r2': r2, 'r3': r3, 'r4': r4, 'rows': rows,'irows':irows})

def AdminLogut(request):
    del request.session['ADMIN']
    return render(request, 'AdminLogin.html')

def Index(request):
    try:
        return render(request, 'Index.html')
    except Exception as e:
        return render(request,'Index.html')
