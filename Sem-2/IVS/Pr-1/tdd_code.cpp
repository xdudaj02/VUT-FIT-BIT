//======== Copyright (c) 2017, FIT VUT Brno, All rights reserved. ============//
//
// Purpose:     Test Driven Development - priority queue code
//
// $NoKeywords: $ivs_project_1 $tdd_code.cpp
// $Author:     Jakub Duda <xdudaj02@stud.fit.vutbr.cz>
// $Date:       $2017-01-04
//============================================================================//
/**
 * @file tdd_code.cpp
 * @author Jakub Duda
 * 
 * @brief Implementace metod tridy prioritni fronty.
 */

#include <stdlib.h>
#include <stdio.h>

#include "tdd_code.h"

//============================================================================//
// ** ZDE DOPLNTE IMPLEMENTACI **
//
// Zde doplnte implementaci verejneho rozhrani prioritni fronty (Priority Queue)
// 1. Verejne rozhrani fronty specifikovane v: tdd_code.h (sekce "public:")
//    - Konstruktor (PriorityQueue()), Destruktor (~PriorityQueue())
//    - Metody Insert/Remove/Find a GetHead
//    - Pripadne vase metody definovane v tdd_code.h (sekce "protected:")
//
// Cilem je dosahnout plne funkcni implementace prioritni fronty implementovane
// pomoci tzv. "double-linked list", ktera bude splnovat dodane testy 
// (tdd_tests.cpp).
//============================================================================//

PriorityQueue::PriorityQueue()
{
    root = nullptr;
}

PriorityQueue::~PriorityQueue() {
    Element_t *item = GetHead();
    Element_t *ptr = nullptr;
    while (item != nullptr)
    {
        ptr = item->pNext;
        free(item);
        item = ptr;
    }
}

void PriorityQueue::Insert(int value)
{
    auto *new_item = (Element_t*)malloc(sizeof(Element_t));
    if (!new_item)
        throw "Allocation failed.";
    new_item->value = value;
    Element_t *item = GetHead();

    //condition: list is empty
    if (item == nullptr) {
        new_item->pNext = nullptr;
        new_item->pPrev = nullptr;
        root = new_item;
    }
    else {
        //loop: goes through the whole list
        while (item->pNext != nullptr) {
            //condition: breaks out of the loop if the value of next item is equal or bigger
            if (item->value >= new_item->value) {
                break;
            }
            item = item->pNext;
        }
        //condition: new item has the highest value
        if (item->value < new_item->value){
            new_item->pNext = nullptr;
            new_item->pPrev = item;
            item->pNext = new_item;
        }
        else {
            new_item->pNext = item;
            //condition: new item has the lowest value
            if (item->pPrev == nullptr){
                new_item->pPrev = nullptr;
                item->pPrev = new_item;
                root = new_item;
            }
            else {
                new_item->pPrev = item->pPrev;
                item->pPrev->pNext = new_item;
                item->pPrev = new_item;
            }
        }
    }
}

bool PriorityQueue::Remove(int value)
{
    Element_t *item = GetHead();
    //loop: goes through the whole list
    while (item != nullptr)
    {
        if (item->value == value) {
            //condition: the list contains only one item
            if (item->pPrev == nullptr && item->pNext == nullptr)
            {
                root = nullptr;
            }
            //condition: item is first in the list
            else if (item->pPrev == nullptr && item->pNext != nullptr)
            {
                root = item->pNext;
                item->pNext->pPrev = nullptr;
            }
            //condition: item is last in the list
            else if (item->pPrev != nullptr && item->pNext == nullptr)
            {
                item->pPrev->pNext = nullptr;
            }
            else
            {
                item->pPrev->pNext = item->pNext;
                item->pNext->pPrev = item->pPrev;
            }
            free(item);
            return true;
        }
        item = item->pNext;
    }
    return false;
}

PriorityQueue::Element_t *PriorityQueue::Find(int value)
{
    Element_t *item = GetHead();
    while (item != nullptr) {
        if (item->value == value) {
            return item;
        }
        item = item->pNext;
    }
    return nullptr;
}

PriorityQueue::Element_t *PriorityQueue::GetHead()
{
    return root;
}

/*** Konec souboru tdd_code.cpp ***/