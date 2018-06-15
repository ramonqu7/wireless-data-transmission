#ifndef __EMPTY_PACKAGE_H__
#define __EMPTY_PACKAGE_H__

#include <ros/ros.h>

class RgbdCompress {
 public:
  explicit RgbdCompress();
  ~RgbdCompress();

  bool Initialize(const ros::NodeHandle& n);

 private:
  bool LoadParameters(const ros::NodeHandle& n);
  bool RegisterCallbacks(const ros::NodeHandle& n);

  std::string name_;
};

#endif
