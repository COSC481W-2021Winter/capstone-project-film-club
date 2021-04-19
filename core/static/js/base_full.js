$(document).ready(function(){
	$('#profile-picture-upload').on('click', function(){
		$('#upload-profile-picture').trigger('click');
	});
	
	$('#upload-profile-picture').on('change', function(){
		$('#profile-picture-form').submit();
	});
});