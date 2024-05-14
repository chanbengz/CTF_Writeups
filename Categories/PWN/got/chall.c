#include <stdio.h>
#include <stdlib.h>

void get_shell(){
        system("/bin/sh");
}

void main(){
        char buf[128];
        read(0 , buf , sizeof(buf));
        printf(buf);
        exit(1);
}