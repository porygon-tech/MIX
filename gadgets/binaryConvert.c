#include <stdio.h>
#include <stdlib.h>
#include <time.h>
//gcc binaryConvert.c -o bc -lm -O3 -fsanitize=address -static-libasan -g -Wall && time ./bc

void printbin(int n, int len){
	int k;
	for (int i = len-1; i >= 0; i--){
			k = n >> i;
			if (k & 1) printf("1");
			else       printf("0");
	}
	printf("\n");
}

void seedinit(void){
	time_t clock;
	srand((unsigned) time(&clock));
}

double uniform(void){
	return (double)rand()/RAND_MAX;
}; // Returns a number in [0,1)



int main(int argc, char const *argv[])
{

	seedinit();

	unsigned int ndigits = 8;
	unsigned char maxbits, d;
	maxbits = ndigits*sizeof(unsigned int);
	d = uniform()*(maxbits-1) + 1;

	printf("length = %d (%d bits)\n%d\n", ndigits, maxbits, d);
	printbin(d, ndigits);

	return 0;
}
/*


*/
