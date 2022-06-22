
/* c401.c: **********************************************************}
{* Téma: Rekurzivní implementace operací nad BVS
**                                         Vytvořil: Petr Přikryl, listopad 1994
**                                         Úpravy: Andrea Němcová, prosinec 1995
**                                                      Petr Přikryl, duben 1996
**                                                   Petr Přikryl, listopad 1997
**                                  Převod do jazyka C: Martin Tuček, říjen 2005
**                                         Úpravy: Bohuslav Křena, listopad 2009
**                                                 Karel Masařík, říjen 2013
**                                                 Radek Hranický 2014-2018
**
** Implementujte rekurzivním způsobem operace nad binárním vyhledávacím
** stromem (BVS; v angličtině BST - Binary Search Tree).
**
** Klíčem uzlu stromu je jeden znak (obecně jím může být cokoliv, podle
** čeho se vyhledává). Užitečným (vyhledávaným) obsahem je zde integer.
** Uzly s menším klíčem leží vlevo, uzly s větším klíčem leží ve stromu
** vpravo. Využijte dynamického přidělování paměti.
** Rekurzivním způsobem implementujte následující funkce:
**
**   BSTInit ...... inicializace vyhledávacího stromu
**   BSTSearch .... vyhledávání hodnoty uzlu zadaného klíčem
**   BSTInsert .... vkládání nové hodnoty
**   BSTDelete .... zrušení uzlu se zadaným klíčem
**   BSTDispose ... zrušení celého stromu
**
** ADT BVS je reprezentován kořenovým ukazatelem stromu (typ tBSTNodePtr).
** Uzel stromu (struktura typu tBSTNode) obsahuje klíč (typu char), podle
** kterého se ve stromu vyhledává, vlastní obsah uzlu (pro jednoduchost
** typu int) a ukazatel na levý a pravý podstrom (LPtr a RPtr). Přesnou definici typů
** naleznete v souboru c401.h.
**
** Pozor! Je třeba správně rozlišovat, kdy použít dereferenční operátor *
** (typicky při modifikaci) a kdy budeme pracovat pouze se samotným ukazatelem
** (např. při vyhledávání). V tomto příkladu vám napoví prototypy funkcí.
** Pokud pracujeme s ukazatelem na ukazatel, použijeme dereferenci.
**/

#include "c401.h"
int solved;

void BSTInit (tBSTNodePtr *RootPtr) {
/*   -------
** Funkce provede počáteční inicializaci stromu před jeho prvním použitím.
**
** Ověřit, zda byl již strom předaný přes RootPtr inicializován, nelze,
** protože před první inicializací má ukazatel nedefinovanou (tedy libovolnou)
** hodnotu. Programátor využívající ADT BVS tedy musí zajistit, aby inicializace
** byla volána pouze jednou, a to před vlastní prací s BVS. Provedení
** inicializace nad neprázdným stromem by totiž mohlo vést ke ztrátě přístupu
** k dynamicky alokované paměti (tzv. "memory leak").
**
** Všimněte si, že se v hlavičce objevuje typ ukazatel na ukazatel.
** Proto je třeba při přiřazení přes RootPtr použít dereferenční operátor *.
** Ten bude použit i ve funkcích BSTDelete, BSTInsert a BSTDispose.
**/
    *RootPtr = NULL; //initialize root pointer to null
}

int BSTSearch (tBSTNodePtr RootPtr, char K, int *Content)	{
/*  ---------
** Funkce vyhledá uzel v BVS s klíčem K.
**
** Pokud je takový nalezen, vrací funkce hodnotu TRUE a v proměnné Content se
** vrací obsah příslušného uzlu.´Pokud příslušný uzel není nalezen, vrací funkce
** hodnotu FALSE a obsah proměnné Content není definován (nic do ní proto
** nepřiřazujte).
**
** Při vyhledávání v binárním stromu bychom typicky použili cyklus ukončený
** testem dosažení listu nebo nalezení uzlu s klíčem K. V tomto případě ale
** problém řešte rekurzivním volání této funkce, přičemž nedeklarujte žádnou
** pomocnou funkci.
**/
    int retval = FALSE; //value to be returned (if found), false by default
    if (RootPtr != NULL){ //if tree not empty
        if (RootPtr->Key == K){ //if found item with the right key
            *Content = RootPtr->BSTNodeCont; //return item content in variable *Content
            return TRUE; //return true
        }
        else { //if item not found
            retval = BSTSearch(RootPtr->LPtr, K, Content); //recursively call this function with left child
            if (!retval){ //if item not found (in left subtree)
                retval = BSTSearch(RootPtr->RPtr, K, Content); //recursively call this function with right child
            }
        }
    }
    return retval;
}


void BSTInsert (tBSTNodePtr* RootPtr, char K, int Content)	{
/*   ---------
** Vloží do stromu RootPtr hodnotu Content s klíčem K.
**
** Pokud již uzel se zadaným klíčem ve stromu existuje, bude obsah uzlu
** s klíčem K nahrazen novou hodnotou. Pokud bude do stromu vložen nový
** uzel, bude vložen vždy jako list stromu.
**
** Funkci implementujte rekurzivně. Nedeklarujte žádnou pomocnou funkci.
**
** Rekurzivní implementace je méně efektivní, protože se při každém
** rekurzivním zanoření ukládá na zásobník obsah uzlu (zde integer).
** Nerekurzivní varianta by v tomto případě byla efektivnější jak z hlediska
** rychlosti, tak z hlediska paměťových nároků. Zde jde ale o školní
** příklad, na kterém si chceme ukázat eleganci rekurzivního zápisu.
**/
    if (*RootPtr == NULL){ //if current item is NULL (end of branch reached)
        tBSTNodePtr new = malloc(sizeof(struct tBSTNode)); //allocate memory for a new item
        *RootPtr = new; //set root pointer to point to the new item
        //set item key, content, pointers
        (*RootPtr)->Key = K;
        (*RootPtr)->BSTNodeCont = Content;
        (*RootPtr)->LPtr = NULL;
        (*RootPtr)->RPtr = NULL;
    }
    else { // if current item not NULL
        if ((*RootPtr)->Key > K){ //if new item has smaller key
            BSTInsert(&(*RootPtr)->LPtr, K, Content); //recursively call this func with left child
        }
        else if ((*RootPtr)->Key == K){ //if found item with the same key
            (*RootPtr)->BSTNodeCont = Content; //rewrite content
        }
        else if ((*RootPtr)->Key < K){ //if new item has bigger key
            BSTInsert(&(*RootPtr)->RPtr, K, Content); //recursively call this func with right child
        }
    }
}

void ReplaceByRightmost (tBSTNodePtr PtrReplaced, tBSTNodePtr *RootPtr) {
/*   ------------------
** Pomocná funkce pro vyhledání, přesun a uvolnění nejpravějšího uzlu.
**
** Ukazatel PtrReplaced ukazuje na uzel, do kterého bude přesunuta hodnota
** nejpravějšího uzlu v podstromu, který je určen ukazatelem RootPtr.
** Předpokládá se, že hodnota ukazatele RootPtr nebude NULL (zajistěte to
** testováním před volání této funkce). Tuto funkci implementujte rekurzivně.
**
** Tato pomocná funkce bude použita dále. Než ji začnete implementovat,
** přečtěte si komentář k funkci BSTDelete().
**/
    if ((*RootPtr)->RPtr != NULL){ //if current item has a right child
        ReplaceByRightmost(PtrReplaced, &(*RootPtr)->RPtr); //recursively call this func with the right child
    }
    else { //if current item does not have a right child => current item is the rightmost item
        //replace the item which is to be replaced with the rightmost item
        PtrReplaced->Key = (*RootPtr)->Key; //set new key
        PtrReplaced->BSTNodeCont = (*RootPtr)->BSTNodeCont; //set new content
        tBSTNodePtr tmp = (*RootPtr)->LPtr; //save old pointer to left child of the rightmost item
        free(*RootPtr); //free the rightmost item
        *RootPtr = tmp; //connect the left child of the rightmost item that was deleted with its parent
    }
}

void BSTDelete (tBSTNodePtr *RootPtr, char K) 		{
/*   ---------
** Zruší uzel stromu, který obsahuje klíč K.
**
** Pokud uzel se zadaným klíčem neexistuje, nedělá funkce nic.
** Pokud má rušený uzel jen jeden podstrom, pak jej zdědí otec rušeného uzlu.
** Pokud má rušený uzel oba podstromy, pak je rušený uzel nahrazen nejpravějším
** uzlem levého podstromu. Pozor! Nejpravější uzel nemusí být listem.
**
** Tuto funkci implementujte rekurzivně s využitím dříve deklarované
** pomocné funkce ReplaceByRightmost.
**/
    if (*RootPtr != NULL){ //if current item is not NULL
        if ((*RootPtr)->Key != K) { //if current item is not the one
            BSTDelete(&(*RootPtr)->LPtr, K); //recursively call this func with the left child
            BSTDelete(&(*RootPtr)->RPtr, K); //recursively call this func with the right child
        }
        else { //if item with the searched key is found
            tBSTNodePtr tmp = *RootPtr; //pointer to the item to be deleted (used for not losing pointers to children)
            if (tmp->RPtr != NULL && tmp->LPtr != NULL){ //if item has both children
                ReplaceByRightmost(tmp, &tmp->LPtr); //call func to delete item and replace it with the rightmost item of left subtree
            }
            else if (tmp->RPtr != NULL){ //if item has right child
                *RootPtr = tmp->RPtr; //replace item with its right child
                free(tmp); //delete item
            }
            else { //if item has left child or no children
                *RootPtr = tmp->LPtr; //replace item with its left child (may be NULL)
                free(tmp); //delete item
            }
        }
    }
}

void BSTDispose (tBSTNodePtr *RootPtr) {
/*   ----------
** Zruší celý binární vyhledávací strom a korektně uvolní paměť.
**
** Po zrušení se bude BVS nacházet ve stejném stavu, jako se nacházel po
** inicializaci. Tuto funkci implementujte rekurzivně bez deklarování pomocné
** funkce.
**/
	if (*RootPtr != NULL){ //if current item is not NULL
	    BSTDispose(&(*RootPtr)->LPtr); //recursively call this func with the left child
        BSTDispose(&(*RootPtr)->RPtr); //recursively call this func with the right child
        free(*RootPtr); //delete item (leaf)
        *RootPtr = NULL; //set pointer to child to NULL
	}
}

/* konec c401.c */

