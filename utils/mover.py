#!/usr/bin/env python3
from geometry_msgs.msg import Twist
from math import pi
import rospy


class Mover:
    """
    Class that incorporates the commands to move the robot.
    """

    def __init__(self):
        """
        Define the publisher where the commands are sent.
        """
        self.base_movement = rospy.Publisher('/mobile_base_controller/cmd_vel', Twist, queue_size = 15)

    def go_left(self, speed: float, distance: float):
        """
        Makes the robot go to the left by specifying the speed in meters per
        second and the time in deciseconds.
        """
        self.rotate('counterclockwise', 90, 30)
        self.go_forward(speed, distance)
        self.rotate('clockwise', 90, 30)

    def go_right(self, speed: float, distance: float):
        """
        Makes the robot go to the right by specifying the speed in meters per
        second and the time in deciseconds.
        """
        self.rotate('clockwise', 90, 30)
        self.go_forward(speed, distance)
        self.rotate('counterclockwise', 90, 30)

    def rotate(self, rotation_type: str, angle: int, speed: int):
        """
        Rotates the robot clockwise/counterclockwise by specifying the angle in
        degrees and the speed in degrees/sec.
        """
        angular_speed = speed * 2 * pi / 360
        relative_angle = angle * 2 * pi / 360

        velocity = Twist()

        if rotation_type == 'clockwise':
            velocity.angular.z = -abs(angular_speed)
        elif rotation_type == 'counterclockwise':
            velocity.angular.z = abs(angular_speed)
        else:
            raise TypeError(F'Unknown rotation type {rotation_type}.')

        t_0 = rospy.Time.now().to_sec()
        current_angle = 0

        while current_angle < relative_angle:
            self.base_movement.publish(velocity)
            t_1 = rospy.Time.now().to_sec()
            current_angle = angular_speed * (t_1 - t_0)

        velocity = Twist()
        self.base_movement.publish(velocity)

    def go_forward(self, speed: float, distance: float):
        """
        Makes the robot go forward by specifying the speed in meters per second
        and the distance in meters.
        """
        velocity = Twist()
        velocity.linear.x = abs(speed)

        t_0 = rospy.Time.now().to_sec()
        current_distance = 0

        while current_distance < distance:
            self.base_movement.publish(velocity)
            t_1 = rospy.Time.now().to_sec()
            current_distance = speed * (t_1 - t_0)

        velocity = Twist()
        self.base_movement.publish(velocity)

    def go_back(self, speed: float, distance: float):
        """
        Makes the robot go back by specifying the speed in meters per second
        and the distance in meters.
        """
        velocity = Twist()
        velocity.linear.x = -abs(speed)

        t_0 = rospy.Time.now().to_sec()
        current_distance = 0

        while current_distance < distance:
            self.base_movement.publish(velocity)
            t_1 = rospy.Time.now().to_sec()
            current_distance = speed * (t_1 - t_0)

        velocity = Twist()
        self.base_movement.publish(velocity)


if __name__ == '__main__':
    rospy.init_node('test')
    mover = Mover()
    mover.go_back(1, 1)
    rospy.sleep(7)
    mover.go_forward(1, 1)
