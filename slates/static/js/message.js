var _PAGE=1;
var _PAGE_SIZE=6;


function displayMessages(messages){
    _PAGE = _PAGE+1;

    var elem = $('.message-container');

    elem.empty();
    fillMessages(elem, messages);

    if(messages.length>_PAGE_SIZE){
        if(messages[messages.length-1].user_type!="student"){
            var apprType=$("#appr-type").val();
        }else{
            var apprType=1;
        }
        elem.append('<button class="sbutton right gap-top10" \
        onclick="getMessages('+apprType+')">Next</button>');
    }
}


function getMessages(is_approved){
    apiCall('/messages', 'get', {"page_size":_PAGE_SIZE, "page":_PAGE, "message_type":"message", "is_approved":is_approved}, displayMessages);
}

function approveSuccess(data){
    sendToast('Approved successfully.');
    _PAGE=1;
    getMessages(0);
}

function approveMessage(messageId){
    apiCall('/message/'+messageId+'/', 'put', toJSON({"is_approved":1}), 
        approveSuccess);
    
}