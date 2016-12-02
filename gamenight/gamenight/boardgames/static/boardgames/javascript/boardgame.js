$(document).ready(function(){


	/* ----------------------------------------------------------------------------------
	Boardgame index page
	*/
	$.urlParam = function(name){
	    var results = new RegExp('[\?&]' + name + '=([^&#+]*)').exec(window.location.href);
	    if (results==null){
	       return null;
	    }
	    else{
	       return results[1] || 0;
	    }
	}

	$.urlParam2 = function(name){
	    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
	    if (results==null){
	       return null;
	    }
	    else{
	       return results[1] || 0;
	    }
	}

	var boardgame_text_array = [];
	// Puts nice unicode text into description
	$('.boardgame_description').each(function(i, obj){
		var myDiv = $(this);
		myDiv.html(myDiv.text());
		boardgame_text_array.push(myDiv.html());
		myDiv.html(myDiv.text().substring(0,300));
		myDiv.after(' <span class="boardgame_readmore"><a href="#">Read more</a></span>');
		var myDiv_a = $('.boardgame_description a');
	});
	
	$('.boardgame_readmore a').on('click', function(event){
		event.preventDefault();

		var myDiv = $(this).closest('.boardgame_body');
		var div_num = myDiv.data('counter');
		var myDiv_newtext = boardgame_text_array[div_num-1];

		// Removes previous description and read more with new text
		myDiv.find('.boardgame_readmore').remove();
		myDiv.find('.boardgame_description').text('');
		detail_link = myDiv.find('a.boardgame_detail_link').attr('href');
		new_detail = myDiv.find('.boardgame_description').html(myDiv_newtext.substring(0,1000));

		// Replaces '#' with an actual link
		$(new_detail).append(' <a href="#">Details Page</a>');
		$(new_detail).find('a').attr('href', detail_link);
	});

	$('.current').on('click', function(event){
		$("html, body").animate({ scrollTop: 0 }, "slow"); return false;
	});

	// $('.boardgames_select').on('click', function(){
	// 	$(this).find('option.active').addClass('active')
	// });

	var result = $.urlParam('results');
	var result2 = $.urlParam2('page');
	if(result2 == null){
		result2 = '';
	}
	else if(result2.indexOf("+") < 0){
		result2 = '';
	}
	else{
		result2 = result2.substr(result2.indexOf("+") + 1);
	}
	if(result == null){
		result = '';
	}
	$('.boardgames_page_submit').on('click', function(){
		var value = $('#want_page').val();
		if(result == '' && result2 != ''){
			$('#want_page').attr('value', value+' '+result2);
			$('#want_page').val(value+' '+result2);
		}
		if(result != '' && result2 == ''){
			$('#want_page').attr('value', value+' '+result);
			$('#want_page').val(value+' '+result);
		}
	});
	$('.boardgames_next_page').on('click', function(){
		var href = $('.boardgames_next_page').attr('href');
		if(result == '' && result2 != ''){
			$('.boardgames_next_page').attr('href', href+'?results='+result2);
		}
		if(result != '' && result2 == ''){
			$('.boardgames_next_page').attr('href', href+'?results='+result);
		}
	});
	$('.boardgames_prev_page').on('click', function(){
		var href = $('.boardgames_prev_page').attr('href');
		if(result == '' && result2 != ''){
			$('.boardgames_prev_page').attr('href', href+'?results='+result2);
		}
		if(result != '' && result2 == ''){
			$('.boardgames_prev_page').attr('href', href+'?results='+result);
		}
	});


	/* ----------------------------------------------------------------------------------
	Boardgame detail page
	*/
	var description_div = $('.description');
	description_div.html(description_div.text());

});