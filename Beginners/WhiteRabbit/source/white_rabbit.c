//gcc -g -o white_rabbit -z execstack -fno-stack-protector --std=c99 white_rabbit.c

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void follow() {
    char buf[100];
    gets(buf);
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    printf("\n  (\\_/)\n");
    printf("  ( •_•)\n");
    printf("  / > %p\n\n", (void*) main);
    printf("follow the white rabbit...\n");
    follow();
    return 0;
}
