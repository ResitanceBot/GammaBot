#include <ros/ros.h>
#include "cnn_image_processing/ArucoDistOri.h"
#include <math.h>
#include <tf/transform_broadcaster.h>


float x_from_base_link, y_from_base_link;

void arucoCallback(const cnn_image_processing::ArucoDistOri::ConstPtr &msg){
    int aruco_distance = msg->distance;
    int aruco_angle = msg->angle;
    x_from_base_link = (aruco_distance*cos(aruco_angle*M_PI/180.0))/1000.0;
    y_from_base_link = (aruco_distance*sin(aruco_angle*M_PI/180.0))/1000.0;
}

int main(int argc, char** argv)
{
    ros::init(argc, argv, "marker_tf_broadcaster");

    ros::NodeHandle nh;
    ros::Subscriber sub = nh.subscribe("/aruco_dist_ori", 100, arucoCallback);
    ros::Rate r(5);

    tf::TransformBroadcaster tf_br;
    tf::Transform tf_base_link_to_marker;
    tf::Quaternion q;

    while (ros::ok())
    {
        ros::spinOnce();
        tf_base_link_to_marker.setOrigin(tf::Vector3(x_from_base_link,y_from_base_link,0.0));
        q.setRPY(0, 0, M_PI);
        tf_base_link_to_marker.setRotation(q);
        tf_br.sendTransform(tf::StampedTransform(tf_base_link_to_marker, ros::Time::now(), "base_link", "marker"));
        printf("alo");

        r.sleep();
    }

    return 0;
}