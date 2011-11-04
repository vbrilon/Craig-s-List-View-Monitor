#!/usr/bin/perl -w

use CGI;
use File::Slurp;
use MLDBM;
use Fcntl;
use LWP;
use JSON;
use Data::Dumper;

my $q = new CGI;
my $dbm = tie %o, 'MLDBM', 'imagedb', O_CREAT|O_RDWR, 0640 or die $!;
my $json = new JSON;
my $api = '30vxksjekc2hzfgw8f4csonxcpazstifj4scuc1i3og89w8fca';
my $ua = LWP::UserAgent->new;

if (!$q->param) { exit }

my %images = (
	1 => 'tv.jpg',
	2 => 'guitar.jpg'
);

my %widgets = (
	1 => 'https://push.ducksboard.com/values/11657/',
	2 => 'https://push.ducksboard.com/values/11658/'
);

my $img = read_file($images{$q->param('image')}, binmode => ':raw');
$count = $o{$q->param('image')}++;

my $data = $json->encode({'value'=>$count});
my $req = HTTP::Request->new(POST, $widgets{$q->param('image')});
$req->content_type('application/json');
$req->authorization_basic($api, 'nottherealpassword');
$req->content($data);
$ua->request($req)->as_string;

print $q->header( 
	type => 'image/jpg',
	content_length=>length($img)
);


print $img;
