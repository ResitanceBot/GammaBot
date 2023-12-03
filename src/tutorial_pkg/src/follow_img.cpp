#include <ros/ros.h>
#include <std_msgs/Float32MultiArray.h>
#include <geometry_msgs/Twist.h>
#include <opencv2/opencv.hpp>

#define OBJECT_TO_FOLLOW 2
#define CAMERA_WIDTH    640 // left 0, right 640

#define MIN_ANG_VEL     0.15f
#define MAX_ANG_VEL     0.5f
#define ANGULAR_GAIN    2e-3 // 0.002 rad/s for each pixel of difference

ros::Publisher vel_pub;
geometry_msgs::Twist vel_msg;

void objectCallback(const std_msgs::Float32MultiArrayPtr &object)
{
    int obj_x_pos;
    float ang_vel;

    // Reset linear and angular speed value
    vel_msg.linear.x = 0;
    vel_msg.angular.z = 0;

    if (object->data.size() > 0){
        int id = object->data[0];
        float objectWidth = object->data[1];
        float objectHeight = object->data[2];

        cv::Mat cvHomography(3, 3, CV_32F);
        std::vector<cv::Point2f> inPts, outPts;
        switch (id)
        {
        case OBJECT_TO_FOLLOW:
        
            // Matrix completion
            for(int i=0; i<9; i++){
                cvHomography.at<float>(i%3, i/3) = object->data[i+3];
            }

            // Save corners to vector
            inPts.push_back(cv::Point2f(0, 0));
            inPts.push_back(cv::Point2f(objectWidth, 0));
            inPts.push_back(cv::Point2f(0, objectHeight));
            inPts.push_back(cv::Point2f(objectWidth, objectHeight));
            cv::perspectiveTransform(inPts, outPts, cvHomography);

            obj_x_pos = (outPts.at(0).x + outPts.at(1).x + outPts.at(2).x + outPts.at(3).x) / 4;
            ang_vel = ANGULAR_GAIN*(CAMERA_WIDTH/2 - obj_x_pos);

            // Set angular speed
            if(ang_vel <= -MIN_ANG_VEL || ang_vel >= MIN_ANG_VEL){
                vel_msg.angular.z = std::max(-MAX_ANG_VEL, std::min(ang_vel, MAX_ANG_VEL));
            }
            ROS_INFO("id: %d\t ang_vel: %f", id, vel_msg.angular.z);
            break;
        }
    }

    vel_pub.publish(vel_msg);
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "follow_obj");
    ros::NodeHandle n("~");
    ros::Subscriber sub = n.subscribe("/objects", 1, objectCallback);
    ros::Rate loop_rate(30);
    vel_pub = n.advertise<geometry_msgs::Twist>("/cmd_vel", 1);
    while (ros::ok())
    {
        ros::spinOnce();
        loop_rate.sleep();
    }
}