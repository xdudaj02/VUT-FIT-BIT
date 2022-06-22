/**
 * @file Positive_human.h
 * @brief Definition of infected person representation.
 * @author Peter Vano, xvanop01
 * @author Jakub Duda, xdudaj02
 * @date 12.12.2021
 */

#ifndef IMS_POSITIVE_HUMAN_H
#define IMS_POSITIVE_HUMAN_H

#include <random>

/**
 * @brief return values for patient's state.
 */
enum Next_day_return {
    IN_INCUBATION,
    BECAME_INFECTIOUS,
    HEALING,
    RECOVERED,
    DIED
};

/**
 * @brief Class representing infected person through whole illness.
 */
class Positive_human {
public:
    /**
     * @brief Constructor of the class preparing patient for his recovering.
     * @param virus_incubation Incubation of the virus.
     * @param illness_decisive_point Time to decisive point.
     * @param time_to_recovery Time to patient's full recovery.
     * @param chance_of_hospitalization Chance, that patient will need to be hospitalized after virus's incubation ends.
     * @param chance_of_death Chance, that patient will die if he is hospitalized when decisive point is reached.
     * @param init If virus_incubation is set to 0 and this is false, virus_incubation will be changed to 1.
     */
    explicit Positive_human(unsigned int virus_incubation, unsigned int illness_decisive_point,
        unsigned int time_to_recovery, float chance_of_hospitalization, float chance_of_death, bool init);
    /**
     * @brief Destructor of the class.
     */
    ~Positive_human();
    /**
     * @brief Executing one simulation's step for the patient.
     * @param free_hospital_capacity Pointer to position, where actual free capacity is located.
     * @return State of the patient after day.
     */
    Next_day_return next_day(unsigned int* free_hospital_capacity);

private:
    unsigned int incubation; /**< Stores how many days to virus' incubation. */
    bool hospitalization; /**< Stores if the patient was hospitalized. */
    unsigned int until_decisive_point; /**< Stores how many days to patient's decisive point. */
    unsigned int until_recovery; /**< Store how many days to patient's full recovery. */
    float probability_of_hospitalization; /**< Store chance, that patient will need hospitalization. */
    float probability_of_death; /**< Store chance, that patient will die if he was also hospitalized. */
};


#endif //IMS_POSITIVE_HUMAN_H
