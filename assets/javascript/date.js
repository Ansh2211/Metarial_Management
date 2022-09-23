$(document).ready(function(){
    var d=new Date()
    var cit=(d.getHours())+":"+(d.getMinutes())
    var cot=(d.getHours())+":"+(d.getMinutes())
    var cd=(d.getFullYear())+"-"+(d.getMonth()+1)+"-"+(d.getDate())
    $('#currentdate').val(cd)
    $('#intime').val(cit)
    $('#outtime').val(cot)
})