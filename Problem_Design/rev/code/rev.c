// #include"rev.h"
#include<stdio.h>
#include<stdlib.h>
#include<string.h>

char passwd[] = "mPa}{yvH@r!sspc3o_p";
int id[] = {2,11,4,18,7,12,16,8,9,14,17,6,5,10,0,15,1,13,3};

int main() {
    printf("secret code: ");
    char str[25];
    fgets(str,25,stdin);
    if(strlen(str) != 20)
        puts("Invalid."),exit(1);
    for(int i = 0;i < 19; i++)
        if(str[id[i]] != passwd[i])
            puts("Invalid."),exit(1);
    puts("Congratulations!");
    
    return 0;
}