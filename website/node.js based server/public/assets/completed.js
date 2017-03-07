$(document).ready(function(){

  //Delete task function
  $('#todoList .showOnHover .btn-danger').on('click', function(){ //fires a function DELETE
      var item = $(this).parent().parent().contents('#onHover').text().replace(/ /g, "-");
      $.ajax({
        type: 'DELETE', //fires delete handler
        url: '/completed/' + item,
        success: function(dataC){
          //do something with the data via front-end framework
          location.reload();
        }
      });
  });

  $('#todoList .showOnHover .btn-warning').on('click', function(){
    var item = $(this).parent().parent().contents('#onHover').text().replace(/ /g, "-");
    var todoItem = $(this).parent().parent().contents('#onHover').text();
    var todo = {item: todoItem};
    $.ajax({
      type: 'POST',
      url: '/todo',
      data: todo,
      success: function(data){
        location.reload();
      }
    });
    $.ajax({
      type: 'DELETE', //fires delete handler
      url: '/completed/' + item,
      success: function(dataC){
        location.reload();
      }
    });

  });

});
