#!/usr/bin/perl -w

use CGI;
use File::Slurp;
use MLDBM;
use Fcntl;
use LWP;
use JSON;

my $q = new CGI;
my $dbm = tie %o, 'MLDBM', 'imagedb', O_CREAT|O_RDWR, 0640 or die $!;
my $json = new JSON;
my $api = 'YOUR API KEY HERE';
my $ua = LWP::UserAgent->new;

if (!$q->param) { exit }

# This is set up for 2 items -- obviously customize as needed for however many items you're tracking

# The key for each item should be the number that's matched that's passed into the script
# The image name should be an absolute or a relative path to a jpg file 

my $items = {
	1 => {
		'image'=>'YOUR IMAGE NAME',
		'widget'=> 'YOUR WIDGET ID'
	},
	2 => {
		'image'=>'YOUR IMAGE NAME',
		'widget'=> 'YOUR WIDGET ID'
	},
};



$count = $o{$q->param('image')}++;
my $data = $json->encode({'value'=>$count});
my $img = read_file($items->{$q->param('image')}->{'image'}, binmode => ':raw');
my $url = "https://push.ducksboard.com/values/" . $items->{$q->param('image')}->{'widget'} . "/";
my $req = HTTP::Request->new(POST, $url);
$req->content_type('application/json');
$req->authorization_basic($api, 'nottherealpassword');
$req->content($data);
$ua->request($req)->as_string;

print $q->header( 
	type => 'image/jpg',
	content_length=>length($img)
);

print $img;
