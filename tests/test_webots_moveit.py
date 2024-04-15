"""Test the `webots_spot` package with Nav2 and Moveit2."""

import os
import pytest
import rclpy
from nav_msgs.msg import Odometry
from sensor_msgs.msg import JointState
from launch import LaunchDescription
import launch_testing.actions
from rclpy.action import ActionClient
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription
from webots_ros2_tests.utils import TestWebots, initialize_webots_test

from moveit_msgs.msg import (
    Constraints,
    JointConstraint,
    MotionPlanRequest,
    PlanningOptions,
)
from moveit_msgs.action import MoveGroup


class MoveGroupActionClient:
    def __init__(self, node):
        self.__node = node
        self._action_client = ActionClient(self.__node, MoveGroup, "/move_action")
        self._action_client.wait_for_server()

    def send_goal(self):
        goal_msg = MoveGroup.Goal()

        motion_plan_request = MotionPlanRequest()

        motion_plan_request.workspace_parameters.header.stamp = (
            self.__node.get_clock().now().to_msg()
        )
        motion_plan_request.workspace_parameters.header.frame_id = "base_link"
        motion_plan_request.workspace_parameters.min_corner.x = -1.0
        motion_plan_request.workspace_parameters.min_corner.y = -1.0
        motion_plan_request.workspace_parameters.min_corner.z = -1.0
        motion_plan_request.workspace_parameters.max_corner.x = 1.0
        motion_plan_request.workspace_parameters.max_corner.y = 1.0
        motion_plan_request.workspace_parameters.max_corner.z = 1.0
        motion_plan_request.start_state.is_diff = True

        joints = {}
        joints["Slider11"] = 0.0
        joints["spotarm_1_joint"] = 0.0
        joints["spotarm_2_joint"] = 3.1415
        joints["spotarm_3_joint"] = 3.0
        joints["spotarm_4_joint"] = 0.0
        joints["spotarm_5_joint"] = 0.2
        joints["spotarm_6_joint"] = 0.2

        constraints = Constraints()
        for joint, angle in joints.items():
            jc = JointConstraint()
            jc.tolerance_above = 0.001
            jc.tolerance_below = 0.001
            jc.weight = 1.0
            jc.joint_name = joint
            jc.position = angle
            constraints.joint_constraints.append(jc)

        motion_plan_request.goal_constraints.append(constraints)

        motion_plan_request.pipeline_id = "move_group"
        motion_plan_request.group_name = "spot_arm"
        motion_plan_request.num_planning_attempts = 10
        motion_plan_request.allowed_planning_time = 5.0
        motion_plan_request.max_velocity_scaling_factor = 0.5
        motion_plan_request.max_acceleration_scaling_factor = 0.5
        motion_plan_request.max_cartesian_speed = 0.0

        planning_options = PlanningOptions()
        planning_options.plan_only = False
        planning_options.look_around = False
        planning_options.look_around_attempts = 0
        planning_options.max_safe_execution_cost = 0.0
        planning_options.replan = True
        planning_options.replan_attempts = 10
        planning_options.replan_delay = 0.1

        goal_msg.request = motion_plan_request
        goal_msg.planning_options = planning_options

        self._send_goal_future = self._action_client.send_goal_async(goal_msg)


@pytest.mark.rostest
def generate_test_description():
    initialize_webots_test()

    # Webots
    webots_spot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("sketch_nav_sim"),
                "launch",
                "spot_launch.py",
            )
        ),
        launch_arguments={"mode": "fast", "nav": "true"}.items(),
    )

    # Moveit2
    moveit = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("sketch_nav_sim"),
                "launch",
                "moveit_launch.py",
            )
        ),
        launch_arguments={"rviz": "false"}.items(),
    )

    return LaunchDescription(
        [
            webots_spot,
            moveit,
            launch_testing.actions.ReadyToTest(),
        ]
    )


class TestSpot(TestWebots):
    @classmethod
    def setUpClass(cls):
        rclpy.init()

    @classmethod
    def tearDownClass(cls):
        rclpy.shutdown()

    def setUp(self):
        self.__node = rclpy.create_node("driver_tester")
        self.wait_for_clock(self.__node, messages_to_receive=20)

    def testMoveitGoal(self):
        moveit = MoveGroupActionClient(self.__node)
        self.wait_for_clock(self.__node, messages_to_receive=1000)
        moveit.send_goal()

        def on_joint_state_message_received(message):
            for name, position in zip(message.name, message.position):
                if name == "spotarm_6_joint":
                    if position > 0.1:
                        return True
            return False

        self.wait_for_messages(
            self.__node,
            JointState,
            "/joint_states",
            condition=on_joint_state_message_received,
            timeout=60 * 5,
        )

    def tearDown(self):
        self.__node.destroy_node()
