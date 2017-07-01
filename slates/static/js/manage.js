function displayUserList(users){
    var html = '';    
    $('#userList').empty();
    users.forEach(function(i){
         html+='<div class="user-details"><div class="user-profile left">';
         if(i["profile_image"]!=""){
            if(window.location.host == "slatesee1.appspot.com"){
              var url = "https://storage.googleapis.com"
              html+='<img src="'+url+i["profile_image"]+'"></img></div>';
            }else{
              html+='<img src="'+i["profile_image"]+'"></img></div>';
            }
         }else{
            html+='<img src="/static/images/teacher.png"></img></div>';
         }
         html+='<div class="pad5">Name:'+i["first_name"]+'</div>\
           <div class="pad5">standard:'+i["standard"]+'</div></div>'; 
    });
    $('#userList').append(html);
}

function getUserList(user_type){
    apiCall('/users', 'get', {'user_type':user_type}, displayUserList);
}

function saveTeacher(data){
  apiCall('/users', 'post', toJSON(data), saveTeacherSuccess)
}

// *** teacher manage related code start ***//

function addStudent(){
    var studName = $('#stud-name').val();
    if (studName.length<4){
      sendToast('Please add student name with atleast 4 characters');
      return;
    }

    var std = $('#std').val();
    
    var userName=$('#user-name').val();
    if (userName.length<4){
      sendToast('Please add user name with atleast 4 characters');
      return;
    }

    var regNo = $('#reg-no').val();
    if(regNo.length<4){
      sendToast('Please add reg no with atleast 4 characters');
      return;  
    }

    var parentName = $('#parent-name').val();
    if(parentName.length<4){
      sendToast('Please add parent name with atleast 4 characters');
      return;  
    }

    var mobileNo = $('#mobile-no').val();
    if(mobileNo.length<10){
      sendToast('Please add valid mobile no');
      return;  
    }

    var dob = $('#dob').val();

    if(file_list.length==0){
        sendToast('Please upload profile image');
        return;
    }

    var data = {'first_name':studName, 
                'standard': std,
                'user_type': "student", 
                'user_name': userName, 
                'reg_no':regNo, 
                'parent_name': parentName, 
                'mobile_no': mobileNo, 
                'dob': dob,
                'password': 'abc', 
                'teacher_id':'',
                'profile_image': file_list}

    saveStudent(data)

}

function saveStudentSuccess(response){
  $('.input-box').val('');
  $('.uploaded-filename').empty();
  sendToast("Student added successfully");
  getStudentList();
}

function saveTeacherSuccess(response){
  $('.input-box').val('');
  $('.uploaded-filename').empty();
  sendToast("Teacher added successfully");
  getUserList('teacher');
}

function saveStudent(data){
  apiCall('/users', 'post', toJSON(data), saveStudentSuccess)
}

function getStudentList(){
    apiCall('/users', 'get', {'user_type':'student'}, displayStudentList);
}

function displayStudentList(users){
    var html = '';
    $('#studentList').empty();
    users.forEach(function(i){
         html+='<div class="student-details"><div class="student-profile left">';
         if(i["profile_image"]!=""){
            if(window.location.host == "slatesee1.com"){
              var url = "https://storage.googleapis.com"
              html+='<img src="'+url+i["profile_image"]+'"></img></div>';
            }else{
              html+='<img src="'+i["profile_image"]+'"></img></div>';
            }
         }else{
            html+='<img src="/static/images/student.jpg"></img></div>';
         }
         html+='<div class="pad5">Student name:'+i["first_name"]+'</div>\
           <div class="pad5">standard:'+i["standard"]+'</div>\
           <div class="pad5">Parent: '+i["parent_name"]+'</div></div>';
 
    });
    $('#studentList').append(html);
}

// *** teacher manage related code end ***//