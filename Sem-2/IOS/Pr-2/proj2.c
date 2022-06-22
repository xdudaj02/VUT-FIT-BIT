// ************************************ //
//                                      //
//                proj2.c               //
//              version 1.0             //
//          Jakub Duda, xdudaj02        //
//              24. 4. 2020             //
//                                      //
// ************************************ //

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>
#include <pthread.h>
#include <semaphore.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/mman.h>
#include <signal.h>
#include <unistd.h>

//typedef structure Tstate - structure for shared data
typedef struct State{
    int action_count; //action counter
    int imm_in_waiting; //imms inside building, not checked, not confirmed (NE)
    int imm_checked_waiting; //imms inside building, checked, not confirmed (NC)
    int imm_in; //all imms in building (NB)
    bool judge_in; //bool: true if judge is in the building
    bool fork_fail; //bool: indicates whether fork fail occured
} Tstate;

//constants and enums
const int argLimits[] = {1, 0, 2000};
enum person {judge, imm};
const char *messages[] = {"starts", "wants to enter", "enters", "checks", "wants certificate", "got certificate", "waits for imm", "starts confirmation", "ends confirmation", "leaves", "finishes"};
enum message {start, want_to_enter, enter, check_in, want_cert, get_cert, wait_for_imm, start_conf, end_conf, leave, finish};

FILE *pFile; //file
Tstate *state; //Tstate structure
pid_t *process; //structure for all process pids

//semaphores
sem_t *memory_use = NULL;
sem_t *building_entry = NULL;
sem_t *checking_in = NULL;
sem_t *all_in_checked = NULL;
sem_t *confirmation = NULL;
sem_t *judge_written = NULL;
sem_t *imm_written = NULL;

//returns number of invalid arguments
int arg_check(char **argv){
    char *ptr;
    //checks if arguments are integer
    for (int i = 1; i < 6; i++){
        strtof(argv[i], &ptr);
        if ((ptr == argv[i]) || (atof(argv[i]) != atoi(argv[i]))) {
            return 1;
        }
    }
    //checks if arguments are in given range
    int wrong_args = atoi(argv[1]) < argLimits[0];
    for(int i = 2; i <= 5; i++){
        if (atoi(argv[i]) < argLimits[1] || atoi(argv[i]) > argLimits[2])
            wrong_args++;
    }
    return wrong_args;
}

//function for initialization of used objects
int initialize(int num_of_procs){
    srand(time(NULL)); //create seed for random generator

    if (!(pFile = fopen("proj2.out", "w")))  //open output file 'proj2.out'
        return 1;

    //map shared memory
    if ((state = mmap(NULL, sizeof(Tstate), PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0)) == MAP_FAILED)
        return 1;
    //set initial values
    state->action_count = 1;
    state->imm_in_waiting = 0;
    state->imm_checked_waiting = 0;
    state->imm_in = 0;
    state->judge_in = false;
    state->fork_fail = false;

    if ((process = mmap(NULL, num_of_procs * sizeof(pid_t), PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0)) == MAP_FAILED)
        return 1;
    for (int i = 0; i < num_of_procs; i++)
        process[i] = 0; //set initial values

    //initialization of semaphores
    //semaphore for shared memory access, init value = 1
    if ((memory_use = sem_open("xdudaj02_semaphore_no.1", O_CREAT | O_EXCL, 0666, 1)) == SEM_FAILED)
        return 1;
    //semaphore for building doors, init value = 1
    if ((building_entry = sem_open("xdudaj02_semaphore_no.2", O_CREAT | O_EXCL, 0666, 1)) == SEM_FAILED)
        return 1;
    //semaphore for check-in window, init value = 1
    if ((checking_in = sem_open("xdudaj02_semaphore_no.3", O_CREAT | O_EXCL, 0666, 1)) == SEM_FAILED)
        return 1;
    //semaphore to determine if all imms in building are also checked, init value = 0
    if ((all_in_checked = sem_open("xdudaj02_semaphore_no.4", O_CREAT | O_EXCL, 0666, 0)) == SEM_FAILED)
        return 1;
    //semaphore for confirmation, init value = 0
    if ((confirmation = sem_open("xdudaj02_semaphore_no.5", O_CREAT | O_EXCL, 0666, 0)) == SEM_FAILED)
        return 1;
    //semaphore to determine whether judge has started/written its pid, init value = 1
    if ((judge_written = sem_open("xdudaj02_semaphore_no.6", O_CREAT | O_EXCL, 0666, 1)) == SEM_FAILED)
        return 1;
    //semaphore to determine whether an imm has started/written its pid, init value = 1
    if ((imm_written = sem_open("xdudaj02_semaphore_no.7", O_CREAT | O_EXCL, 0666, 1)) == SEM_FAILED)
        return 1;
    return 0;
} //end of initialize function

//function for deallocating resources
int clean_up(int num_of_procs){
    int cleanup_errs = 0; //error count
    //unmap shared memory
    cleanup_errs += munmap(state, sizeof(Tstate)); //unmap shared memory for the state of imms
    cleanup_errs += munmap(process, num_of_procs * sizeof(pid_t)); //unmap shared memory for process array

    //close semaphores
    cleanup_errs += sem_close(memory_use);
    cleanup_errs += sem_close(building_entry);
    cleanup_errs += sem_close(checking_in);
    cleanup_errs += sem_close(all_in_checked);
    cleanup_errs += sem_close(confirmation);
    cleanup_errs += sem_close(judge_written);
    cleanup_errs += sem_close(imm_written);

    //unlink semaphores
    cleanup_errs += sem_unlink("xdudaj02_semaphore_no.1");
    cleanup_errs += sem_unlink("xdudaj02_semaphore_no.2");
    cleanup_errs += sem_unlink("xdudaj02_semaphore_no.3");
    cleanup_errs += sem_unlink("xdudaj02_semaphore_no.4");
    cleanup_errs += sem_unlink("xdudaj02_semaphore_no.5");
    cleanup_errs += sem_unlink("xdudaj02_semaphore_no.6");
    cleanup_errs += sem_unlink("xdudaj02_semaphore_no.7");

    cleanup_errs += fclose(pFile); //close file
    return cleanup_errs;
} //end of clean_up function

//function to kill all processes stored in an array
void kill_procs(int who, int num_of_procs){
    state->fork_fail = true;
    for (int i = 1; i <= num_of_procs; i++) { //all processes
        if (process[i] != 0) //if not zero
            kill(process[i], SIGKILL);
    }
    if (who == judge) //if failed fork is judge
        kill(process[0], SIGKILL); //kill first process in array - imm generator
}

//custom sleep func, puts process asleep for random time from range <0 ; (milliseconds)arg> if arg != 0
void sleep_func(int millisecs){
    if (millisecs != 0){
        int time = (rand() % (millisecs + 1));
        usleep(time * 1000);
    }
}

//custom print func, prints a line to output file
void print_func(int person, int imm_no, int mess_no){
    bool detailed = true; //indicates if message contains information about state of imms
    switch (mess_no){
        case 0:
        case 1:
        case 10:
            detailed = false; //non detailed messages
            break;
        default:
            break;
    }
    fseek(pFile, 0, SEEK_END); //set position to end of file
    if (!detailed) { //detailed messages output
        if (!person) //judge message
            fprintf(pFile, "%i\t: JUDGE\t\t: %s\n", state->action_count, messages[mess_no]);
        else //imm message
            fprintf(pFile, "%i\t: IMM %i\t\t: %s\n", state->action_count, imm_no, messages[mess_no]);
    }
    else { //non detailed
        if (!person) //judge
            fprintf(pFile, "%i\t: JUDGE\t\t: %s\t\t: %i\t: %i\t: %i\n", state->action_count, messages[mess_no], state->imm_in_waiting, state->imm_checked_waiting, state->imm_in);
        else //imm
            fprintf(pFile, "%i\t: IMM %i\t\t: %s\t\t: %i\t: %i\t: %i\n", state->action_count, imm_no, messages[mess_no], state->imm_in_waiting, state->imm_checked_waiting, state->imm_in);
    }
    fflush(pFile); //flush the output file
    state->action_count++; //increment action count
}//end of print_func

//judge function, judge process code
void judge_func(int enter_time, int cert_time, int num_of_imms){
    int person = judge;
    int no = 0;
    int imms_left = num_of_imms; //number of imms not confirmed yet
    while(imms_left){ //if there are imms to be confirmed left
        sleep_func(enter_time); // sleep before entering
        sem_wait(memory_use);
            print_func(person, no, want_to_enter);
        sem_post(memory_use);
        sem_wait(building_entry); //close the building doors
            sem_wait(memory_use);
                state->judge_in = true;
                print_func(person, no, enter);
                int all_checked = state->imm_in_waiting - state->imm_checked_waiting; //number of imms in building but not checked
                if (all_checked){ //if imms in building but not checked exist
                    print_func(person, no, wait_for_imm);
                    sem_post(memory_use);
                    sem_wait(all_in_checked); //wait until all imms check
                } else {
                    sem_post(memory_use);
                }
            sem_wait(memory_use);
                print_func(person, no, start_conf);
                sleep_func(cert_time); //sleep - confirmation
                imms_left -= state->imm_checked_waiting; //substitute imms getting confirmed from 'imms to be confirmed' counter
                int i = state->imm_checked_waiting; //number of imms confirmed
                state->imm_in_waiting = 0; //no more imms waiting
                state->imm_checked_waiting = 0; //no more imms waiting
                for(int j = 0; j < i; j++) //allow all confirmed imms through
                    sem_post(confirmation);
                print_func(person, no, end_conf);
            sem_post(memory_use);
            sleep_func(cert_time); //sleep before leaving
            sem_wait(memory_use);
                print_func(person, no, leave);
                state->judge_in = false;
            sem_post(memory_use);
        sem_post(building_entry); //open building doors
    }
    sem_wait(memory_use);
        print_func(person, no, finish);
    sem_post(memory_use);
    exit(0);
} //end of judge_func

//immigrant function, code for imm process
void imm_func(int imm_no, int getcert_time){
    int person = imm;
    sem_wait(memory_use);
        print_func(person, imm_no, start);
    sem_post(memory_use);
    sem_wait(building_entry); //try to get into building
        sem_wait(memory_use);
            (state->imm_in_waiting)++;
            (state->imm_in)++;
            print_func(person, imm_no, enter);
        sem_post(memory_use);
    sem_post(building_entry); //doors are open for next entry
    sem_wait(checking_in); //try to check in
        sem_wait(memory_use);
            (state->imm_checked_waiting)++;
            print_func(person, imm_no, check_in);
            //if judge in the house and all imms inside are checked
            if ((state->judge_in) && (state->imm_in_waiting == state->imm_checked_waiting)) {
                    sem_post(all_in_checked); //signal that all imms in are checked
            }
        sem_post(memory_use);
    sem_post(checking_in); //leave check-in, open for next imm
    sem_wait(confirmation); //wait for confirmation start and then confirmation end
    sem_wait(memory_use);
        print_func(person, imm_no, want_cert);
    sem_post(memory_use);
    sleep_func(getcert_time); //sleep - getting certificate
    sem_wait(memory_use);
        print_func(person, imm_no, get_cert);
    sem_post(memory_use);
    sem_wait(building_entry); //try to exit building
        sem_wait(memory_use);
            (state->imm_in)--;
            print_func(person, imm_no, leave);
        sem_post(memory_use);
    sem_post(building_entry); //signal doors are empty
    process[imm_no] = 0;
    exit(0);
} //end of imm_func

//immigrants generator function, code for imm process generator process
void imm_gen_func(int num_of_imms, int gen_time, int getcert_time){
    //loop for creating desired number of imm processes
    for (int i = 1; i <= num_of_imms; i++) {
        sleep_func(gen_time); //sleep - imm generation time
        sem_wait(imm_written);
        pid_t imm = fork(); //fork immigrant
        if (imm < 0) { //fork fail
            fprintf(stderr, "Error. Process forking failed.\n");
            sem_wait(judge_written);
            sem_wait(memory_use);
                kill_procs(imm, num_of_imms + 2);
            sem_post(memory_use);
            exit(1);
        }
        else if (imm == 0) { //child process = immigrant
            imm_func(i, getcert_time);
        }
        else { //parent process = imm_generator
            sem_wait(memory_use);
                process[i] = imm;
            sem_post(memory_use);
            sem_post(imm_written);
        }
    }
    while ((wait(NULL))!=-1){} //wait for all imm processes to end
    exit(0);
} //end of imm_gen_func

//main function
int main(int argc, char **argv) {
    //number of arguments check
    if (argc != 6){
        fprintf(stderr, "Error. Invalid number of arguments.\n");
        return 1;
    }
    //call to function; for argument checking
    if (arg_check(argv)){
        fprintf(stderr, "Error. Invalid arguments.\n");
        return 1;
    }
    //argument initialization
    int num_of_imms = atoi(argv[1]);
    int imm_gen_time = atoi(argv[2]);
    int judge_enter_time = atoi(argv[3]);
    int imm_getcert_time = atoi(argv[4]);
    int judge_cert_time = atoi(argv[5]);

    //call to function for initializing shared memory and other needed resources
    if (initialize(num_of_imms + 2)) {
        fprintf(stderr, "Error. Initialization failed.\n");
        return 1;
    }

    pid_t imm_generator = fork(); //fork imm generator process
    if (imm_generator < 0){ //if fork failed
        fprintf(stderr, "Error. Process forking failed.\n");
    }
    else if (imm_generator == 0) { //child process = imm generator
        imm_gen_func(num_of_imms, imm_gen_time, imm_getcert_time);
    }
    else { //parent process
        process[0] = imm_generator;
        sem_wait(judge_written);
        pid_t judge = fork(); //fork judge process
        if (judge < 0){ //if fork failed
            fprintf(stderr, "Error. Process forking failed.\n");
            sem_wait(imm_written);
            sem_wait(memory_use);
                kill_procs(judge, num_of_imms + 2);
            sem_post(memory_use);
        }
        else if (judge == 0){ //child process = judge
            judge_func(judge_enter_time, judge_cert_time, num_of_imms);
        }
        else { //parent process
            sem_wait(memory_use);
                process[num_of_imms+1] = judge;
            sem_post(memory_use);
            sem_post(judge_written);
            wait(NULL); //wait for judge process to end
        }
        wait(NULL); //wait for imm generator process to end
    }

    int ret_val = state->fork_fail;

    //call to function for cleaning up shared memory and other needed resources
    if (clean_up(num_of_imms + 2)) {
        fprintf(stderr, "Error occurred when trying to free used resources.\n");
        return 1;
    }

    return ret_val;
} //end of main

//end of file proj2.c

