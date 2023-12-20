#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <sensor_msgs/Joy.h>
#include <cstdio>

#define BREAKOUT_JOYSTICKS 0.4
//! Ajustar velocidades
#define INC_SPEED 0.1 
#define DEC_SPEED 0.1
#define MAX_SPEED 1
#define MIN_SPEED 0.1

// AXES
#define JOY_L_H 0
#define JOY_L_V 1
#define LT 2
#define JOY_R_H 3
#define JOY_R_V 4
#define RT 5
#define R_L 6
#define U_D 7

// BUTTONS
#define A 0
#define B 1
#define X 2
#define Y 3
#define LB 4
#define RB 5
#define SETTINGS 6
#define WINDOWS 7
#define XBOX 8
#define BJI 9
#define BJD 10

float SPEED = 0.5;
float SPEED_ANT = SPEED;

ros::Publisher pub;
ros::Subscriber sub;

void joyCallback(const sensor_msgs::Joy::ConstPtr& joy)
{
    geometry_msgs::Twist twist;

    // AJUSTE SPEED
    SPEED_ANT = SPEED;
    
    if(joy->axes[U_D] == 1){
      SPEED += INC_SPEED;
      if(SPEED > MAX_SPEED)
        SPEED = MAX_SPEED;
    }
    else if(joy->axes[U_D] == -1){
      if (SPEED >= 1) SPEED -= INC_SPEED;
      else SPEED -= DEC_SPEED;
      if(SPEED < MIN_SPEED)
        SPEED = MIN_SPEED;
    }

    if(joy->axes[R_L] == 1){
      SPEED = MIN_SPEED;
    }
    else if(joy->axes[R_L] == -1){
      SPEED = MAX_SPEED;
    }

    // FORWARD / BACKWARD (Avance/Retroceso)
    if(joy->axes[JOY_L_V] < -BREAKOUT_JOYSTICKS) twist.linear.x = SPEED * float(-1.0);
    else if(joy->axes[JOY_L_V] > BREAKOUT_JOYSTICKS) twist.linear.x = SPEED * float(1.0);
    // TURN LEFT / RIGHT (Rotacion)
    if(joy->axes[JOY_R_H] < -BREAKOUT_JOYSTICKS) twist.angular.z = 2*SPEED * float(-1.0);
    else if(joy->axes[JOY_R_H] > BREAKOUT_JOYSTICKS) twist.angular.z = 2*SPEED * float(1.0);


    // INTERFAZ TERMINAL
    printf("------------------------- \n");
    // FORWARD / BACKWARD (Avance/Retroceso)
    if(joy->axes[JOY_L_V] < -BREAKOUT_JOYSTICKS) printf("BACKWARD \n");
    else if(joy->axes[JOY_L_V] > BREAKOUT_JOYSTICKS) printf("FORWARD \n");
    // ROTATE LEFT / RIGHT (Rotacion)
    if(joy->axes[JOY_R_H] < -BREAKOUT_JOYSTICKS) printf("ROT.RIGHT \n");
    else if(joy->axes[JOY_R_H] > BREAKOUT_JOYSTICKS) printf("ROT.LEFT \n");
    // SPEED
    if(SPEED != SPEED_ANT) printf("SPEED = %f \n", SPEED);

    pub.publish(twist);
}

int main(int argc, char** argv)
{
    ros::init(argc, argv, "joy_to_cmd_vel");

    ros::NodeHandle nh;
    pub = nh.advertise<geometry_msgs::Twist>("cmd_vel", 1);
    sub = nh.subscribe("joy", 10, joyCallback);

    while (ros::ok())
    {
        ros::spinOnce();
    }

    return 0;
}