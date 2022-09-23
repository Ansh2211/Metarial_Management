from django.shortcuts import render
from . import Pool
from . import PoolDict

def Attend(request):
    try:
        result=request.session['EMPLOYEE']
        return render(request,"MarkAttendance.html",{'result':result})
    except Exception as e:
        print(e)
        return render(request,"MarkAttendance.html")

def AttendSubmit(request):
    try:
        employeeid=request.POST['employeeid']
        employeename=request.POST['fullname']
        currentdate=request.POST['currentdate']
        intime=request.POST['intime']
        q="insert into attendance(employeeid,employeename,date,intime)values({},'{}','{}','{}')".format(employeeid,employeename,currentdate,intime)
        print(q)
        db,cmd=PoolDict.ConnectionPool()
        cmd.execute(q)
        db.commit()
        db.close()
        return render(request, 'MarkAttendance.html',{'msg':'Saved'})

    except Exception as e:
        print("Error:",e)
        return render(request, 'MarkAttendance.html',{'msg':'Not Saved'})

def Leave(request):
    try:
        result=request.session['EMPLOYEE']
        return render(request,"Leave.html",{'result':result})
    except Exception as e:
        print(e)
        return render(request,"Leave.html")

def LeaveSubmit(request):
    try:
        employeeid=request.POST['employeeid']
        date=request.POST['currentdate']
        outtime=request.POST['outtime']
        db, cmd = Pool.ConnectionPool()
        p="select intime from attendance where employeeid={} and date='{}'".format(employeeid,date)
        print(p)
        cmd.execute(p)
        intime=cmd.fetchone()
        print(intime)
        db.close()
        I = intime[0].split(":")
        O = outtime.split(":")
        W = int(O[0]) - int(I[0])
        working = str(W) + " hours"
        if (W == 6):
            status = "Full Day"
        elif (W > 6):
            t = W - 6
            status = "Overtime of " + str(t) + " hours"
        else:
            t = 6 - W
            status = "Leave of " + str(t) + " hours"

        q="update attendance set outtime='{}',working='{}',status='{}' where employeeid={} and date='{}'".format(outtime,working,status,employeeid,date)
        print(q)
        db,cmd=Pool.ConnectionPool()
        cmd.execute(q)
        db.commit()
        db.close()
        return render(request, 'Leave.html',{'msg':'Saved'})

    except Exception as e:
        print("Error:",e)
        return render(request, 'Leave.html',{'msg':'Not Saved'})

def ShowAttendance(request):
    try:
        db,cmd=Pool.ConnectionPool()
        q="select * from attendance"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        result = request.session['ADMIN']
        return render(request,'AttendanceInterface.html',{'rows':rows,'result':result})

    except Exception as e:
        print(e)
        return  render(request,'AttendanceInterface.html',{'rows': []})
