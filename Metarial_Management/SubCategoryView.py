from django.shortcuts import render
from django.http import JsonResponse
from . import Pool
import uuid
import os


def SubCategoryInterface(request):
    try:
        result=request.session['ADMIN']
        return render(request,'SubCategoryInterface.html',{'result':result})

    except Exception as e:
        return render(request, 'AdminLogin.html')



def SubCategorySubmit(request):
    try:
        categoryid = request.POST['categoryid']
        categoryname = request.POST['subcategoryname']
        description = request.POST['description']

        icon = request.FILES['icon']
        filename = str(uuid.uuid4()) + icon.name[icon.name.rfind('.'):]

        q = "insert into subcategory (categoryid, subcategoryname, description, icon) values ({},'{}','{}','{}')".format(categoryid,categoryname,description,filename)
        print(q)
        dbe, cmd = Pool.ConnectionPool()
        cmd.execute(q)
        dbe.commit()
        F = open("D:/Metarial_Management/assets/" + filename, "wb")
        for chunk in icon.chunks():
            F.write(chunk)
        F.close()
        dbe.close()
        return render(request, "SubCategoryInterface.html", {'msg': 'Record Successfully Submitted'})
    except Exception as e:
        print("Error :", e)
        return render(request, "SubCategoryInterface.html", {'msg': 'Fail to Submit Record'})


def DisplayAllSubCategory(request):
    try:
        dbe, cmd = Pool.ConnectionPool()
        q = "select S.*,(select C.categoryname from categories C where C.categoryid = S.categoryid) from subcategory S"
        cmd.execute(q)
        rows = cmd.fetchall()
        dbe.close()
        result = request.session['ADMIN']
        return render(request, "DisplayAllSubCategory.html", {'rows': rows,'result':result})
    except Exception as e:
        print(e)
        return render(request, "DisplayAllSubCategory.html", {'rows': []})


def DisplaySubCategoryById(request):
    subcategoryid = request.GET['subcategoryid']
    try:
        dbe, cmd = Pool.ConnectionPool()
        q = "select S.*,(select C.categoryname from categories C where C.categoryid = S.categoryid) from subcategory S where subcategoryid = {}".format(subcategoryid)
        cmd.execute(q)
        row = cmd.fetchone()
        dbe.close()
        return render(request, "DisplaySubCategoryById.html", {'row': row})
    except Exception as e:
        print(e)
        return render(request, "DisplaySubCategoryById.html", {'row': []})


def EditDeleteSubCategoryRecord(request):
    btn = request.GET['btn']
    subcategoryid = request.GET['subcategoryid']
    if (btn == "Edit"):
        categoryid = request.GET['categoryid']
        categoryname = request.GET['subcategoryname']
        description = request.GET['description']
        try:
            dbe, cmd = Pool.ConnectionPool()
            q = "update subcategory set categoryid = {}, subcategoryname = '{}', description = '{}' where subcategoryid = {}".format(categoryid, categoryname, description, subcategoryid)
            cmd.execute(q)
            dbe.commit()
            row = cmd.fetchone()
            dbe.close()
            return DisplayAllSubCategory(request)
        except Exception as e:
            print(e)
            return DisplayAllSubCategory(request)

    elif (btn == "Delete"):
        try:
            dbe, cmd = Pool.ConnectionPool()
            q = "delete from subcategory where subcategoryid = {}".format(subcategoryid)
            cmd.execute(q)
            p = "update subcategory set subcategoryid=subcategoryid-1 where subcategoryid>{}".format(subcategoryid)
            cmd.execute(p)
            dbe.commit()
            row = cmd.fetchone()
            dbe.close()
            return DisplayAllSubCategory(request)
        except Exception as e:
            print(e)
            return DisplayAllSubCategory(request)


def EditSubCategoryPicture(request):
    try:
        subcategoryid = request.GET['subcategoryid']
        subcategoryname = request.GET['subcategoryname']
        picture = request.GET['picture']
        row = [subcategoryid, subcategoryname, picture]
        return render(request, "EditSubCategoryPicture.html", {'row': row})
    except Exception as e:
        return render(request, "EditSubCategoryPicture.html", {'row': []})


def SaveEditSubCategoryPicture(request):
    try:
        subcategoryid = request.POST['subcategoryid']
        oldpicture = request.POST['oldpicture']
        picture = request.FILES['picture']
        filename = str(uuid.uuid4()) + picture.name[picture.name.rfind('.'):]

        q = "update subcategory set icon = '{}' where subcategoryid = {}".format(filename, subcategoryid)
        print(q)
        dbe, cmd = Pool.ConnectionPool()
        cmd.execute(q)
        dbe.commit()
        F = open("D:/Metarial_Management/assets/" +filename, "wb")
        for chunk in picture.chunks():
            F.write(chunk)
        F.close()
        dbe.close()
        os.remove('D:/Metarial_Management/assets/' +oldpicture)
        return DisplayAllSubCategory(request)
    except Exception as e:
        print("Error :", e)
        return DisplayAllSubCategory(request)


def GetSubCategoryJSON(request):
    try:
        dbe, cmd = Pool.ConnectionPool()
        categoryid = request.GET['categoryid']
        q = "select * from subcategory where categoryid = {}".format(categoryid)
        cmd.execute(q)
        rows = cmd.fetchall()
        dbe.close()
        return JsonResponse(rows, safe=False)
    except Exception as e:
        return JsonResponse([], safe=False)