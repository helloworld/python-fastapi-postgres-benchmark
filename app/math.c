#include "math.h"

int add(int a, int b) {
    return a + b;
}

int subtract(int a, int b) {
    return a - b;
}

int multiply(int a, int b) {
    return a * b;
}

bool is_even(int n) {
    return n % 2 == 0;
}

int calculate_expression(int x, int y) {
    return multiply(add(x, 2), subtract(y, 1));
}
