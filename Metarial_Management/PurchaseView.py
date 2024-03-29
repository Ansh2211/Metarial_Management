from django.shortcuts import render
from django.http import JsonResponse
from . import Pool
from . import PoolDict
#import uuid
#import os


def PurchaseInterface(request):
    try:
        result=request.session['EMPLOYEE']
        return render(request,'purchaseinterface.html',{'result':result})

    except Exception as e:
        return render(request, 'EmployeeLogin.html')
def PurchaseProductSubmit(request):
    try:
        employeeid = request.POST['employeeid']
        categoryid = request.POST['categoryid']
        subcategoryid = request.POST['subcategoryid']
        productid = request.POST['productid']
        finalproductid = request.POST['finalproductid']
        purchasedate = request.POST['purchasedate']
        supplierid = request.POST['supplierid']
        stock = request.POST['stock']
        amount = request.POST['amount']

        q = "insert into purchase (employeeid, categoryid, subcategoryid, productid, finalproductid, purchasedate, supplierid, stock, amount) values ({}, {}, {}, {}, {}, '{}', {}, {}, {} )".format(employeeid, categoryid, subcategoryid, productid, finalproductid, purchasedate, supplierid, stock, amount)
        print(q)
        dbe, cmd = Pool.ConnectionPool()
        cmd.execute(q)

        #Update Stock
        q="update finalproducts set price=((price+{})/2), stock=stock+{} where finalproductid={}".format(amount,stock,finalproductid)
        cmd.execute(q)

        dbe.commit()
        dbe.close()
        return render(request, "purchaseinterface.html", {'msg': 'Record Successfully Submitted'})
    except Exception as e:
        print("Error :", e)
        return render(request, "purchaseinterface.html", {'msg': 'Fail to Submit Record'})


def DisplayAllPurchaseProduct(request):
    try:
        dbe, cmd = Pool.ConnectionPool()
        q = "select PP.*,(select C.categoryname from categories C where C.categoryid = PP.categoryid),(select S.subcategoryname from subcategory S where S.subcategoryid = PP.subcategoryid), (select P.productname from products P where P.productid = PP.productid), (select FP.finalproductname from finalproducts FP where FP.finalproductid = PP.finalproductid), (select S.firstname from suppliers S where S.supplierid = PP.supplierid) from purchase PP"
        cmd.execute(q)
        rows = cmd.fetchall()
        dbe.close()
        result = request.session['EMPLOYEE']
        return render(request, "DisplayAllPurchaseProduct.html", {'rows': rows,'result':result})
    except Exception as e:
        print(e)
        return render(request, "DisplayAllPurchaseProduct.html", {'rows': []})


def EditDeletePurchaseProductRecord(request):
    btn = request.GET['btn']
    transactionid = request.GET['transactionid']
    if(btn == "Edit"):
        employeeid = request.GET['employeeid']
        categoryid = request.GET['categoryid']
        subcategoryid = request.GET['subcategoryid']
        productid = request.GET['productid']
        finalproductid = request.GET['finalproductid']
        purchasedate = request.GET['purchasedate']
        supplierid = request.GET['supplierid']
        stock = request.GET['stock']
        amount = request.GET['amount']
        try:
            dbe, cmd = Pool.ConnectionPool()
            q = "update purchase set employeeid = {}, categoryid = {}, subcategoryid = {}, productid = {}, finalproductid = {},  supplierid = {}, purchasedate = '{}', stock = {}, amount = {} where transactionid={}".format(employeeid, categoryid, subcategoryid, productid, finalproductid,  supplierid, purchasedate, stock, amount, transactionid)
            print(q)
            cmd.execute(q)
            dbe.commit()
            row = cmd.fetchone()
            dbe.close()
            return DisplayAllPurchaseProduct(request)
        except Exception as e:
            print(e)
            return DisplayAllPurchaseProduct(request)

    elif(btn == "Delete"):
        try:
            dbe, cmd = Pool.ConnectionPool()
            q = "delete from purchase where transactionid={}".format(transactionid)
            cmd.execute(q)
            p = "update purchase set transactionid=transactionid-1 where transactionid>{}".format(transactionid)
            cmd.execute(p)
            dbe.commit()
            row = cmd.fetchone()
            dbe.close()
            return DisplayAllPurchaseProduct(request)
        except Exception as e:
            print(e)
            return DisplayAllPurchaseProduct(request)

def DisplayPurchaseAllJSON(request):
    fromdate = request.GET['fromdate']
    todate = request.GET['todate']
    try:
        dbe, cmd = PoolDict.ConnectionPool()
        q = "select PP.*,(select C.categoryname from categories C where C.categoryid = PP.categoryid) as categoryname,(select S.subcategoryname from subcategory S where S.subcategoryid = PP.subcategoryid) as subcategoryname, (select P.productname from products P where P.productid = PP.productid) as productname, (select FP.finalproductname from finalproducts FP where FP.finalproductid = PP.finalproductid) as finalproductname, (select S.firstname from suppliers S where S.supplierid = PP.supplierid) as suppliername from purchase PP where purchasedate between '{}' and '{}'".format(fromdate,todate)
        cmd.execute(q)
        rows = cmd.fetchall()
        dbe.close()
        return JsonResponse(rows, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse([], safe=False)

def ListPurchaseEmployee(request):
    try:
        result = request.session['EMPLOYEE']
        return render(request,"ListPurchaseEmployee.html",{'result':result})
    except Exception as e:
        return render(request, 'EmployeeLogin.html')

