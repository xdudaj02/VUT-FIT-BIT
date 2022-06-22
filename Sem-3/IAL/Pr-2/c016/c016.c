
/* c016.c: **********************************************************}
{* Téma:  Tabulka s Rozptýlenými Položkami
**                      První implementace: Petr Přikryl, prosinec 1994
**                      Do jazyka C prepsal a upravil: Vaclav Topinka, 2005
**                      Úpravy: Karel Masařík, říjen 2014
**                              Radek Hranický, 2014-2018
**
** Vytvořete abstraktní datový typ
** TRP (Tabulka s Rozptýlenými Položkami = Hash table)
** s explicitně řetězenými synonymy. Tabulka je implementována polem
** lineárních seznamů synonym.
**
** Implementujte následující procedury a funkce.
**
**  HTInit ....... inicializuje tabulku před prvním použitím
**  HTInsert ..... vložení prvku
**  HTSearch ..... zjištění přítomnosti prvku v tabulce
**  HTDelete ..... zrušení prvku
**  HTRead ....... přečtení hodnoty prvku
**  HTClearAll ... zrušení obsahu celé tabulky (inicializace tabulky
**                 poté, co již byla použita)
**
** Definici typů naleznete v souboru c016.h.
**
** Tabulka je reprezentována datovou strukturou typu tHTable,
** která se skládá z ukazatelů na položky, jež obsahují složky
** klíče 'key', obsahu 'data' (pro jednoduchost typu float), a
** ukazatele na další synonymum 'ptrnext'. Při implementaci funkcí
** uvažujte maximální rozměr pole HTSIZE.
**
** U všech procedur využívejte rozptylovou funkci hashCode.  Povšimněte si
** způsobu předávání parametrů a zamyslete se nad tím, zda je možné parametry
** předávat jiným způsobem (hodnotou/odkazem) a v případě, že jsou obě
** možnosti funkčně přípustné, jaké jsou výhody či nevýhody toho či onoho
** způsobu.
**
** V příkladech jsou použity položky, kde klíčem je řetězec, ke kterému
** je přidán obsah - reálné číslo.
*/

#include "c016.h"

int HTSIZE = MAX_HTSIZE;
int solved;

/*          -------
** Rozptylovací funkce - jejím úkolem je zpracovat zadaný klíč a přidělit
** mu index v rozmezí 0..HTSize-1.  V ideálním případě by mělo dojít
** k rovnoměrnému rozptýlení těchto klíčů po celé tabulce.  V rámci
** pokusů se můžete zamyslet nad kvalitou této funkce.  (Funkce nebyla
** volena s ohledem na maximální kvalitu výsledku). }
*/

int hashCode ( tKey key ) {
	int retval = 1;
	int keylen = strlen(key);
	for ( int i=0; i<keylen; i++ )
		retval += key[i];
	return ( retval % HTSIZE );
}

/*
** Inicializace tabulky s explicitně zřetězenými synonymy.  Tato procedura
** se volá pouze před prvním použitím tabulky.
*/

void htInit ( tHTable* ptrht ) {
    // initialize all item pointers in the table to NULL
    for (int i = 0; i < HTSIZE; i++){
        (*ptrht)[i] = NULL;
    }
}

/* TRP s explicitně zřetězenými synonymy.
** Vyhledání prvku v TRP ptrht podle zadaného klíče key.  Pokud je
** daný prvek nalezen, vrací se ukazatel na daný prvek. Pokud prvek nalezen není,
** vrací se hodnota NULL.
**
*/

tHTItem* htSearch ( tHTable* ptrht, tKey key ) {
    tHTItem* searched_item = (*ptrht)[hashCode(key)]; //item at index determined by hashed key
    //loop over items until item with the searched key is found or the end of the list of synonyms
    while (searched_item != NULL && searched_item->key != key){
        searched_item = searched_item->ptrnext;
    }
    return searched_item;
}

/*
** TRP s explicitně zřetězenými synonymy.
** Tato procedura vkládá do tabulky ptrht položku s klíčem key a s daty
** data.  Protože jde o vyhledávací tabulku, nemůže být prvek se stejným
** klíčem uložen v tabulce více než jedenkrát.  Pokud se vkládá prvek,
** jehož klíč se již v tabulce nachází, aktualizujte jeho datovou část.
**
** Využijte dříve vytvořenou funkci htSearch.  Při vkládání nového
** prvku do seznamu synonym použijte co nejefektivnější způsob,
** tedy proveďte.vložení prvku na začátek seznamu.
**/

void htInsert ( tHTable* ptrht, tKey key, tData data ) {
    tHTItem* searched_item = htSearch(ptrht, key); //tries to find item with given key
    // if item exists, change its data
    if (searched_item != NULL){
        searched_item->data = data;
    }
    //if item does not already exist
    else {
        tHTItem* new_item = malloc(sizeof(tHTItem)); //allocate new item
        tHTItem* next_item = (*ptrht)[hashCode(key)]; //save pointer to former first item in the list of synonyms
        (*ptrht)[hashCode(key)] = new_item; //insert at the index determined by hashed key
        new_item->ptrnext = next_item; //at the beginning of the list of synonyms
        new_item->key = key; //set key
        new_item->data = data; //set data
    }
}

/*
** TRP s explicitně zřetězenými synonymy.
** Tato funkce zjišťuje hodnotu datové části položky zadané klíčem.
** Pokud je položka nalezena, vrací funkce ukazatel na položku
** Pokud položka nalezena nebyla, vrací se funkční hodnota NULL
**
** Využijte dříve vytvořenou funkci HTSearch.
*/

tData* htRead ( tHTable* ptrht, tKey key ) {
    tHTItem* searched_item = htSearch(ptrht, key); //tries to search for item with given key
    tData* data = NULL; //set returned value to NULL by default
    if (searched_item != NULL){ //if found
        data = &searched_item->data; //set returned value to pointer to the found data
    }
    return data;
}

/*
** TRP s explicitně zřetězenými synonymy.
** Tato procedura vyjme položku s klíčem key z tabulky
** ptrht.  Uvolněnou položku korektně zrušte.  Pokud položka s uvedeným
** klíčem neexistuje, dělejte, jako kdyby se nic nestalo (tj. nedělejte
** nic).
**
** V tomto případě NEVYUŽÍVEJTE dříve vytvořenou funkci HTSearch.
*/

void htDelete ( tHTable* ptrht, tKey key ) {
    tHTItem* searched_item = (*ptrht)[hashCode(key)]; //item to be deleted, at first pointer to the beginning of the list of synonyms
    tHTItem* previous_item = (*ptrht)[hashCode(key)]; //item before the one to be deleted
    int first = 1; //signals if item to be deleted was first in list, 1 by default
    while (searched_item != NULL) { //while not end of list of synonyms
        if (searched_item->key != key) { //if not the correct item
            first = 0; //searched item is not first in list of synonyms
            previous_item = searched_item; //set current item as previous
            searched_item = searched_item->ptrnext; //move current item pointer to next item
        }
        else { // if correct item found
            tHTItem *next_item = searched_item->ptrnext; //save pointer to the next item
            free(searched_item); //free item to be deleted
            // connect items around the deleted item (or table with new first item)
            if (first){
                (*ptrht)[hashCode(key)] = next_item;
            }
            else {
                previous_item->ptrnext = next_item;
            }
            break;
        }
    }
}

/* TRP s explicitně zřetězenými synonymy.
** Tato procedura zruší všechny položky tabulky, korektně uvolní prostor,
** který tyto položky zabíraly, a uvede tabulku do počátečního stavu.
*/

void htClearAll ( tHTable* ptrht ) {
    //loop over all indexes in table
    for (int i = 0; i < HTSIZE; i++){
        //loop over the whole length of the list of synonyms
        while ((*ptrht)[i] != NULL) {
            tHTItem* next = ((*ptrht)[i])->ptrnext; //save pointer to next item
            free((*ptrht)[i]); //free current item
            (*ptrht)[i] = next; //set pointer to next item as new current item
        }
    }
}