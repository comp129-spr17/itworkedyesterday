$(document).ready(function(){

  //Add task function
  $('#createButton').on('click', function(){

      var item = $('#titleInput');
      var todo = {item: item.val()};

      $.ajax({
        //this is a post request to the /todo route when ajax request made and passes
        //todo object
        type: 'POST',
        url: '/todo',
        data: todo,
        success: function(data){
          //do something with the data via front-end framework
          location.reload();
        }
      });

      return false;

  });

  //editModal show
  $('#todoList .showOnHover .btn-warning').on('click', function(){

      $('#editModal').modal('show');
      var item = $(this).parent().parent().contents('#onHover').text().replace(/ /g, "-"); //get the normal item

      //Edit task function within the modal
      $('#editButton').on('click',function(){

        var editedItem = $('#editInput');
        var todo = {editedItem: item.val()};
        
        $.ajax({
          type: 'DELETE', //fires delete handler
          url: '/todo/' + item,
          success: function(data){
            //do something with the data via front-end framework
            location.reload();
          }
        });
        $.ajax({
          //this is a post request to the /todo route when ajax request made and passes
          //todo object
          type: 'POST',
          url: '/todo',
          data: todo,
          success: function(data){
            //do something with the data via front-end framework
            location.reload();
          }
        });

      });
  });

  //Delete task function
  $('#todoList .showOnHover .btn-danger').on('click', function(){ //fires a function DELETE
      var item = $(this).parent().parent().contents('#onHover').text().replace(/ /g, "-");
      $.ajax({
        type: 'DELETE', //fires delete handler
        url: '/todo/' + item,
        success: function(data){
          //do something with the data via front-end framework
          location.reload();
        }
      });
  });

});
