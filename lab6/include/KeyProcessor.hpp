#pragma once

enum class ProcessingMode { NORMAL, INVERT, BLUR, CANNY };

class KeyProcessor {
private:
    ProcessingMode currentMode;
    bool running;
public:
    KeyProcessor();
    void processKey(int key);
    ProcessingMode getMode() const;
    bool isRunning() const;
};