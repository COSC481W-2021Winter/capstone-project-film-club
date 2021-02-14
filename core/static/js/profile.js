$(document).ready(function(){
	$('#user-friend').on('click', function(){
		var button = this;
		
		$.ajax({
			url: '/friend/',
			type: 'POST',
			data: {
				'username': $('#profile-username').val()
			},
			success: function(data){
				if (data['added']){
					$(button).addClass('friend');
					
					$(button).find('.main-label').text('Friends');
				} else {
					$(button).removeClass('friend');
					
					$(button).find('.main-label').text('Add friend');
				}
			},
			error: function(request, error){
				console.log('FAILED');
			}
		});
	});
});