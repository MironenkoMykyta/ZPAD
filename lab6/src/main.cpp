#include <opencv2/opencv.hpp>
#include "CameraProvider.hpp"
#include "KeyProcessor.hpp"
#include "FrameProcessor.hpp"
#include "Display.hpp"
#include <iostream>

int brightness_slider = 50;

void on_trackbar(int, void*) {}

int main() {
    CameraProvider camera(0);
    if (!camera.isOpened()) {
        std::cerr << "Camera not found!" << std::endl;
        return -1;
    }

    KeyProcessor keyProc;
    FrameProcessor frameProc;
    Display display("Lab 6 - OpenCV");

    cv::createTrackbar("Brightness", "Lab 6 - OpenCV", &brightness_slider, 100, on_trackbar);

    while (keyProc.isRunning()) {
        cv::Mat frame = camera.getFrame();
        if (frame.empty()) break;

        cv::Mat processed = frameProc.process(frame, keyProc.getMode(), brightness_slider);
        
        cv::putText(processed, "1:Norm 2:Inv 3:Blur 4:Canny ESC:Quit", 
                    cv::Point(10, 30), cv::FONT_HERSHEY_SIMPLEX, 0.6, cv::Scalar(0, 255, 0), 2);

        display.show(processed);

        int key = cv::waitKey(30);
        if (key >= 0) keyProc.processKey(key);
    }
    return 0;
}