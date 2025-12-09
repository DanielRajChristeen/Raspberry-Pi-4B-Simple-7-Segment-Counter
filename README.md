# **Raspberry Pi 4B – Simple 7-Segment Counter**

<img src= "https://github.com/DanielRajChristeen/Raspberry-Pi-4B-Simple-7-Segment-Counter/blob/258b61db86f1173bf83ace07dbd3b93f4fce5c08/hardware-circuit.jpg">

This project demonstrates how to build a **simple counter system** using a **Raspberry Pi 4B**, **two push buttons**, and a **single 7-segment display**.
The counter updates from **0 to 9**, displaying the current value and reacting to button presses in real time.

* **Button 1 → Increment**
* **Button 2 → Decrement**
* **Display shows digits 0–9**
* **Debounced + edge-detected inputs**
* **Optimized for clean GPIO handling**

A perfect hands-on project for beginners learning Raspberry Pi hardware interfacing, GPIO outputs, and state-based logic.

---

## **1. Project Concept**

The system is built on a very straightforward hardware–logic flow:

1. **Two buttons** are connected as GPIO inputs with internal pull-up resistors.
2. A **7-segment LED display** is driven using **seven GPIO output pins**, each controlling one segment (A–G).
3. A `count` variable (0–9) is updated based on button presses.
4. The display refreshes **only when the count changes** to reduce GPIO switching.
5. Button presses are captured using **falling-edge detection** with **software debouncing**.

This foundation mimics real-world embedded design patterns involving:

* input event handling
* output visualization
* state tracking
* hardware abstraction layers

---

## **2. Hardware Requirements**

* Raspberry Pi 4B
* 1× Common Cathode 7-Segment Display
* 2× Momentary Push Buttons
* 7× 220Ω–330Ω resistors (for segments)
* Breadboard & jumper wires
* Optional: tactile button caps, GPIO breakout

---

## **3. Wiring Overview**

### **3.1 Buttons (BCM numbering)**

| Function         | GPIO |
| ---------------- | ---- |
| Increment Button | 17   |
| Decrement Button | 18   |

Using internal pull-ups:

* **Idle state = HIGH**
* **Pressed = LOW**

### **3.2 7-Segment Segment Mapping**

| Segment | GPIO |
| ------- | ---- |
| A       | 2    |
| B       | 3    |
| C       | 4    |
| D       | 14   |
| E       | 15   |
| F       | 23   |
| G       | 24   |

Connect each segment → resistor → GPIO pin
Common cathode → GND

---

## **4. Code Explanation**

The full Python script is included in the repo (`COUNT_WITH_7_SEG_DISPLAY.py`).

### **4.1 Segment Definitions**

```python
SEGMENTS = {
    'A': 2, 'B': 3, 'C': 4, 'D': 14,
    'E': 15, 'F': 23, 'G': 24
}
```

Each logical segment name maps directly to a GPIO output pin.

### **4.2 Digit-to-Segment Mapping**

`DIGIT_MAP` defines which segments must light up for each number 0–9.

Example:

* `0` lights up A, B, C, D, E, F
* `1` lights up B, C
* `8` lights all segments

### **4.3 Display Logic**

```python
def display_digit(number):
    clear_display()
    for seg in DIGIT_MAP[number]:
        GPIO.output(SEGMENTS[seg], GPIO.HIGH)
```

* Clears the display
* Selectively turns ON the segments for the requested digit

### **4.4 Button Logic**

Two key principles:

#### **1. Edge Detection**

Only count on transitions:

```python
if (inc == GPIO.LOW) and (pre_inc == GPIO.HIGH):
    count += 1
```

#### **2. Debouncing**

Mechanical noise is filtered with:

```python
time.sleep(0.02)
```

### **4.5 Count Limiting**

Prevents invalid displays:

```python
if count < 0: count = 0
if count > 9: count = 9
```

### **4.6 Optimized Redraw**

Segment refresh happens **only when count changes**:

```python
if count != pre_count:
    display_digit(count)
```

This avoids unnecessary GPIO switching.

---

## **5. Running the Project**

### **5.1 Install Dependencies**

```bash
sudo apt update
sudo apt install python3-rpi.gpio
```

### **5.2 Run the Script**

```bash
sudo python3 COUNT_WITH_7_SEG_DISPLAY.py
```

### **5.3 Use the Buttons**

* Press increment → value goes up
* Press decrement → value goes down
* Range is always bound 0–9

Stop the program with **Ctrl + C**.

---

## **6. Future Enhancements**

Some evolution paths you can explore:

* Add long-press acceleration (auto +1 every 100ms)
* Use **gpiozero** for a cleaner API
* Extend to **2-digit or 4-digit multiplexing**
* Add a “reset” button
* Replace 7-seg with an OLED or LCD

---

## **7. License**

This project is released under the **MIT License**.
See `LICENSE` file for full details.

---
