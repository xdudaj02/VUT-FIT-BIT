/********************************************************************************************/
/* * *                   Calculation of the voltage across the diode                    * * */
/* * *                                                                                  * * */
/* * *                                  Version No. 1                                   * * */
/* * *                                                                                  * * */
/* * *                              Jakub Duda, xdudaj02                                * * */
/* * *                                  november 2019                                   * * */
/* * *                                                                                  * * */
/********************************************************************************************/

#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <errno.h>

#define I_0 1E-12
#define U_t 25.8563E-3

/*********************************** FUNCTIONS *****************************************/

//function to calculate the result of an equation which uses the shockley diode equation and the kirchoffs first law
double equation (double U_0, double R, double U_p)
{
	double result;
	result = (I_0 * (exp (U_p / U_t) - 1)) - ( (U_0 - U_p) / R);
	return result;
}

//function that using the bisectional method calculates the voltage across the diode with a certain accuracy
double diode (double U_0, double R, double eps)
{
	double a, b, U_p, last_Up, result;
	a = 0;
	b = U_0;
	if (fabs (a - b) > eps)
	{
		U_p = (a + b) / 2;
		result = equation (U_0, R, U_p);
	}
	else 
	{
		U_p = U_0;
	}
	while (fabs (a - b) > eps)
	{
		if (((equation (U_0, R, a)) * result) < 0)
			b = U_p;
		else
			a = U_p;
		last_Up = U_p;
		if (fabs (a - b) > eps)
		{
			U_p = (a + b) / 2;
			result = equation (U_0, R, U_p);
		}
		if (last_Up == U_p)
			return U_p;
				
	}
	return U_p;
}

//function to calculate the value of the diode current using the shockley diode equation
double diode_current (double U_p)
{
	return (I_0 * (exp (U_p / U_t) - 1));
}

//function to check the validity of an argument
int argument_check (char x)
{
	if ((errno==ERANGE) || (x!='\0'))
		return 1;
	else
		return 0;
}

/************************************** MAIN *******************************************/

int main (int argc, char *argv[])
{
	if (argc<4) //not enough arguments
	{
		fprintf(stderr,"error: not enough arguments\n");
		return 1;
	}
	else if (argc>4) //too many arguments
	{
		fprintf(stderr,"error: too many arguments\n");
		return 1;
	}

	char *a1, *a2, *a3;
	double U_0 = strtod(argv[1], &a1);
	if (argument_check(*a1))
	{
		fprintf(stderr,"error: invalid arguments\n");
		return 1;
	}
	double R = strtod(argv[2], &a2);
	if (argument_check(*a2))
	{
		fprintf(stderr,"error: invalid arguments\n");
		return 1;
	}
	double eps = strtod(argv[3], &a3);
	if (argument_check(*a3))
	{
		fprintf(stderr,"error: invalid arguments\n");
		return 1;
	}

	if ((U_0<0) || (R<0) || (eps<0)) //condition for invalid arguments 
	{
		fprintf(stderr,"error: invalid arguments\n");
		return 1;
	}

	double U_p = 0;
	double I_p = 0;
	if (R==0) //condition for zero resistance
	{
		U_p = U_0;
		I_p = INFINITY;
	}
	else if (R==INFINITY) //condition for resistance = infinity
	{
		U_p = 0;
		I_p = 0;
	}
	else
	{
		U_p = diode (U_0, R, eps);
		I_p = diode_current (U_p);
	}
	printf("Up=%g V\nIp=%g A\n", U_p, I_p);
	return 0;
}
