var _PAGE=1;
var _PAGE_SIZE=6;


function fillFlashCards(elem, flashcards){
    elem.empty();
    for (var m=0;m<flashcards.length-1;m++){
        var html = '<div class="flashcard-box flip-container" onclick="this.classList.toggle(\'hover\');">'+
                    '<div class="flashcard flipper">'+'<span class="front pad10">'+flashcards[m].side_a+
                    '</span><span class="back pad10">'+flashcards[m].side_b+'</span>';

        if(flashcards[flashcards.length-1].user_type=="principal" && flashcards[m].is_approved==false){
            html += '<input type="button" value="Approve" class="sbutton approve hide"'+ 
                    'onclick="approveFlash('+flashcards[m].id+')">';
        }
        html += '</div></div>';
        elem.append(html);
        if(flashcards[m].is_approved==0)
            $('.flashcard').css("position", "relative");
    }

    if(flashcards.length==0){
        elem.append('<div class="no-item">No Items</div>');
    }
}


function displayFlashCards(flashcards){
    _PAGE = _PAGE+1;

    var elem = $('.flashcard-container');

    elem.empty();
    fillFlashCards(elem, flashcards);

    if(flashcards.length>_PAGE_SIZE){
        if(flashcards[flashcards.length-1].user_type!="student"){
            var apprType=$("#appr-type").val();
        }else{
            var apprType=1;
        }
        elem.append('<button class="sbutton right gap-top10" \
        onclick="getFlashCards('+apprType+')">Next</button>');
    }
}


function getFlashCards(is_approved){
    apiCall('/flashcards', 'get', {"page_size":_PAGE_SIZE, "page":_PAGE, 
    	"is_approved":is_approved}, displayFlashCards);
}


function approveSuccess(data){
    sendToast('Approved successfully.');
    _PAGE=1;
    getFlashCards(0);
}

function approveFlash(flashId){
    apiCall('/flashcard/'+flashId+'/', 'put', toJSON({"is_approved":1}), 
        approveSuccess);
    
}