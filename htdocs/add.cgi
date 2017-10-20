#!C:\Perl64\bin\perl5.24.2

# Author: Ashish Utagikar
# Date: 10/19/2017

# This script adds an appointment to the MySQL database
# It validates the datetime and description parameter and if the
# validation is successful, then it adds the appointment and then
# again displays the appointment form

use strict;

use warnings;
use CGI;
use DBI;
use Time::Local;
use JSON;
use DateTime;

$| = 1;    # Forces a flush right away

my $CGI = new CGI();

sub main {

	print $CGI->header();

	my $appt =
	  $CGI->param("datetimepicker");    ## Get the appointment date and time
	my $desc =
	  $CGI->param("description");    ### Get the description of the appointment

	my $validateform = validate_form();    # Validate the form before processing

	# If the validation fails just return
	if ( !$validateform ) {

		return 0;
	}

	## Connect to the mysql database
	my $dbh = DBI->connect( "dbi:mysql:webapp", "autagika", "arizona" );

	## Exit if it fails to connect to the database
	unless ( defined($dbh) ) {
		die "Cannot connect to the database.\n";
	}

	# Insert the appointment in to the database using prepared statements

	my $sth = $dbh->prepare(
qq{INSERT INTO appointments (appointmenttime,Description) VALUES(STR_TO_DATE(?, '%Y/%m/%d %H:%i'), ?)}
	);
	my $result = $sth->execute( $appt, $desc );
	#########################

	## If the insert fails, display error and show the form again
	if ( !$result ) {

		my $error_message =
"An error occurred during the creation of the appointment. Please check the server log file";
		my $success_message = "";

		display_form( $error_message, $success_message );
		die
"An error occurred during the creation of the appointment. Please check the server log file\n!";
	}

	else
	{ # If the insert succeeds then give a success message and siplay the form again

		my $success_message = "The appointment was scheduled successfully";

		my $error_message = "";

		display_form( $error_message, $success_message );

	}

	## Disconnect from the database
	$dbh->disconnect();

}

sub validate_form {

	my $appointment_value = $CGI->param("datetimepicker");
	my $description_value = $CGI->param("description");
	my $success_message   = "";
	my $error_message     = "";

	if ($appointment_value) {

		my ( $date, $time ) = split /\s+/, $appointment_value;

		my ( $hours, $minutes ) = split /\:/, $time;

		my ( $year, $mon, $mday ) = split /\//, $date;

		## Construct new data apointment object after getting the year, month, day, hours and minutes
		my $dt = DateTime->new(
			year       => $year,
			month      => $mon,
			day        => $mday,
			hour       => $hours,
			minute     => $minutes,
			second     => 0,
			nanosecond => 0,
			time_zone  => 'America/Phoenix',
		);

		my $appt_time =
		  $dt->epoch;    # Get the appointment time since epoch (Jan 1 1970)

		$dt = DateTime->now;

		my $current_time = $dt->epoch;    # Get the current time since epoch

		# Display error if the appointments are made in the past
		if ( $current_time > $appt_time ) {
			$error_message .=
"Appointment cannot be made in the past. Please check appointment date and time <br /><br />";
		}
	}
	else {

		$error_message .=
		  "Appointment date and time cannot be empty <br /> <br />"
		  ;    # Display error if the appointment time is empty
	}

	## Display error if appointment description is empty
	if ( !$description_value ) {
		$error_message .=
		  "Appointment description cannot be empty <br /> <br />";
	}

	if ($error_message) {

		$success_message = "";
		display_form( $error_message, $success_message );

		return 0;
	}

	else {
		return 1;
	}
}

## Display appointment form
sub display_form {
	my $error_message   = shift;
	my $success_message = shift;

	print <<EOF2;

	<!DOCTYPE html>
<html>

<head>
<meta charset="UTF-8">
<title>Appointment Form</title>
<link rel="stylesheet" type="text/css" href="css/style1.css">
<link rel="stylesheet" type="text/css" href="css/style2.css">
</head>
<body>
    <div id="errorMessage">$error_message</div>
    <p id = "successmessage">$success_message</p>
    
    <div id="frontend">
		<input type="button" name="new" id="new" value="NEW">

	</div>

	<form action="./add.cgi" method="post" id="apptform" >
		<input type="submit" name="add" id="add" value="ADD" />

		<input type="button" name="cancel" id="cancel" value="CANCEL" /> <br />
		<br /> <label for="datetimepicker" >DATE</label>

		<input type="text" id="datetimepicker" name="datetimepicker" class="datetimepicker" />

		<br />

		<br /> <label for="description" >DESCRIPTION</label>
		<input type="text" name="description" id="description"/>
	</form>

	

	<br />
	<br />
	<div id="frontend1">
	<input type="text" name="appointments" id="appointments">
	<input type="submit" id="search" name="search" value="SEARCH">
	</div>
	<br />
	<br />
	<table id="table" border="1" class="atable">
    <caption>Appointments</caption>

	</table>
	
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>

<link rel="stylesheet" type="text/css" href="datetimepicker-master/datetimepicker-master/jquery.datetimepicker.css"/ >
<script src="datetimepicker-master/datetimepicker-master/jquery.js"></script>
<script src="datetimepicker-master/datetimepicker-master/build/jquery.datetimepicker.full.min.js"></script>

<script src="js/appointments.js"></script>

</body>
</html>

EOF2

}

main();
