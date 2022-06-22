/**
 * @file Positive_human.cpp
 * @brief Implementation of Positive_human.h
 * @author Peter Vano, xvanop01
 * @author Jakub Duda, xdudaj02
 * @date 12.12.2021
 */

#include "Positive_human.h"


Positive_human::Positive_human(unsigned int virus_incubation, unsigned int illness_decisive_point,
    unsigned int time_to_recovery, float chance_of_hospitalization, float chance_of_death, bool init) { // constructor
    hospitalization = false;
    incubation = virus_incubation;
    if (incubation == 0 && !init) {
        // only people infected at the start of the simulation are infectious at the same day
        incubation++;
    }
    // time of the illness' points must be different
    until_decisive_point = illness_decisive_point;
    if (incubation >= illness_decisive_point) {
        until_decisive_point = virus_incubation + 1;
    }
    until_recovery = time_to_recovery;
    if (until_recovery <= until_decisive_point) {
        until_recovery = until_decisive_point + 1;
    }
    // store patient's chances
    probability_of_hospitalization = chance_of_hospitalization;
    probability_of_death = chance_of_death;
}

Positive_human::~Positive_human() = default; // destructor

Next_day_return Positive_human::next_day(unsigned int* free_hospital_capacity) { // one simulation's step for patient
    if (until_decisive_point > 0) { // IF #DECISION
        // patient's fate is not decided yet
        if (incubation > 0) { // IF #INCUBATION
            // virus is still in incubation
            incubation--;
            until_decisive_point--;
            until_recovery--;
            if (incubation == 0) { // incubation time reached, patient became infectious
                std::random_device hospital_device;
                std::mt19937 hospital_generator(hospital_device());
                std::uniform_real_distribution<> uni_hospital_distribution(0,1);
                // decision, if patient needs hospitalization
                if (uni_hospital_distribution(hospital_generator) <= probability_of_hospitalization) {
                    if (*free_hospital_capacity > 0) {
                        // there is room for patient, patient is being hospitalized
                        (*free_hospital_capacity)--;
                        hospitalization = true;
                    } else {
                        // patient didn't get needed care and died
                        return DIED;
                    }
                }
                return BECAME_INFECTIOUS;
            }
        } else { // ELSE #INCUBATION
            // incubation already ended
            until_decisive_point--;
            until_recovery--;
        }
        if (until_decisive_point == 0 && hospitalization) { // decisive point reached
            std::random_device death_device;
            std::mt19937 death_generator(death_device());
            std::uniform_real_distribution<> uni_death_distribution(0,1);
            if (uni_death_distribution(death_generator) <= probability_of_death) { // decision if patient dies
                // patient died
                if (hospitalization) {
                    (*free_hospital_capacity)++;
                }
                return DIED;
            }
        }
    } else { // ELSE #DECISION
        // patient's fate is already decided
        until_recovery--;
    } // END IF #DECISION

    // day's conclusion
    if (incubation > 0) {
        return IN_INCUBATION;
    } else if (until_recovery > 0) {
        return HEALING;
    } else {
        // patient successfully recovered and is healthy again
        if (hospitalization) {
            (*free_hospital_capacity)++;
        }
        return RECOVERED;
    }
}
