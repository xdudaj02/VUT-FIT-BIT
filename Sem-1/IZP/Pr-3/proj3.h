#ifndef PROJ3_H
#define PROJ3_H
:
/**
* @file		proj3.h
* @brief        Header file for a maze solving program
* @author	Jakub Duda (xdudaj02)
* @date		22.12.2019
* @version	1.0
*/

/**
* @brief Structure to represent the map of the maze.
*/
typedef struct {
    int rows;			/**<number of rows in the map		*/
    int cols;			/**<number of columns in the map	*/
    unsigned char *cells;	/**<pointer to the first cell of the map*/
} Map;

/**
* @brief bit values of individual borders
*/
enum borders { 
	BLEFT=0x1,	/**<the bit specifying the left border	*/
	BRIGHT=0x2,	/**<the bit specifying the right border	*/
	BTOP=0x4,  	/**<the bit specifying the top border	*/ 
	BBOTTOM=0x4 	/**<the bit specifying the bottom border*/
};

/**
* @brief	function for freeing the memory used by a map structure
* @pre		map pointer must be pointing to an existent Map structure 
* @post		memory used by map structure should be freed
* @param[in]	*map	pointer to a Map structure
*/
void free_map(Map *map);

/**
* @brief	function for initializing the map structure
* @details	function opens a file, allocates memory for a Map structure, checks allocation success,
assigns values from the file to this Map structure, closes the file and based on succes rate returns an integer
* @pre		Map pointer must be existent
* @pre		filename must be a name of an accessible file
* @post		map pointer has a non null value and points to a Map structure that is properly initialized
* @param[in]	*map		pointer to a Map structure to have memory allocated for itself and to be wrtitten to
* @param[in]	*filename	pointer to a constant char that is a filename of the file to be opened, read and closed
* @return       0 if map structure was initialized correctly
*/
int load_map(const char *filename, Map *map);

/**
* @brief	function to check the state of a given side of a certain cell in the maze
* @pre		map pointer must be assigned and pointing to a valid Map structure
* @pre		parameters r and c must have integer values in the range of the maze size 
* @pre		parameter border must have one of the borders enumeration values
* @post		no special postconditions
* @param[in]	*map	pointer to a Map structure
* @param[in]	r	the row number
* @param[in]	c	the column number
* @param[in]	border	integer value indicating which side is to be checked
* @return       true if the given side is a wall
* @return       false if the given side is not a wall
*/
bool isborder(Map *map, int r, int c, int border);

/**
* @brief	function to check whether the given cell has a wall on its bottom side
* @pre		parameters r and c must have integer values in the range of the maze size
* @post		no special postconditions
* @param[in]	r	the row number
* @param[in]    c       the column number
* @return	true if the bottom side of the given cell is a wall
* @return	false if the bottom side of the given cell is not a wall
*/
bool hasbottom(int r, int c);

/**
* @brief	function to determine the first direction to try to go to from the entry cell
* @pre		the pointer map points to a valid initialized map structure
* @pre		parameters r and c are both integers in the range of the map size
* @pre		parameter leftright is an integer number with one of the two specific values
* @post		program knows which direction to go to
* @param[in]	*map		pointer to a Map structure which is to be read
* @param[in]	r		the row number 
* @param[in]	c		the column number
* @param[in]	leftright	integer value inidicating to which side to turn on crossroads
* @return	integer with one of the values of the borders enumeration 
*/
int start_border(Map *map, int r, int c, int leftright);

/**
* @brief	function for checking the validity of the Map structure
* @pre		map pointer points to an initialized Map structure
* @post		validity of the concrete Map structure is known
* @param[in]	*map	pointer pointing to a Map structure
* @return       integer value based on the result of the validity check
*/
int check_map(Map *map);

/**
* @brief	function for loading and checking the validity of a Map structure
* @details	function calls function load_map to load a Map structure and then calls 
the check_map function to check the validity of this Map_structure
* @pre		pointer map had been created
* @pre		pointer filename is the name of an existant and accessible file 
* @post		pointer map points to a Map structure and its validity was tested
* @param[in]	*filename	pointer to a char constant that is a name of a file to be opened, read from and then closed 	
* @param[in]	*map		pointer to a Map structure 
* @return       integer value based on the result of the validity check
*/
int load_and_check_map(const char *filename, Map *map);

/**
* @brief	function to check whether the current position is within the maze
* @pre		pointer map points to a valid and initialized Map structure
* @pre		parameters r and c are both integer values in the range of the maze size
* @post		program knows whether it has already exited the maze or not
* @param[in]	*map	pointer to a Map structure
* @param[in]	r	the row number of the cell to be checked
* @param[in]	c	the column number of the cell to be checked
* @return	true in case the given coordinates are of a cell that is outside of the maze
* @return       false in case the given coordinates are not of a cell that is outside of the maze
*/
bool is_out(Map *map, int r, int c);

/**
* @brief	function for printing out coordinates of the cells passed on the way through the maze
* @pre		the pointer map points to a valid and initialized Map structure
* @pre          parameters r and c are both integers in the range of the map size
* @pre          parameter leftright is an integer number with one of the two specific values
* @post		coordinates of all cells passed on the way through the maze were printed out
* @param[in]	*map		pointer to a Map structure
* @param[in]    r               the row number
* @param[in]    c               the column number
* @param[in]    leftright       integer value inidicating to which side to turn on crossroads
*/
void print_path(Map *map, int r, int c, int leftright);

#endif
