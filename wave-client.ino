#include "InputDebounce.h"

#define BUTTON_DEBOUNCE_DELAY   20   // [ms]

static const int ledL1 = 7;
static const int ledL2 = 8;
static const int ledL3 = 9;
static const int ledL4 = 10;
static const int ledL5 = 11;
static const int linia1 = 2;
static const int linia2 = 3;
static const int linia3 = 4;
static const int linia4 = 5;
static const int linia5 = 6;

static InputDebounce senzorLinia1; // not enabled yet, setup has to be called first, see setup() below
static InputDebounce senzorLinia2;
static InputDebounce senzorLinia3;
static InputDebounce senzorLinia4;
static InputDebounce senzorLinia5;

void pressedCallback(uint8_t pinIn)
{
  // handle pressed state
  if(pinIn == 2){
    digitalWrite(ledL1, HIGH);
    Serial.println("1");
  } 
  else if(pinIn == 3){
    digitalWrite(ledL2, HIGH);
    Serial.println("2");
  }
  else if(pinIn == 4){
    digitalWrite(ledL3, HIGH);
    Serial.println("3");
  }
  else if(pinIn == 5){
    digitalWrite(ledL4, HIGH);
    Serial.println("2A");
  }
  else if(pinIn == 6){
    digitalWrite(ledL5, HIGH);
    Serial.println("3A");
  }
}

void releasedCallback(uint8_t pinIn)
{
  // handle released state
  if(pinIn == 2)
    digitalWrite(ledL1, LOW);
  else if(pinIn == 3)
    digitalWrite(ledL2, LOW);
  else if(pinIn == 4)
    digitalWrite(ledL3, LOW);
  else if(pinIn == 5)
    digitalWrite(ledL4, LOW);
  else if(pinIn == 6)
    digitalWrite(ledL5, LOW);  
}

void setup()
{
  // initialize digital pin as an output
  pinMode(ledL1, OUTPUT);
  pinMode(ledL2, OUTPUT);
  pinMode(ledL3, OUTPUT);
  pinMode(ledL4, OUTPUT);
  pinMode(ledL5, OUTPUT);
  
  // init serial
  Serial.begin(9600);
  
   senzorLinia1.registerCallbacks(pressedCallback, releasedCallback, NULL, NULL); // no continuous pressed-on time duration, ...
   senzorLinia2.registerCallbacks(pressedCallback, releasedCallback, NULL, NULL); 
   senzorLinia3.registerCallbacks(pressedCallback, releasedCallback, NULL, NULL); 
   senzorLinia4.registerCallbacks(pressedCallback, releasedCallback, NULL, NULL);
   senzorLinia5.registerCallbacks(pressedCallback, releasedCallback, NULL, NULL);
   
   senzorLinia1.setup(linia1, DEFAULT_INPUT_DEBOUNCE_DELAY, InputDebounce::PIM_EXT_PULL_UP_RES, 150);
   senzorLinia2.setup(linia2, DEFAULT_INPUT_DEBOUNCE_DELAY, InputDebounce::PIM_EXT_PULL_UP_RES, 150);
   senzorLinia3.setup(linia3, DEFAULT_INPUT_DEBOUNCE_DELAY, InputDebounce::PIM_EXT_PULL_UP_RES, 150);
   senzorLinia4.setup(linia4, DEFAULT_INPUT_DEBOUNCE_DELAY, InputDebounce::PIM_EXT_PULL_UP_RES, 150);
   senzorLinia5.setup(linia5, DEFAULT_INPUT_DEBOUNCE_DELAY, InputDebounce::PIM_EXT_PULL_UP_RES, 150);
}

void loop()
{
  unsigned long now = millis();
  
  // poll button state
  senzorLinia1.process(now); // callbacks called in context of this function
  senzorLinia2.process(now);
  senzorLinia3.process(now);
  senzorLinia4.process(now);
  senzorLinia5.process(now);
  delay(1); // [ms]
}
