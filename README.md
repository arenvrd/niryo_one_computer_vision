# niryo_one_computer_vision


1. open docker
2. run the following command in the command prompt

    ```bash
    docker run -it --rm -p 10000:10000 unity-robotics:pick-and-place /bin/bash
    ```
3. Run the following command to open the ROS workspace
    ```bash
    roslaunch niryo_moveit part_3.launch
    ```
4. Execution of the tasks
    - hand tracking
    - finger counting
