var _PAGE=1;
var _PAGE_SIZE=6;
function getEvents(){
    apiCall('/messages', 'get', {"page_size":_PAGE_SIZE, "page":_PAGE, "message_type":"event"}, displayEvents);
}

function getEventsGallery(){
    apiCall('/event_list', 'get', {}, displayEventsGallery);
}


function displayEvents(messages){
    _PAGE = _PAGE+1;

    var elem = $('.event-container');
    fillMessages(elem, messages);
    if(messages.length>_PAGE_SIZE){
        elem.append('<button class="sbutton" onclick="getEvents()" style="float:right">Next</button>');
    }
}

function displayEventsGallery(data){
    var elem = $('#slides');
    var url="";
    for (var e=0;e<data.length;e++){
      if(window.location.host == "eduslates.appspot.com"){
        var url = "https://storage.googleapis.com"
      }
      elem.append('<img id="event-img'+e+'"src="'+url+data[e]["image_url"]+'"></img>');
      $('#event-img'+e).attr('event-name', data[e]["event_detail"]);
      $('#event-img'+e).attr('event-date', data[e]["event_date"]);
      $('#event-img'+e).attr('organizer', data[e]["organizer"]);
    }

    $(function() {
      $('#slides').slidesjs({ 
      width: 940,
      height: 528,
      callback: {
          loaded:function(number){
            $('.event-details').html('<div>Event: '+$("#event-img0").attr("event-name")+'</div>'+
            '<div>Date: '+$("#event-img0").attr("event-date")+'</div>'+
            '<div>Organizer: '+$("#event-img0").attr("organizer")+'</div>');
              },
          start:function(number){
              var n = number;
              if ($('.slidesjs-control').children().length == number){
                  n=0
              }
              $('.event-details').html('<div>Event: '+$("#event-img"+n).attr("event-name")+'</div>'+
              '<div>Date: '+$("#event-img"+n).attr("event-date")+'</div>'+
              '<div>Organizer: '+$("#event-img"+n).attr("organizer")+'</div>');
          }
      },    
      play: {
          active: true,
          auto: true,
          interval: 4000,
          swap: true
        }
      });
    });
}