#include "CameraProvider.hpp"

CameraProvider::CameraProvider(int deviceId) {
    cap.open("/home/nikmir/Desktop/lab7/video.mp4");
}

CameraProvider::~CameraProvider() {
    if (cap.isOpened()) cap.release();
}

cv::Mat CameraProvider::getFrame() {
    cv::Mat frame;
    cap >> frame;
    return frame;
}

bool CameraProvider::isOpened() const {
    return cap.isOpened();
}
