const int redPin1 = 7, yellowPin1 = 6, greenPin1 = 5;  
const int redPin2 = 8, yellowPin2 = 9, greenPin2 = 10; 

String lastCommand = "";

void setup() {
    pinMode(redPin1, OUTPUT);
    pinMode(yellowPin1, OUTPUT);
    pinMode(greenPin1, OUTPUT);

    pinMode(redPin2, OUTPUT);
    pinMode(yellowPin2, OUTPUT);
    pinMode(greenPin2, OUTPUT);

    Serial.begin(9600);
}

void switchLights(int greenLane) {
    if (greenLane == 1) {

        digitalWrite(greenPin2, LOW);
        digitalWrite(yellowPin2, HIGH);
        delay(1000);
        digitalWrite(yellowPin2, LOW);
        digitalWrite(redPin2, HIGH);

        digitalWrite(redPin1, LOW);
        digitalWrite(yellowPin1, HIGH);
        delay(1000);
        digitalWrite(yellowPin1, LOW);
        digitalWrite(greenPin1, HIGH);
    } 
    else if (greenLane == 2) {

        digitalWrite(greenPin1, LOW);
        digitalWrite(yellowPin1, HIGH);
        delay(1000);
        digitalWrite(yellowPin1, LOW);
        digitalWrite(redPin1, HIGH);

        digitalWrite(redPin2, LOW);
        digitalWrite(yellowPin2, HIGH);
        delay(1000);
        digitalWrite(yellowPin2, LOW);
        digitalWrite(greenPin2, HIGH);
    }
}

void loop() {
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');
        command.trim();
        Serial.println(command);

        if (command == "LANE1_GREEN" && lastCommand != "LANE1_GREEN") {
            switchLights(1);
            lastCommand = "LANE1_GREEN";
        }
        else if (command == "LANE2_GREEN" && lastCommand != "LANE2_GREEN") {
            switchLights(2);
            lastCommand = "LANE2_GREEN";
        }
    }
}
