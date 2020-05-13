#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define Max_line_length 132
#define Max_line_number 300
void start_formatting(int space,int width,int flag, int counter,const char* file){
	FILE *f = fopen(file,"r");
	char *del = " ";
	char *word;
	char buffer1[300];
	int space_tracker;
	int width_tracker = width-space;
	int word_length;
	//int exception = 0;
	
	while(counter>0){
		fgets(buffer1,Max_line_number,f);
		counter--;
	}
	
	while(fgets(buffer1,Max_line_length,f)){
		
		while(flag==0){    //"?fmt" is off,nothing will be change
			printf("%s",buffer1);
			if(fgets(buffer1,Max_line_length,f)){
			    if(buffer1[0]=='?'&&buffer1[1]=='f'&&buffer1[7]=='n'){
					flag = 1;
				}
			}else{
				exit(0);
			}
		}
		
		while(flag==1){
			if(buffer1[0]=='?'&&buffer1[1]=='f'&&buffer1[7]=='f'){
				flag = 0;
			}       
			space_tracker = space;
			while(space_tracker>0){
				printf(" ");
				space_tracker--;
			}
			word = strtok(buffer1,del);
			
			while(word&&flag==1){
				word_length = strlen(word);
				
				if(word[word_length-1]=='\n' && word[0]!='\n'){
					word[word_length-1] =' ';
					word_length = word_length-1;
					//exception = 1;
				}
				if(word[0]=='\n'){
					printf("\n");
				}
				
				
				//when word_length greater than the rest space of width of one line
				if(word_length>width_tracker){
					space_tracker = space;
					width_tracker = width-space;
					printf("\n");
					while(space_tracker>0){
						printf(" ");
						space_tracker--;
					}
					printf("%s ",word);
					width_tracker = width-space-word_length-1;
					word = strtok(NULL,del);
				}
				// when word_length less than the rest space of the width of one line
				else if(word_length<width_tracker){
					printf("%s ",word);
					width_tracker = width_tracker-word_length-1;
					word = strtok(NULL,del);
				}
				// when word_length is equal to the rest space of the width of one line
				else{
					printf("%s\n",word);
					space_tracker = space;
					width_tracker = width-space;
					while(space_tracker>0){
						printf(" ");
						space_tracker--;
					}
					word = strtok(NULL,del);
				}
			}
			if(fgets(buffer1,Max_line_length,f)){
				flag = 1;
			}else{
			    printf("\n");
			    exit(0);
			}
		}
	}
}
int main(int argc, char* argv[]){
		char buffer[Max_line_length]; //store formatting lines.    

		const char* filename = argv[1];
		FILE* f = fopen(argv[1], "r");
		if(!f) return 1;
		int line_counter = 0;
		int left_space = 0;
		int line_width = 0;
		int flag = 0;
		while(line_counter<=Max_line_number){
			fgets(buffer,Max_line_length,f);
			if(buffer[0]!='?'){ //finishing reading formatting commands and start formatting line by line
				fclose(f);
				start_formatting(left_space,line_width,flag,line_counter,argv[1]);
				exit(0);
			}else{
				char label = buffer[1];
				switch (label){
					case 'w':
					    line_width = atoi(&buffer[7]);
						flag = 1;
						line_counter++;
						break;
					case 'm':
					    left_space = atoi(&buffer[6]);
						line_counter++;
						
						break;
					case 'f':
					    if(buffer[7]=='n'){
							flag = 1;
							line_counter++;
						}else{
							flag = 0;
							line_counter++;
						}
						break;
				}
				
			}
		}
}
