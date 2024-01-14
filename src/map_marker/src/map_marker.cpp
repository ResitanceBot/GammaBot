#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <visualization_msgs/Marker.h>
#include <cstdio>
#include "cnn_image_processing/ArucoDistOri.h"
#include <math.h>
#include <tf/transform_listener.h>
#include <tf/transform_broadcaster.h>

#define VALID_DISTANCE_LIMIT 500

int aruco_distance, aruco_angle;
float x_from_base_link, y_from_base_link;
bool flag_initial = false;

void arucoCallback(const cnn_image_processing::ArucoDistOri::ConstPtr &msg){
    aruco_distance = msg->distance;
    aruco_angle = msg->angle;
    x_from_base_link = (aruco_distance*cos(aruco_angle*M_PI/180.0))/1000.0;
    y_from_base_link = (aruco_distance*sin(aruco_angle*M_PI/180.0))/1000.0;
    flag_initial = true;

}

int main(int argc, char** argv)
{
    ros::init(argc, argv, "map_marker");

    ros::NodeHandle nh;
    ros::Publisher vis_pub = nh.advertise<visualization_msgs::Marker>( "/visualization_marker", 0 );
    ros::Subscriber sub = nh.subscribe("/aruco_dist_ori", 100, arucoCallback);
    ros::Rate r(5);

    visualization_msgs::Marker marker;
    tf::TransformListener tf_listener;
    static tf::TransformBroadcaster tf_br;
    tf::StampedTransform tf_map_to_marker;
    tf::Transform tf_base_link_to_marker;
    tf::Quaternion q;

    tf_base_link_to_marker.setOrigin(tf::Vector3(0.0,0.0,0.0));
    q.setRPY(0, 0, M_PI);
    tf_base_link_to_marker.setRotation(q);
    tf_br.sendTransform(tf::StampedTransform(tf_base_link_to_marker, ros::Time::now(), "base_link", "marker"));

    while (ros::ok())
    {
        ros::spinOnce();

        if (flag_initial){

            tf_base_link_to_marker.setOrigin(tf::Vector3(x_from_base_link,y_from_base_link,0.0));
            q.setRPY(0, 0, 0);
            tf_base_link_to_marker.setRotation(q);
            tf_br.sendTransform(tf::StampedTransform(tf_base_link_to_marker, ros::Time::now(), "base_link", "marker"));
            printf("\n\n\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n\n\n");
            tf_listener.waitForTransform("marker", "map", ros::Time::now(), ros::Duration(1000.0));
            tf_listener.lookupTransform("marker", "map", ros::Time(0), tf_map_to_marker);

            if(aruco_distance >= VALID_DISTANCE_LIMIT){
                marker.header.frame_id = "map";
                marker.header.stamp = ros::Time();
                marker.ns = "my_namespace";
                marker.id = 0;
                marker.type = visualization_msgs::Marker::SPHERE;
                marker.action = visualization_msgs::Marker::ADD;
                marker.pose.position.x = tf_map_to_marker.getOrigin().x();
                marker.pose.position.y = tf_map_to_marker.getOrigin().y();
                marker.pose.position.z = 0;
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
            }
            vis_pub.publish( marker );
        }
        r.sleep();
    }

    return 0;
}