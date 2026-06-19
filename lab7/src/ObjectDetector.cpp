#include "ObjectDetector.hpp"

ObjectDetector::ObjectDetector(const std::string& modelPath, const std::string& configPath) {
   // net = cv::dnn::readNetFromCaffe("/home/nikmir/Desktop/lab7/data/deploy.prototxt", "/home/nikmir/Desktop/lab7/data/mobilenet_iter_73000.caffmodel");
}

cv::Mat ObjectDetector::detect(const cv::Mat& frame) {
   // cv::Mat blob = cv::dnn::blobFromImage(frame, 1.0, cv::Size(300, 300), cv::Scalar(104.5, 177.1, 123.9));
    //net.setInput(blob);
    //cv::Mat detections = net.forward(); 
    return frame; 
}
