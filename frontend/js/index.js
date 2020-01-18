$string1 = $("#string1")
$string2 = $("#string2")
$mcu = $('#mcu')
$dynamicPricing = $('#dynamicPricing')
$button = $("#submit-button")

$button.click(function(event){
	
	document.getElementById("loading").style.visibility = "visible"
	
	var str1 = $string1.val()
	var str2 = $string2.val()
	var dynamicPricing = document.getElementById( "dynamicPricing" )
	var mcu = document.getElementById( "mcu" )
	var requestData = JSON.stringify({'string1': str1, 'string2': str2, 'mcu': mcu.selectedIndex, 'dynamicPricing':dynamicPricing.checked})
	
	console.log("This is what we're sending to the server:")
	console.log(requestData)

	$.ajax({
		type: 'POST',
		url: 'submit',
		data: requestData,
		contentType: 'application/json',
		dataType: 'json',
		timeout: 5000,

		success: function(responseData){
			console.log("We Recieved Data from Server!")
			console.log(responseData)
			document.getElementById("success").style.display = "block"
			document.getElementById("loading").style.visibility = "hidden"
			document.getElementById("serverMessage").innerHTML = JSON.parse(responseData).data
			$('#serverSuccess').modal('show')
		},
		error: function(jqXHR, exception){
			console.log(exception)
			document.getElementById("loading").style.visibility = "hidden"
			document.getElementById("success").style.display = "none"
			$('#serverError').modal('show')
		}
	})

})