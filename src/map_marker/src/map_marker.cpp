#include <ros/ros.h>
#include <visualization_msgs/Marker.h>
#include <math.h>
#include <tf/transform_listener.h>

int main(int argc, char** argv)
{
    ros::init(argc, argv, "map_marker");

    ros::NodeHandle nh;
    ros::Publisher vis_pub = nh.advertise<visualization_msgs::Marker>( "/visualization_marker", 0 );
    ros::Rate r(5);

    visualization_msgs::Marker marker;
    tf::TransformListener tf_listener;
    tf::StampedTransform tf_map_to_marker;

    while (ros::ok())
    {
        ros::spinOnce();

            // tf_listener.waitForTransform("marker", "map", ros::Time(0), ros::Duration(1000.0));
            // tf_listener.lookupTransform("marker", "map", ros::Time(0), tf_map_to_marker);

            marker.header.frame_id = "marker";
            marker.header.stamp = ros::Time();
            marker.ns = "my_namespace";
            marker.id = 0;
            marker.type = visualization_msgs::Marker::SPHERE;
            marker.action = visualization_msgs::Marker::ADD;
            marker.pose.position.x = 0.0;
            marker.pose.position.y = 0.0;
            marker.pose.position.z = 0.0;
            marker.pose.orientation.x = 0.0;
            marker.pose.orientation.y = 0.0;
            marker.pose.orientation.z = 0.0;
            marker.pose.orientation.w = 1.0;
            marker.scale.x = 0.1;
            marker.scale.y = 0.1;
            marker.scale.z = 0.1;
            marker.color.a = 1.0;
            marker.color.r = 1.0;
            marker.color.g = 1.0;
            marker.color.b = 0.0;

            vis_pub.publish( marker );
        r.sleep();
    }

    return 0;
}