#pragma once
#include <opencv2/opencv.hpp>
#include <opencv2/dnn.hpp>

class ObjectDetector {
private:
    cv::dnn::Net net;
public:
    ObjectDetector(const std::string& modelPath, const std::string& configPath);
    cv::Mat detect(const cv::Mat& frame);
};