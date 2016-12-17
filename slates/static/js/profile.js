function setTheme(){
	window.localStorage['theme'] = $('#theme').val();
	if ($('#theme').val() == "black"){
		window.localStorage['theme']=''
	}
	window.location.reload();
}