$(document).ready(function() {
  $(':checkbox').on('click', changeTodoStatus);
  $('.ediatbleTask').on('change', makeTaskEditable);
});



function changeTodoStatus() {
  putNewStatus(this.getAttribute('data-todo-id'), $(this).is(':checked'));
}

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// function from the django docs
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(
          cookie.substring(name.length + 1)
        );
        break;
      }
    }
  }
  return cookieValue;
}


function ajaxSetup(){
    // setup ajax to csrf token
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    });
}

function makeTaskEditable(event){
  let todoID = event.target.dataset.todoId
  let todoDescription = event.target.value;

  ajaxSetup()

  var todoURL = '/api/todos/' + todoID + '/'

  // console.log("OnDblClick");
  // console.log(todoID);
  // console.log(event.target.value);
  if(todoDescription == ""){
    // console.log('DELETE')
    $.getJSON(todoURL, function(data) {

      // console.log("DATA AT FE",data);
      data.description = todoDescription;
      // console.log("DATA after change",data);
      $.ajax({
        url: todoURL,
        type: 'DELETE',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function() {
          location.reload();
        }
      });
    });
  }

  else{
    // console.log('EDIT');

    $.getJSON(todoURL, function(data) {

      // console.log("DATA AT FE",data);
      data.description = todoDescription;
      // console.log("DATA after change",data);
      $.ajax({
        url: todoURL,
        type: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function() {
          location.reload();
        }
      });
    });
  }
}


function putNewStatus(todoID, isFinished) {
  ajaxSetup()

  var todoURL = '/api/todos/' + todoID + '/'

  $.getJSON(todoURL, function(data) {
    data.is_finished = isFinished;
    if (isFinished) {
      data.finished_at = moment().toISOString();
    } else {
      data.finished_at = null;
    }
    // console.log("DATA AT FE",data)
    $.ajax({
      url: todoURL,
      type: 'PUT',
      contentType: 'application/json',
      data: JSON.stringify(data),
      success: function() {
        location.reload();
      }
    });
  });
}
