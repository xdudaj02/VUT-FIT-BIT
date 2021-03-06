/**
 * @file main.cpp
 * @brief Main file for simulator. Parameters' handler and main loop is located here.
 * @author Peter Vano, xvanop01
 * @author Jakub Duda, xdudaj02
 * @date 12.12.2021
 */

/** @mainpage
 * Welcome to documentation of Covid simulator project!\n
 * Default values used in this project were taken from statistics actual at the beginning of the december 2021.
 * @section Makefile
 * In Makefile, you can find all commands that you will need to operate the simulator:\n
 * make all - compile source codes and creates program.\n
 * make run [ARGS='[PARAM ARGUMENT]'] - launch program with parameter defined as [PARAM ARGUMENT]
 * (for example: make run ARGS='-p 100')\n
 * make pack - make .tar file with whole project.\n
 * make doc - create Doxygen documentation.\n
 * make clean - delete files generated by Makefile.\n
 * @section contents Project contents
 * |-src/\n
 * |  |-Positive_human.cpp\n
 * |  |-Positive_human.h\n
 * |  |-Stats.cpp\n
 * |  |-Stats.h\n
 * |-doxygen.config\n
 * |-main.cpp\n
 * |-Makefile\n
 * |-README\n
 */

#include <iostream>
#include <unistd.h>
#include "src/Stats.h"

/**
 * @brief Convert string in optarg to unsigned integer using std::stoi()
 */
#define INTEGER_ARGUMENT(argument, save_to) \
    try { \
        int integer = std::stoi(optarg); \
        if (integer >= 0) { \
            save_to = integer; \
        } else { \
            std::cerr << "Argument" << argument << "must be greater than 0! Ignoring argument.\n"; \
        } \
    } catch (std::invalid_argument& e) { \
        std::cerr << "Ignoring invalid argument for " << argument << ": " << e.what() << std::endl; \
    } catch (std::out_of_range& e) { \
        std::cerr << "Argument for " << argument << " is out of range for an integer: " << e.what() << std::endl; \
    }

/**
 * @brief Convert string to float number between 0 and 1 using std::stof()
 */
#define FLOAT_ARGUMENT(argument, save_to) \
    try { \
        float number = std::stof(optarg); \
        if (number >= 0 && number <= 1) { \
            save_to = number; \
        } else { \
            std::cerr << "Argument" << argument << "must be between 0 and 1! Ignoring argument.\n"; \
        } \
    } catch (std::invalid_argument& e) { \
        std::cerr << "Ignoring invalid argument for " << argument << ": " << e.what() << std::endl; \
    } catch (std::out_of_range& e) { \
        std::cerr << "Argument for " << argument << " is out of range for a float: " << e.what() << std::endl; \
    }

/**
 * @brief Prints help message to std::cout.
 */
void help(){
    std::cout << "This is a COVID-19 simulator. You can change what waves look like by setting\n";
    std::cout << "different reproduction numbers in different intervals. You can do that inside\n";
    std::cout << "the for loop in the main function (in the file main.cpp).\n\n";
    std::cout << "Usage: ./covid_simulator [PARAMETERS]\n";
    std::cout << "Each parameter, except -h needs argument and following parameters are valid:\n";
    std::cout << "  -h    Print help message.\n";
    std::cout << "  -d  [ARGUMENT]  Set duration of the simulation in days. How many simulation's\n" <<
                 "        steps will be done. ARGUMENT should be an integer larger than 0.\n";
    std::cout << "  -p  [ARGUMENT]  Set total population at the start of the simulation. ARGUMENT\n" <<
                 "        should be an integer larger than 0.\n";
    std::cout << "  -i  [ARGUMENT]  Set number of infected people at the start of the simulation.\n" <<
                 "        Those people are already infectious. ARGUMENT should be an integer\n" <<
                 "        larger than 0.\n";
    std::cout << "  -v  [ARGUMENT]  Set a percentage of the population, that is vaccinated.\n" <<
                 "        ARGUMENT should be a float number between 0 and 1 (including both),\n" <<
                 "        where 0 is 0% and 1 is 100%.\n";
    std::cout << "  -m  [ARGUMENT]  Set a chance of having mask, when person came to contact with\n" <<
                 "        the virus. By default, this chance is adaptive based on the infectious\n" <<
                 "        population (1% for each 10000 infectious). Using this parameter will\n" <<
                 "        make it static. ARGUMENT should be a float number between 0 and 1\n" <<
                 "        (including both), where 0 is 0% and 1 is 100%.\n";
    std::cout << "  -e  [ARGUMENT]  Set mask's efficiency. Chance, that mask will protect person\n" <<
                 "        from being infected. ARGUMENT should be a float number between 0 and 1\n" <<
                 "        (including both), where 0 is 0% and 1 is 100%.\n";
    std::cout << "  -n  [ARGUMENT]  Set how many new people enter the simulation. This value is\n" <<
                 "        used as an argument for normal distribution. ARGUMENT should be\n" <<
                 "        an integer larger than or equal to 0.\n";
    std::cout << "  -c  [ARGUMENT]  Set total hospital capacity. This is limit how many people\n" <<
                 "        can be hospitalized at the same time. If someone new need\n" <<
                 "        hospitalization, and there isn't free capacity. Patient will die.\n" <<
                 "        ARGUMENT should be an integer larger than or equal to 0.\n";
    std::cout << "  -a  [ARGUMENT]  Set virus incubation. This value is used as an argument for\n" <<
                 "        normal distribution. ARGUMENT should be an integer larger than or\n" <<
                 "        equal to 0.\n";
    std::cout << "  -r  [ARGUMENT]  Set patient's recovery duration. This value is used as\n" <<
                 "        an argument for normal distribution. ARGUMENT should be an integer\n" <<
                 "        larger than or equal to 0.\n";
    std::cout << "  -s  [ARGUMENT]  Set a decisive point for the patient. This point is symbolize\n" <<
                 "        the duration after which patient's fate will be decided. This point has\n" <<
                 "        meaning only when patient was also hospitalized (had hard symptoms).\n" <<
                 "        The value is used as an argument for normal distribution. ARGUMENT\n" <<
                 "        should be an integer larger than or equal to 0.\n";
    std::cout << "  -u  [ARGUMENT]  Set an immunity duration. How long will person be immune to\n" <<
                 "        the virus after successful recovery. Argument should be an integer\n" <<
                 "        larger than 0.\n";
    std::cout << "  -t  [ARGUMENT]  Set a chance of being protected by immunity, if vaccinated.\n" <<
                 "        ARGUMENT should be a float number between 0 and 1 (including both),\n" <<
                 "        where 0 is 0% and 1 is 100%.\n";
    std::cout << "  -o  [ARGUMENT]  Set a chance of being hospitalized when virus' incubation is\n" <<
                 "        over, if vaccinated. ARGUMENT should be a float number between 0 and 1\n" <<
                 "        (including both), where 0 is 0% and 1 is 100%.\n";
    std::cout << "  -b  [ARGUMENT]  Set a chance of death when patient reach decisive point\n" <<
                 "        and is hospitalized, if patient was vaccinated. ARGUMENT should be\n" <<
                 "        a float number between 0 and 1 (including both), where 0 is 0%\n" <<
                 "        and 1 is 100%.\n";
    std::cout << "  -f  [ARGUMENT]  Set a chance of being protected by immunity, if unvaccinated.\n" <<
                 "        ARGUMENT should be a float number between 0 and 1 (including both),\n" <<
                 "        where 0 is 0% and 1 is 100%.\n";
    std::cout << "  -g  [ARGUMENT]  Set a chance of being hospitalized when virus' incubation is\n" <<
                 "        over, if unvaccinated. ARGUMENT should be a float number between 0\n" <<
                 "        and 1 (including both), where 0 is 0% and 1 is 100%.\n";
    std::cout << "  -j  [ARGUMENT]  Set a chance of death when patient reach decisive point\n" <<
                 "        and is hospitalized, if patient was unvaccinated. ARGUMENT should be\n" <<
                 "        a float number between 0 and 1 (including both), where 0 is 0%\n" <<
                 "        and 1 is 100%.\n";
}

/**
 * @brief Main function of the program. It handles the parameters and includes main loop which represents days.
 */
int main(int argc, char* argv[]) {
    auto statistics = new Stats();
    int option;
    unsigned int duration = 365;
    while ((option = getopt(argc, argv, "hd:p:i:v:m:e:n:c:a:r:s:u:t:o:b:f:g:j")) != -1) {
        switch (option) {
            case 'h':
                help();
                delete statistics;
                return 0;
            case 'd': // simulation duration
                INTEGER_ARGUMENT("-d", duration)
                break;
            case 'p': // total population
                INTEGER_ARGUMENT("-p", statistics->total_population)
                break;
            case 'i': // infected population
                INTEGER_ARGUMENT("-i", statistics->ill_population)
                break;
            case 'v': // vaccinated population {0 (none) - 1 (all)}
                FLOAT_ARGUMENT("-v", statistics->vaccinated)
                break;
            case 'm': // chance of having mask when meeting infected
                FLOAT_ARGUMENT("-m", statistics->percentage_of_population_using_masks)
                statistics->masks_defined = true;
                break;
            case 'e': // mask efficiency
                FLOAT_ARGUMENT("-e", statistics->mask_effectiveness)
                break;
            case 'n': // new population entering simulation each day
                INTEGER_ARGUMENT("-n", statistics->daily_new_population)
                break;
            case 'c': // hospital capacity
                INTEGER_ARGUMENT("-c", statistics->hospital_capacity)
                statistics->free_hospital_capacity = statistics->hospital_capacity;
                break;
            case 'a': // virus incubation
                INTEGER_ARGUMENT("-a", statistics->virus_incubation)
                break;
            case 'r': // recovery point
                INTEGER_ARGUMENT("-r", statistics->recovery)
                break;
            case 's': // decisive point for patients
                INTEGER_ARGUMENT("-s", statistics->decisive_point)
                break;
            case 'u': // immunity duration
                INTEGER_ARGUMENT("-u", statistics->immunity_duration)
                if (statistics->immunity_duration == 0) {
                    statistics->immunity_duration = 1;
                }
                break;
            case 't': // vaccine protection
                FLOAT_ARGUMENT("-o", statistics->vaccinated_risks.protection)
                break;
            case 'o': // vaccinated population hospitalization probability
                FLOAT_ARGUMENT("-h", statistics->vaccinated_risks.chance_of_hospitalization_need)
                break;
            case 'b': // vaccinated population death risk
                FLOAT_ARGUMENT("-b", statistics->vaccinated_risks.risk_of_death)
                break;
            case 'f': // default protection
                FLOAT_ARGUMENT("-f", statistics->unvaccinated_risks.protection)
                break;
            case 'g': // unvaccinated population hospitalization probability
                FLOAT_ARGUMENT("-g", statistics->unvaccinated_risks.chance_of_hospitalization_need)
                break;
            case 'j': // unvaccinated population death risk
                FLOAT_ARGUMENT("-j", statistics->unvaccinated_risks.risk_of_death)
                break;
            default:
                std::cerr << "Ignoring invalid option \"" << (char)optopt << "\"" << std::endl;
                break;
        }
    }
    if (statistics->ill_population > statistics->total_population) {
        statistics->ill_population = statistics->total_population;
        std::cerr << "Starting ill population is greater than total population - decreasing number.\n";
    }
    statistics->init();
    
    std::cout << "Launching simulation with following parameters:\n";
    std::cout << "-d  Simulation duration     " << duration << std::endl;
    statistics->print();

    std::cout << "Day\tPopulation\tInfectious\tInfected\tHospitalized\tImmune\tDeaths\n";
    for (unsigned int i = 0; i < duration; i++) { // main loop
        // set of ifs generating waves by manipulating with reproduction number's range
        if (i % 30 == 0) {
            statistics->min_reproduction = 1;
            statistics->max_reproduction = 3;
        } else if (i % 15 == 0 && i % 45 != 0) {
            statistics->min_reproduction = 0.5;
            statistics->max_reproduction = 1.2;
        } else if (i % 20 == 0 && i % 40 != 0) {
            statistics->min_reproduction = 0.9;
            statistics->max_reproduction = 1.7;
        }

        std::cout << i << "\t";
        statistics->another_day();
    }

    delete statistics;
    return 0;
}