var activate_msg_elem = function(text,is_response){
  // var user_name = "{{current_user.name}}";
  $('#message_header').html(text);
  if($('#new_post:visible').length){
    $("#new_post").hide();
    $("#create_post_icon").html("add");
    $("#new_post_a").removeClass("yellow darken-3");
    $("#new_post_a").css({"color":"red"});
  }else{
    $("#new_post").show();
    $("#create_post_icon").html("clear");
    $("#new_post_a").addClass("yellow darken-3");
  };
  if(is_response){
    console.log("is response!!");
    $("#message_card").css({"color":"blue"});
    $("#message_card").removeClass("teal");
    $("#message_card").addClass("blue");
    $("#card_footer").removeClass("red");
    $("#card_footer").addClass("yellow darken-3");
  }else{
    $("#message_card").removeClass("blue");
    $("#message_card").addClass("teal");
    $("#card_footer").removeClass("yellow darken-3");
    $("#card_footer").addClass("red");
  }
};
