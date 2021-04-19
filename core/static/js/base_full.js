$(document).ready(function(){
	$('#profile-picture-upload').on('click', function(){
		$('#upload-profile-picture').trigger('click');
	});
	
	$('#upload-profile-picture').on('change', function(){
		$('#profile-picture-form').submit();
	});
	
	$('#user-privacy').on('click', function(){
		var private = $(this).hasClass('public');
		
		if (private){
			$(this).text('Private');
			$(this).removeClass('public');
			$(this).addClass('private');
		} else{
			$(this).text('Public');
			$(this).removeClass('private');
			$(this).addClass('public');
		}
		
		$('#user-privacy-setting').val(private ? 'True' : 'False');
		
		showUpdateButton();
	});
	
	$('#update-user-bio').on('keyup', showUpdateButton);
	$('#user-edit-name input').on('keyup', showUpdateButton);
});

function showUpdateButton(){
	$('#user-bio input').css('display', 'block');
}