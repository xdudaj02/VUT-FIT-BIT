/********************************************************************************************/
/* * *			Vyhľadávanie kontaktov podľa zadaného reťazca 			* * */
/* * * 											* * */
/* * * 					   Verze:1 					* * */
/* * * 											* * */
/* * * 			            Jakub Duda, xdudaj02				* * */
/* * * 				        november 2019 					* * */
/* * * 											* * */
/********************************************************************************************/

#include <stdio.h>
#include <string.h>

#define LINES 100
#define LENGTH 100

/********************************   FUNCTION DECLARATIONS:  **********************************/
//funkcia, porovnanie dvoch znakov, vystup 1 ak je druhy znak jednym zo znakov, ktore reprezentuje prvy znak, inak 0
int character_equality_check(char x, char y); 

/*****************************************  MAIN: ********************************************/
int main(int argc, char *argv[])
{
	//inicializacia premennych
	char input[LINES][LENGTH+1];
	char c;
	unsigned x=0, y=0;
	unsigned invalid_lines_count=0;
	int invalid_line[LINES];
	for (unsigned i=0; i<LINES; i++)
		invalid_line[i]=0;

	//tu som sa trosku inspiroval internetom
	if ((fseek(stdin, 0, SEEK_END), ftell(stdin))<=0) //kontrola vyskytu vstupu
	{
		fprintf(stderr, "Error. No input dectected.\n");
		return 1;
	}
	else
		rewind(stdin);

	//priradenie hodnot zo standartneho vstupu stdin premennej input[][]
	while ((c = fgetc(stdin)) != EOF) //citanie znakov zo vstupu
	{ 
		if ((c!='\n') && (x<LINES) && (y<LENGTH))
		{
			input[x][y]=c;	//priradenie znakov dvojrozmernemu polu
			y++;
		}
		else if (c=='\n') //prvy rozmer pola reprezentuje cislo riadku, druhy poradie znaku v riadku
		{
			input[x][y]='\0';
			x++;
			y=0;
		}
		else if (x==LINES) //program sa ukonci a vypise chybu ak je pocet riadkov vstupu vacsi ako hodnota konstanty LINES
		{
			fprintf(stderr, "Error. Input too long.\n");
			return 1;
		}
		else if (y==LENGTH) //ak je dlzka riadku vacsia ako konstanta LENGTH, riadok je oznaceny ako neplatny
		{
			strcpy(input[x],"");
			invalid_line[x]=1;
			invalid_lines_count++;
		}
	}

	//podmienky pre hladany retazec
	if (argc==1) //ziadny dalsi argument okrem mena programu -> ziadna podmienka ->  vyhovuju vsetky vstupy(kontakty)
	{	
		for (unsigned print=0; print<x; print+=2) //vypis vsetkych platnych riadkov
		{
			if ((invalid_line[print]==0) && (invalid_line[print+1]==0))
				printf("%s, %s\n", input[print], input[print+1]);
		}
		if (invalid_lines_count>0) //vypis varovani pre neplatne riadky
		{
			for (unsigned i; i<LINES; i++)
			{
				if (invalid_line[i]==1)
					fprintf(stderr, "Warning. Line %d too long.\n", i+1);
			}
		}
		return 0;
	}
	unsigned argv1_length=strlen(argv[1]);
	if (argc>2) //podmienka pre ukoncenie programu pri zadani viac ako jedneho argumentu okrem mena programu
	{
		fprintf(stderr, "Error. Too many arguments.\n");
		return 1;
	}
	
	for (unsigned i=0; i<(argv1_length); i++) //hladany retazec moze obsahovat iba cisla od 0 do 9, inak je neplatny
	{
		if (((argv[1][i])<'0') || ((argv[1][i])>'9'))
		{
			fprintf(stderr, "Error. False entry.\n");
			return 1;
		}
	}


	//hlavna funkcia programu, detekcia hladaneho retazca
	int good_lines[LINES]; //premenna 'dobre'riadky 
	for (int i=0; i<LINES; i++) //pre kazdy riadok ma najprv priradenu hodnotu 0
		good_lines[i]=0;

	//cyklus na opakovanie pre kazdy riadok vstupu
	for (unsigned lines=0; lines<x; lines++) 
	{
		unsigned characters=0;
		//cyklus na opakovanie pre celu dlzku riadku (dlzka riadku + 1 - dlzka hladaneho retazca) 
		while ((characters<((strlen(input[lines]))+1-(argv1_length))) && (good_lines[lines]!=1)) 
		{
			unsigned good_characters=0; //premenna 'dobre' znaky
			//cyklus na opakovanie pre celu dlzku hladaneho retazca
			for (unsigned searched_characters=0; searched_characters<(argv1_length); searched_characters++) 
			{
				//volanie funkcie character_check na porovnanie jedneho znaku hladaneho retazca a jedneho znaku zo vstupu
				//podmienka, v pripade uspechu zvysi hodnotu premennej good_characters o 1
				if (character_equality_check(argv[1][searched_characters], input[lines][(characters+searched_characters)])==1) 
					good_characters++;
			}
			//podmienka, po vykonani cyklu na opakovanie pre celu dlzku hladaneho retazca, skontroluje kolko znakov z hladaneho retazca bolo 'najdenych' vo vstupe
			//ak pocet 'najdenych' znakov je rovnaky ako dlzka hladaneho retazca, t.j. vsetky znaky hladaneho retazca boli 'najdene', premennej good_lines sa priradi hodnota 1
			if (good_characters==argv1_length)
				good_lines[lines]=1;
			characters++;
		}	
	}

	int nothing=0;
	//cyklus na vypisanie kontaktov v ktorych bol najdeny hladany retazec
	for (unsigned print=0; print<x; print+=2) //opakovanie pre pocet kontaktov
	{
		//podmienka, ak je kontakt 'dobry' (aspon jedno z dvojice meno a cislo je 'dobre') a kontakt neobsahuje ani jeden neplatny riadok
		if (((good_lines[print]==1) || (good_lines[print+1]==1)) && ((invalid_line[print])==0 && (invalid_line[print+1]==0)))
		{
			nothing++; //premenna sa zvysuje pri vypise kazdeho 'dobreho' kontaktu
			printf("%s, %s\n", input[print], input[print+1]);
		}
        }
	if (nothing==0) //ak sa nezvysila ani raz, nebol najdeny ziadny 'dobry' kontakt
		printf("Not found.\n");
	if (invalid_lines_count>0) //ak existuje neplatny riadok
	{
		for (unsigned i; i<LINES; i++) //vypis varovani pre neplatne riadky
		{
			if (invalid_line[i]==1)
				fprintf(stderr, "Warning. Line %d too long.\n", i+1);
		}
	}
	return 0;
}

/********************************   FUNCTION DEFINITIONS:  ***********************************/
int character_equality_check(char x, char y) //funkcia, porovnanie dvoch znakov
{
	unsigned r=0;
	switch(x) //switch, podla prveho vstupneho znaku prebieha kontrola druheho znaku
	{	
		case '1':
			if (y=='1')
				r=1;
			break;
		case '2':
			if (y=='2' || y=='a' || y=='A' || y=='b' || y=='B' || y=='c' || y=='C')
				r=1;
			break;
		case '3':
			if (y=='3' || y=='d' || y=='D' || y=='e' || y=='E' || y=='f' || y=='F')
				r=1;
			break;
		case '4':
			if (y=='4' || y=='g' || y=='G' || y=='h' || y=='H' || y=='i' || y=='I')
				r=1;
			break;
		case '5':
			if (y=='5' || y=='j' || y=='J' || y=='k' || y=='K' || y=='l' || y=='L')
				r=1;
			break;
		case '6':
			if (y=='6' || y=='m' || y=='M' || y=='n' || y=='N' || y=='o' || y=='O')
				r=1;
			break;
		case '7':
			if (y=='7' || y=='p' || y=='P' || y=='q' || y=='Q' || y=='r' || y=='R' || y=='s' || y=='S')
				r=1;
			break;
		case '8':
			if (y=='8' || y=='t' || y=='T' || y=='u' || y=='U' || y=='v' || y=='V')
				r=1;
			break;
		case '9':
			if (y=='9' || y=='w' || y=='W' || y=='x' || y=='X' || y=='y' || y=='Y' || y=='z' || y=='Z')
				r=1;
			break;
		case '0':
			if (y=='0' || y=='+')
				r=1;
			break;	
		default:
			break;
	}
	return r;
}
