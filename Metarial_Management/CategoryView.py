from django.shortcuts import render
from django.http import JsonResponse
from . import Pool
import uuid
import os


def CategoryInterface(request):
    try:
        result = request.session['ADMIN']
        return render(request, 'CategoryInterface.html')

    except Exception as e:
        return render(request, "AdminLogin.html")


def CategorySubmit(request):
    try:
        categoryname = request.POST['categoryname']

        icon = request.FILES['icon']
        filename = str(uuid.uuid4()) + icon.name[icon.name.rfind('.'):]

        q = "insert into categories (categoryname, icon) values ('{}', '{}')".format(categoryname, filename)
        print(q)
        dbe, cmd = Pool.ConnectionPool()
        cmd.execute(q)
        dbe.commit()
        F = open("D:/Metarial_Management/assets/"+filename, "wb")
        for chunk in icon.chunks():
            F.write(chunk)
        F.close()
        dbe.close()
        return render(request, "CategoryInterface.html", {'msg': 'Record Successfully Submitted'})
    except Exception as e:
        print("Error :", e)
        return render(request, "CategoryInterface.html", {'msg': 'Fail to Submit Record'})


def DisplayAllCategory(request):
    try:
        dbe, cmd = Pool.ConnectionPool()
        q = "select * from categories"
        cmd.execute(q)
        rows = cmd.fetchall()
        dbe.close()
        return render(request, "DisplayAllCategory.html", {'rows': rows})
    except Exception as e:
        print(e)
        return render(request, "DisplayAllCategory.html", {'rows': []})


def DisplayCategoryById(request):
    categoryid = request.GET['categoryid']
    try:
        dbe, cmd = Pool.ConnectionPool()
        q = "select * from categories where categoryid = {} ".format(categoryid)
        cmd.execute(q)
        row = cmd.fetchone()
        dbe.close()
        return render(request, "DisplayCategoryById.html", {'row': row})
    except Exception as e:
        print(e)
        return render(request, "DisplayCategoryById.html", {'row': []})


def EditDeleteCategoryRecord(request):
    btn = request.GET['btn']
    categoryid = request.GET['categoryid']
    if (btn == 'Edit'):
        categoryname = request.GET['categoryname']
        try:
            dbe, cmd = Pool.ConnectionPool()
            q = "update categories set categoryname = '{}' where categoryid = {}".format(categoryname, categoryid)
            cmd.execute(q)
            dbe.commit()
            row = cmd.fetchone()
            dbe.close()
            return DisplayAllCategory(request)
        except Exception as e:
            print(e)
            return DisplayAllCategory(request)

    elif (btn == 'Delete'):
        try:
            dbe, cmd = Pool.ConnectionPool()
            q = "delete from categories where categoryid = {}".format(categoryid)
            cmd.execute(q)
            dbe.commit()
            row = cmd.fetchone()
            dbe.close()
            return DisplayAllCategory(request)
        except Exception as e:
            print(e)
            return DisplayAllCategory(request)


def EditCategoryPicture(request):
    try:
        categoryid = request.GET['categoryid']
        categoryname = request.GET['categoryname']
        picture = request.GET['picture']
        row = [categoryid, categoryname, picture]
        return render(request, "EditCategoryPicture.html", {'row': row})
    except Exception as e:
        return render(request, "EditCategoryPicture.html", {'row': []})


def SaveEditCategoryPicture(request):
    try:
        categoryid = request.POST['categoryid']
        oldpicture = request.POST['oldpicture']
        picture = request.FILES['picture']
        filename = str(uuid.uuid4()) + picture.name[picture.name.rfind('.'):]

        q = "update categories set icon = '{}' where categoryid = {}".format(filename, categoryid)
        print(q)
        dbe, cmd = Pool.ConnectionPool()
        cmd.execute(q)
        dbe.commit()
        F = open("D:/Metarial_Management/assets/"+filename, "wb")
        for chunk in picture.chunks():
            F.write(chunk)
        F.close()
        dbe.close()
        os.remove("D:/Metarial_Management/assets/" + oldpicture)
        return DisplayAllCategory(request)
    except Exception as e:
        print("Error :", e)
        return DisplayAllCategory(request)


def GetCategoryJSON(request):
    try:
        dbe, cmd = Pool.ConnectionPool()
        q = "select * from categories"
        cmd.execute(q)
        rows = cmd.fetchall()
        dbe.close()
        return JsonResponse(rows, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse(rows, safe=False)