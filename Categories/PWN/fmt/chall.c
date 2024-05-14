#include <stdio.h>

int main(int argc, char **argv) {
  setbuf(stdout, 0);
  setbuf(stdin, 0);
  setbuf(stderr, 0);

  char buf[128];
  char flag[64];

  puts("Welcome to echo server!");
  
  FILE *file = fopen("flag.txt", "r");
  fgets(flag, sizeof(flag), file);
  
  while(1) {
    printf("> ");
    fgets(buf, sizeof(buf), stdin);
    printf(buf);
  }  
  return 0;
}