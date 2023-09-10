#include <rclcpp/rclcpp.hpp>
#include <tf2_ros/buffer.h>
#include <tf2_ros/transform_listener.h>
#include <tf2_ros/transform_broadcaster.h>
#include <tf2/LinearMath/Transform.h>
#include <geometry_msgs/msg/transform_stamped.hpp>

class MyTransformNode : public rclcpp::Node
{
public:
  MyTransformNode()
  : Node("my_transform_node"),
    tfBuffer_(this->get_clock()),
    tfListener_(tfBuffer_)
  {
    // Initialize Transform Broadcaster
    tfBroadcaster_ = std::make_shared<tf2_ros::TransformBroadcaster>(this);

    // Create a timer to update the transform
    timer_ = this->create_wall_timer(
      std::chrono::milliseconds(100),
      std::bind(&MyTransformNode::updateTransform, this));
  }

private:
  void updateTransform()
  {
    // Listen to the transforms
    geometry_msgs::msg::TransformStamped map_to_ndt;
    geometry_msgs::msg::TransformStamped odom_to_base;

    try {
      map_to_ndt = tfBuffer_.lookupTransform("map", "ndt_base_link", tf2::TimePointZero);
      odom_to_base = tfBuffer_.lookupTransform("odom", "base_link", tf2::TimePointZero);
    } catch (tf2::TransformException & ex) {
      RCLCPP_WARN(this->get_logger(), "%s", ex.what());
      return;
    }

    // Compute the new transform (this is a simplified example; you'll need to replace this with your actual logic)
    geometry_msgs::msg::TransformStamped map_to_odom;
    map_to_odom.header.stamp = this->now();
    map_to_odom.header.frame_id = "map";
    map_to_odom.child_frame_id = "odom";
    map_to_odom.transform.translation.x = map_to_ndt.transform.translation.x - odom_to_base.transform.translation.x;
    map_to_odom.transform.translation.y = map_to_ndt.transform.translation.y - odom_to_base.transform.translation.y;
    map_to_odom.transform.translation.z = map_to_ndt.transform.translation.z - odom_to_base.transform.translation.z;
    map_to_odom.transform.rotation = map_to_ndt.transform.rotation;  // Simplified; you may want to compute the rotation differently

    // Broadcast the new transform
    tfBroadcaster_->sendTransform(map_to_odom);
  }

  tf2_ros::Buffer tfBuffer_;
  tf2_ros::TransformListener tfListener_;
  std::shared_ptr<tf2_ros::TransformBroadcaster> tfBroadcaster_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MyTransformNode>());
  rclcpp::shutdown();
  return 0;
}
