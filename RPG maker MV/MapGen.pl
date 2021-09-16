#RMMV map generator
#melt data:
%meltIDs = (
	00000000 => 0,
	10000000 => -1,
	01000000 => -2,
	00100000 => -3,
	00010000 => -4,
	11000000 => -5,
	"11001000" => -6,
	01100000 => -7,
	"01100100" => -8,
	00110000 => -9,
	"00110010" => -10,
	10010000 => -11,
	"10010001" => -12,
	"1010\d\d\d\d" => -13,
	"0101\d\d\d\d" => -14,
	11100000 => -15,
	11100100 => -16,
	11101000 => -17,
	11101100 => -18,
	01110000 => -19,
	01110010 => -20,
	01110100 => -21,
	01110110 => -22,
	10110000 => -23,
	10110001 => -24,
	10110010 => -25,
	10110011 => -26,
	11010000 => -27,
	11011000 => -28,
	11010001 => -29,
	11011001 => -30,
	11110000 => -31,
	11110100 => -32,
	11111000 => -33,
	11111100 => -34,
	11110001 => -35,
	11110101 => -36,
	11110001 => -37,
	11111101 => -38,
	11110010 => -39,
	11110110 => -40,
	11111010 => -41,
	11111110 => -42,
	11110011 => -43,
	11110111 => -44,
	11111011 => -45,
	11111111 => -46);




$ID		= $ARGV[0];
$height	= $ARGV[1];
$width	= $ARGV[2];

#Layer 1 initializing
@grid = ();
for (my $row = 0; $row < $height; $row++) {
	for (my $column = 0; $column < $width; $column++) {
		$grid[$row][$column] = 0;
	}
}



@terrainTypes = (2862,2478); #tipos de terreno, puede ampliarse la lista:
=pod

2862	grassland
2478	pond
3246	wasteland
3342	dirt field
3678	desert B
3390	dirt field B
=cut

#SEEDING
#ese 12 puede cambiarse. Se puede entender como un factor de seed population
for (1..int($width*$height/12)) {
	$terrainID = $terrainTypes[int(rand(@terrainTypes))];

	$randX = int(rand($width));
	$randY = int(rand($height));
	#print (($randX+1) . "," . ($randY+1) . "\n");
	$grid[$randY][$randX] = $terrainID;
}

#GROWING
#Gap filling and proliferation
	fillGaps:
	$gaps = 0;
	for (my $x = 0; $x < $width; $x++) {
		for (my $y = 0; $y < $height; $y++) {
			#print ("$grid[$y][$x]	");
			if ($grid[$y][$x] != 0) {
	
				$randGrow = int(rand(4))+1;
				#print $randGrow;

				if 		($randGrow == 1 and $y != 0) {
					$grid[$y-1][$x] = $grid[$y][$x];
	
				}elsif	($randGrow == 2 and $x != 0) {
					$grid[$y][$x-1] = $grid[$y][$x];
	
				}elsif	($randGrow == 3 and $y != $height-1) {
					$grid[$y+1][$x] = $grid[$y][$x];
	
				}elsif	($randGrow == 4 and $x != $width-1) {
					$grid[$y][$x+1] = $grid[$y][$x];
				}

			}else{
				$gaps++
			}
			#print "\n";
		}
	}
	#print "\n";
=view map stage at every "gap filling loop"
	foreach my $t (@grid) {
		foreach my $i (@$t) {
			print "$i ";
		}
		print "\n";
	}
	print $gaps."\n";
=cut

if ($gaps != 0) {
	goto fillGaps;
}


#MELTING
#creating melting matrix
for (my $x = 0; $x < $width; $x++) {
	for (my $y = 0; $y < $height; $y++) {

#	00	01	02
#	10	--	12
#	20	21	22

		$adjacent[1] = $grid[$y][$x-1] ;
		$adjacent[2] = $grid[$y-1][$x] ;
		$adjacent[3] = $grid[$y][$x+1] ;
		$adjacent[0] = $grid[$y+1][$x] ;
		$adjacent[5] = $grid[$y-1][$x-1];
		$adjacent[6] = $grid[$y-1][$x+1];
		$adjacent[7] = $grid[$y+1][$x+1];
		$adjacent[4] = $grid[$y+1][$x-1];


		undef($codeID);
		foreach my $t (@adjacent) {
			if ($t == $grid[$y][$x]) {
				$codeID .= 1;
			}elsif (!defined($t)){
				$codeID .= 1;
			}else{
				$codeID .= 0;
			}
		}
		if ($codeID =~ /\^0000\d\d\d\d\$/ or 
			$codeID =~ /\^1000\d\d\d\d\$/ or 
			$codeID =~ /\^0100\d\d\d\d\$/ or 
			$codeID =~ /\^0010\d\d\d\d\$/ or 
			$codeID =~ /\^0001\d\d\d\d\$/ or
			$codeID =~ /\^0101\d\d\d\d\$/ or
			$codeID =~ /\^1010\d\d\d\d\$/ or
			$codeID =~ /\^111011\d\d\$/ or
			$codeID =~ /\^0111\d11\d\$/ or
			$codeID =~ /\^1011\d\d11\$/ or
			$codeID =~ /\^11011\d\d1\$/ 
			
			) {
			substr($codeID, 4, 4) =~ s/\d/0/g;
		}








		$meltMatrix[$y][$x] = $meltIDs{$codeID};
=poc
		$codeID = 	"$grid[$y][$x+1] " . 
					"$grid[$y-1][$x] " . 
					"$grid[$y][$x-1] " . 
					"$grid[$y+1][$x] " . 
					"$grid[$y-1][$x+1]" . 
					"$grid[$y-1][$x-1]" . 
					"$grid[$y+1][$x-1]" . 
					"$grid[$y+1][$x+1]";
=cut
		print $codeID." ";
	}
	print "\n";
}
print "MELTING MATRIX:\n";
foreach my $t (@meltMatrix) {
	foreach my $i (@$t) {
		print "$i\t";
	}
	print "\n";
}

=pod
@grid2 = ();
for (my $row = 0; $row < $height; $row++) {
	for (my $column = 0; $column < $width; $column++) {
		$grid2[$row][$column] = 0;
	}
}
#Operar de este modo hasta las 6 layers del mapa. De momento sólo operamos con terreno.
=cut


#FORMATTING
for (my $x = 0; $x < $width; $x++) {
	for (my $y = 0; $y < $height; $y++) {
		print "$grid[$y][$x] ";
		$formatGrid .= ($grid[$y][$x]+$meltMatrix[$y][$x]) . ",";
	}
	print "\n";
}



for (1..($width*$height*5-1)) { $formatGrid .= "0,"; }
$formatGrid .= "0"; #esto es para evitar la última coma, ya se cambiará.

$formatOutput = "\"data\":[$formatGrid],\n\"events\":[\n]\n}";






open MAPFILE, ">Map$ID.json";
print MAPFILE "{\n\"autoplayBgm\":false,\"autoplayBgs\":false,\"battleback1Name\":\"\",\"battleback2Name\":\"\",\"bgm\":{\"name\":\"\",\"pan\":0,\"pitch\":100,\"volume\":90},\"bgs\":{\"name\":\"\",\"pan\":0,\"pitch\":100,\"volume\":90},\"disableDashing\":false,\"displayName\":\"\",\"encounterList\":[],\"encounterStep\":30,\"height\":$height,\"note\":\"\",\"parallaxLoopX\":false,\"parallaxLoopY\":false,\"parallaxName\":\"SeaofClouds\",\"parallaxShow\":true,\"parallaxSx\":0,\"parallaxSy\":0,\"scrollType\":0,\"specifyBattleback\":false,\"tilesetId\":1,\"width\":$width,\n";

print MAPFILE $formatOutput;
close MAPFILE;

