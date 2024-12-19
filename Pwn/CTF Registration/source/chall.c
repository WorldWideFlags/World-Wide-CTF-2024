#include <stdio.h>
#include <string.h>
#include "rpmalloc/rpmalloc.h"

#define MAX_BLOCK 100

typedef struct {
	unsigned long age;
	char name[8];
	char description[32];
} hacker_t;

hacker_t* hackers[MAX_BLOCK];
rpmalloc_interface_t interface;
char credits[] = "Credits to Mattias Jansson for creating this awesome memory allocator : \nhttps://github.com/mjansson/rpmalloc\n";


// Actual challenge code
void banner() {
	puts(" _____ ___________  ______           _     _             _   _             \n/  __ \\_   _|  ___| | ___ \\         (_)   | |           | | (_)            \n| /  \\/ | | | |_    | |_/ /___  __ _ _ ___| |_ _ __ __ _| |_ _  ___  _ __  \n| |     | | |  _|   |    // _ \\/ _` | / __| __| '__/ _` | __| |/ _ \\| '_ \\ \n| \\__/\\ | | | |     | |\\ \\  __/ (_| | \\__ \\ |_| | | (_| | |_| | (_) | | | |\n \\____/ \\_/ \\_|     \\_| \\_\\___|\\__, |_|___/\\__|_|  \\__,_|\\__|_|\\___/|_| |_|\n                                __/ |                                      \n                               |___/  \n");
}

int menu() {
	puts("1) Register hacker\n2) Read hacker profile\n3) Quit\n");
	printf(">> ");

	int choice;
	scanf("%d", &choice);
	getchar();
	return choice;
}

void register_hacker() {
	size_t free_index = 0;
	while(hackers[free_index]) free_index++;
	if(free_index >= MAX_BLOCK) {
		puts("Sorry ! No spots left :/");
		return;
	}

	hacker_t* hacker = (hacker_t*) rpmalloc(sizeof(hacker_t));
	printf("How old is the hacker? ");
	scanf("%lu", &hacker->age);
	getchar();

	printf("What's the hacker's name ? ");
	scanf("%16[^\n]s", hacker->name);
	getchar();

	printf("How would you describe this hacker ? ");
	scanf("%32[^\n]s", hacker->description); // MAIN VULN
	getchar();

	hackers[free_index] = hacker;
	printf("Your hacker number is %zu !\n", free_index);
}


void read_hacker() {
	size_t index;
	printf("What is the hacker's number ? ");
	scanf("%zu", &index);
	getchar();

    // Avoid overflow or underflow
    if(index < 0 || index >= MAX_BLOCK) {
        puts("Invalid index.");
        return;
    }

	if(hackers[index] == NULL) {
		printf("Sorry, but no hacker is registered as number %zu...\n", index);
		return;
	}

	hacker_t* hacker = hackers[index];
	puts("========================= HACKER ========================");
	printf("Name: %s\n", hacker->name);
	printf("Age: %lu\n", hacker->age);
	printf("Description: %s\n", hacker->description);
	puts("=========================================================");
}

int main()
{
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

	rpmalloc_initialize(&interface);

	banner();
	while(1) {
		int choice = menu();
		switch(choice) {
			case 1:
				register_hacker();
				break;
			case 2:
				read_hacker();
				break;
			case 3:
				rpmalloc_finalize();
				return 0; // Terminate program
            case 69:
                // I love rpmalloc ! 
                {
                    char** test = rpmalloc(8);
                    *test = credits;
                    printf("%s\n", *test);
                    break;
                }
			default:
				printf("Invalid option \"%d\".\n", choice);
		}
	}

	rpmalloc_finalize();
	return 0;

}

