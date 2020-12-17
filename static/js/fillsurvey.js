//set global variables

// var is_validated;

//define classes that will be used
class Answer{
    constructor(type,answer) {
        this.type = type;
        this.answer = answer;
    }
};
//functions
function getAnswers(){
    //returns all survey questions as objects with their respective
    // question options.
    var new_answers = [];
    var surveyQuestions = $("#accordion-1").children(".question-item");
    surveyQuestions.each(function(i,e){
        questionType = parseInt($(this).attr("data-type"));
        // console.log(questionObj);
        if(questionType===1){
        //get checked radio button:
            var answer = $(this).find('input:checked').val();
            answer = answer==null ? null : answer
        }else if(questionType===2){
            var answer = $(this).find("input:checked").map(function(){return $(this).val()}).get();
             answer = answer.length==0 ? null : answer
        }else if(questionType===3){
          // if the question is a text one we want to grab the selected text length
            var answer = $(this).find("textarea").val();
            answer = answer.length==0 ? null : answer
        }else{
            //if the question is a numeric one we want to grab the selected number type
            var answer = $(this).find("input").val();
            answer = answer=="" ? null : Number(answer);
        };
        new_answer = new Answer(questionType,answer)
        new_answers.push(new_answer);
    });
    return new_answers;
};

function SetNewSize(textarea) {
    //https://stackoverflow.com/questions/47905010/if-there-is-a-new-line-in-a-textarea-add-1-row-and-increase-size-of-textarea
   textarea.style.height = "0px";
   textarea.style.height = textarea.scrollHeight + "px";
};

function checkTextAreaMax(textarea,autoerase=true){
    maxLength = parseInt(textarea.parent().parent().next().find("span").html());
    // mkyong.com: Add maxlength on textArea using jQuery ...
    currentLengthInTextarea = textarea.val().length;
    remainingLength = parseInt(maxLength) - parseInt(currentLengthInTextarea);
    if (currentLengthInTextarea > (maxLength)) {
        // Trim the field current length over the maxlength.
        if(autoerase){
            textarea.val(textarea.val().slice(0, maxLength));
        }else{
            textarea.addClass("form-control is-invalid");
            textarea.css({"margin":0,"padding":0});
        }
        // $(remainingLengthTempId).text(0);
    }else{
        textarea.removeClass("form-control is-invalid");
    };
};

function verifyNumberInput(numberInput){
    type = parseInt(numberInput.parent().find(".numbertype").html());
    val = Number(numberInput.val());
    if(type==2 && !Number.isInteger(val)){
        numberInput.addClass("is-invalid");
    }else if(type==3 && val < 1){
        numberInput.addClass("is-invalid");
    }else{
        numberInput.removeClass("is-invalid");
    };
};

function OnWrapSurveyBtnClick(post_answer_url){
    var newAnswers = getAnswers();
    var survey_id = parseInt($("#surveyFiller").attr("data-surveyid"));
    var new_answers_data = {"survey_id":survey_id, "answers":newAnswers}
    var json_string = JSON.stringify(new_answers_data);
    $.ajax({
          type : 'POST',
          contentType: 'application/json',
          dataType: 'json',
          url : post_answer_url,
          data : json_string
    });
    console.log(json_string);
    return true;

}
