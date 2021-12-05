from django.shortcuts import render
from django.http import JsonResponse
from . import Pool
import uuid
import os


def ProductInterface(request):
    try:
        result=request.session['ADMIN']
        return render(request,'ProductInterface.html')

    except Exception as e:
        return render(request, 'AdminLogin.html')


def ProductSubmit(request):
    try:
        categoryid = request.POST['categoryid']
        subcategoryid = request.POST['subcategoryid']
        productname = request.POST['productname']
        description = request.POST['description']
        gst = request.POST['gst']

        picture = request.FILES['picture']
        filename = str(uuid.uuid4()) + picture.name[picture.name.rfind('.'):]

        q = "insert into products (categoryid, subcategoryid, productname, description, gst, picture) values ({}, {}, '{}', '{}', {}, '{}')".format(
            categoryid, subcategoryid, productname, description, gst, filename)
        print(q)
        dbe, cmd = Pool.ConnectionPool()
        cmd.execute(q)
        dbe.commit()
        F = open("D:/Metarial_Management/assets/" + filename, "wb")
        for chunk in picture.chunks():
            F.write(chunk)
        F.close()
        dbe.close()
        return render(request, "ProductInterface.html", {'msg': 'Record Successfully Submitted'})
    except Exception as e:
        print("Error :", e)
        return render(request, "ProductInterface.html", {'msg': 'Fail to Submit Record'})


def DisplayAllProduct(request):
    try:
        dbe, cmd = Pool.ConnectionPool()
        q = "select P.*,(select C.categoryname from categories C where C.categoryid = P.categoryid),(select S.subcategoryname from subcategory S where S.subcategoryid = P.subcategoryid) from products P"
        cmd.execute(q)
        rows = cmd.fetchall()
        dbe.close()
        return render(request, "DisplayAllProduct.html", {'rows': rows})
    except Exception as e:
        print(e)
        return render(request, "DisplayAllProduct.html", {'rows': []})


def DisplayProductById(request):
    productid = request.GET['productid']
    try:
        dbe, cmd = Pool.ConnectionPool()
        q = "select P.*,(select C.categoryname from categories C where C.categoryid = P.categoryid),(select S.subcategoryname from subcategory S where S.subcategoryid = P.subcategoryid) from products P where productid = {}".format(
            productid)
        cmd.execute(q)
        row = cmd.fetchone()
        dbe.close()
        return render(request, "DisplayProductbyId.html", {'row': row})
    except Exception as e:
        print(e)
        return render(request, "DisplayProductById.html", {'row': []})


def EditDeleteProductRecord(request):
    btn = request.GET['btn']
    productid = request.GET['productid']
    if (btn == "Edit"):
        categoryid = request.GET['categoryid']
        subcategoryid = request.GET['subcategoryid']
        productname = request.GET['productname']
        description = request.GET['description']
        gst = request.GET['gst']
        try:
            dbe, cmd = Pool.ConnectionPool()
            q = "update products set categoryid={}, subcategoryid={}, productname='{}', description='{}', gst={} where productid={}".format(categoryid,subcategoryid,productname,description,gst,productid)
            cmd.execute(q)
            dbe.commit()
            dbe.close()
            return DisplayAllProduct(request)
        except Exception as e:
            print(e)
            return DisplayAllProduct(request)

    elif (btn == "Delete"):
        try:
            dbe, cmd = Pool.ConnectionPool()
            q = "delete from products where productid={}".format(productid)
            cmd.execute(q)
            dbe.commit()
            dbe.close()
            return DisplayAllProduct(request)
        except Exception as e:
            print(e)
            return DisplayAllProduct(request)


def EditProductPicture(request):
    try:
        productid = request.GET['productid']
        productname = request.GET['productname']
        picture = request.GET['picture']
        row = [productid, productname, picture]
        return render(request, "EditProductPicture.html", {'row': row})
    except Exception as e:
        return render(request, "EditProductPicture.html", {'row': []})


def SaveEditProductPicture(request):
    try:
        productid = request.POST['productid']
        oldpicture = request.POST['oldpicture']
        picture = request.FILES['picture']
        filename = str(uuid.uuid4()) + picture.name[picture.name.rfind('.'):]

        q = "update products set picture = '{}' where productid = {}".format(filename, productid)
        print(q)
        dbe, cmd = Pool.ConnectionPool()
        cmd.execute(q)
        dbe.commit()
        F = open("D:/Metarial_Management/assets/" + filename, "wb")
        for chunk in picture.chunks():
            F.write(chunk)
        F.close()
        dbe.close()
        os.remove('D:/Metarial_Management/assets/' + oldpicture)
        return DisplayAllProduct(request)
    except Exception as e:
        print("Error :", e)
        return DisplayAllProduct(request)

def GetProductJSON(request):
    try:
        dbe, cmd = Pool.ConnectionPool()
        subcategoryid = request.GET['subcategoryid']
        q = "select * from products where subcategoryid = {}".format(subcategoryid)
        cmd.execute(q)
        rows = cmd.fetchall()
        dbe.close()
        return JsonResponse(rows, safe=False)
    except Exception as e:
        return JsonResponse([], safe=False)

def DisplayProductEmployee(request):
    try:
        dbe, cmd = Pool.ConnectionPool()
        q = "select P.*,(select C.categoryname from categories C where C.categoryid = P.categoryid),(select S.subcategoryname from subcategory S where S.subcategoryid = P.subcategoryid) from products P"
        cmd.execute(q)
        rows = cmd.fetchall()
        dbe.close()
        return render(request, "DisplayProductEmployee.html", {'rows': rows})
    except Exception as e:
        print(e)
        return render(request, "DisplayProductEmployee.html", {'rows': []})