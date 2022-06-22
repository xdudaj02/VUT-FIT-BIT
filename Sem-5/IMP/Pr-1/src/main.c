#include <stdio.h>
#include <sys/time.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "driver/gpio.h"
#include "esp_system.h"
#include "nvs_flash.h"

#define GPIO_LED_RED  2  // led gpio
#define GPIO_INPUT    5  // input gpio

#define ESP_INTR_FLAG_DEFAULT 0
#define MSG_MAX 50  // maximum input sequence length

static xQueueHandle event_queue = NULL;  // event queue
const char decoded[] = {'-', 'E', 'I', 'S', 'H', 'V', 'U', 'F', '-', 'A', 'R', 'L', '-', 'W', 'P', 'J', 'T', 'N', 'D', 'B', 'X', 'K', 'C', 'Y', 'M', 'G', 'Z', 'Q', 'O', '-', '-'};
const int dash_jump[] = {16, 8, 4, 2};  // change of index when receiving dash input on different levels
const int dot_jump = 1;  // change of index when recieving dot input
int mc_level = 0;  // morse code level (number of received symbols), 0 by default
int mc_index = 0;  // morse code index (index in the decoded[] array), 0 by default
int between_letters = 0;  // indicates whether a letter has been processed and the program is waiting for the next symbol
struct timeval time_s;  // timeval object
int64_t start_us = 0;  // starting time of certain actions
char *message = NULL;  // char pointer for storing the read message
int msg_index = 0;  // index in the message array

// function for handling interrupts
static void IRAM_ATTR gpio_isr_handler(void* arg) {
    uint32_t gpio_num = (uint32_t) arg;  // get gpio number
    xQueueSendFromISR(event_queue, &gpio_num, NULL);  // append to event queue
}

// function for handling execution of the task
static void gpio_task(void* arg) {
    uint32_t io_num;
    gettimeofday(&time_s, NULL);  // get starting time
    start_us = ((int64_t)time_s.tv_sec * 1000000L + (int64_t)time_s.tv_usec) / 1000;  // get time in milliseconds

    // never ending loop
    while (1) {
        // if event in queue (blocking wait for 1500ms - new letter timeout)
        if(xQueueReceive(event_queue, &io_num, 150)) {
            gettimeofday(&time_s, NULL);  // get current time
            int64_t now_us = ((int64_t)time_s.tv_sec * 1000000L + (int64_t)time_s.tv_usec) / 1000;  // get time in milliseconds
            // ignore events for 200ms - debounce
            if (now_us - start_us >= 200) {
                vTaskDelay(50 / portTICK_RATE_MS);
                ESP_ERROR_CHECK(gpio_set_level(GPIO_LED_RED, !gpio_get_level(io_num)));  // set led state ('button' pressed = led on)
                // if event on falling edge ('button' is now pressed, 0 on gpio)
                if (!gpio_get_level(io_num)) {
                    // if program in state 'between letters'
                    if (between_letters) {
                        // if 4 seconds have passed since last action - new word timeout
                        if (now_us - start_us >= 4000) {
                            printf("\n");
                            message[msg_index % MSG_MAX] = ' ';  // append space
                            msg_index++;
                        }
                    }
                }
                // if event on raising edge ('button' is now not pressed, 1 on gpio)
                else {
                    between_letters = 0;
                    // if button was pressed for less then 700ms -> dot
                    if (now_us - start_us <= 700) {
                        printf(".");
                        fflush(stdout);
                        mc_index += dot_jump;
                        mc_level++;
                    // if button was pressed for more then 700ms -> dash
                    } else {
                        printf("-");
                        fflush(stdout);
                        mc_index += dash_jump[mc_level % 4];
                        mc_level++;
                    }
                }
                start_us = now_us;  // update time of last action
            }
        // if no event in queue and letter timeout has run out 
        } else {
            // if 'button' is not pressed, 1 on gpio
            if (gpio_get_level(io_num)) {
                gettimeofday(&time_s, NULL);
                int64_t now_us = ((int64_t)time_s.tv_sec * 1000000L + (int64_t)time_s.tv_usec) / 1000;
                // if any symbols were read
                if (mc_level) {
                    if (now_us - start_us >= 1500) {
                        // 4 symbols is maximum valid length
                        if (mc_level <= 4) {
                            char letter = decoded[mc_index];  // get decoded letter      
                            // if valid combination of symbols was entered
                            if (letter != '-'){
                                printf(" : '%c'\n", letter);
                                message[msg_index % MSG_MAX] = letter;  // append letter
                                msg_index++;
                            } else {
                                printf(" : invalid\n");  // not a valid letter
                            }
                        } else {
                            printf(" : invalid\n");  // not a valid letter
                        }
                        // reset morse code index and level
                        mc_level = 0;
                        mc_index = 0;
                        between_letters = 1;  // set state 'between letters'
                    }
                }
                // if 6 seconds from last action (new sequence timeout)
                if (now_us - start_us >= 6000) {
                    // if any letters were decoded
                    if (message[0] != '\0') {
                        // print decoded sequence and reset buffer
                        printf("%s\n\n", message);
                        for (int i = 0; i < (MSG_MAX); i++) {
                            message[i] = '\0';
                        }
                        msg_index = 0;
                        between_letters = 0;
                    }
                }
            }
        }
    }
}

// function for handling initialization
void gpio_init() {
    // initialize gpio for led (output)
    gpio_pad_select_gpio(GPIO_LED_RED);
    ESP_ERROR_CHECK(gpio_set_direction(GPIO_LED_RED, GPIO_MODE_OUTPUT));

    // initialize gpio for morse code input (input, interrupt enabled, interrupt on any edge, use pullup resitor)
    gpio_pad_select_gpio(GPIO_INPUT);
    ESP_ERROR_CHECK(gpio_set_direction(GPIO_INPUT, GPIO_MODE_INPUT));
    ESP_ERROR_CHECK(gpio_intr_enable(GPIO_INPUT));
    ESP_ERROR_CHECK(gpio_set_intr_type(GPIO_INPUT, GPIO_INTR_ANYEDGE));
    ESP_ERROR_CHECK(gpio_set_pull_mode(GPIO_INPUT, GPIO_PULLUP_ENABLE));

    // interrupt settings
    gpio_install_isr_service(ESP_INTR_FLAG_DEFAULT);
    gpio_isr_handler_add(GPIO_INPUT, gpio_isr_handler, (void*) GPIO_INPUT);
    
    // initalize falsh memory
    ESP_ERROR_CHECK(nvs_flash_init());

    // initialize event queue
    event_queue = xQueueCreate(10, sizeof(uint32_t));

    // create task
    xTaskCreate(gpio_task, "gpio_task", 2048, NULL, 10, NULL);

    // set led status
    ESP_ERROR_CHECK(gpio_set_level(GPIO_LED_RED, !gpio_get_level(GPIO_INPUT)));

    // initialize buffer for read sequence
    message = (char*)malloc((MSG_MAX + 1) * sizeof(char));
    for (int i = 0; i < (MSG_MAX); i++) {
        message[i] = '\0';
    }
    message[MSG_MAX] = '\0';
}

void app_main() {
    gpio_init();

    // never ending loop
    while(1) {
        vTaskDelay(100 / portTICK_RATE_MS);
    }
}
