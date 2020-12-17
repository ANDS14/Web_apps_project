var activate_msg_elem = function(){
  // var user_name = "{{current_user.name}}";
  if($('.new_survey_container:visible').length){
    $(".new_survey_container").hide();
    $("#create_survey_icon").html("poll");
    $("#new_survey_a").removeClass("red");
    $("#new_survey_a").addClass("blue darken-3");
  }else{
    $(".new_survey_container").show();
    $("#create_survey_icon").html("clear");
    $("#new_survey_a").removeClass("blue darken-3");
    $("#new_survey_a").addClass("red");
  };
};
