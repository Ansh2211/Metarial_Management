$(document).ready(function () {

    $.getJSON("/getcategoryjson", { ajax: true }, function (data) {

        $.each(data, function (index, item) {
            $('#categoryid').append($('<option>').text(item[1]).val(item[0]))
        })

    })

    $('#categoryid').change(function() {
        $('#subcategoryid').empty()
        $.getJSON("/getsubcategoryjson", { ajax: true, categoryid: $('#categoryid').val()}, function (data) {
            $('#subcategoryid').append($('<option>').text('-Select Sub Category-'))
            $.each(data, function (index, item) {
                $('#subcategoryid').append($('<option>').text(item[2]).val(item[1]))
            })

        })

    })

    $('#subcategoryid').change(function() {
        $('#productid').empty()
        $.getJSON("/getproductjson", { ajax: true,subcategoryid: $('#subcategoryid').val()}, function (data) {
            $('#productid').append($('<option>').text('-Select Product-'))
            $.each(data, function (index, item) {
                $('#productid').append($('<option>').text(item[3]).val(item[2]))
            })

        })

    })

    $('#productid').change(function(){
        $('#finalproductid').empty()
        $.getJSON("/getfinalproductjson",{ ajax: true,productid: $('#productid').val()}, function(data){
            $('#finalproductid').append($('<option>').text('-Select Final Product-'))
            $.each(data, function(index, item) {
                $('#finalproductid').append($('<option>').text(item[4]).val(item[3]))
            })

        })

    })


    $.getJSON("/getsupplierjson", { ajax: true }, function (data) {

        $.each(data, function (index, item) {
            $('#supplierid').append($('<option>').text(item[1]).val(item[0]))
        })

    })

        $('#btnsubmit').click(function () {
        $.getJSON("/displaypuchasealljson", { fromdate: $('#fromdate').val(),todate: $('#todate').val() }, function (data) {
            var htm = "<table class='table'><tr><th>Id</th><th>Category Name</th><th>Subcategory Name</th><th>Product Name</th><th>FinalProduct Name</th><th>Purchase Date</th><th>Supplier Name</th><th>Stock</th><th>Price</th></tr>"
            $.each(data, function (index, item) {
              htm += "<tr><th scope='row'>"+item.transactionid+"</th><td>"+item.categoryname+"</td><td>"+item.subcategoryname+"</td><td>"+item.productname+"</td><td>"+item.finalproductname+"</td><td>"+item.datepurchase+"</td><td>"+item.suppliername+"</td><td>"+item.stock+"</td><td>"+item.amount+"</td></tr>"
            })
            htm+= "</table>"
            $('#result').html(htm)
        })
    })


})