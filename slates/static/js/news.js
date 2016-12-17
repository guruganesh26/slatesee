var _PAGE=1;
var _PAGE_SIZE=6;

function getNews(){
    apiCall('/messages', 'get', {"page_size":_PAGE_SIZE, "page":_PAGE, "message_type":"news"}, displayNews);

}

function displayNews(messages){
    _PAGE = _PAGE+1;

    var elem = $('.news-container');
    fillMessages(elem, messages);

    if(messages.length>_PAGE_SIZE){
        elem.append('<button class="sbutton" onclick="getNews()" style="float:right">Next</button>');
    }
}

getNews();