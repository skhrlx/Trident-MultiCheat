#include <Keyboard.h>
#include <Mouse.h>

#define CMD_JUMP   1  // No arguments
#define CMD_SHOOT  2  // No arguments
#define CMD_AIM    3  // x, y -> how much to move mouse to in X and Y axis
#define CMD_RCS    4  // n - number of NOT dormant enemies (hp, weapon, position)
#define CMD_AFK    5

void setup() {
  delay(2000);
  Keyboard.begin();
  delay(2000);
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
