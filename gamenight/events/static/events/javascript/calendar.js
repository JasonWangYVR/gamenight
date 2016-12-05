var $j =jQuery.noConflict();

$j(document).ready(function() {
    $j('.datepicker').datepicker();
	$j(body).hover(function(){alert('test');});
});