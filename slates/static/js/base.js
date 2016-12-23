var apiCall = function(url, method, data, callback){

    jQuery.ajax({
    url:url,
    headers: {"Content-Type": "application/json"},
    data: data,
    type: method,
        success:function (data) {
            if (callback)
                callback(data);

        },
        error:function (jqXHR, textStatus, errorThrown) {
        }
    });
    
}

function fillMessages(elem, messages){
    elem.empty();
    for (var m=0;m<messages.length-1;m++){
        var html = '<div class="message-box"><span class="message-icon"></span><span class="message">'+
                    messages[m].message;
        if(messages[messages.length-1].user_type=="principal" && messages[m].is_approved==false){
            html += '<input type="button" value="Approve" class="sbutton approve hide"'+ 
                    'onclick="approveMessage('+messages[m].id+')">';
        }
        html += '</span></div>';
        elem.append(html);
        if(messages[m].is_approved==0)
            $('.message').css("position", "relative");
    }

    if(messages.length==0){
        elem.append('<div class="no-item">No Items</div>');
    }
}

function toJSON(data) {
    return JSON.stringify(data, null, " ");
}

function parseJSON(data) {
    return JSON.parse(data);
}

function sendToast(message){
    $.tips(message, 5000);
}

$(document).ready(function(){
   var ids = window.location.pathname.split('/')[1];
   $('#'+ids).addClass('active');
   var theme = window.localStorage['theme'];
   $('body').addClass(theme);
   $('#theme').val(theme);
});


function showSideNav(){
    $('.notification-container').toggleClass('show');
    $('.slide-container').toggleClass('hide');
    $('.event-container').toggleClass('show');
    $('.flashcard-container').toggleClass('hide');
}

function showTeacherSideNav(){
    $('.notification-container').toggleClass('show');
    $('.teacher-menu').toggleClass('hide');
    $('.add-user-menu').toggleClass('hide');
    $('.user-list').toggleClass('hide');
}

function showAddItem(){
    $('.notification-container').toggleClass('show');
    $('.send-message-box').hide();
    $('#add-item').show();
    $('.user-list').show();
    $('.teacher-menu').toggleClass('hide');
    $('.add-user-menu').toggleClass('hide');
}


$(document).ajaxStart($.blockUI).ajaxStop($.unblockUI);

$.ajaxSetup({ 
     beforeSend: function(xhr, settings){
         function getCookie(name){
             var cookieValue = null;if(document.cookie && document.cookie !=''){
                 var cookies = document.cookie.split(';');for(var i =0; i < cookies.length; i++){
                     var cookie = jQuery.trim(cookies[i]);
                     //Does this cookie string begin with the name we want?
                     if(cookie.substring(0, name.length +1)==(name +'=')){
                         cookieValue = decodeURIComponent(cookie.substring(name.length +1));break;}}}return cookieValue;}
                         if(!(/^http:.*/.test(settings.url)||/^https:.*/.test(settings.url))){
                         //Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));}
    }
});

