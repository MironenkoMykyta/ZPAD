#pragma once
#include <opencv2/opencv.hpp>
#include "ObjectDetector.hpp"
#include "KeyProcessor.hpp"


class FrameProcessor {
private:
	ObjectDetector* detector;
public:
	FrameProcessor();
	~FrameProcessor();
	cv::Mat process(const cv::Mat& input, ProcessingMode mode, int brightness);
};
