
/* c206.c **********************************************************}
{* Téma: Dvousměrně vázaný lineární seznam
**
**                   Návrh a referenční implementace: Bohuslav Křena, říjen 2001
**                            Přepracované do jazyka C: Martin Tuček, říjen 2004
**                                            Úpravy: Kamil Jeřábek, září 2020
**
** Implementujte abstraktní datový typ dvousměrně vázaný lineární seznam.
** Užitečným obsahem prvku seznamu je hodnota typu int.
** Seznam bude jako datová abstrakce reprezentován proměnnou
** typu tDLList (DL znamená Double-Linked a slouží pro odlišení
** jmen konstant, typů a funkcí od jmen u jednosměrně vázaného lineárního
** seznamu). Definici konstant a typů naleznete v hlavičkovém souboru c206.h.
**
** Vaším úkolem je implementovat následující operace, které spolu
** s výše uvedenou datovou částí abstrakce tvoří abstraktní datový typ
** obousměrně vázaný lineární seznam:
**
**      DLInitList ...... inicializace seznamu před prvním použitím,
**      DLDisposeList ... zrušení všech prvků seznamu,
**      DLInsertFirst ... vložení prvku na začátek seznamu,
**      DLInsertLast .... vložení prvku na konec seznamu,
**      DLFirst ......... nastavení aktivity na první prvek,
**      DLLast .......... nastavení aktivity na poslední prvek,
**      DLCopyFirst ..... vrací hodnotu prvního prvku,
**      DLCopyLast ...... vrací hodnotu posledního prvku,
**      DLDeleteFirst ... zruší první prvek seznamu,
**      DLDeleteLast .... zruší poslední prvek seznamu,
**      DLPostDelete .... ruší prvek za aktivním prvkem,
**      DLPreDelete ..... ruší prvek před aktivním prvkem,
**      DLPostInsert .... vloží nový prvek za aktivní prvek seznamu,
**      DLPreInsert ..... vloží nový prvek před aktivní prvek seznamu,
**      DLCopy .......... vrací hodnotu aktivního prvku,
**      DLActualize ..... přepíše obsah aktivního prvku novou hodnotou,
**      DLPred .......... posune aktivitu na předchozí prvek seznamu,
**      DLSucc .......... posune aktivitu na další prvek seznamu,
**      DLActive ........ zjišťuje aktivitu seznamu.
**
** Při implementaci jednotlivých funkcí nevolejte žádnou z funkcí
** implementovaných v rámci tohoto příkladu, není-li u funkce
** explicitně uvedeno něco jiného.
**
** Nemusíte ošetřovat situaci, kdy místo legálního ukazatele na seznam 
** předá někdo jako parametr hodnotu NULL.
**
** Svou implementaci vhodně komentujte!
**
** Terminologická poznámka: Jazyk C nepoužívá pojem procedura.
** Proto zde používáme pojem funkce i pro operace, které by byly
** v algoritmickém jazyce Pascalovského typu implemenovány jako
** procedury (v jazyce C procedurám odpovídají funkce vracející typ void).
**/

#include "c206.h"

int solved;
int errflg;

void DLError() {
/*
** Vytiskne upozornění na to, že došlo k chybě.
** Tato funkce bude volána z některých dále implementovaných operací.
**/	
    printf ("*ERROR* The program has performed an illegal operation.\n");
    errflg = TRUE;             /* globální proměnná -- příznak ošetření chyby */
    return;
}

void DLInitList (tDLList *L) {
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
    L->Last = NULL;
}

void DLDisposeList (tDLList *L) {
/*
** Zruší všechny prvky seznamu L a uvede seznam do stavu, v jakém
** se nacházel po inicializaci. Rušené prvky seznamu budou korektně
** uvolněny voláním operace free. 
**/
    //loop over every element of the list - until the pointer to the next one is NULL
    while(L->First != NULL){
        tDLElemPtr next = L->First->rptr; //save pointer to the next item in a variable
        free(L->First); //free current item
        L->First = next; //set next item as current item
    }
    L->Act = NULL; //set pointer to active item to NULL
    L->Last = NULL; //set pointer to last item to NULL
}

void DLInsertFirst (tDLList *L, int val) {
/*
** Vloží nový prvek na začátek seznamu L.
** V případě, že není dostatek paměti pro nový prvek při operaci malloc,
** volá funkci DLError().
**/
    tDLElemPtr old_first = L->First; //save pointer to the first item in a variable
    tDLElemPtr new = malloc(sizeof(struct tDLElem)); //allocate memory for new item
    //check for allocation error, if occurs call DLError function
    if (new == NULL) {
        DLError();
    }
    else {
        L->First = new; //set pointer to allocated memory as a pointer to first item
        L->First->data = val; //set value of the new first item
        L->First->rptr = old_first; //set old first item as next (second) item
        L->First->lptr = NULL; //set pointer to the item to the left as NULL (it is the first item)
        //if list was not empty, former first item is not NULL
        if(old_first != NULL){
            old_first->lptr = new; //set the new first item as an item to the left of the former first item
        }
        //else list was empty
        else {
            L->Last = new; //new first item is also the last item in the list
        }
    }
}

void DLInsertLast(tDLList *L, int val) {
/*
** Vloží nový prvek na konec seznamu L (symetrická operace k DLInsertFirst).
** V případě, že není dostatek paměti pro nový prvek při operaci malloc,
** volá funkci DLError().
**/
    tDLElemPtr old_last = L->Last; //save pointer to the last item in a variable
    tDLElemPtr new = malloc(sizeof(struct tDLElem)); //allocate memory for new item
    //check for allocation error, if occurs call DLError function
    if (new == NULL) {
        DLError();
    }
    else {
        L->Last = new; //set pointer to allocated memory as a pointer to last item
        L->Last->data = val; //set value of the new last item
        L->Last->lptr = old_last; //set old last item as the penultimate item
        L->Last->rptr = NULL; //set pointer to the item to the right as NULL (it is the last item)
        //if list was not empty, former last item is not NULL
        if (old_last != NULL) {
            old_last->rptr = new; // set the new last item as a pointer to the item to the right of the penultimate item
        }
        //else list was empty
        else {
            L->First = new; //new last item is also the first item in the list
        }
    }
}

void DLFirst (tDLList *L) {
/*
** Nastaví aktivitu na první prvek seznamu L.
** Funkci implementujte jako jediný příkaz (nepočítáme-li return),
** aniž byste testovali, zda je seznam L prázdný.
**/
    L->Act = L->First; //set activity to the first item
}

void DLLast (tDLList *L) {
/*
** Nastaví aktivitu na poslední prvek seznamu L.
** Funkci implementujte jako jediný příkaz (nepočítáme-li return),
** aniž byste testovali, zda je seznam L prázdný.
**/
    L->Act = L->Last; //set activity to the last item
}

void DLCopyFirst (tDLList *L, int *val) {
/*
** Prostřednictvím parametru val vrátí hodnotu prvního prvku seznamu L.
** Pokud je seznam L prázdný, volá funkci DLError().
**/
    //check if the list is empty (pointer to first item is NULL)
    if (L->First == NULL) {
        DLError(); //if empty call DLError func
    }
    else {
        *val = L->First->data; //else copy its value to variable val
    }
}

void DLCopyLast (tDLList *L, int *val) {
/*
** Prostřednictvím parametru val vrátí hodnotu posledního prvku seznamu L.
** Pokud je seznam L prázdný, volá funkci DLError().
**/
    //check if the list is empty (pointer to first item is NULL)
    if (L->First == NULL) {
        DLError(); //if empty call DLError func
    }
    else {
        *val = L->Last->data; //else copy value of the last item to variable val
    }
}

void DLDeleteFirst (tDLList *L) {
/*
** Zruší první prvek seznamu L. Pokud byl první prvek aktivní, aktivita 
** se ztrácí. Pokud byl seznam L prázdný, nic se neděje.
**/
    //if list is not empty
    if (L->First != NULL){
        //if the first item is active, cancel activity
        if (L->Act == L->First){
            L->Act = NULL;
        }
        tDLElemPtr second = L->First->rptr; //save pointer to second item in a variable
        free(L->First); //free (delete) first item
        L->First = second; //set former second item as first
        //if the new first item exists, is not NULL
        if (L->First != NULL){
            L->First->lptr = NULL; //set pointer to the left of the first item to NULL
        }
        //else list is now empty
        else {
            L->Last = NULL;
        }
    }
}

void DLDeleteLast (tDLList *L) {
/*
** Zruší poslední prvek seznamu L.
** Pokud byl poslední prvek aktivní, aktivita seznamu se ztrácí.
** Pokud byl seznam L prázdný, nic se neděje.
**/
    //if list is not empty
    if (L->First != NULL){
        //if the last item is active, cancel activity
        if (L->Act == L->Last){
            L->Act = NULL;
        }
        tDLElemPtr penultimate = L->Last->lptr; //save pointer to penultimate item in a variable
        free(L->Last); //free (delete) last item
        L->Last = penultimate; //set former penultimate item as last
        //if the new last item exists, is not NULL
        if (L->Last != NULL){
            L->Last->rptr = NULL; //set pointer to the right of the last item to NULL
        }
        //else list is now empty
        else {
            L->First = NULL;
        }
    }
}

void DLPostDelete (tDLList *L) {
/*
** Zruší prvek seznamu L za aktivním prvkem.
** Pokud je seznam L neaktivní nebo pokud je aktivní prvek
** posledním prvkem seznamu, nic se neděje.
**/
    //if there is an active item and its not the last one
    if (L->Act != NULL && L->Act->rptr != NULL){
        tDLElemPtr next = L->Act->rptr->rptr; //save pointer to the second item to the right of the active item in a variable
        free(L->Act->rptr); //free (delete) the item to the right of the active item
        L->Act->rptr = next; //connect the active item with the item that followed after the deleted one
        //if the item after the deleted one exists, is not NULL
        if (next != NULL){
            next->lptr = L->Act; //connect the item that followed after the deleted one with the active item
        }
        //else the deleted item was last in the list
        else {
            L->Last = L->Act; //the active item is now the last item
        }
    }
}

void DLPreDelete (tDLList *L) {
/*
** Zruší prvek před aktivním prvkem seznamu L .
** Pokud je seznam L neaktivní nebo pokud je aktivní prvek
** prvním prvkem seznamu, nic se neděje.
**/
    //if there is an active item and its not the first one
    if (L->Act != NULL && L->Act->lptr != NULL){
        tDLElemPtr previous = L->Act->lptr->lptr; //save pointer to the second item to the left of the active item in a variable
        free(L->Act->lptr); //free (delete) the item to the left of the active item
        L->Act->lptr = previous; //connect the active item with the item that that was to the left of the deleted one
        //if the item before the deleted one exists, is not NULL
        if (previous != NULL){
            previous->rptr = L->Act; //connect the item that was to the left of the deleted one with the active item
        }
        //else the deleted item was first in the list
        else {
            L->First = L->Act; //the active item is now the first item
        }
    }
}

void DLPostInsert (tDLList *L, int val) {
/*
** Vloží prvek za aktivní prvek seznamu L.
** Pokud nebyl seznam L aktivní, nic se neděje.
** V případě, že není dostatek paměti pro nový prvek při operaci malloc,
** volá funkci DLError().
**/
    //if there is an active item
    if (L->Act != NULL){
        tDLElemPtr next = L->Act->rptr; //save pointer to the item after the active one
        tDLElemPtr new = malloc(sizeof(struct tDLElem)); //allocate memory for a new item
        //check for allocation error, if occurs call DLError() func
        if (new == NULL){
            DLError();
        }
        else {
            L->Act->rptr = new; //insert new item after the active one
            new->rptr = next; //set the pointer to the item to the right of the newly inserted one
            new->lptr = L->Act; //set the pointer to the item to the left of the new one (the active one)
            new->data = val; //set the data parameter of the new item to the value of parameter val
            //if the item to the right of the active item does not exist (active one was last)
            if (next == NULL){
                L->Last = new; //set the the new item as the last item
            }
            else {
                next->lptr = new; //connect the item formerly to the right of the active item with the new item
            }
        }
    }
}

void DLPreInsert (tDLList *L, int val) {
/*
** Vloží prvek před aktivní prvek seznamu L.
** Pokud nebyl seznam L aktivní, nic se neděje.
** V případě, že není dostatek paměti pro nový prvek při operaci malloc,
** volá funkci DLError().
**/
    //if there is an active item
    if (L->Act != NULL){
        tDLElemPtr previous = L->Act->lptr; //save pointer to the item to the left of the active one
        tDLElemPtr new = malloc(sizeof(struct tDLElem)); //allocate memory for a new item
        //check for allocation error, if occurs call DLError() func
        if (new == NULL){
            DLError();
        }
        else {
            L->Act->lptr = new; //insert new item in front of the active one
            new->lptr = previous; //set the pointer to the item to the left of the newly inserted one
            new->rptr = L->Act; //set the pointer to the item to the right of the new one (the active one)
            new->data = val; //set the data parameter of the new item to the value of parameter val
            //if the item to the left of the active item does not exist (active one was first)
            if (previous == NULL){
                L->First = new; //set the the new item as the first item
            }
            else {
                previous->rptr = new; //connect the item formerly to the left of the active item with the new item
            }
        }
    }
}

void DLCopy (tDLList *L, int *val) {
/*
** Prostřednictvím parametru val vrátí hodnotu aktivního prvku seznamu L.
** Pokud seznam L není aktivní, volá funkci DLError ().
**/
    //if there is no active item, call DLError() func
    if (L->Act == NULL){
        DLError();
    }
        //else copy its value to the memory pointed to by parameter val
    else {
        *val = L->Act->data;
    }
}

void DLActualize (tDLList *L, int val) {
/*
** Přepíše obsah aktivního prvku seznamu L.
** Pokud seznam L není aktivní, nedělá nic.
**/
    //if list is active
    if (L->Act != NULL){
        L->Act->data = val; //set new value of the active item to the value of param val
    }
}

void DLSucc (tDLList *L) {
/*
** Posune aktivitu na následující prvek seznamu L.
** Není-li seznam aktivní, nedělá nic.
** Všimněte si, že při aktivitě na posledním prvku se seznam stane neaktivním.
**/
    //if list is active
    if (L->Act != NULL){
        L->Act = L->Act->rptr; //move activity to the next item
    }
}


void DLPred (tDLList *L) {
/*
** Posune aktivitu na předchozí prvek seznamu L.
** Není-li seznam aktivní, nedělá nic.
** Všimněte si, že při aktivitě na prvním prvku se seznam stane neaktivním.
**/
    //if list is active
    if (L->Act != NULL){
        L->Act = L->Act->lptr; //move activity to the previous item
    }
}

int DLActive (tDLList *L) {
/*
** Je-li seznam L aktivní, vrací nenulovou hodnotu, jinak vrací 0.
** Funkci je vhodné implementovat jedním příkazem return.
**/
    //return true if list is active else return false
    return (L->Act != NULL);
}

/* Konec c206.c*/
