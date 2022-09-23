"""Metarial_Management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import AdminView
from . import EmployeeView
from . import StateCityView
from . import CategoryView
from . import SubCategoryView
from . import ProductView
from . import FinalProductView
from . import SupplierView
from . import PurchaseView
from . import IssueView
from . import AttendanceView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',AdminView.Index),
    path('adminlogin/',AdminView.AdminLogin),
    path('checkadminlogin',AdminView.CheckAdminLogin),
    path('admindashboard/',AdminView.AdminDashboard),
    path('adminlogout/',AdminView.AdminLogut),

    #ForEmployees
    path('employeelogin/',EmployeeView.EmployeeLogin),
    path('checkemployeelogin',EmployeeView.CheckEmployeeLogin),
    path('employeedashboard/',EmployeeView.EmployeeDashboard),
    path('employeelogout/',EmployeeView.EmployeeLogout),
    path('EmployeeInterface/',EmployeeView.EmployeeInterface),
    path('employeesubmit',EmployeeView.EmployeeSubmit),
    path('displayall/',EmployeeView.DisplayAll),
    path('displayemployeebyid/',EmployeeView.DisplayByID),
    path('editdeleterecord/',EmployeeView.EditDeleteRecord),
    path('editemployeepicture/',EmployeeView.EditEmployeePicture),
    path('saveeditpicture',EmployeeView.SaveEditPicture),

    #ForCategory
    path('categoryinterface/', CategoryView.CategoryInterface),
    path('categorysubmit', CategoryView.CategorySubmit),
    path('displayallcategory/', CategoryView.DisplayAllCategory),
    path('displaycategorybyid/', CategoryView.DisplayCategoryById),
    path('editdeletecategoryrecord/', CategoryView.EditDeleteCategoryRecord),
    path('editcategorypicture/', CategoryView.EditCategoryPicture),
    path('saveeditcategorypicture', CategoryView.SaveEditCategoryPicture),
    path('getcategoryjson/', CategoryView.GetCategoryJSON),

    #ForSubCategory
    path('subcategoryinterface/', SubCategoryView.SubCategoryInterface),
    path('subcategorysubmit', SubCategoryView.SubCategorySubmit),
    path('displayallsubcategory/', SubCategoryView.DisplayAllSubCategory),
    path('displaysubcategorybyid/', SubCategoryView.DisplaySubCategoryById),
    path('editdeletesubcategoryrecord/', SubCategoryView.EditDeleteSubCategoryRecord),
    path('editsubcategorypicture/', SubCategoryView.EditSubCategoryPicture),
    path('saveeditsubcategorypicture', SubCategoryView.SaveEditSubCategoryPicture),
    path('getsubcategoryjson/', SubCategoryView.GetSubCategoryJSON),

    #ForProduct
    path('productinterface/', ProductView.ProductInterface),
    path('productsubmit', ProductView.ProductSubmit),
    path('displayallproduct/', ProductView.DisplayAllProduct),
    path('displayproductbyid/', ProductView.DisplayProductById),
    path('editdeleteproductrecord/', ProductView.EditDeleteProductRecord),
    path('editproductpicture/', ProductView.EditProductPicture),
    path('saveeditproductpicture', ProductView.SaveEditProductPicture),
    path('getproductjson/',ProductView.GetProductJSON),
    path('displayproductemployee/',ProductView.DisplayProductEmployee),

    # FinalProduct Urls
    path('finalproductinterface/',FinalProductView.FinalProductInterface),
    path('finalproductsubmit',FinalProductView.FinalProductSubmit),
    path('displayallfinalproduct/',FinalProductView.DisplayAllFinalProduct),
    path('displayfinalproductbyid/',FinalProductView.DisplayFinalProductById),
    path('editdeletefinalproductrecord/',FinalProductView.EditDeleteFinalProductRecord),
    path('editfinalproductpicture/',FinalProductView.EditFinalProductPicture),
    path('saveeditfinalproductpicture',FinalProductView.SaveEditFinalProductPicture),
    path('getfinalproductjson/',FinalProductView.GetFinalProductJSON),
    path('displayfinalproductemployee/',FinalProductView.DisplayFinalProductEmployee),
    path('displayallfinalproductbyidjson/',FinalProductView.DisplayFinalProductByIdJSON),
    path('displayfinalproductalljson/',FinalProductView.DisplayFinalProductAllJSON),
    path('displayupdatedstock/',FinalProductView.DisplayUpdatedStock),

    #ForSupplier
    path('supplierinterface/',SupplierView.SupplierInterface),
    path('suppliersubmit',SupplierView.SupplierSubmit),
    path('displayallsupplier/',SupplierView.DisplayAllSupplier),
    path('getsupplierjson/',SupplierView.GetSupplierJSON),

    #ForPurchase
    path('purchaseinterface/',PurchaseView.PurchaseInterface),
    path('purchaseproductsubmit',PurchaseView.PurchaseProductSubmit),
    path('displayallpurchaseproduct/',PurchaseView.DisplayAllPurchaseProduct),
    path('editdeletepurchaseproductrecord/',PurchaseView.EditDeletePurchaseProductRecord),
    path('displaypuchasealljson/', PurchaseView.DisplayPurchaseAllJSON),
    path('listpurchaseemployee/', PurchaseView.ListPurchaseEmployee),

    # Issue Urls
    path('issueinterface/', IssueView.IssueInterface),
    path('issueproductsubmit', IssueView.IssueProductSubmit),
    path('displayallissueproduct/', IssueView.DisplayAllIssueProduct),
    path('editdeleteissueproductrecord/', IssueView.EditDeleteIssueProductRecord),
    path('displayissuealljson/', IssueView.DisplayIssueAllJSON),
    path('listissueemployee/',IssueView.ListIssueEmployee),

    # For Attendance
    path('attendance/', AttendanceView.Attend),
    path('markattendance', AttendanceView.AttendSubmit),
    path('leave/', AttendanceView.Leave),
    path('markleave', AttendanceView.LeaveSubmit),
    path('viewattendance/', AttendanceView.ShowAttendance),

    path('fetchallstates/',StateCityView.FetchAllStates),
    path('fetchallcities/',StateCityView.FetchAllCities)
]
