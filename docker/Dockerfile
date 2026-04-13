########################################################################
#### Ubuntu
########################################################################
FROM ubuntu:24.04 AS base

ARG DEBIAN_FRONTEND=noninteractive
ARG ROS_DISTRO=jazzy

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    ROS_DISTRO=${ROS_DISTRO}

# Base OS deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    gnupg2 \
    lsb-release \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

########################################################################
#### NVIDIA graphics drivers
########################################################################
RUN apt update && apt install -y --no-install-recommends \
    libglvnd0 \
    libgl1 \
    libglx0 \
    libegl1 \
    libxext6 \
    libx11-6 \
    libgles2 \
    && rm -rf /var/lib/apt/lists/*

ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=graphics,utility,compute
ENV TURTLEBOT3_MODEL=burger

########################################################################
#### BUild tools and common dependencies
########################################################################
RUN apt update && apt install -q -y --no-install-recommends \
    build-essential \
    bash-completion \
    cmake \
    dirmngr \
    git \
    gnupg2 \
    lsb-release \
    wget \
    curl \
    clang \
    ca-certificates \
    iputils-ping \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

########################################################################
#### ROS2 installation + Gazebo
########################################################################

RUN apt update && apt install -y curl gnupg lsb-release \
    && curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null \
    && apt update && apt install -y ros-jazzy-ros-base

RUN apt update && apt install -y --no-install-recommends \
    ros-${ROS_DISTRO}-ros-base \
    ros-${ROS_DISTRO}-ros-gz \
    ros-${ROS_DISTRO}-turtlesim \
    ros-${ROS_DISTRO}-demo-nodes-cpp \
    ros-${ROS_DISTRO}-demo-nodes-py \
    ros-${ROS_DISTRO}-turtlebot3 \
    ros-${ROS_DISTRO}-turtlebot3-simulations \
    ros-${ROS_DISTRO}-nav2-bringup \
    ros-${ROS_DISTRO}-joint-state-publisher-gui \
    ros-${ROS_DISTRO}-ros2-control \
    ros-${ROS_DISTRO}-ros2-controllers \
    && rm -rf /var/lib/apt/lists/*

# install packages
RUN apt update && apt install -q -y --no-install-recommends \
    python3-apt \
    python3-colcon-common-extensions \
    python3-colcon-mixin \
    python3-pip \
    python3-rosdep \
    python3-testresources \
    python3-vcstool \
    python3-colcon-common-extensions \
    python3-pytest \
    python3-pytest-cov \
    python3-setuptools \
    python3-flake8 \
    python3-flake8-blind-except \
    python3-flake8-builtins \
    python3-flake8-class-newline \
    python3-flake8-comprehensions \
    python3-flake8-deprecated \
    python3-flake8-docstrings \
    python3-flake8-import-order \
    python3-flake8-quotes \
    python3-pytest-rerunfailures \
    python3-requests \
    nlohmann-json3-dev \
    && rm -rf /var/lib/apt/lists/*


# Initialize rosdep
RUN rosdep init && \
    rosdep update

COPY . /opt/ws/src/code

########################################################################
#### Setup entrypoint
########################################################################
COPY docker/entrypoint.bash /entrypoint.bash
RUN chmod +x /entrypoint.bash
ENTRYPOINT ["/entrypoint.bash"]

CMD ["bash"]
