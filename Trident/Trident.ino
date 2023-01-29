#include <Keyboard.h>
#include <Mouse.h>

char incomingByte;

void setup() {
  delay(2000);
  Keyboard.begin();
  delay(2000);
  Serial.begin(128000);
}
void loop(){
  
  if(Serial.available()>0){
    incomingByte = Serial.read();
    if(incomingByte == 'l'){
      gc_bhop();
    }
    
    if(incomingByte == 'o'){
      mm_bhop();
    }

    if(incomingByte == 'k'){
      rcs();
    }

    if(incomingByte == 'i'){
      valorant_bhop();
    }

    if(incomingByte == 'j'){
      shoot_kb();
    }

    if(incomingByte == 'm'){
      left_ac();
    }

    if(incomingByte == 'n'){
      left_ac();
    }
    
  }
}


void mm_bhop(){
  Mouse.move(0, 0, 1);
}

void rcs(){
  Mouse.move(0, 1, 0);
}

void gc_bhop(){
  Keyboard.write('l');
  Keyboard.write('o');
  Keyboard.write('k');
  Keyboard.write('i');
 }

 
void shoot_kb(){
  Keyboard.write('l');
}

void valorant_bhop(){
  Keyboard.write('o');
}

void left_ac(){
  Mouse.click(MOUSE_LEFT);
}

void right_ac(){
  Mouse.click(MOUSE_RIGHT);
}
