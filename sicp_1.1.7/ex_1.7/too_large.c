#include <stdio.h>

int main(int argc, char **argv) {
    printf("An examination of rounding error in 32-bit floats:\n");
    printf("10.001: %f\n", 10.001f);
    printf("100.001: %f\n", 100.001f);
    printf("1000.001: %f\n", 1000.001f);
    printf("10000.001: %f\n", 10000.001f);
    printf("\n");
    printf("100,000 is already too large to represent a tolerance of 0.001:\n");
    printf("100000.001: %f\n", 100000.001f);
    printf("\n");
    printf("One million could be ten times outside of tolerance, undetected:\n");
    printf("1000000.01: %f\n", 1000000.01f);
}
