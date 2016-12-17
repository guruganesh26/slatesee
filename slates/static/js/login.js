function validate(username, passwd){
	do_login_request(username, passwd);
}

function showRegisterForm(){
	$('#login-container').hide();
	$('#register-container').show();
}

function showLoginForm(){
	$('#register-container').hide();
	$('#login-container').show();
}

function toJSON(data) {
    return JSON.stringify(data, null, " ");
}

function parseJSON(data) {
    return JSON.parse(data);
}