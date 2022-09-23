from django.shortcuts import render
from django.http import JsonResponse
from . import Pool
from . import PoolDict

def SupplierInterface(request):
    try:
        result=request.session['ADMIN']
        return render(request,'SupplierInterface.html',{'result':result})

    except Exception as e:
        return render(request, 'AdminLogin.html')


def SupplierSubmit(request):
    try:
        supplierid=request.POST['supplierid']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        address=request.POST['address']
        states=request.POST['states']
        city=request.POST['city']
        email=request.POST['email']
        mobilenumber=request.POST['mobilenumber']

        q="insert into suppliers(supplierid, firstname, lastname, address, stateid, cityid, email, mobilenumber)values({},'{}','{}','{}',{},{},'{}','{}')".format(supplierid, firstname, lastname, address, states, city, email, mobilenumber)
        db,cmd=PoolDict.ConnectionPool()
        cmd.execute(q)
        db.commit()
        db.close()
        return render(request, 'SupplierInterface.html', {'msg': 'Record Submitted Successfully'})

    except Exception as e:
        print("Error:",e)
        return render(request, 'SupplierInterface.html',{'msg':'Failed To Submit Record'})

def DisplayAllSupplier(request):
    try:
        db, cmd = Pool.ConnectionPool()
        q="select SU.*,(select C.cityname from cities C where C.cityid=SU.cityid),(select S.statename from states S where S.stateid=SU.stateid) from suppliers SU"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        result = request.session['ADMIN']
        return render(request, 'DisplayAllSupplier.html', {'rows':rows,'result':result})

    except Exception as e:
        return render(request, 'AdminLogin.html', {'rows': []})



def GetSupplierJSON(request):
    try:
        dbe, cmd = Pool.ConnectionPool()
        q = "select * from suppliers"
        cmd.execute(q)
        rows = cmd.fetchall()
        dbe.close()
        return JsonResponse(rows, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse(rows, safe=False)