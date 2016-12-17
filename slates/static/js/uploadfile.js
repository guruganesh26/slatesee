var file_list = [];
var convert_to_base64 = function(file, name, size, callback) {
    var reader = new FileReader();
    reader.onload = function(readerEvt) {
        var binaryString = readerEvt.target.result;
        file_content = btoa(binaryString);
        callback(file_content, name, size)
    };
    reader.readAsBinaryString(file);
}

var uploadFileFormat = function(size, name, content) {
    result = {
        "file_size": parseInt(size),
        "file_name": name,
        "file_content": content
    }
    return result
}


var uploadFile = function(fileListener, callback) {
    var evt = fileListener
    if(evt.target.id =="profile-image"){
        file_list = [];
    }
    max_limit =  1024 * 1024 * 50
    // file max limit 50MB
    var files = evt.target.files;
    var results = [];
    for(var i = 0; i < files.length; i++){
        var file = files[i];
        file_name = file.name
        file_size = file.size
        var file_extension = file_name.substring(file_name.lastIndexOf('.') + 1);
        console.log("file.size : "+file.size);
        console.log("max_limit : "+max_limit);
        if (file_size > max_limit) {
            sendToast("File max limit exceeded");
            return;
        }
        else if(file_extension == 'exe'){
            sendToast("Invalid file format");
            return;
        }
        else if(file_extension == 'htm'){
            sendToast("Invalid file format");
            return;
        }
        else if(file_extension == 'xhtml'){
            sendToast("Invalid file format");
            return;
        }
        else if(file_extension == 'html'){
            sendToast("Invalid file format");
            return;
        }
        else{
            file_content = null;
            if (file) {
                convert_to_base64(file, file_name, file_size, function(file_content, name, size) {
                    if (file_content == null) {
                        callback("File content is empty")
                    }
                    result = uploadFileFormat(
                            size, name, file_content
                    );
                    results.push(result);
                    if (results.length == files.length){
                        callback(results)
                    }
                });
            }
        }
    }

}

var uploadedFile = function(e){
    uploadFile(e, function result_data(data) {
        if(data == "File max limit exceeded"){
            sendToast(message.file_maxlimit_exceed);
            $(".uploaded-filename").html('');
            $("#upload_file").val("");
            return;
        }
        else if(data != 'File max limit exceeded' || data != 'File content is empty'){
            file_list.push(data);
            var result = ""
            for(i = 0; i < data.length; i++){
                var fileclassname;
                var filename = data[i]['file_name']
                fileclassname = filename.replace(/[^\w\s]/gi,"");
                fileclassname = fileclassname.replace(/\s/g, "");
                result += "<span class='"+fileclassname+"'>" + filename + "<img src='/static/images/delete.png' class='removeicon' style='width:16px;height:16px;' onclick='remove_temp_file(\""+fileclassname+"\")' /></span>";
            }
            $('.uploaded-filename').show()
            $(".uploaded-filename").append(result);
        }
        else{
          sendToast(data);
        }
    });
}

var uploadStatus = function(response, status){
    sendToast(status);
} 

var saveUploadedFiles = function(orgr){
    if(file_list.length==0){
        sendToast('Please upload atleast one file');
        return;
    }
    var event_name=$('#event-details').val();
    var event_date=$('#event-date').val();
    console.info(file_list);
    apiCall('/event_upload', 'post', toJSON({"event_detail":event_name, "organizer":orgr, 
        "event_date":event_date, "file_list":file_list}), uploadStatus);
    $('.uploaded-filename').toggleClass('hide');
    sendToast('Files upload started successfully');
}

/*function displayOrgrList(orgrs){
    $('#orgr').empty();
    orgrs.forEach(function(i){
       $('#orgr').append('<option value='+i["id"]+'>'+i["first_name"]+'</option')
    });

}

function getOrgrList(){
    var user_type="teacher";
    apiCall('users', 'get', {'user_type':user_type}, displayOrgrList);
}*/