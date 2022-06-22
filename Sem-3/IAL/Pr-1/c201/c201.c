
/* c201.c *********************************************************************}
{* Téma: Jednosměrný lineární seznam
**
**                     Návrh a referenční implementace: Petr Přikryl, říjen 1994
**                                          Úpravy: Andrea Němcová listopad 1996
**                                                   Petr Přikryl, listopad 1997
**                                Přepracované zadání: Petr Přikryl, březen 1998
**                                  Přepis do jazyka C: Martin Tuček, říjen 2004
**                                              Úpravy: Kamil Jeřábek, září 2020
**
** Implementujte abstraktní datový typ jednosměrný lineární seznam.
** Užitečným obsahem prvku seznamu je celé číslo typu int.
** Seznam bude jako datová abstrakce reprezentován proměnnou typu tList.
** Definici konstant a typů naleznete v hlavičkovém souboru c201.h.
**
** Vaším úkolem je implementovat následující operace, které spolu s výše
** uvedenou datovou částí abstrakce tvoří abstraktní datový typ tList:
**
**      DisposeList ... zrušení všech prvků seznamu,
**      InitList ...... inicializace seznamu před prvním použitím,
**      InsertFirst ... vložení prvku na začátek seznamu,
**      First ......... nastavení aktivity na první prvek,
**      CopyFirst ..... vrací hodnotu prvního prvku,
**      DeleteFirst ... zruší první prvek seznamu,
**      PostDelete .... ruší prvek za aktivním prvkem,
**      PostInsert .... vloží nový prvek za aktivní prvek seznamu,
**      Copy .......... vrací hodnotu aktivního prvku,
**      Actualize ..... přepíše obsah aktivního prvku novou hodnotou,
**      Succ .......... posune aktivitu na další prvek seznamu,
**      Active ........ zjišťuje aktivitu seznamu.
**
** Při implementaci funkcí nevolejte žádnou z funkcí implementovaných v rámci
** tohoto příkladu, není-li u dané funkce explicitně uvedeno něco jiného.
**
** Nemusíte ošetřovat situaci, kdy místo legálního ukazatele na seznam předá
** někdo jako parametr hodnotu NULL.
**
** Svou implementaci vhodně komentujte!
**
** Terminologická poznámka: Jazyk C nepoužívá pojem procedura.
** Proto zde používáme pojem funkce i pro operace, které by byly
** v algoritmickém jazyce Pascalovského typu implemenovány jako
** procedury (v jazyce C procedurám odpovídají funkce vracející typ void).
**/

#include "c201.h"

int errflg;
int solved;

void Error() {
/*
** Vytiskne upozornění na to, že došlo k chybě.
** Tato funkce bude volána z některých dále implementovaných operací.
**/
    printf ("*ERROR* The program has performed an illegal operation.\n");
    errflg = TRUE;                      /* globální proměnná -- příznak chyby */
}

void InitList (tList *L) {
/*
** Provede inicializaci seznamu L před jeho prvním použitím (tzn. žádná
** z následujících funkcí nebude volána nad neinicializovaným seznamem).
** Tato inicializace se nikdy nebude provádět nad již inicializovaným
** seznamem, a proto tuto možnost neošetřujte. Vždy předpokládejte,
** že neinicializované proměnné mají nedefinovanou hodnotu.
**/
    //initialize pointers to NULL
    L->Act = NULL;
    L->First = NULL;
}

void DisposeList (tList *L) {
/*
** Zruší všechny prvky seznamu L a uvede seznam L do stavu, v jakém se nacházel
** po inicializaci. Veškerá paměť používaná prvky seznamu L bude korektně
** uvolněna voláním operace free.
***/
    //loop over every element of the list - until the pointer to the next one is NULL
	while(L->First != NULL){
        tElemPtr next = L->First->ptr; //save pointer to the next item in a variable
        free(L->First); //free current item
        L->First = next; //set next item as current item
	}
	L->Act = NULL; //set pointer to active item to NULL
}

void InsertFirst (tList *L, int val) {
/*
** Vloží prvek s hodnotou val na začátek seznamu L.
** V případě, že není dostatek paměti pro nový prvek při operaci malloc,
** volá funkci Error().
**/
    tElemPtr next = L->First; //save pointer to the first item in a variable
    tElemPtr new = malloc(sizeof(struct tElem)); //allocate memory for new item
    //check for allocation error, if occurs call Error function
    if (new == NULL) {
        Error();
    }
    else {
        L->First = new; //set pointer to allocated memory as a pointer to first item
        L->First->data = val; //set value of the new first item
        L->First->ptr = next; //set old first item as next (second) item
    }
}

void First (tList *L) {
/*
** Nastaví aktivitu seznamu L na jeho první prvek.
** Funkci implementujte jako jediný příkaz, aniž byste testovali,
** zda je seznam L prázdný.
**/
    L->Act = L->First; //set activity on the first item
}

void CopyFirst (tList *L, int *val) {
/*
** Prostřednictvím parametru val vrátí hodnotu prvního prvku seznamu L.
** Pokud je seznam L prázdný, volá funkci Error().
**/
    //check if the list is empty (pointer to first item is NULL)
    if (L->First == NULL) {
        Error(); //if empty call Error func
    }
    else {
        *val = L->First->data; //else copy its value to variable val
    }
}

void DeleteFirst (tList *L) {
/*
** Zruší první prvek seznamu L a uvolní jím používanou paměť.
** Pokud byl rušený prvek aktivní, aktivita seznamu se ztrácí.
** Pokud byl seznam L prázdný, nic se neděje.
**/
    //if list is not empty
	if (L->First != NULL){
	    //if the first item is active, cancel activity
	    if (L->Act == L->First){
	        L->Act = NULL;
	    }
	    tElemPtr second = L->First->ptr; //save pointer to next item in a variable
        free(L->First); //free (delete) first item
        L->First = second; //set former second item as first
	}
}

void PostDelete (tList *L) {
/* 
** Zruší prvek seznamu L za aktivním prvkem a uvolní jím používanou paměť.
** Pokud není seznam L aktivní nebo pokud je aktivní poslední prvek seznamu L,
** nic se neděje.
**/
    //if there is an active item and its not the last one
	if (L->Act != NULL && L->Act->ptr != NULL){
	    tElemPtr next = L->Act->ptr->ptr; //save pointer to the second item after the active item in a variable
        free(L->Act->ptr); //free (delete) item after the active item
        L->Act->ptr = next; //connect the active item with the item that followed after the deleted one
	}
}

void PostInsert (tList *L, int val) {
/*
** Vloží prvek s hodnotou val za aktivní prvek seznamu L.
** Pokud nebyl seznam L aktivní, nic se neděje!
** V případě, že není dostatek paměti pro nový prvek při operaci malloc,
** zavolá funkci Error().
**/
    //if there is an active item
	if (L->Act != NULL){
        tElemPtr next = L->Act->ptr; //save pointer to the item after the active one
        tElemPtr new = malloc(sizeof(struct tElem)); //allocate memory for a new item
        //check for allocation error, if occurs call Error() func
        if (new == NULL){
            Error();
        }
        else {
            L->Act->ptr = new; //insert new item after the active one
            new->ptr = next; //set the next item after the newly inserted one
            new->data = val; //set the data parameter of the new item to the value of parameter val
        }
	}
}

void Copy (tList *L, int *val) {
/*
** Prostřednictvím parametru val vrátí hodnotu aktivního prvku seznamu L.
** Pokud seznam není aktivní, zavolá funkci Error().
**/
    //if there is no active item, call Error() func
    if (L->Act == NULL){
        Error();
    }
    //else copy its value to the memory pointed to by parameter val
    else {
        *val = L->Act->data;
    }
}

void Actualize (tList *L, int val) {
/*
** Přepíše data aktivního prvku seznamu L hodnotou val.
** Pokud seznam L není aktivní, nedělá nic!
**/
    //if list is active
	if (L->Act != NULL){
	    L->Act->data = val; //set new value of the active item to the value of param val
	}
}

void Succ (tList *L) {
/*
** Posune aktivitu na následující prvek seznamu L.
** Všimněte si, že touto operací se může aktivní seznam stát neaktivním.
** Pokud není předaný seznam L aktivní, nedělá funkce nic.
**/
    //if list is active
	if (L->Act != NULL){
	    L->Act = L->Act->ptr; //move activity to the next item
	}
}

int Active (tList *L) {
/*
** Je-li seznam L aktivní, vrací nenulovou hodnotu, jinak vrací 0.
** Tuto funkci je vhodné implementovat jedním příkazem return. 
**/
    //return true if list is active else return false
    return (L->Act != NULL);
}

/* Konec c201.c */
