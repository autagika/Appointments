// Author: Ashish Utagikar
// Date: 10/19/2017

// This script contains the code for all the events handlers. The events are new , add, cancel and search. 
// It also searches and displays the database records based on the search string

//getAppointments function gets the appointments table from the database
// when a search is done

function getAppointments(appointments) {

	var datastring = 'searchstring=' + appointments;

	$.ajax({
		dataType : 'json',
		method : 'GET',
		data : datastring,
		url : 'search.cgi',

		success : function(data) {
			if (data) {
				var len = data.length;
				var txt = "";
				txt += "<tr><td>" + "Date" + "</td><td>" + "Time" + "</td><td>"
						+ "Description" + "</td></tr>";

				for (var i = 0; i < len; i += 3) {

					txt += "<tr><td>" + data[i] + "</td><td>" + data[i + 1]
							+ "</td><td>" + data[i + 2] + "</td></tr>";

				}

				$("#table").append(txt);

			}

		},
		error : function(jqXHR, textStatus, errorThrown) {
			alert('error: ' + textStatus + ': ' + errorThrown);
		}
	});

	return false;
}

$(document)
		.ready(
				function() {

					$(window).load(function() {

						getAppointments("");
					});

					// Adds an appointment to the database after doing the client side validation
					// if the validation fails then return false
					$('#add')
							.click(
									function(e) {

										$("#successmessage").empty();
										$("#errorMessage").empty();

										var appointmenttime = $(
												'#datetimepicker').val();
										var description = $('#description')
												.val();
										var error = 0;

										if (!$('#datetimepicker').val()) {

											error = 1;

											$("#errorMessage").append(
													'Please enter the appointment date and time'
															+ '<br /><br />');

										}

										if (!$("#description").val()) {

											error = 1;
											$("#errorMessage")
													.append(
															'<br />'
																	+ 'Please enter the appointment description'
																	+ '<br /><br />');

										}

										var currenttime = Date.now();
										var d = $('#datetimepicker')
												.datetimepicker('getValue');
										var apt_time;
										if (d !== null) {
											apt_time = d.getTime();
										}

										if (currenttime > apt_time) {
											error = 1;
											 $("#errorMessage")
													.append(
															'<br />'
																	+ 'Cannot make appointments in the past. Please check appointment date and time '
																	+ '<br /><br />');
										}

										if (error === 1) {

											 return false;
										}

										return true;

									});

					// If the new button is clicked, show the appointment form and hide the new button
					$("#new").click(function() {
						$("#frontend").hide();
						$("#apptform").show();
					});

					// If the cancel button is clicked, hide the appointment form and show the new button
					$("#cancel").click(function() {

						$("#errorMessage").empty();

						$("#successmessage").empty();

						$("#frontend").show();
						$("#apptform").hide();

					});

					// Show the Appointment widget
					$('#datetimepicker').datetimepicker({});

					// When the search button is clicked, search the database using the search string and return back the
					// database records
					$("#search").click(
							function() {
								$("#table").empty();

								$('<caption />').html("Appointments")
										.prependTo("#table");
								var appointments = $('#appointments').val();

								getAppointments(appointments);

							});

				});
