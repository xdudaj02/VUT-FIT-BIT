/**
 * @file Stats.h
 * @brief Main file for simulator. Parameters' handler and main loop is located here.
 * @author Peter Vano, xvanop01
 * @author Jakub Duda, xdudaj02
 * @date 12.12.2021
 */

#ifndef IMS_STATS_H
#define IMS_STATS_H

#include "Positive_human.h"
#include <iostream>
#include <random>
#include <cmath>
#include <cstring>

/**
 * @brief Struct for storing probabilities, that differentiates between population.
 */
struct risks {
    float protection; /**< Number between 0 and 1 (including) for chance of being protected by virus. */
    float chance_of_hospitalization_need; /**< Number between 0 and 1 (including) for chance of being hospitalized. */
    float risk_of_death; /**< Number between 0 and 1 (including) for chance of dying. */
};

/**
 * @brief Class remembering simulation's parameters and executing simulation's steps.
 */
class Stats {
public:
    /**
     * @brief Constructor of the class, setting default values to variables.
     * @warning This isn't enough to start simulation, void init() must be also used.
     */
    Stats();
    /**
     * @brief Do memory allocation and initial infected people creation.
     * @note This should be called right before simulation's start.
     */
    void init();
    /**
     * @brief Destructor of the class.
     */
    ~Stats();
    /**
     * @brief Function doing one simulation's step and printing statistics to std::out in TSV format.
     */
    void another_day();
    /**
     * @brief Print simulation's parameters and their values.
     */
    void print();

    unsigned int total_population; /**< Total population in the simulation. */
    unsigned int ill_population; /**< Population, that is infectious and therefore known as infected. */
    float min_reproduction; /**< Minimum value of the reproduction number, can be changed during simulation. */
    float max_reproduction; /**< Maximum value of the reproduction number, can be changed during simulation. */
    float vaccinated; /**< Float number between 0 and 1 (including) representing the population, that is vaccinated. */
    float percentage_of_population_using_masks; /**< Chance, that person had mask when was in contact with the virus. */
    bool masks_defined; /**< Variable storing if mask parameter was defined or dynamic (default) change will be used. */
    float mask_effectiveness; /**< Float number between 0 and 1 (including) representing mask's effectiveness. */
    unsigned int daily_new_population; /**< Number of people entering simulation daily. */
    unsigned int hospital_capacity; /**< Maximum value of patients, that can be hospitalized at the same time. */
    unsigned int free_hospital_capacity; /**< Number representing how many more patients can be hospitalized */
    unsigned int virus_incubation; /**< Number for poisson's distribution for the duration of the virus' incubation. */
    unsigned int recovery; /**< Number for poisson's distribution for the duration of the patient recovery. */
    /**
     * Number for poisson's distribution for the time needed to make the decision, if patient dies.
     */
    unsigned int decisive_point;
    unsigned int immunity_duration; /**< Number representing how long will person be immune after recovery. */
    struct risks unvaccinated_risks; /**< Structure storing risks for unvaccinated people. */
    struct risks vaccinated_risks; /**< Structure storing risks for vaccinated people. */

private:
    /**
     * @brief Function for managing immune people. Moves values in unsigned int* immune and prepares it for another day.
     */
    void move_immune();

    unsigned int total_immune; /**< Actual number of people, that are immune among the population. */
    unsigned int new_infectious; /**< Number storing how much people became infectious during day. */
    unsigned int deaths; /**< Total number of people, that died. */
    /**
     * Has field for each day of unsigned int immunity_duration to store people with that many days remaining.
     */
    unsigned int* immune;
    std::vector<Positive_human*> humans; /**< Vector storing all currently infected people */
};


#endif //IMS_STATS_H
