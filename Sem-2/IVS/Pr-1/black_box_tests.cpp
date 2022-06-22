//======== Copyright (c) 2017, FIT VUT Brno, All rights reserved. ============//
//
// Purpose:     Red-Black Tree - public interface tests
//
// $NoKeywords: $ivs_project_1 $black_box_tests.cpp
// $Author:     Jakub Duda <xdudaj02@stud.fit.vutbr.cz>
// $Date:       $2017-01-04
//============================================================================//
/**
 * @file black_box_tests.cpp
 * @author Jakub Duda
 * 
 * @brief Implementace testu binarniho stromu.
 */

#include <vector>
#include "gtest/gtest.h"
#include "red_black_tree.h"

//============================================================================//

class EmptyTree : public ::testing::Test
{
protected:
    BinaryTree tree;
};

class NonEmptyTree : public ::testing::Test
{
protected:
    virtual void SetUp() {
        int number_of_values = 10;
        int values[] = {20, 30, 40, 60, 80, 15, 45, 100, 5, 85};
        for (int i=0; i < number_of_values; i++)
            tree.InsertNode(values[i]);
    }

    BinaryTree tree;
};

class TreeAxioms : public ::testing::Test
{
protected:
    virtual void SetUp() {
        int number_of_values = 10;
        int values[] = {20, 30, 40, 60, 80, 15, 45, 100, 5, 85};
        for (int i=0; i < number_of_values; i++)
            tree.InsertNode(values[i]);
    }

    BinaryTree tree;

};

TEST_F(EmptyTree, InsertNode)
{
    ASSERT_TRUE(tree.GetRoot() == NULL);

    int value = 100;
    EXPECT_TRUE(tree.InsertNode(value).first);
    ASSERT_TRUE(tree.GetRoot() != NULL);
    EXPECT_EQ(tree.GetRoot()->key, value);
    EXPECT_TRUE(tree.GetRoot()->pParent == NULL);

    std::vector<BinaryTree::Node_t *> outLeafNodes;
    tree.GetLeafNodes(outLeafNodes);
    EXPECT_TRUE(tree.GetRoot()->pLeft == outLeafNodes[0]);
    EXPECT_TRUE(tree.GetRoot()->pRight == outLeafNodes[1]);

    EXPECT_TRUE(tree.GetRoot()->pRight->pParent == tree.GetRoot());
    EXPECT_TRUE(tree.GetRoot()->pLeft->pParent == tree.GetRoot());
}

TEST_F(EmptyTree, DeleteNode)
{
    ASSERT_TRUE(tree.GetRoot() == NULL);
    EXPECT_FALSE(tree.DeleteNode(0));
    EXPECT_TRUE(tree.GetRoot() == NULL);
}

TEST_F(EmptyTree, FindNode)
{
    ASSERT_TRUE(tree.GetRoot() == NULL);
    EXPECT_TRUE(tree.FindNode(0) == NULL);
    EXPECT_TRUE(tree.GetRoot() == NULL);
}

TEST_F(NonEmptyTree, InsertNode)
{
    EXPECT_FALSE(tree.InsertNode(20).first);
    int value = 10;
    EXPECT_TRUE(tree.InsertNode(value).first);
    EXPECT_FALSE(tree.InsertNode(value).first);
}

TEST_F(NonEmptyTree, DeleteNode)
{
    EXPECT_FALSE(tree.DeleteNode(10));
    int value = 100;
    EXPECT_TRUE(tree.DeleteNode(value));
    EXPECT_FALSE(tree.DeleteNode(value));
}

TEST_F(NonEmptyTree, FindNode)
{
    int value_1 = 10;
    EXPECT_TRUE(tree.FindNode(value_1) == NULL);
    int value_2 = 100;
    EXPECT_FALSE(tree.FindNode(value_2) == NULL);
}

TEST_F(TreeAxioms, Axiom1)
{
    std::vector<Node_t *> outLeafNodes;
    tree.GetLeafNodes(outLeafNodes);
    for (int i = 0; i < outLeafNodes.size(); ++i) {
        EXPECT_TRUE(outLeafNodes[i]->color == BLACK);
    }
}

TEST_F(TreeAxioms, Axiom2)
{
    std::vector<Node_t *> outAllNodes;
    tree.GetAllNodes(outAllNodes);
    for (int i = 0; i<(outAllNodes.size()); ++i){
        if (outAllNodes[i]->color == RED)
            EXPECT_TRUE((outAllNodes[i]->pLeft->color == BLACK) && (outAllNodes[i]->pRight->color == BLACK));
    }
}

TEST_F(TreeAxioms, Axiom3)
{
    std::vector<Node_t *> outLeafNodes;
    tree.GetLeafNodes(outLeafNodes);
    std::vector<int> count;
    int j;
    for (int i = 0; i<(outLeafNodes.size()); ++i){
        j = 0;
        while(outLeafNodes[i]->pParent != NULL) {
            if (outLeafNodes[i]->color == BLACK)
                j++;
            outLeafNodes[i] = outLeafNodes[i]->pParent;
        }
        count.push_back(j);
    }
    for (int i = 1; i<(outLeafNodes.size()); ++i){
        EXPECT_TRUE(count[i] == count[0]);
    }
}

//============================================================================//

/*** Konec souboru black_box_tests.cpp ***/