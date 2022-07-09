from django.shortcuts import render
from . import PoolDict
from . import Pool

def Attendance(request):
    try:
        result=request.session['EMPLOYEE']
        #print(result)
        return render(request,"MarkAttendance.html",{'result':result})
    except Exception as e:
        print(e)
        return render(request,"MarkAttendance,html")

def MarkAttendance(request):
    try:
        employeeid=request.POST['employeeidattendance']
        employeename=request.POST['fullname']
        currentdate=request.POST['currentdate']
        intime=request.POST['intime']
        outtime=request.POST['outtime']
        I=intime.split(":")
        O=outtime.split(":")
        W=int(O[0])-int(I[0])
        working=str(W)+" hours"
        if(W==6):
            status="Full Day"
        elif(W>6):
            t=W-6
            status="Overtime of "+str(t)+" hours"
        else:
            t=6-W
            status="Leave of "+str(t)+" hours"
        q="insert into attendance(employeeid,employeename,date,intime,outtime,working,status)values({},'{}','{}','{}','{}','{}','{}')".format(employeeid,employeename,currentdate,intime,outtime,working,status)
        print(q)
        db,cmd=PoolDict.ConnectionPool()
        cmd.execute(q)
        db.commit()
        db.close()
        return render(request, 'MarkAttendance.html',{'msg':'Attendance Submitted'})

    except Exception as e:
        print("Error:",e)
        return render(request, 'MarkAttendance.html',{'msg':'Attendance Not Submitted'})


def DisplayAttendance(request):
    try:
        db,cmd=Pool.ConnectionPool()
        q="select * from attendance"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return render(request,'ViewAttendance.html',{'rows':rows})

    except Exception as e:
        print(e)
        return  render(request,'ViewAttendance.html',{'rows': []})


