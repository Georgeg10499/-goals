var new_item_html = '<div class="list_item"> <h3>What do you want to accomplish today?' + '<input type= "text" name= "goal"> </h3>' +
'<h3>How long do you want to spend on this? (Hours)' + '<input type= "number" name= "hour" min= "0"  max= "12" ></h3>'
+ '<h3>How long do you want to spend on this? (Minutes) <input type= "number" name= "minutes" min= "0" max= "59" ></h3>   </div>'
var num = 2;

function setUpHandlers (){
  $("#add_item").click(addItems);
  $("#remove_item").click(removeItems);
}

function addItems(event){
  var index_of_goal = new_item_html.indexOf('goal');
  var index_of_hour = new_item_html.indexOf('hour');
  var index_of_minutes = new_item_html.indexOf('minutes');
  new_item_html = new_item_html.slice(0,index_of_goal+4) + num +
                  new_item_html.slice(index_of_goal+4,index_of_hour+4) + num +
                  new_item_html.slice(index_of_hour+4,index_of_minutes+7) + num +
                  new_item_html.slice(index_of_minutes+7,new_item_html.length);
  $("#check_list").append(new_item_html);
  new_item_html = '<div class="list_item"> <h3>What do you want to accomplish today?' + '<input type= "text" name= "goal"> </h3>' +
  '<h3>How long do you want to spend on this? (Hours)' + '<input type= "number" name= "hour" min= "0"  max= "12" ></h3>'
  + '<h3>How long do you want to spend on this? (Minutes) <input type= "number" name= "minutes" min= "0" max= "59" ></h3>   </div>';
}

function removeItems(event){
  $("#check_list .list_item").eq(-1).remove();
}


$(document).ready(setUpHandlers);
