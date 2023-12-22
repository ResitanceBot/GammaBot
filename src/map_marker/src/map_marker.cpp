#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <visualization_msgs/Marker.h>
#include <cstdio>

int main(int argc, char** argv)
{
    ros::init(argc, argv, "joy_to_cmd_vel");

    ros::NodeHandle nh;
    ros::Publisher vis_pub = node_handle.advertise<visualization_msgs::Marker>( "visualization_marker", 0 );
visualization_msgs::Marker marker;
marker.header.frame_id = "base_link";
marker.header.stamp = ros::Time();
marker.ns = "my_namespace";
marker.id = 0;
marker.type = visualization_msgs::Marker::SPHERE;
marker.action = visualization_msgs::Marker::ADD;
marker.pose.position.x = 1;
marker.pose.position.y = 1;
marker.pose.position.z = 1;
marker.pose.orientation.x = 0.0;
marker.pose.orientation.y = 0.0;
marker.pose.orientation.z = 0.0;
marker.pose.orientation.w = 1.0;
marker.scale.x = 1;
marker.scale.y = 0.1;
marker.scale.z = 0.1;
marker.color.a = 1.0; // Don't forget to set the alpha!
marker.color.r = 0.0;
marker.color.g = 1.0;
marker.color.b = 0.0;
//only if using a MESH_RESOURCE marker type:
marker.mesh_resource = "package://pr2_description/meshes/base_v0/base.dae";

    ros::Rate r(50);

    while (ros::ok())
    {
        ros::spinOnce();
        vis_pub.publish( marker );
        r.sleep();
    }

    return 0;
}