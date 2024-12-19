#include <cstdio>
#include <stdlib.h>


bool check(char* s) {
    char tmp[384] = {0,};
    int i = 0, j = 0, cnt = 0;
    bool run = false;

    for (; i < 384; i++) {
        j = 0;
        if (s[i] != '%') continue;

        cnt += 1;
        i += 1;
        if (s[i] == '0') {
            // don't waste space!!
            return false;
        }

        while (s[i] >= '0' && s[i] <= '9') {
            tmp[j] = s[i];
            i += 1;
            j += 1;
        }

        if (j <= 1) {
            return false; 
        }

        tmp[j] = 0;
        int fmt_val = strtol(tmp, (char**)(&tmp), 10);
        if (fmt_val >= 58) {
            return false;
        }

    }
    return true;
}


int main(int argc, char** argv, char** envp) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    char s[384] = {0,};
    while(1) {
        printf(">> ");
        fgets(s, 384, stdin);
        if (check(s)) printf(s);
        else break;
    }
    return 0;
}

// gcc chall.cpp -o chall -O0 -Wno-format-security -Wl,-z,relro,-z,lazy -no-pie