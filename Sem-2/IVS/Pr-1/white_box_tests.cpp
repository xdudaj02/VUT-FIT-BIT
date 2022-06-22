//======== Copyright (c) 2017, FIT VUT Brno, All rights reserved. ============//
//
// Purpose:     White Box - Tests suite
//
// $NoKeywords: $ivs_project_1 $white_box_code.cpp
// $Author:     JMENO PRIJMENI <xlogin00@stud.fit.vutbr.cz>
// $Date:       $2017-01-04
//============================================================================//
/**
 * @file white_box_tests.cpp
 * @author JMENO PRIJMENI
 * 
 * @brief Implementace testu prace s maticemi.
 */

#include "gtest/gtest.h"
#include "white_box_code.h"

//============================================================================//

class SquareMatrix1x1 : public ::testing::Test
{
protected:
    void SetUp(){
        matrix = Matrix();
    }

    Matrix matrix;
};

class SquareMatrix2x2 : public ::testing::Test
{
protected:
    void SetUp(){
        matrix = Matrix(2, 2);
        std::vector<std::vector<double>> values = {{1, 1.5}, {2, 2.5}};
        matrix.set(values);
    }

    Matrix matrix;

};

class SquareMatrix3x3 : public ::testing::Test
{
protected:
    void SetUp(){
        matrix = Matrix(3, 3);
        std::vector<std::vector<double>> values = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
        matrix.set(values);
    }

    Matrix matrix;

};

class SquareMatrix4x4 : public ::testing::Test
{
protected:
    void SetUp(){
        matrix = Matrix(4, 4);
    }

    Matrix matrix;

};

class NonSquareMatrix2x3 : public ::testing::Test
{
protected:
    void SetUp(){
        matrix = Matrix(2, 3);
    }

    Matrix matrix;
};

//tests construction of 1x1 sized matrix
TEST_F(SquareMatrix1x1, Constructor1x1)
{
    ASSERT_NO_THROW(Matrix());
    EXPECT_EQ(matrix.get(0, 0), 0);
}

//tests construction of 2x2 sized matrix
TEST_F(SquareMatrix2x2, ConstructorAxB)
{
    ASSERT_ANY_THROW(Matrix(0,2));
    ASSERT_ANY_THROW(Matrix(0,0));
    ASSERT_NO_THROW(Matrix(2, 2));

    Matrix test_matrix = Matrix(2, 2);
    EXPECT_EQ(test_matrix.get(0, 1), 0);
    EXPECT_EQ(test_matrix.get(1, 0), 0);
    EXPECT_EQ(test_matrix.get(1, 1), 0);
}

//tests construction of 3x3 sized matrix
TEST_F(SquareMatrix3x3, ConstructorAxB)
{
    ASSERT_NO_THROW(Matrix(3, 3));
    Matrix test_matrix = Matrix(3, 3);
    EXPECT_EQ(test_matrix.get(1, 1), 0);
    EXPECT_EQ(test_matrix.get(0, 0), 0);
    EXPECT_EQ(test_matrix.get(2, 2), 0);
}

//tests construction of 4x4 sized matrix
TEST_F(SquareMatrix4x4, ConstructorAxB)
{
    ASSERT_NO_THROW(Matrix(4, 4));
    Matrix test_matrix = Matrix(4, 4);
    EXPECT_EQ(test_matrix.get(1, 1), 0);
    EXPECT_EQ(test_matrix.get(2, 0), 0);
    EXPECT_EQ(test_matrix.get(3, 3), 0);
}

//tests construction of 2x3 sized matrix
TEST_F(NonSquareMatrix2x3, ConstructorAxB)
{
    ASSERT_NO_THROW(Matrix(2, 3));
    Matrix test_matrix = Matrix(2, 3);
    EXPECT_EQ(test_matrix.get(1, 2), 0);
    EXPECT_EQ(test_matrix.get(0, 0), 0);
    EXPECT_EQ(test_matrix.get(1, 1), 0);
}

//tests setting value of a cell in a 2x2 sized matrix
TEST_F(SquareMatrix2x2, SetValue)
{
    ASSERT_TRUE(matrix.set(1, 1, 10));
    EXPECT_EQ(matrix.get(1, 1), 10);

    EXPECT_FALSE(matrix.set(1, 2, 10));
    EXPECT_FALSE(matrix.set(2, 1, 10));
    EXPECT_FALSE(matrix.set(2, 2, 10));
    EXPECT_FALSE(matrix.set(4, 4, 10));
}

//tests setting value of a cell in a 3x3 sized matrix
TEST_F(SquareMatrix3x3, SetValue)
{
    ASSERT_TRUE(matrix.set(0, 0, -10));
    EXPECT_EQ(matrix.get(0, 0), -10);
    ASSERT_TRUE(matrix.set(1, 1, 0.1));
    EXPECT_EQ(matrix.get(1, 1), 0.1);
    ASSERT_TRUE(matrix.set(2, 2, 10));
    EXPECT_EQ(matrix.get(2, 2), 10);

    EXPECT_FALSE(matrix.set(1, 3, 10));
    EXPECT_FALSE(matrix.set(3, 1, 10));
    EXPECT_FALSE(matrix.set(3, 3, 10));
    EXPECT_FALSE(matrix.set(10, 10, 100));
}

//tests setting value of a cell in a 4x4 sized matrix
TEST_F(SquareMatrix4x4, SetValue)
{
    ASSERT_TRUE(matrix.set(0, 0, -10));
    EXPECT_EQ(matrix.get(0, 0), -10);
    ASSERT_TRUE(matrix.set(1, 1, 0.1));
    EXPECT_EQ(matrix.get(1, 1), 0.1);
    ASSERT_TRUE(matrix.set(3, 3, 100));
    EXPECT_EQ(matrix.get(3, 3), 100);

    EXPECT_FALSE(matrix.set(1, 4, 10));
    EXPECT_FALSE(matrix.set(4, 1, 10));
    EXPECT_FALSE(matrix.set(4, 4, 10));
    EXPECT_FALSE(matrix.set(40, 40, 10));
}

//tests setting value of a cell in a 2x3 sized matrix
TEST_F(NonSquareMatrix2x3, SetValue)
{
    ASSERT_TRUE(matrix.set(0, 0, -10));
    EXPECT_EQ(matrix.get(0, 0), -10);
    ASSERT_TRUE(matrix.set(1, 1, 0.1));
    EXPECT_EQ(matrix.get(1, 1), 0.1);
    ASSERT_TRUE(matrix.set(1, 2, 100));
    EXPECT_EQ(matrix.get(1, 2), 100);

    EXPECT_FALSE(matrix.set(1, 3, 10));
    EXPECT_FALSE(matrix.set(2, 2, 10));
    EXPECT_FALSE(matrix.set(2, 3, 10));
    EXPECT_FALSE(matrix.set(20, 20, 10));
}

//tests setting value of all cells in a 1x1 sized matrix
TEST_F(SquareMatrix1x1, SetValues)
{
    std::vector<std::vector<double>> bad_values_1 = {{1, 2}};
    std::vector<std::vector<double>> bad_values_2 = {{1}, {2}};
    ASSERT_FALSE(matrix.set(bad_values_1));
    ASSERT_FALSE(matrix.set(bad_values_2));

    std::vector<std::vector<double>> good_values = {{1}};
    ASSERT_TRUE(matrix.set(good_values));
    EXPECT_EQ(matrix.get(0, 0), 1);
}

//tests setting value of all cells in a 2x2 sized matrix
TEST_F(SquareMatrix2x2, SetValues)
{
    std::vector<std::vector<double>> bad_values_1 = {{1, 2, 3}, {7, 8, 9}};
    std::vector<std::vector<double>> bad_values_2 = {{1, 2}, {4, 5}, {7, 9}};
    ASSERT_FALSE(matrix.set(bad_values_1));
    ASSERT_FALSE(matrix.set(bad_values_2));

    std::vector<std::vector<double>> good_values = {{1, 2}, {3, 4}};
    ASSERT_TRUE(matrix.set(good_values));
    EXPECT_EQ(matrix.get(0, 0), 1);
    EXPECT_EQ(matrix.get(1, 1), 4);
}

//tests setting value of all cells in a 3x3 sized matrix
TEST_F(SquareMatrix3x3, SetValues)
{
    std::vector<std::vector<double>> bad_values_1 = {{1, 2, 3}, {7, 8, 9}};
    std::vector<std::vector<double>> bad_values_2 = {{1, 2}, {4, 5}, {7, 9}};
    ASSERT_FALSE(matrix.set(bad_values_1));
    ASSERT_FALSE(matrix.set(bad_values_2));

    std::vector<std::vector<double>> good_values = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
    ASSERT_TRUE(matrix.set(good_values));
    EXPECT_EQ(matrix.get(0, 0), 1);
    EXPECT_EQ(matrix.get(1, 2), 6);
    EXPECT_EQ(matrix.get(2, 2), 9);
}

//tests setting value of all cells in a 4x4 sized matrix
TEST_F(SquareMatrix4x4, SetValues) {
    std::vector<std::vector<double>> bad_values_1 = {{1, 2, 3, 4}, {5, 6, 7, 8}};
    std::vector<std::vector<double>> bad_values_2 = {{1, 2}, {4, 5}, {7, 9}};
    std::vector<std::vector<double>> bad_values_3 = {{1, 2, 3, 4}, {5, 6, 7, 8, 9}};
    ASSERT_FALSE(matrix.set(bad_values_1));
    ASSERT_FALSE(matrix.set(bad_values_2));
    ASSERT_FALSE(matrix.set(bad_values_3));

    std::vector<std::vector<double>> good_values = {{1,  2,  3,  4},
                                                    {5,  6,  7,  8},
                                                    {9,  10, 11, 12},
                                                    {13, 14, 15, 16}};
    ASSERT_TRUE(matrix.set(good_values));
    EXPECT_EQ(matrix.get(0, 0), 1);
    EXPECT_EQ(matrix.get(1, 0), 5);
    EXPECT_EQ(matrix.get(2, 3), 12);
    EXPECT_EQ(matrix.get(3, 1), 14);
}

//tests setting value of all cells in a 2x3 sized matrix
TEST_F(NonSquareMatrix2x3, SetValues)
{
    std::vector<std::vector<double>> bad_values_1 = {{1, 2}, {7, 8, 9}};
    std::vector<std::vector<double>> bad_values_2 = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
    ASSERT_FALSE(matrix.set(bad_values_1));
    ASSERT_FALSE(matrix.set(bad_values_2));

    std::vector<std::vector<double>> good_values = {{1, 2, 3}, {4, 5, 6}};
    ASSERT_TRUE(matrix.set(good_values));
    EXPECT_EQ(matrix.get(0, 0), 1);
    EXPECT_EQ(matrix.get(1, 2), 6);
    EXPECT_EQ(matrix.get(0, 2), 3);
}

//tests getting value from a cell in a 1x1 sized matrix
TEST_F(SquareMatrix1x1, GetValue)
{
    ASSERT_ANY_THROW(matrix.get(0, 1));
    ASSERT_ANY_THROW(matrix.get(1, 0));
    ASSERT_ANY_THROW(matrix.get(5, 5));

    ASSERT_NO_THROW(matrix.get(0, 0));
    EXPECT_EQ(matrix.get(0, 0), 0);
}

//tests getting value from a cell in a 2x2 sized matrix
TEST_F(SquareMatrix2x2, GetValue)
{
    ASSERT_ANY_THROW(matrix.get(2, 1));
    ASSERT_ANY_THROW(matrix.get(1, 2));
    ASSERT_ANY_THROW(matrix.get(2, 2));

    ASSERT_NO_THROW(matrix.get(1, 1));
    EXPECT_EQ(matrix.get(0, 0), 1);
    EXPECT_EQ(matrix.get(1, 1), 2.5);
}

//tests getting value from a cell in a 3x3 sized matrix
TEST_F(SquareMatrix3x3, GetValue)
{
    ASSERT_ANY_THROW(matrix.get(3, 1));
    ASSERT_ANY_THROW(matrix.get(1, 3));
    ASSERT_ANY_THROW(matrix.get(3, 3));

    ASSERT_NO_THROW(matrix.get(1, 1));
    EXPECT_EQ(matrix.get(0, 0), 1);
    EXPECT_EQ(matrix.get(1, 1), 5);
    EXPECT_EQ(matrix.get(2, 2), 9);
}

//tests getting value from a cell in a 4x4 sized matrix
TEST_F(SquareMatrix4x4, GetValue)
{
    ASSERT_ANY_THROW(matrix.get(4, 1));
    ASSERT_ANY_THROW(matrix.get(1, 4));
    ASSERT_ANY_THROW(matrix.get(4, 4));

    ASSERT_NO_THROW(matrix.get(2, 2));
    EXPECT_EQ(matrix.get(0, 0), 0);
    EXPECT_EQ(matrix.get(2, 0), 0);
    EXPECT_EQ(matrix.get(2, 3), 0);
    EXPECT_EQ(matrix.get(3, 3), 0);
}

//tests getting value from a cell in a 2x3 sized matrix
TEST_F(NonSquareMatrix2x3, GetValue)
{
    ASSERT_ANY_THROW(matrix.get(2, 1));
    ASSERT_ANY_THROW(matrix.get(1, 3));
    ASSERT_ANY_THROW(matrix.get(2, 3));

    ASSERT_NO_THROW(matrix.get(1, 1));
    EXPECT_EQ(matrix.get(0, 0), 0);
    EXPECT_EQ(matrix.get(1, 2), 0);
}

//tests comparison of a 1x1 sized matrix with other matrices
TEST_F(SquareMatrix1x1, Equality)
{
    Matrix matrix_2 = Matrix(1, 1);
    ASSERT_NO_THROW(matrix.operator==(matrix_2));
    Matrix matrix_3 = Matrix(2, 1);
    ASSERT_ANY_THROW(matrix.operator==(matrix_3));

    EXPECT_TRUE(matrix.operator==(matrix_2));

    matrix_2.set(0, 0, 1);
    EXPECT_FALSE(matrix.operator==(matrix_2));
}

//tests comparison of a 2x2 sized matrix with other matrices
TEST_F(SquareMatrix2x2, Equality)
{
    Matrix matrix_2 = Matrix(2, 2);
    ASSERT_NO_THROW(matrix.operator==(matrix_2));
    Matrix matrix_3 = Matrix(2, 3);
    ASSERT_ANY_THROW(matrix.operator==(matrix_3));

    EXPECT_FALSE(matrix.operator==(matrix_2));
    EXPECT_TRUE(matrix.operator==(matrix));
}

//tests comparison of a 4x4 sized matrix with other matrices
TEST_F(SquareMatrix4x4, Equality)
{
    Matrix matrix_2 = Matrix(4, 4);
    ASSERT_NO_THROW(matrix.operator==(matrix_2));
    Matrix matrix_3 = Matrix(4, 3);
    ASSERT_ANY_THROW(matrix.operator==(matrix_3));

    EXPECT_TRUE(matrix.operator==(matrix_2));
    matrix_2.set(0, 0, 1);
    EXPECT_FALSE(matrix.operator==(matrix_2));
}

//tests comparison of a 2x3 sized matrix with other matrices
TEST_F(NonSquareMatrix2x3, Equality)
{
    Matrix matrix_2 = Matrix(2, 3);
    ASSERT_NO_THROW(matrix.operator==(matrix_2));
    Matrix matrix_3 = Matrix(2, 4);
    ASSERT_ANY_THROW(matrix.operator==(matrix_3));

    EXPECT_TRUE(matrix.operator==(matrix_2));
    matrix_2.set(1, 2, 1);
    EXPECT_FALSE(matrix.operator==(matrix_2));
}

//tests matrix adding with a 1x1 sized matrix
TEST_F(SquareMatrix1x1, Adding)
{
    Matrix matrix_2 = Matrix(1, 2);
    ASSERT_ANY_THROW(matrix.operator+(matrix_2));
    Matrix matrix_3 = Matrix(1, 1);
    ASSERT_NO_THROW(matrix.operator+(matrix_3));

    EXPECT_EQ(matrix.operator+(matrix_3), matrix);
    matrix_3.set({{1}});
    EXPECT_EQ(matrix.operator+(matrix_3), matrix_3);
    matrix_3.set({{-1}});
    EXPECT_EQ(matrix.operator+(matrix_3), matrix_3);
}

//tests matrix adding with a 2x2 sized matrix
TEST_F(SquareMatrix2x2, Adding)
{
    Matrix matrix_1 = Matrix(1, 2);
    ASSERT_ANY_THROW(matrix.operator+(matrix_1));
    Matrix matrix_2 = Matrix(3, 3);
    ASSERT_ANY_THROW(matrix.operator+(matrix_2));
    Matrix matrix_3 = Matrix(2, 2);
    ASSERT_NO_THROW(matrix.operator+(matrix_3));

    EXPECT_EQ(matrix.operator+(matrix_3), matrix);

    std::vector<std::vector<double>> values_1 = {{2, 3}, {4, 5}};
    matrix_3.set(values_1);
    EXPECT_EQ(matrix.operator+(matrix), matrix_3);

    std::vector<std::vector<double>> values_2 = {{-1, -1.5}, {-2, -2.5}};
    matrix_3.set(values_2);
    Matrix matrix_4 = Matrix(2, 2);
    EXPECT_EQ(matrix.operator+(matrix_3), matrix_4);
}

//tests matrix adding with a 4x4 sized matrix
TEST_F(SquareMatrix4x4, Adding)
{
    Matrix matrix_1 = Matrix(1, 2);
    ASSERT_ANY_THROW(matrix.operator+(matrix_1));
    Matrix matrix_2 = Matrix(5, 4);
    ASSERT_ANY_THROW(matrix.operator+(matrix_2));
    Matrix matrix_3 = Matrix(4, 4);
    ASSERT_NO_THROW(matrix.operator+(matrix_3));

    EXPECT_EQ(matrix.operator+(matrix_3), matrix);

    std::vector<std::vector<double>> values_1 = {{1,  2,  3,  4},
                                                 {5,  6,  7,  8},
                                                 {9,  10, 11, 12},
                                                 {13, 14, 15, 16}};
    matrix_3.set(values_1);
    EXPECT_EQ(matrix.operator+(matrix_3), matrix_3);

    matrix.set(values_1);
    Matrix matrix_4 = Matrix(4, 4);
    std::vector<std::vector<double>> values_2 = {{2,  4,  6,  8},
                                                 {10,  12,  14,  16},
                                                 {18,  20, 22, 24},
                                                 {26, 28, 30, 32}};
    matrix_4.set(values_2);
    EXPECT_EQ(matrix.operator+(matrix_3), matrix_4);
}

//tests matrix adding with a 2x3 sized matrix
TEST_F(NonSquareMatrix2x3, Adding)
{
    Matrix matrix_1 = Matrix(2, 2);
    ASSERT_ANY_THROW(matrix.operator+(matrix_1));
    Matrix matrix_2 = Matrix(3, 3);
    ASSERT_ANY_THROW(matrix.operator+(matrix_2));
    Matrix matrix_3 = Matrix(2, 3);
    ASSERT_NO_THROW(matrix.operator+(matrix_3));

    EXPECT_EQ(matrix.operator+(matrix_3), matrix);

    std::vector<std::vector<double>> values_1 = {{2, 3}, {4, 5}, {-2, 0.2}};
    matrix_3.set(values_1);
    EXPECT_EQ(matrix.operator+(matrix_3), matrix_3);
}

//tests matrix multiplication with a 1x1 sized matrix
TEST_F(SquareMatrix1x1, Multiplication)
{
    Matrix matrix_2 = Matrix(2, 1);
    ASSERT_ANY_THROW(matrix.operator*(matrix_2));

    Matrix matrix_3 = Matrix();
    ASSERT_NO_THROW(matrix.operator*(matrix_3));
    EXPECT_EQ(matrix.operator*(matrix_3), matrix_3);

    matrix_3.set({{1}});
    matrix.set(0, 0, 1);
    ASSERT_NO_THROW(matrix.operator*(matrix_3));
    EXPECT_EQ(matrix.operator*(matrix_3), matrix_3);

    Matrix matrix_4 = Matrix(1, 4);
    matrix_4.set({{1, 2, 3, 4}});
    ASSERT_NO_THROW(matrix.operator*(matrix_4));
    EXPECT_EQ(matrix.operator*(matrix_4), matrix_4);
}

//tests matrix multiplication with a 2x2 sized matrix
TEST_F(SquareMatrix2x2, Multiplication)
{
    Matrix matrix_1 = Matrix(1, 5);
    ASSERT_ANY_THROW(matrix.operator*(matrix_1));
    Matrix matrix_2 = Matrix(3, 2);
    ASSERT_ANY_THROW(matrix.operator*(matrix_2));

    Matrix matrix_3 = Matrix(2, 2);
    ASSERT_NO_THROW(matrix.operator*(matrix_3));
    EXPECT_EQ(matrix.operator*(matrix_3), matrix_3);

    matrix_3.set({{1, 0}, {0, 1}});
    EXPECT_EQ(matrix.operator*(matrix_3), matrix);

    matrix_3.set({{2, -2}, {-2, 2}});
    Matrix matrix_4 = Matrix(2, 2);
    matrix_4.set({{-1, 1}, {-1, 1}});
    EXPECT_EQ(matrix.operator*(matrix_3), matrix_4);
}

//tests matrix multiplication with a 4x4 sized matrix
TEST_F(SquareMatrix4x4, Multiplication)
{
    Matrix matrix_1 = Matrix(1, 3);
    ASSERT_ANY_THROW(matrix.operator*(matrix_1));
    Matrix matrix_2 = Matrix(5, 4);
    ASSERT_ANY_THROW(matrix.operator*(matrix_2));

    Matrix matrix_3 = Matrix(4, 1);
    ASSERT_NO_THROW(matrix.operator*(matrix_3));
    EXPECT_EQ(matrix.operator*(matrix_3), matrix_3);

    matrix.set({{1,  2,  3,  4}, {5,  6,  7,  8}, {9,  10, 11, 12}, {13, 14, 15, 16}});
    matrix_3.set({{1}, {1}, {1}, {1}});
    Matrix matrix_4 = Matrix(4, 1);
    matrix_4.set({{10}, {26}, {42}, {58}});
    EXPECT_EQ(matrix.operator*(matrix_3), matrix_4);

    Matrix matrix_5 = Matrix(4, 4);
    matrix_5.set({{1, 0, 0, 0}, {0, 1, 0, 0}, {0, 0, 1, 0}, {0, 0, 0, 1}});
    EXPECT_EQ(matrix.operator*(matrix_5), matrix);
}

//tests matrix multiplication with a 2x3 sized matrix
TEST_F(NonSquareMatrix2x3, Multiplication)
{
    Matrix matrix_1 = Matrix(1, 3);
    ASSERT_ANY_THROW(matrix.operator*(matrix_1));
    Matrix matrix_2 = Matrix(2, 4);
    ASSERT_ANY_THROW(matrix.operator*(matrix_2));

    Matrix matrix_3 = Matrix(3, 2);
    Matrix matrix_4 = Matrix(2, 2);
    ASSERT_NO_THROW(matrix.operator*(matrix_3));
    EXPECT_EQ(matrix.operator*(matrix_3), matrix_4);
}

//tests multiplying a 1x1 sized matrix with a constant
TEST_F(SquareMatrix1x1, ConstantMultiplication)
{
    ASSERT_NO_THROW(matrix.operator*(3));
    Matrix matrix_2 = Matrix();
    matrix_2.set(0, 0, 0);
    EXPECT_EQ(matrix.operator*(3), matrix_2);
}

//tests multiplying a 1x1 sized matrix with a constant
TEST_F(SquareMatrix3x3, ConstantMultiplication)
{
    ASSERT_NO_THROW(matrix.operator*(3));
    ASSERT_NO_THROW(matrix.operator*(-3));
    ASSERT_NO_THROW(matrix.operator*(0.5));
    EXPECT_EQ(matrix.operator*(0), Matrix(3, 3));
    EXPECT_EQ(matrix.operator*(1), matrix);

    Matrix matrix_2 = Matrix(3, 3);
    matrix_2.set({{-2, -4, -6}, {-8, -10, -12}, {-14, -16, -18}});
    EXPECT_EQ(matrix.operator*(-2), matrix_2);

    Matrix matrix_3 = Matrix(3, 3);
    matrix_3.set({{0.5, 1, 1.5}, {2, 2.5, 3}, {3.5, 4, 4.5}});
    EXPECT_EQ(matrix.operator*(0.5), matrix_3);
}

//tests multiplying a 1x1 sized matrix with a constant
TEST_F(SquareMatrix4x4, ConstantMultiplication)
{
    ASSERT_NO_THROW(matrix.operator*(3));
    ASSERT_NO_THROW(matrix.operator*(-3));
    ASSERT_NO_THROW(matrix.operator*(0.5));

    EXPECT_EQ(matrix.operator*(0), Matrix(4, 4));
    EXPECT_EQ(matrix.operator*(1), matrix);

    Matrix matrix_2 = Matrix(4, 4);
    matrix.set({{2,  4,  6,  8}, {10,  12,  14,  16}, {18,  20, 22, 24}, {26, 28, 30, 32}});
    matrix_2.set({{-2, -4, -6, -8}, {-10, -12, -14, -16}, {-18, -20, -22, -24}, {-26 , -28, -30, -32}});
    EXPECT_EQ(matrix.operator*(-1), matrix_2);

    Matrix matrix_3 = Matrix(4, 4);
    matrix_3.set({{1,  2,  3,  4}, {5,  6,  7,  8}, {9,  10, 11, 12}, {13, 14, 15, 16}});
    EXPECT_EQ(matrix.operator*(0.5), matrix_3);
}

//tests multiplying a 1x1 sized matrix with a constant
TEST_F(NonSquareMatrix2x3, ConstantMultiplication)
{
    ASSERT_NO_THROW(matrix.operator*(2));
    EXPECT_EQ(matrix.operator*(2), matrix);
}

//tests solving an equation using a matrix
TEST_F(SquareMatrix1x1, EquationSolution)
{
    std::vector<double> equation_1 = {1};
    std::vector<double> equation_2 = {2};
    EXPECT_ANY_THROW(matrix.solveEquation(equation_1));

    matrix.set(0, 0, 1);
    EXPECT_EQ(matrix.solveEquation(equation_1), equation_1);
    EXPECT_EQ(matrix.solveEquation(equation_2), equation_2);
}

//tests solving a system of two equations using a matrix
//test not working without a change in line 164 in white_box_code.cpp ('abs' -> 'std::abs')
/*
TEST_F(SquareMatrix2x2, EquationSolution)
{

    std::vector<double> equation_1 = {1, 1};
    std::vector<double> result_1 = {-2, 2};
    ASSERT_NO_THROW(matrix.solveEquation(equation_1));
    EXPECT_EQ(matrix.solveEquation(equation_1), result_1);

    //wrong parameters
    std::vector<double> equation_2 = {2, 2, 2};
    ASSERT_ANY_THROW(matrix.solveEquation(equation_2));
}
*/

//tests solving a system of three equations using a matrix
TEST_F(SquareMatrix3x3, EquationSolution)
{
    //singular matrix
    std::vector<double> equation_1 = {3, 3, 3};
    ASSERT_ANY_THROW(matrix.solveEquation(equation_1));

    //wrong parameters
    std::vector<double> equation_2 = {2, 2};
    ASSERT_ANY_THROW(matrix.solveEquation(equation_2));

    matrix.set({{1, 6, 4}, {2, 7, 3}, {8, 9, 5}});
    ASSERT_NO_THROW(matrix.solveEquation(equation_1));
    std::vector<double> result_1 = {-0.2, 0.4, 0.2};
    EXPECT_EQ(matrix.solveEquation(equation_1), result_1);
}

//tests solving a system of four equations using a matrix
TEST_F(SquareMatrix4x4, EquationSolution)
{
    std::vector<double> equation_1 = {1, 1, 1, 1};
    matrix.set({{1, -2, 1, 0}, {-1, 2 -4, 2}, {1, -1.5, 1, 1}, {2, 12, 1, 0}});
    ASSERT_NO_THROW(matrix.solveEquation(equation_1));

    std::vector<double> equation_2 = {-3, -32, -47, 49};
    std::vector<double> result_2 = {2, -12, -4, 1};
    matrix.set({{2, -1, 5, 1}, {3, 2, 2, -6}, {1, 3, 3, -1}, {5, -2, -3, 3}});
    ASSERT_NO_THROW(matrix.solveEquation(equation_1));
    EXPECT_EQ(matrix.solveEquation(equation_2), result_2);
}

//tests solving a system of equations using a nonsquare matrix
TEST_F(NonSquareMatrix2x3, EquationSolution)
{
    //wrong parameters
    std::vector<double> equation_1 = {1, 1, 1};
    ASSERT_ANY_THROW(matrix.solveEquation(equation_1));

    //nonsquare matrix
    std::vector<double> equation_2 = {1, 1};
    ASSERT_ANY_THROW(matrix.solveEquation(equation_2));
}

//============================================================================//
/*** Konec souboru white_box_tests.cpp ***/