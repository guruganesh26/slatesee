// *** Home related code start ***//

function sendMessage(teacher_id) {
    var message  = $('#message-area').val();
    if(message==''){
        sendToast('Please write message then send');
        return;
    }
    var message_type = $('#message-type').val(); 
    $('.message-text').toggleClass('hide');
    $('#message-area').val('');
    apiCall('/messages', 'post', toJSON({"message": message, "message_type":message_type,
      "created_by":teacher_id, "updated_by":teacher_id}), 
      sendToast('message sent successfully.'))
}

function addMarks(teacher_id){
  var sid = $("#student-mark-list").val();
  var data = {"user_id": sid,
              "s1": $('#s1').val(),
              "s2": $('#s2').val(),
              "s3": $('#s3').val(),
              "s4": $('#s4').val(),
              "s5": $('#s5').val(),
              "exam_name": $('#mark-type').val(),
              "updated_by": teacher_id
              }
  apiCall('/mark_list', 'post', toJSON(data), saveSuccess)
}

function addMcq(teacher_id){
  var data = {
              "question": $('#question').val(),
              "option1": $('#option1').val(),
              "option2": $('#option2').val(),
              "option3": $('#option3').val(),
              "option4": $('#option4').val(),
              "answer": $('#answer').val(),
              "correct_text": $('#correct-text').val(),
              "wrong_text": $('#wrong-text').val()
              }
  if($('#set-name').val()!=undefined && $('#set-name').val()!=''){
    data["set_name"]=$('#set-name').val();
  }else{
    data["set_id"]=$('#mcqset').val();
  }
  apiCall('/mcqs', 'post', toJSON(data), saveSuccess)
}

function addFlashCard(teacher_id){
  var data = {
              "side_a": $('#sidea').val(),
              "side_b": $('#sideb').val(),
              }
  apiCall('/flashcards', 'post', toJSON(data), saveSuccess)
}

function displayStudentForMarkList(users){
  var html = '';
  var elem = $('#student-mark-list');
  elem.empty()

  users.forEach(function(i){
         html+='<option value='+i["id"]+'>'+i['first_name']+'</option>'; 
  });
  elem.append(html);


}

function getStudentListForMark(){
  apiCall('/users', 'get', {'user_type':'student'}, displayStudentForMarkList);
}

function saveSuccess(response){
  $('.input-box').val('');
  $('.uploaded-filename').empty();
  sendToast('Added successfully');
}


function showAction(val){
  if(val=="marks"){
    $('.add-flash-form').hide();
    $('.add-mcq-form').hide();
    $('.add-marks-form').show()
  }else if(val=="flash"){
    $('.add-flash-form').show();
    $('.add-mcq-form').hide();
    $('.add-marks-form').hide()
  }else if(val=="mcq"){
    $('.add-flash-form').hide();
    $('.add-mcq-form').show();
    $('.add-marks-form').hide()    
  }
}

function displayMcqSetT(mcqSets){
  $('#mcqset').empty();
  for(var m=0;m<mcqSets.length-1;m++){
    $('#mcqset').append('<option value='+mcqSets[m]["id"]+'>'+mcqSets[m]["set_name"]+'</option>');
  }
}

function getMcqSets(){
    apiCall('/mcqsets', 'get', {"all":"all"}, displayMcqSetT);
}

// *** Home related code end ***//