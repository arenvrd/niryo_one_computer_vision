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
      - Download the hand tracking Unity project on following link: https://drive.google.com/drive/u/0/folders/1MAdrQnk41cZzv3r1LkEkDQfhxCFg8P_x
      - launch the _HandTracking.py_ script 
      - Run the Unity project
      - Move the orbot
	
    - finger counting
        - Download the Finger Counter Unity project on following link: https://drive.google.com/drive/u/0/folders/1hW28iVmVSTmGeHNyQtn1y-85rIHlRVDW
         - launch the _FingersCounter.py_ script 
        - Run the Unity project
        - Move the orbot
