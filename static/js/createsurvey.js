//set global variables

// var is_validated;

//define classes that will be used
class Question{
    constructor(type) {
        this.type = type;
        this.title = null;
        this.options = [];
    }
};

class Option{
    constructor(number) {
        this.number = number;
        this.text = null; //text of the single/multi choice question option
    }
};

//functions
function getQuestionsIfVerified(){
    //returns all survey questions as objects with their respective
    // question options.
    var new_questions = [];
    var surveyQuestions = $("#accordion-1").children(".card").not("[id]");
    if(surveyQuestions.length ===0) //if a survey with no questions
        return false;
    if($("#survey-name-input").val().length===0){
      //if survey with no name
      console.log("survey with no name");
      return false;
    }
    var is_verified = true;
    surveyQuestions.each(function(i,e){
        questionObj = $(this).data("Question");
        questionTitle = $(this).find(".question-statement-input").val()
        if(questionTitle.length === 0){
          console.log("question with no title");
          return false;
        };
        questionObj.title = questionTitle;
        // console.log(questionObj);
        if(questionObj.type < 3){
            //if question is a single or multi-choice one we should check the added choices/options
            questionOptions = $(this).find("li").not("[id]");
            if(questionOptions.length == 0){
                //if the user has created one of these questions but not added options
                is_verified = false;
                return false;
            };
            for(var j=0; j<questionOptions.length; j++){
                //for each option in the question we need to assign it
                //to the question's options array.
                opt = questionOptions.eq(j);
                // console.log(opt.find("textarea").val().length);
                if(opt.find("textarea").val().length == 0){
                    //If the user has created an option but not added any label to it.
                    is_verified = false;
                    return false;
                };
                newOption = new Option(j+1);
                newOption.text = opt.find("textarea").val();
                questionObj.options.push(newOption);
            };
        }else if(questionObj.type === 3){
          // if the question is a text one we want to grab the selected text length
            maxTextLength = $(this).find(".form-control-range").val();
            newOption = new Option(maxTextLength);
            questionObj.options.push(newOption);
        }else{
            //if the question is a numeric one we want to grab the selected number type
            numberType = $(this).find("select").children("option:selected").val();
            newOption = new Option(parseInt(numberType));
            questionObj.options.push(newOption);
        };
        new_questions.push(questionObj);
    });
    if(is_verified){
        return new_questions;
    }else{
        //if not verified remove all options to the Question objects that came before the verification
        console.log("Unverified");
        surveyQuestions.each(function(){
            questionObj = $(this).data("Question");
            questionObj.options = [];
        });
    }
    return is_verified;
};

function AssignSingleChoiceClick(singleOption){
    // Assigns the function to customize the select and deselect of a new single-choice answer option.
    singleOption.on('click', function (e) {
        e.preventDefault()
        if ($(e.target).is("textarea")){
            return;
        }
        $(this).tab('show')
        var lis = $(this).parent().find("li");
        lis.each(function(){
            $(this).removeClass("active");
            $(this).addClass("unactive");
            $(this).css("color","black");
            // console.log($(this).children("i").first());
            $(this).children("i").first().removeClass('fa-circle');
            $(this).children("i").first().addClass('fa-circle-thin');
        });
        $(this).removeClass('unactive');
        $(this).addClass('active');
        $(this).children("i").first().removeClass('fa-circle-thin');
        $(this).children("i").first().addClass('fa-circle');
        $(this).css("color","white");
        // console.log("single choice!");
    });

}


function AssignMultiChoiceClick(multiOption){
    // Assigns the function used customize the select and deselect of a new multi-choice answer option.
    multiOption.on('click',function(e){
        e.preventDefault()
        if ($(e.target).is("textarea")){
            return;

        }
        // // $(this).tab('show')
        if($(this).hasClass("active")){
            // console.log("was active!");
            $(this).removeClass('active');
            $(this).addClass('unactive');
            $(this).css("color","black");
            $(this).children("i").first().removeClass('fa-circle');
            $(this).children("i").first().addClass('fa-circle-thin');
        }else if($(this).hasClass("unactive")){
            // console.log("was unactive!");
            $(this).removeClass('unactive');
            $(this).addClass('active');
            $(this).css("color","white");
            $(this).children("i").first().removeClass('fa-circle-thin');
            $(this).children("i").first().addClass('fa-circle');
        }else{
            $(this).removeClass('unactive');
            $(this).addClass('active');
            $(this).css("color","white");
            $(this).children("i").first().removeClass('fa-circle-thin');
            $(this).children("i").first().addClass('fa-circle');
        };
    });
};

function SetNewSize(textarea) {
    //https://stackoverflow.com/questions/47905010/if-there-is-a-new-line-in-a-textarea-add-1-row-and-increase-size-of-textarea

   textarea.style.height = "0px";
   textarea.style.height = textarea.scrollHeight + "px";
};

function onRangeInput(e){
    //sets the appropiate number to the range input label
    e.next().html(e.val());
    checkTextAreaMax(e.parent().parent().find("textarea"),false);
}

function checkTextAreaMax(textarea,autoerase=true){
    maxLength = parseInt(textarea.parent().parent().find("span").html());
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

function checkNumberInputType(numberInput){
    type = parseInt(numberInput.parent().parent().find("select").val());
    val = Number(numberInput.val());
    if(type==2 && !Number.isInteger(val)){
        numberInput.addClass("is-invalid");
    }else if(type==3 && val < 1){
        numberInput.addClass("is-invalid");
    }else{
        numberInput.removeClass("is-invalid");
    };
};

function newSurveyQuestion(questionType){
    //creates a new survey question depending on the type of button selected.
    // console.log("Question type "+questionType)
    if(questionType==1){
        var questionElementId = "#single-choice-question";
    }else if(questionType==2){
        var questionElementId = "#multi-choice-question";
    }else if(questionType==3){
        var questionElementId = "#text-question";
    }else{
        var questionElementId = "#numeric-question";
    }

    var answer_number = $("#accordion-1").children().length + 1;
    var new_question = $(questionElementId).clone();
    // console.log(answer_number);
    new_question.removeAttr("id");
    new_question.removeAttr("style");
    new_question_href = new_question.find("a")
    new_question_href.attr("data-toggle","collapse");
    new_question_href.attr("aria-expanded","false");
    new_question_href.attr("aria-controls","#accordion-1 .item-"+answer_number);
    new_question_href.attr("href","#accordion-1 .item-"+answer_number);
    new_question.appendTo($("#accordion-1"));
    collapse_card = new_question.find(".collapse");
    collapse_card.removeClass();
    collapse_card.addClass("collapse item-"+answer_number);
    new_question.show();

    //create class object defining this question and added to the element's data:
    newQuestionObj = new Question(questionType);
    new_question.data("Question",newQuestionObj);
    new_question.find(".question-statement-input").attr("required","")
}


function newSingleAnswerOption(e){
    //creates a new single answer option when the button is pressed
    var new_opt =  $("#single-choice-option").clone();
    new_opt.removeAttr("id");
    new_opt.removeAttr("style");
    new_opt.attr("required");
    new_opt.find("textarea").attr("required");
    new_opt.appendTo(e.parent().children().first("ul"));
    AssignSingleChoiceClick(new_opt);
    // console.log("url for new_survey:"+create_survey_link)
    new_opt.show();
}

function newMultiAnswerOption(e){
    //creates a new multi=answer option when the button is pressed
    var new_opt =  $("#multi-choice-option").clone();
    new_opt.removeAttr("id");
    new_opt.removeAttr("style");
    new_opt.find("textarea").attr("required","");
    new_opt.appendTo(e.parent().children().first("ul"));
    AssignMultiChoiceClick(new_opt);
    new_opt.show();
    // activateChoiceActions();

}

function OnWrapSurveyBtnClick(create_survey_url){
  console.log("url for new_survey:"+create_survey_url)
    var verifiedQuestions = getQuestionsIfVerified();
    var survey_name = $("#survey-name-input").val()
    if(verifiedQuestions === false){
        console.log("unvalidated");
        questionsStatus = $("#questions-status-txt");
        prevColor = questionsStatus.css("color");
        setTimeout(function(){
            questionsStatus.html("Questions you add will appear here.");
            questionsStatus.css("color","black");
        },6000);
        questionsStatus.html("Your survey was not validated! Check that questions and survey name are set up properly.");
        questionsStatus.css("color","FireBrick");
        return false;

    }else{
        var new_survey_data = {"name":survey_name, "questions":verifiedQuestions}
        var json_string = JSON.stringify(new_survey_data);
        $.ajax({
          type : 'POST',
          contentType: 'application/json',
          dataType: 'json',
          url : create_survey_url,
          data : json_string
        });

        console.log(json_string);
        return true;
        // window.location.replace("/");
        //post this
    }
}
