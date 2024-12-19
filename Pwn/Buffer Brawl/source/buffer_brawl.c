// gcc -fstack-protector-all -fPIE -pie -O2 -Wl,-z,relro,-z,now buffer_brawl.c -o buffer_brawl

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int stack_life_points = 100; 

void stack_smash();

void banner() {
    puts("");
    puts("        |||||||||");
    puts("        | _   _ |      ");
    puts("       (  ' _ '  )");
    puts("        |  ___  |");
    puts("         |_____|                   ");
    puts("  _______/     \\_______         ");
    puts(" /                     \\          ");
    puts("|   |\\             /|   |");
    puts("|   ||  .       .  ||   |     ");
    puts("|   / \\           / \\   |");
    puts("\\  |   | |_ | _| |   |  /     ");
    puts("|==|   | |_ | _| |   |==|");
    puts("/  /_ _|_|__|__|_|_ _\\  \\ ");
    puts("|___| /            \\|___|");
    puts("      |     |      |");
    puts("      |     |      |");
    puts("      |     |      |");
    puts("      |     |      |");
    puts("      ''|''|''|''|''           ");
    puts("        |  |  |  |   ");
    puts("        |  |  |  |   ");
    puts("       /   )  (   \\ ");
    puts("      Ooooo    ooooO");
}

void setup() {
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
}

void welcome() {
    puts("");
    puts("Ladies and gentlemen...\nAre you ready? For the main event of the CTF?");
    puts("Introducing...\nA challenge that packs a punch, tests your mettle, and overflows with excitement!");
    puts("Let's get ready to buffeeeeeeeer!!!\n");
}

void stack_check_up() { 
    if (stack_life_points == 13) {
        stack_smash();
    }
    else if (stack_life_points > 0) {
        printf("\nStack's life points: %d\n", stack_life_points);
    }
    else {
        puts("\nStack fainted! You're too brutal for it!");
        exit(0);
    }
}

void TKO() {
    puts("\nYou've been hit hard by the stack!\nTKO!");
    exit(0);
}

void jab() {
    puts("\nYou threw a jab! -1 to the stack's life points.");
    stack_life_points -= 1;

    stack_check_up();
}

void hook() {
    puts("\nYou threw a hook! -2 to the stack's life points.");
    stack_life_points -= 2;

    stack_check_up();
}

void uppercut() {
    puts("\nYou threw an uppercut! -3 to the stack's life points.");
    stack_life_points -= 3;

    stack_check_up();
}

void slip() {
    char buffer[30];

    puts("\nTry to slip...\nRight or left?");
    read(0, buffer, 29);
    printf(buffer);
}

void stack_smash() {
    char buffer[24];

    puts("\nThe stack got dizzy! Now it's your time to win!");
    puts("Enter your move: ");

    scanf("%s", &buffer);
}

void menu() {
    int choice;

    while (1) {
        puts("");
        puts("Choose:");
        puts("1. Throw a jab");
        puts("2. Throw a hook");
        puts("3. Throw an uppercut");
        puts("4. Slip");
        puts("5. Call off");
        
        printf("> ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                jab();
                break;
            case 2:
                hook();
                break;
            case 3:
                uppercut();
                break;
            case 4:
                slip();
                break;
            case 5:
                TKO();
                break;
            default:
                puts("Invalid choice. Try again.");
                break;
        }
    }
}


int main() {
    banner();
    setup();
    welcome();
    menu();
}
