/**
 * @file Stats.cpp
 * @brief Implementation of Stats.h
 * @author Peter Vano, xvanop01
 * @author Jakub Duda, xdudaj02
 * @date 12.12.2021
 */

#include "Stats.h"

Stats::Stats() { // set class' variables to default values - values from the december 2021
    masks_defined = false;
    total_population = 10700000;
    ill_population = 223906;
    min_reproduction = 1;
    max_reproduction = 3;
    vaccinated = 0.6;
    percentage_of_population_using_masks = 0.25;
    mask_effectiveness = 0.95;
    daily_new_population = 302;
    hospital_capacity = 29669;
    free_hospital_capacity = hospital_capacity;
    virus_incubation = 2;
    recovery = 14;
    decisive_point = 7;
    immunity_duration = 180;
    unvaccinated_risks.protection = 0;
    unvaccinated_risks.chance_of_hospitalization_need = 0.048;
    unvaccinated_risks.risk_of_death = 0.25;
    vaccinated_risks.protection = 0.43;
    vaccinated_risks.chance_of_hospitalization_need = 0.15 * 0.048;
    vaccinated_risks.risk_of_death = 0.04;
}

void Stats::init() { // finish initialization of the class
    // memory allocation
    immune = (unsigned int*)malloc(immunity_duration * sizeof(unsigned int));

    // infected people creation
    new_infectious = ill_population / 100 * 15;
    std::random_device device;
    std::mt19937 generator(device());
    Positive_human* human;
    std::normal_distribution<> decisive_distribution(decisive_point);
    std::normal_distribution<> recovery_distribution(recovery);
    std::uniform_real_distribution<> probability_distribution(0,1);
    for (unsigned int i = 0; i < ill_population; i++) {
        if (probability_distribution(generator) <= vaccinated) {
            human = new Positive_human(0, decisive_distribution(generator), recovery_distribution(generator),
                                       vaccinated_risks.chance_of_hospitalization_need, vaccinated_risks.risk_of_death, true);
        } else {
            human = new Positive_human(0, decisive_distribution(generator), recovery_distribution(generator),
                                       unvaccinated_risks.chance_of_hospitalization_need, unvaccinated_risks.risk_of_death, true);
        }
        humans.push_back(human);
    }
}

Stats::~Stats() { // destructor
    free(immune);
    for (auto & human : humans) {
        delete human;
    }
}

void Stats::another_day() { // simulation's step
    move_immune();
    if (!masks_defined) { // if masks wasn't defined by parameters, there will be 1% for each 10000 infected
        percentage_of_population_using_masks = (float)ill_population / 1000000;
    }

    // infect new people based on reproduction number and last day cases
    std::random_device device;
    std::mt19937 generator(device());
    std::normal_distribution<> daily_new_people(daily_new_population);
    std::uniform_real_distribution<> uni_distribution(min_reproduction,max_reproduction);
    auto new_cases = (unsigned int)round(new_infectious * uni_distribution(generator));
    // if all were ill but no one new became infectious last day, new cases are based on already infected
    if (new_cases == 0) {
        new_cases = ill_population * 15 / 100;
    }
    // set new cases to maximal number if there should be more infected than there is healthy population
    if (new_cases > total_population - humans.size() - total_immune) {
        new_cases = total_population - humans.size() - total_immune;
    }
    new_infectious = 0; // counter for people that became infectious (virus incubation ended)
    Positive_human* human;
    std::uniform_real_distribution<> probability_distribution(0,1);
    std::normal_distribution<> incubation_distribution(virus_incubation);
    std::normal_distribution<> decisive_distribution(decisive_point);
    std::normal_distribution<> recovery_distribution(recovery);
    // creating new infected people
    for (unsigned int i = 0; i < new_cases; i++) {
        if (probability_distribution(generator) <= percentage_of_population_using_masks) {
            // had mask when was in contact with the virus
            if (probability_distribution(generator) <= mask_effectiveness) {
                // mask helped protect against the virus
                continue;
            }
        }
        if (probability_distribution(generator) <= vaccinated) { // was vaccinated
            if (probability_distribution(generator) <= vaccinated_risks.protection){
                // immunity by vaccine protected person
                continue;
            }
            // person infected
            human = new Positive_human(incubation_distribution(generator), decisive_distribution(generator),
                    recovery_distribution(generator), vaccinated_risks.chance_of_hospitalization_need,
                    vaccinated_risks.risk_of_death, false);
        } else { // wasn't vaccinated
            if (probability_distribution(generator) <= unvaccinated_risks.protection){
                // default immunity protected person
                continue;
            }
            // person infected
            human = new Positive_human(incubation_distribution(generator), decisive_distribution(generator),
                    recovery_distribution(generator), unvaccinated_risks.chance_of_hospitalization_need,
                    unvaccinated_risks.risk_of_death, false);
        }
        humans.push_back(human);
    }

    // next step of simulation for each infected person
    Next_day_return status;
    for (unsigned int i = 0; i < humans.size(); i++) {
        status = (humans[i]->next_day(&free_hospital_capacity));
        switch (status) {
            case HEALING:
            case IN_INCUBATION:
                break;
            case BECAME_INFECTIOUS: // disease became detectable
                ill_population++;
                new_infectious++;
                break;
            case RECOVERED: // patient recovered and is immune for immunity_duration days
                ill_population--;
                total_immune++;
                immune[immunity_duration - 1] += 1;
                delete humans[i];
                humans.erase(humans.begin() + i);
                break;
            case DIED: // patient died
                ill_population--;
                total_population--;
                deaths++;
                delete humans[i];
                humans.erase(humans.begin() + i);
                break;
        }
    }

    if (ill_population > humans.size()) {
        ill_population = humans.size();
    }
    // print stats of the day and prepare new population for the next one
    std::cout << total_population << "\t" << ill_population << "\t" << humans.size() <<"\t" << \
        hospital_capacity - free_hospital_capacity << "\t" << total_immune << "\t" << deaths << std::endl;
    total_population += (unsigned int)round(daily_new_people(generator));
}

void Stats::move_immune() {
    total_immune = immune[0];
    for (unsigned int i = 1; i < immunity_duration; i++) {
        total_immune += immune[i];
        immune[i-1] = immune[i];
    }
    immune[immunity_duration - 1] = 0;
}

void Stats::print() {
    std::cout << "-p  Total population        " << total_population << std::endl;
    std::cout << "-i  Infected population     " << ill_population << std::endl;
    std::cout << "-v  Vaccinated population   " << vaccinated << std::endl;
    if (masks_defined) {
        std::cout << "-m  Chance of having mask   " << percentage_of_population_using_masks << std::endl;
    } else {
        std::cout << "-m  Chance of having mask   " << "DYNAMIC" << std::endl;
    }
    std::cout << "-e  Mask efficiency         " << mask_effectiveness << std::endl;
    std::cout << "-n  Daily new population    " << daily_new_population << std::endl;
    std::cout << "-c  Hospital capacity       " << hospital_capacity << std::endl;
    std::cout << "-a  Virus incubation        " << virus_incubation << std::endl;
    std::cout << "-r  Patient's recovery      " << recovery << std::endl;
    std::cout << "-s  Decisive point          " << decisive_point << std::endl;
    std::cout << "-u  Immunity duration       " << immunity_duration << std::endl;
    std::cout << "Vaccinated population chances:" << std::endl;
    std::cout << "-t  Immunity protection     " << vaccinated_risks.protection << std::endl;
    std::cout << "-o  Hospitalization chance  " << vaccinated_risks.chance_of_hospitalization_need << std::endl;
    std::cout << "-b  Chance of death         " << vaccinated_risks.risk_of_death << std::endl;
    std::cout << "Unvaccinated population chances:" << std::endl;
    std::cout << "-f  Immunity protection     " << unvaccinated_risks.protection << std::endl;
    std::cout << "-g  Hospitalization chance  " << unvaccinated_risks.chance_of_hospitalization_need << std::endl;
    std::cout << "-j  Chance of death         " << unvaccinated_risks.risk_of_death << std::endl;
}