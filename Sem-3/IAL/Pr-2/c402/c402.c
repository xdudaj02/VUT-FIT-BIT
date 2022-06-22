
/* c402.c: ********************************************************************}
{* Téma: Nerekurzivní implementace operací nad BVS
**                                     Implementace: Petr Přikryl, prosinec 1994
**                                           Úpravy: Petr Přikryl, listopad 1997
**                                                     Petr Přikryl, květen 1998
**			  	                        Převod do jazyka C: Martin Tuček, srpen 2005
**                                         Úpravy: Bohuslav Křena, listopad 2009
**                                                 Karel Masařík, říjen 2013
**                                                 Radek Hranický 2014-2018
**
** S využitím dynamického přidělování paměti, implementujte NEREKURZIVNĚ
** následující operace nad binárním vyhledávacím stromem (předpona BT znamená
** Binary Tree a je u identifikátorů uvedena kvůli možné kolizi s ostatními
** příklady):
**
**     BTInit .......... inicializace stromu
**     BTInsert ........ nerekurzivní vložení nového uzlu do stromu
**     BTPreorder ...... nerekurzivní průchod typu pre-order
**     BTInorder ....... nerekurzivní průchod typu in-order
**     BTPostorder ..... nerekurzivní průchod typu post-order
**     BTDisposeTree ... zruš všechny uzly stromu
**
** U všech funkcí, které využívají některý z průchodů stromem, implementujte
** pomocnou funkci pro nalezení nejlevějšího uzlu v podstromu.
**
** Přesné definice typů naleznete v souboru c402.h. Uzel stromu je typu tBTNode,
** ukazatel na něj je typu tBTNodePtr. Jeden uzel obsahuje položku int Cont,
** která současně slouží jako užitečný obsah i jako vyhledávací klíč
** a ukazatele na levý a pravý podstrom (LPtr a RPtr).
**
** Příklad slouží zejména k procvičení nerekurzivních zápisů algoritmů
** nad stromy. Než začnete tento příklad řešit, prostudujte si důkladně
** principy převodu rekurzivních algoritmů na nerekurzivní. Programování
** je především inženýrská disciplína, kde opětné objevování Ameriky nemá
** místo. Pokud se Vám zdá, že by něco šlo zapsat optimálněji, promyslete
** si všechny detaily Vašeho řešení. Povšimněte si typického umístění akcí
** pro různé typy průchodů. Zamyslete se nad modifikací řešených algoritmů
** například pro výpočet počtu uzlů stromu, počtu listů stromu, výšky stromu
** nebo pro vytvoření zrcadlového obrazu stromu (pouze popřehazování ukazatelů
** bez vytváření nových uzlů a rušení starých).
**
** Při průchodech stromem použijte ke zpracování uzlu funkci BTWorkOut().
** Pro zjednodušení práce máte předem připraveny zásobníky pro hodnoty typu
** bool a tBTNodePtr. Pomocnou funkci BTWorkOut ani funkce pro práci
** s pomocnými zásobníky neupravujte
** Pozor! Je třeba správně rozlišovat, kdy použít dereferenční operátor *
** (typicky při modifikaci) a kdy budeme pracovat pouze se samotným ukazatelem
** (např. při vyhledávání). V tomto příkladu vám napoví prototypy funkcí.
** Pokud pracujeme s ukazatelem na ukazatel, použijeme dereferenci.
**/

#include "c402.h"
int solved;

void BTWorkOut (tBTNodePtr Ptr)		{
/*   ---------
** Pomocná funkce, kterou budete volat při průchodech stromem pro zpracování
** uzlu určeného ukazatelem Ptr. Tuto funkci neupravujte.
**/

	if (Ptr==NULL)
    printf("Chyba: Funkce BTWorkOut byla volána s NULL argumentem!\n");
  else
    printf("Výpis hodnoty daného uzlu> %d\n",Ptr->Cont);
}

/* -------------------------------------------------------------------------- */
/*
** Funkce pro zásobník hotnot typu tBTNodePtr. Tyto funkce neupravujte.
**/

void SInitP (tStackP *S)
/*   ------
** Inicializace zásobníku.
**/
{
	S->top = 0;
}

void SPushP (tStackP *S, tBTNodePtr ptr)
/*   ------
** Vloží hodnotu na vrchol zásobníku.
**/
{
                 /* Při implementaci v poli může dojít k přetečení zásobníku. */
  if (S->top==MAXSTACK)
    printf("Chyba: Došlo k přetečení zásobníku s ukazateli!\n");
  else {
		S->top++;
		S->a[S->top]=ptr;
	}
}

tBTNodePtr STopPopP (tStackP *S)
/*         --------
** Odstraní prvek z vrcholu zásobníku a současně vrátí jeho hodnotu.
**/
{
                            /* Operace nad prázdným zásobníkem způsobí chybu. */
	if (S->top==0)  {
		printf("Chyba: Došlo k podtečení zásobníku s ukazateli!\n");
		return(NULL);
	}
	else {
		return (S->a[S->top--]);
	}
}

bool SEmptyP (tStackP *S)
/*   -------
** Je-li zásobník prázdný, vrátí hodnotu true.
**/
{
  return(S->top==0);
}

/* -------------------------------------------------------------------------- */
/*
** Funkce pro zásobník hotnot typu bool. Tyto funkce neupravujte.
*/

void SInitB (tStackB *S) {
/*   ------
** Inicializace zásobníku.
**/

	S->top = 0;
}

void SPushB (tStackB *S,bool val) {
/*   ------
** Vloží hodnotu na vrchol zásobníku.
**/
                 /* Při implementaci v poli může dojít k přetečení zásobníku. */
	if (S->top==MAXSTACK)
		printf("Chyba: Došlo k přetečení zásobníku pro boolean!\n");
	else {
		S->top++;
		S->a[S->top]=val;
	}
}

bool STopPopB (tStackB *S) {
/*   --------
** Odstraní prvek z vrcholu zásobníku a současně vrátí jeho hodnotu.
**/
                            /* Operace nad prázdným zásobníkem způsobí chybu. */
	if (S->top==0) {
		printf("Chyba: Došlo k podtečení zásobníku pro boolean!\n");
		return(NULL);
	}
	else {
		return(S->a[S->top--]);
	}
}

bool SEmptyB (tStackB *S) {
/*   -------
** Je-li zásobník prázdný, vrátí hodnotu true.
**/
  return(S->top==0);
}

/* -------------------------------------------------------------------------- */
/*
** Následuje jádro domácí úlohy - funkce, které máte implementovat.
*/

void BTInit (tBTNodePtr *RootPtr)	{
/*   ------
** Provede inicializaci binárního vyhledávacího stromu.
**
** Inicializaci smí programátor volat pouze před prvním použitím binárního
** stromu, protože neuvolňuje uzly neprázdného stromu (a ani to dělat nemůže,
** protože před inicializací jsou hodnoty nedefinované, tedy libovolné).
** Ke zrušení binárního stromu slouží procedura BTDisposeTree.
**
** Všimněte si, že zde se poprvé v hlavičce objevuje typ ukazatel na ukazatel,
** proto je třeba při práci s RootPtr použít dereferenční operátor *.
**/
    *RootPtr = NULL; //set root pointer to NULL
}

void BTInsert (tBTNodePtr *RootPtr, int Content) {
/*   --------
** Vloží do stromu nový uzel s hodnotou Content.
**
** Z pohledu vkládání chápejte vytvářený strom jako binární vyhledávací strom,
** kde uzly s hodnotou menší než má otec leží v levém podstromu a uzly větší
** leží vpravo. Pokud vkládaný uzel již existuje, neprovádí se nic (daná hodnota
** se ve stromu může vyskytnout nejvýše jednou). Pokud se vytváří nový uzel,
** vzniká vždy jako list stromu. Funkci implementujte nerekurzivně.
**/
    tBTNodePtr tmp = *RootPtr;
    while (tmp != NULL){ //while current item is not NULL
        if (tmp->Cont > Content){ //if new item is smaller than current item (has smaller content)
            if (tmp->LPtr == NULL){ //if current item does not have a left child
                tmp->LPtr = malloc(sizeof(struct tBTNode)); //allocate memory for new item as left child of current item
                //set content and pointers to children of the new item
                tmp->LPtr->Cont = Content;
                tmp->LPtr->LPtr = NULL;
                tmp->LPtr->RPtr = NULL;
                return;
            }
            else { //if current item does have a left child
                tmp = tmp->LPtr; //set left child as new current item
            }
        }
        else if (tmp->Cont < Content){ //if new item is bigger than current item (has bigger content)
            if (tmp->RPtr == NULL){ //if current item does not have a right child
                tmp->RPtr = malloc(sizeof(struct tBTNode)); //allocate memory for new item as right child of current item
                //set content and pointers to children of the new item
                tmp->RPtr->Cont = Content;
                tmp->RPtr->LPtr = NULL;
                tmp->RPtr->RPtr = NULL;
                return;
            }
            else { //if current item does have a right child
                tmp = tmp->RPtr; //set right child as new current item
            }
        }
        else { //if new item has the same value as current item (new item already exists)
            return; //do nothing
        }
    } //end while
    //only reached when the tree was empty
    *RootPtr = malloc(sizeof(struct tBTNode)); //allocate memory for new item that is now root
    //set content and child pointers
    (*RootPtr)->Cont = Content;
    (*RootPtr)->LPtr = NULL;
    (*RootPtr)->RPtr = NULL;
}

/*                                  PREORDER                                  */

void Leftmost_Preorder (tBTNodePtr ptr, tStackP *Stack)	{
/*   -----------------
** Jde po levě větvi podstromu, dokud nenarazí na jeho nejlevější uzel.
**
** Při průchodu Preorder navštívené uzly zpracujeme voláním funkce BTWorkOut()
** a ukazatele na ně is uložíme do zásobníku.
**/
    while (ptr != NULL){ //while current item is not null
        BTWorkOut(ptr); // process item
        SPushP(Stack, ptr); //push item to the item stack
        ptr = ptr->LPtr; //set left child as new current item
    }
}

void BTPreorder (tBTNodePtr RootPtr)	{
/*   ----------
** Průchod stromem typu preorder implementovaný nerekurzivně s využitím funkce
** Leftmost_Preorder a zásobníku ukazatelů. Zpracování jednoho uzlu stromu
** realizujte jako volání funkce BTWorkOut().
**/
    tStackP* StackP = malloc(sizeof(tStackP)); //allocate memory for item stack
    SInitP(StackP); //initialize item stack
    Leftmost_Preorder(RootPtr, StackP); //travel to leftmost item (and process items on the way)
    while (!SEmptyP(StackP)){ //while item stack not empty
        RootPtr = STopPopP(StackP); //pop and move to item from item stack
        Leftmost_Preorder(RootPtr->RPtr, StackP); //travel to leftmost item of the right child of the current item
                                                  // (and process items on the way)
    }
    free(StackP); //free item stack
}


/*                                  INORDER                                   */

void Leftmost_Inorder(tBTNodePtr ptr, tStackP *Stack)		{
/*   ----------------
** Jde po levě větvi podstromu, dokud nenarazí na jeho nejlevější uzel.
**
** Při průchodu Inorder ukládáme ukazatele na všechny navštívené uzly do
** zásobníku.
**/
    while (ptr != NULL){ //while current item is not NULL
        SPushP(Stack, ptr); //push item to the item stack
        ptr = ptr->LPtr; //set left child as new current item
    }
}

void BTInorder (tBTNodePtr RootPtr)	{
/*   ---------
** Průchod stromem typu inorder implementovaný nerekurzivně s využitím funkce
** Leftmost_Inorder a zásobníku ukazatelů. Zpracování jednoho uzlu stromu
** realizujte jako volání funkce BTWorkOut().
**/
    tStackP* StackP = malloc(sizeof(tStackP)); //allocate memory for item stack
    SInitP(StackP); //initialize item stack
    Leftmost_Inorder(RootPtr, StackP); //travel to the leftmost item
    while (!SEmptyP(StackP)){ //while item stack is not empty
        RootPtr = STopPopP(StackP); //pop and move to item from stack
        BTWorkOut(RootPtr); //process item
        Leftmost_Inorder(RootPtr->RPtr, StackP); //travel to the leftmost item of the right child of the current item
    }
    free(StackP); //free item stack
}

/*                                 POSTORDER                                  */

void Leftmost_Postorder (tBTNodePtr ptr, tStackP *StackP, tStackB *StackB) {
/*           --------
** Jde po levě větvi podstromu, dokud nenarazí na jeho nejlevější uzel.
**
** Při průchodu Postorder ukládáme ukazatele na navštívené uzly do zásobníku
** a současně do zásobníku bool hodnot ukládáme informaci, zda byl uzel
** navštíven poprvé a že se tedy ještě nemá zpracovávat.
**/
    while (ptr != NULL){ //while current item not NULL
        SPushP(StackP, ptr); //push item to item stack
        SPushB(StackB, TRUE); //push TRUE to bool stack (item visited first time)
        ptr = ptr->LPtr; //set left child as new current item
    }
}

void BTPostorder (tBTNodePtr RootPtr)	{
/*           -----------
** Průchod stromem typu postorder implementovaný nerekurzivně s využitím funkce
** Leftmost_Postorder, zásobníku ukazatelů a zásobníku hotdnot typu bool.
** Zpracování jednoho uzlu stromu realizujte jako volání funkce BTWorkOut().
**/
    tStackP* StackP = malloc(sizeof(tStackP)); //allocate memory for item stack
    tStackB* StackB = malloc(sizeof(tStackB)); //allocate memory for bool stack
    SInitP(StackP); //initialize item stack
    SInitB(StackB); //initialize bool stack
    bool visited; //bool variable, indicates whether the item has been visited once (true) or more times (false)
    Leftmost_Postorder(RootPtr, StackP, StackB); //travel to the leftmost item of the tree
    while (!SEmptyP(StackP)){ //while item stack not empty
        RootPtr = StackP->a[StackP->top]; //move to the top value from stack
        visited = STopPopB(StackB); //pop value from bool stack
        if (visited == TRUE){ //if item was visited only once
            SPushB(StackB, FALSE); //push false to bool stack (item visited more than once)
            Leftmost_Postorder(RootPtr->RPtr, StackP, StackB); //travel to the leftmost item of the right child of the current item
        }
        else { //if item was already visited twice
            STopPopP(StackP); //pop value from item stack
            BTWorkOut(RootPtr); //process item
        }
    } //end while
    free(StackP); //free item stack
    free(StackB); //free bool stack
}


void BTDisposeTree (tBTNodePtr *RootPtr)	{
/*   -------------
** Zruší všechny uzly stromu a korektně uvolní jimi zabranou paměť.
**
** Funkci implementujte nerekurzivně s využitím zásobníku ukazatelů.
**/
    tStackP* StackP = malloc(sizeof(tStackP)); //allocate memory for an item stack
    SInitP(StackP); //initialize the item stack
    do { //do while current item is not NULL or the item stack is not empty
        if (*RootPtr == NULL){ //if current item is NULL
            if (!SEmptyP(StackP)){ //if item stack is not empty
                *RootPtr = STopPopP(StackP); //pop and move to item from stack
            }
        }
        else { // if current item is not NULL
            if ((*RootPtr)->RPtr != NULL){ //if current item has right child
                SPushP(StackP, (*RootPtr)->RPtr); //push right child to item stack
            }
            tBTNodePtr tmp = *RootPtr; //save pointer to current item
            *RootPtr = (*RootPtr)->LPtr; //set left child as new current item
            free(tmp); //free current item
        }
    } while ((*RootPtr != NULL) || (!SEmptyP(StackP)));
    free(StackP); //free item stack
}

/* konec c402.c */

