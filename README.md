# 👶 Smart Baby Monitor & RTSP Recorder
### *AI-Powered Sleep & Safety Monitoring System*

<div align="center">

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.12-green.svg)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

*Transform your IP camera into an intelligent baby monitoring system with real-time AI detection, sleep tracking, and safety alerts.*

</div>

![SnapShot](assets/snapshots/snapshot_1.png)

---

## 🌟 Features

### 🤖 **AI-Powered Detection**
- **Person Detection**: Advanced YOLOv8 model for accurate human detection
- **Smart Tracking**: DeepSORT algorithm for consistent person tracking across frames
- **Child Selection**: Click-to-select or automatic smallest-person detection

### 😴 **Sleep & Wake Monitoring**
- **Movement Detection**: Tracks child movement with configurable sensitivity
- **Sleep State Tracking**: Automatically detects when child falls asleep (customizable duration)
- **Wake Alerts**: Instant notifications when child wakes up and starts moving
- **Visual Indicators**: Real-time sleep/wake status overlay

### 🛡️ **Safety Features**
- **Fall Risk Detection**: Monitors if child moves near bed edges
- **Safe Zone Definition**: Automatic bed detection with customizable safety margins
- **Real-time Alerts**: Immediate notifications for potential safety risks
- **Persistent Monitoring**: Tracks multiple consecutive frames before triggering alerts

### 📹 **Recording & Storage**
- **Automatic Segmentation**: Videos split into configurable time segments (default: 30 minutes)
- **Organized Storage**: Files organized by date and time blocks for easy access
- **Dual Recording Modes**: Save raw footage or AI-annotated videos with detection overlays
- **Snapshot Capability**: Instant photo capture with keyboard shortcut

### 🔄 **Smart Connectivity**
- **RTSP Stream Support**: Compatible with IP cameras supporting RTSP protocol
- **MJPEG Stream Support**: Compatible with variety of devices that stream this protocol
- **Auto-Reconnection**: Intelligent reconnection on network interruptions
- **Buffering Optimization**: Low-latency streaming with minimal delay
- **Connection Status**: Visual indicators for stream health

### 👥 **Multi-User Web Interface**
- **Secure Authentication**: Login/signup system with role-based access control
- **Family Management**: Relationship-based user profiles (Mother, Father, Guardian, Caregiver)
- **Stream Permissions**: Admin control over who can view the live stream
- **Real-time Monitoring**: See which family members are currently watching
- **Activity Tracking**: Monitor user sessions and login history
- **Admin Dashboard**: Complete user management with enable/disable capabilities

---

### 📋 Prerequisites

- **Python 3.8+** installed on your system
- **IP Camera** with RTSP support (tested with TP-Link Tapo cameras)
- **Network Connection** between your computer and camera

### 🔧 Installation

#### Run with Docker (Recommended)

1. **Clone the Repository**
   ```bash
   git clone https://github.com/codeperfectplus/AI-Baby-Monitor.git
   cd AI-Baby-Monitor
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your RTSP camera credentials
   ```

3. **Deploy the application:**
   ```bash
   ./deploy.sh
   ```
4. **Access the Web Interface**
   Open your web browser and go to:
   ```
   http://localhost:8847
   ```

5. **Default Login Credentials**
   - **Username**: admin
   - **Password**: password
   - **⚠️ Change password after first login!**


#### Run with Python Script

1. **Clone the Repository**
   ```bash
   git clone https://github.com/codeperfectplus/AI-Baby-Monitor.git
   cd AI-Baby-Monitor
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Camera Settings**
   
   Copy and edit the environment file:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your camera credentials:
   ```env
   # RTSP Camera Configuration
   RTSP_USERNAME=your_camera_username
   RTSP_PASSWORD=your_camera_password
   RTSP_IP=192.168.1.100
   RTSP_PORT=554
   RTSP_STREAM=stream1
   ```

4. **Run the Web Application**
   ```bash
   python app.py
   ```

5. **Access the Interface**
   Open your browser and navigate to:
   ```
   http://localhost:8847
   ```

## 📷 Camera Setup Guide

### 🔍 Finding Your Camera's RTSP URL

#### **For TP-Link Tapo Cameras:**
1. **Enable RTSP** in the Tapo app:
   - Open Tapo app → Select your camera
   - Go to Settings → Advanced Settings → Camera Account
   - Enable "RTSP Authentication" and set username/password

2. **RTSP URL Format:**
   ```
   rtsp://username:password@camera_ip:554/stream1
   ```

#### **For Other IP Cameras:**
Common RTSP URL patterns:
- **Hikvision**: `rtsp://username:password@ip:554/Streaming/Channels/101`
- **Dahua**: `rtsp://username:password@ip:554/cam/realmonitor?channel=1&subtype=0`
- **Axis**: `rtsp://username:password@ip:554/axis-media/media.amp`
- **Foscam**: `rtsp://username:password@ip:554/videoMain`

### 🌐 Network Configuration

1. **Find Camera IP Address:**
   ```bash
   # Scan your network for connected devices
   nmap -sn 192.168.1.0/24
   
   # Or check your router's admin panel
   ```

2. **Test RTSP Connection:**
   ```bash
   # Using VLC Media Player
   vlc rtsp://username:password@camera_ip:554/stream1
   
   # Using FFmpeg
   ffprobe rtsp://username:password@camera_ip:554/stream1
   ```

---

## 👥 Web Interface & User Management

### 🔐 **Authentication System**

The application provides a comprehensive web-based interface with secure user management:

#### **User Roles & Relationships**
- **Father** - Full administrative access
- **Mother** - Full administrative access  
- **Guardian** - Limited monitoring access
- **Caregiver** - Supervised access with restricted features

#### **Admin Features**
- **User Management**: Create, edit, enable/disable user accounts
- **Stream Control**: Grant or revoke streaming permissions per user
- **Activity Monitoring**: See who's currently watching and their login history
- **Relationship Management**: Assign family roles to users

#### **Family Monitoring Dashboard**
- **Active Users Display**: Real-time view of family members currently monitoring
- **Session Tracking**: Monitor login times and activity duration
- **Permission Management**: Control access to live stream on per-user basis
- **Login History**: Track family member access patterns

#### **Security Features**
- **First-time Password Change**: Mandatory password update on initial login
- **Session Management**: Automatic timeout and secure session handling
- **IP Tracking**: Log access attempts with IP address and browser information
- **Account Status Control**: Enable/disable accounts without deletion

### 🌐 **Web Interface Navigation**

#### **Main Dashboard** (`/`)
- Live RTSP stream with AI detection overlays
- Real-time sleep/wake status monitoring
- Family activity indicators

#### **User Management** (`/auth/user-management`)
- Add new family members with relationship assignments
- Edit existing user profiles and permissions
- View comprehensive login history
- Enable/disable streaming access per user

#### **Authentication Pages**
- **Login** (`/auth/login`) - Secure access with remember me option
- **Signup** (`/auth/signup`) - New user registration with relationship selection
- **Password Management** (`/auth/change-password`) - Secure password updates

---

## 🔴 Real-Time Monitoring Features

### 👨‍👩‍👧‍👦 **Family Activity Tracking**
- **Live User Status**: See which family members are currently watching
- **Session Duration**: Track how long each user has been monitoring  
- **Relationship Display**: Identify watchers by their family role (Mother, Father, etc.)
- **Multi-User Support**: Multiple family members can monitor simultaneously

### 🎛️ **Admin Control Panel**
- **Stream Access Control**: Enable/disable streaming for specific users
- **User Account Management**: Create accounts for family members with specific relationships
- **Login History**: Comprehensive audit trail of family member access
- **Real-time Permissions**: Instantly grant or revoke monitoring access

### 🔐 **Security & Privacy**  
- **Relationship-Based Access**: Different permission levels based on family relationship
- **Secure Sessions**: Automatic timeout and secure session management
- **Activity Logging**: Track all user interactions for security purposes
- **Password Policies**: Enforce strong passwords and mandatory password changes

---

## 🎮 Controls & Interactions

### ⌨️ **Keyboard Shortcuts**

| Key | Action | Description |
|-----|--------|-------------|
| `Q` | **Quit** | Exit the application |
| `P` | **Pause/Resume** | Toggle recording pause |
| `S` | **Snapshot** | Capture instant photo |
| `R` | **Raw/Annotated** | Switch between raw and AI-annotated recording |
| `C` | **Clear Selection** | Reset child selection and sleep detection |
| `Z` | **Sleep Detection** | Toggle sleep/wake monitoring |

### 🖱️ **Mouse Interactions**

- **Left Click**: Select child to track (click on person in video)
- **Auto-Selection**: System automatically tracks smallest person if no manual selection

### 📱 **Real-time Notifications**

The system sends desktop notifications for:
- ✅ Child selection confirmation
- 😴 Sleep state detection
- 🚨 Wake-up alerts
- ⚠️ Fall risk warnings

---

## 📁 File Organization

```
~/baby-monitor-recordings/
├── 2025-08-13/           # Date folder
│   ├── 00-06/            # Time block (midnight to 6 AM)
│   │   ├── tapo_023015.avi
│   │   └── tapo_053015.avi
│   ├── 06-12/            # Morning block (6 AM to noon)
│   └── 12-18/            # Afternoon block (noon to 6 PM)
└── 2025-08-14/
    └── ...

~/logs/
└── detections.log        # All alerts and events log
```

---

## ⚙️ Configuration Options

### 🎯 **Detection Settings**
Located in `config/settings.py`:
```python
CONFIDENCE_THRESHOLD = 0.4    # AI detection confidence (0.0-1.0)
TARGET_FPS = 15.0            # Video frame rate (lower = less CPU usage)
```

### 😴 **Sleep Detection**
```python
MOVEMENT_THRESHOLD = 30       # Pixels of movement to detect activity
SLEEP_TIME_SEC = 150         # Seconds of stillness = sleep (2.5 minutes)
WAKE_NOTIFICATION_COOLDOWN = 60  # Seconds between wake notifications
```

### 🛡️ **Safety Monitoring**
```python
SAFE_MARGIN_RATIO = 0.15     # Safety zone margin (15% inside bed)
RISK_FRAMES_THRESHOLD = 10    # Frames outside safe zone before alert
ALERT_COOLDOWN_SEC = 20      # Seconds between repeated alerts
```

### 📹 **Recording Options**
```python
SEGMENT_MINUTES = 30         # Minutes per video file
TIME_BLOCK_HOURS = 6         # Hours per folder block
SAVE_ANNOTATED = True        # Save AI-annotated videos
SHOW_PREVIEW = True          # Show live preview window
```

---

## 🔧 Troubleshooting

### ❌ **Connection Issues**

**Problem**: "Cannot open RTSP stream"
**Solutions**:
1. Verify camera IP address: `ping your_camera_ip`
2. Check username/password in `.env` file
3. Confirm RTSP is enabled on camera
4. Test with VLC: `vlc rtsp://user:pass@ip:554/stream1`

**Problem**: "Connection lost frequently"
**Solutions**:
1. Check WiFi signal strength
2. Reduce video quality on camera
3. Use wired connection if possible

### 🖥️ **Performance Issues**

**Problem**: High CPU usage
**Solutions**:
1. Lower `TARGET_FPS` in config (try 10 or 5)
2. Reduce camera resolution
3. Set `SHOW_PREVIEW = False` for headless mode

**Problem**: Video files corrupted
**Solutions**:
1. Check disk space availability
2. Ensure stable power supply
3. Try different video codec in recording module

### 🤖 **Detection Issues**

**Problem**: Child not detected
**Solutions**:
1. Lower `CONFIDENCE_THRESHOLD` in config (try 0.3)
2. Ensure good lighting
3. Check if child is clearly visible
4. Manually click on child to select

### 🔧 **Module Issues**

**Problem**: Import errors in modular version
**Solutions**:
1. Run from project root directory
2. Test modules: `python dev.py test`
3. Check installation: `python dev.py status`

---

## 🎨 Visual Interface

### 📺 **Live Preview Window**

The application displays a rich, real-time interface showing:

- 🟢 **Green boxes**: Selected child being tracked
- 🔵 **Blue boxes**: Other detected persons  
- 🟡 **Yellow boxes**: Detected beds and furniture
- 🟢 **Green rectangle**: Safe zone boundary
- 💤 **Sleep indicators**: "SLEEPING [ZZZ]" overlay
- ⚠️ **Risk alerts**: "RISK: Near edge!" warnings
- 🎯 **Child info**: Track ID, confidence, and class
- 📊 **Status display**: Sleep/wake state with color coding

### 🎛️ **Status Overlays**

- **Top Right**: Child tracking information and confidence scores
- **Center**: Large wake-up alerts with attention-grabbing colors
- **Bottom**: Interactive instructions and keyboard shortcuts
- **Edges**: Safety zone visualization and risk warnings

---

## 📊 Technical Specifications

### 🧠 **AI Models**
- **Object Detection**: YOLOv8n (optimized for CPU)
- **Tracking Algorithm**: DeepSORT with cosine distance matching
- **Processing Mode**: CPU-only (CUDA disabled for stability)

### 🎥 **Video Processing**
- **Codecs**: MJPG (primary), XVID (fallback)
- **Container**: AVI format
- **Streaming**: RTSP over UDP (low latency)
- **Buffering**: Minimal buffering for real-time processing

### 💾 **System Requirements**
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: ~1GB per hour of recording
- **CPU**: Multi-core processor (Intel i5/AMD Ryzen 5 or better)
- **Network**: Stable connection to camera (wired preferred)

---

## 🤝 Contributing

We welcome contributions! Please feel free to:

1. 🐛 Report bugs and issues
2. 💡 Suggest new features
3. 📝 Improve documentation
4. 🔧 Submit pull requests

### 📋 Development Setup
```bash
# Fork the repository
git clone https://github.com/your-fork/AI-Baby-Monitor.git
cd AI-Baby-Monitor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install development dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your RTSP camera details

# Initialize database and run
python app.py
```

#### **Testing Authentication Without RTSP**
For testing user management features without a camera:
```bash
export AUTH_ONLY_MODE=true
python app.py
```

---

## 🏗️ Architecture Overview

The application has evolved into a full-stack web-based monitoring system with Flask backend and real-time capabilities:

### 📁 **Project Structure**
```
AI-Baby-Monitor/
├── app.py                  # 🚀 Flask web application entry point
├── config/                 # ⚙️ Configuration management
│   └── settings.py        # Application settings and RTSP config
├── models/                 # �️ Database models
│   ├── auth.py            # User authentication and login logs
│   └── notification.py    # Notification system
├── api/                    # 🌐 REST API endpoints
│   ├── auth_route.py      # Authentication routes
│   ├── monitor_route.py   # Monitoring endpoints
│   ├── active_users_route.py # Real-time user tracking
│   └── websocket_handlers.py # WebSocket for live streaming
├── services/               # 🔧 Core business logic
│   ├── detection/         # 🤖 YOLO object detection
│   ├── tracking/          # 📍 DeepSORT tracking
│   ├── streaming/         # 📡 RTSP streaming & web sockets
│   ├── monitoring/        # 👶 Sleep & safety monitoring
│   └── recording/         # 🎥 Video recording
├── templates/              # 🎨 HTML templates
│   ├── index.html         # Main dashboard
│   └── auth/              # Authentication pages
├── forms/                  # 📝 WTForms for user input
└── utils/                  # 🛠️ Utility functions  
```

### 🔄 **System Flow**
```
Browser ←→ Flask App ←→ WebSocket ←→ RTSP Stream
    ↓         ↓                        ↓
 Auth DB ← User Mgmt              AI Detection
    ↓         ↓                        ↓
Login Logs  Activity Track        Recording
```

### 🌐 **Technology Stack**
- **Backend**: Flask + Flask-SocketIO for real-time communication
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login with session management
- **Frontend**: HTML5, JavaScript, WebSocket for live streaming
- **AI Processing**: YOLOv8 + OpenCV for computer vision
- **Deployment**: Docker + Docker Compose

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **[Ultralytics](https://ultralytics.com/)** for YOLOv8 object detection
- **[Deep Sort Realtime](https://github.com/levan92/deep_sort_realtime)** for tracking implementation
- **[OpenCV](https://opencv.org/)** for video processing capabilities
- **Community contributors** for testing and feedback

---

<div align="center">

### 🌟 Star this repository if it helps you monitor your little ones safely! 🌟

**Made with ❤️ by [CodePerfectPlus](https://github.com/codeperfectplus)**

</div>