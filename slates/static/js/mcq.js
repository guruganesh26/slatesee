var _PAGE=1;
var _PAGE_SIZE=6;


function fillMcqSets(elem, mcqs){
    elem.empty();
    for (var m=0;m<mcqs.length-1;m++){
        var html = '<div class="mcq-box point"><span class="mcq-icon">'+
                    '</span><span class="mcq" onclick="viewMcq('+mcqs[m].id+')">'+
                    mcqs[m].set_name;
/*        if(mcqs[mcqs.length-1].user_type=="principal" && mcqs[m].is_approved==false){
            html += '<input type="button" value="Approve" class="sbutton approve hide"'+ 
                    'onclick="approveMessage('+mcqs[m].id+')">';
        }*/
/*        html += '<input type="button" value="View" class="sbutton approve hide"'+ 
        'onclick="viewMcq('+mcqs[m].id+')">';*/
        html += '</span></div>';
        elem.append(html);
        
        // $('.mcq').css("position", "relative");
    }

    if(mcqs.length==0){
        elem.append('<div class="no-item">No Items</div>');
    }
}

function displayMcqSets(mcqs){
    _PAGE = _PAGE+1;

    var elem = $('.mcq-container');

    elem.empty();
    fillMcqSets(elem, mcqs);

    if(mcqs.length>_PAGE_SIZE){
        if(mcqs[mcqs.length-1].user_type!="student"){
            var apprType=$("#appr-type").val();
        }else{
            var apprType=1;
        }
        elem.append('<button class="sbutton right gap-top10" \
        onclick="getMcqs('+apprType+')">Next</button>');
    }
}


function getMcqSets(is_approved){
    apiCall('/mcqsets', 'get', {"page_size":_PAGE_SIZE, "page":_PAGE, 
    	"is_approved":is_approved}, displayMcqSets);
}


function displayMcq(mcqs) {
    var questions = [];
    for(var m=0;m<mcqs.length-1;m++){
        var q = {};
        q['a'] = [];
        q['q'] = mcqs[m]['question'];
        var options = ['option1', 'option2', 'option3', 'option4']
        for(var o=0;o<options.length;o++){
            if(mcqs[m]['answer'] == options[o]){
                q['a'].push({"option": mcqs[m][options[o]],"correct": true});    
            }else{
                q['a'].push({"option": mcqs[m][options[o]],"correct": false});
            }
        }
        if(mcqs[m]['correct_text']!=null){
            q["correct"]="<p><span>"+mcqs[m]['correct_text']+"</span></p>";
        }else{
            q['correct']="<p><span>Great, This is correct one.</span></p>"
        }

        if(mcqs[m]['wrong_text']!=null){
            q["incorrect"]="<p><span>"+mcqs[m]['wrong_text']+"</span></p>";
        }else{
            q['incorrect']="<p><span>No, This is wrong one.</span></p>"
        }
        

        questions.push(q)
    }
    quizJSON['questions'] = questions;
    $('.mcq-view-container').slickQuiz();
    $('.mcq-view-box').show();
    $('.mcq-container').hide();$('#appr-type').hide()


}

function showMcqSets(){
    window.location.reload()
}



function viewMcq(mcqSetId){
    apiCall('/mcqs', 'get', {"page_size":_PAGE_SIZE, "page":_PAGE, 
    "set_id":mcqSetId}, displayMcq);
}