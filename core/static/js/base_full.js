$(document).ready(function(){
	$('#profile-picture-upload').on('click', function(){
		$('#upload-profile-picture').trigger('click');
	});
	
	$('#upload-profile-picture').on('change', function(){
		$('#profile-picture-form').submit();
	});
	
	$('#update-user-bio').on('keyup', showUpdateButton);
	$('#user-edit-name input').on('keyup', showUpdateButton);
});

function showUpdateButton(){
	$('#user-bio input').css('display', 'block');
}