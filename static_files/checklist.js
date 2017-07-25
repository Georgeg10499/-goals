new_item_html = '  <div class="list_item"> <h3>What do you want to accomplish today?' + '<input type= "text" name= "goal"> </h3>' +
'<h3>How long do you want to spend on this? (Hours)' + '<input type= "number" name= "hour" min= "0"  max= "12" ></h3>'
+ '<h3>How long do you want to spend on this? (Minutes) <input type= "number" name= "minutes" min= "0" max= "59" ></h3>   </div>'

function setUpHandlers (){
  $("#add_item").click(addItems);
  $("#remove_item").click(removeItems);
}

function addItems(event){
  $("#check_list").append(new_item_html);
}

function removeItems(event){
  $("#check_list .list_item").eq(-1).remove();
}


$(document).ready(setUpHandlers);
