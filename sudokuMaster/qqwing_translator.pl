#https://qqwing.com/generate.html (IMPORTANT: select compact-style)
use strict;
use warnings;
open (FH, "<".$ARGV[0]);
my @raw = <FH>;
close (FH);
foreach my $row (@raw) {
	$row =~ s/\./0/g;
}
#print @raw;
#=pod
my $headname = $ARGV[0];
$headname =~ s/\.txt//;
open (FH, ">".$headname."_translation.txt");
print FH (@raw);
close (FH);

#=cut