#include "KeyProcessor.hpp"

KeyProcessor::KeyProcessor() : currentMode(ProcessingMode::NORMAL), running(true) {}

void KeyProcessor::processKey(int key) {
    if (key == 27 || key == 'q') running = false;
    else if (key == '1') currentMode = ProcessingMode::NORMAL;
    else if (key == '2') currentMode = ProcessingMode::INVERT;
    else if (key == '3') currentMode = ProcessingMode::BLUR;
    else if (key == '4') currentMode = ProcessingMode::CANNY;
}

ProcessingMode KeyProcessor::getMode() const {
    return currentMode;
}

bool KeyProcessor::isRunning() const {
    return running;
}