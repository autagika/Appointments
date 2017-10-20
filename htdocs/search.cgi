#!C:\Perl64\bin\perl5.24.2

# Author: Ashish Utagikar
# Date: 10/19/2017

# This script searches an appointment using the search
# string in the description column and diplays the records
# If the search string is empty then it displays all the records

use strict;

use warnings;
use CGI;
use DBI;
use Time::Local;
use JSON;
use DateTime;

$| = 1;

my $CGI = new CGI();

my $json_obj = new JSON;

sub main {

	print $CGI->header( -type => "application/json", -charset => "utf-8" );

	# Get the search string from the client
	my $search = $CGI->param("searchstring");

	## Connecting to the database
	my $dbh = DBI->connect( "dbi:mysql:webapp", "autagika", "arizona" );

	# Exit if it failed to connect to the database
	unless ( defined($dbh) ) {
		die "Cannot connect to the database.\n";
	}

	my $sth1;

	# search the description column using the search string
	if ($search) {
		$sth1 = $dbh->prepare(

qq{SELECT appointmenttime,Description FROM appointments WHERE Description LIKE ?}
		);
		my $result1 = $sth1->execute( "%" . $search . "%" );

		if ( !$result1 ) {
			die
"An error occurred during the search. Please see the server log file";
		}

	}
	else {
		$sth1 =
		  $dbh->prepare(
			qq{SELECT appointmenttime,Description FROM appointments})
		  ;   ## if the search string is empty then get all the database records

		my $result2 = $sth1->execute();
		if ( !$result2 ) {
			die
"An error occurred during the search. Please see the server log file";
		}

	}

	my @array = ();

	# Loop over all the database records and fetch them

	while ( my @ary = $sth1->fetchrow_array() ) {

		my ( $date, $time ) = split /\s+/, $ary[0];

		my ( $hours, $minutes, $sec ) = split /\:/, $time;

		my $hoursmin = $hours . ":" . "$minutes";

		push( @array, $date, $hoursmin, $ary[1] );

	}

	## Write the database data as the JSON object

	print $json_obj->pretty->encode( \@array );

	$sth1->finish();

	$dbh->disconnect();

}

main();
