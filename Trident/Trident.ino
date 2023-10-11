#include <Keyboard.h>
#include <Mouse.h>

#define CMD_JUMP   1
#define CMD_SHOOT  2
#define CMD_AIM    3
#define CMD_RCS    4

void setup() {
  Keyboard.begin();
  Serial.begin(128000);
}
void loop() {
  if (Serial.available()) {
    int cmd = Serial.read();
    switch (cmd) {
      case CMD_JUMP: {
        Mouse.move(0, 0, -10);
      }
      break;
      case CMD_SHOOT: {
        Mouse.click(MOUSE_LEFT);
      }
      break;
      case CMD_RCS: {
        Mouse.move(-1, 2, 0);
      }
      break;
      case CMD_AIM: {
        char delta_x = static_cast<char>(Serial.read());
        char delta_y = static_cast<char>(Serial.read());
        Mouse.move(delta_x, delta_y, 0);
        }
      break;
    }
  }
}
