#include "FrameProcessor.hpp"

cv::Mat FrameProcessor::process(const cv::Mat& input, ProcessingMode mode, int brightness) {
    if (input.empty()) return input;
    
    cv::Mat result;
    input.copyTo(result);
    
    result.convertTo(result, -1, 1, brightness - 50);
    
    switch (mode) {
        case ProcessingMode::INVERT: 
            cv::bitwise_not(result, result); 
            break;
        case ProcessingMode::BLUR: 
            cv::GaussianBlur(result, result, cv::Size(15, 15), 0); 
            break;
        case ProcessingMode::CANNY: 
            cv::cvtColor(result, result, cv::COLOR_BGR2GRAY); 
            cv::Canny(result, result, 100, 200); 
            break;
        default: 
            break;
    }
    return result;
}