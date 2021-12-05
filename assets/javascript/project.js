$(document).ready(function(){
 $.getJSON("/fetchallstates",{ajax:true},function(data){
  $.each(data,function(index,item){
   $('#states').append($('<option>').text(item[1]).val(item[0]))
   })
 })
 $('#states').change(function() {
  $.getJSON("/fetchallcities",{ajax:true,stateid:$('#states').val()},function(data){
  $('#city').empty()
  $('#city').append($('<option>').text('-City-'))
  $.each(data,function(index,item){
   $('#city').append($('<option>').text(item[2]).val(item[1]))
   })
 })
  })
  $('#picture').change(function(){
      var file=picture.files[0]
      pic.src=URL.createObjectURL(file)
  })

})