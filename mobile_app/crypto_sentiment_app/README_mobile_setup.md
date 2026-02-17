# Mobile App Backend Connection Guide

## Backend URL Configuration

The mobile app needs to connect to the backend API server. The correct URL depends on your setup:

### Android Emulator

- Use: `http://10.0.2.2:8000`
- This is the standard address for Android emulators to access the host machine

### iOS Simulator

- Use: `http://127.0.0.1:8000` or `http://localhost:8000`

### Physical Device (Android/iOS)

- Use the actual IP address of the machine running the backend
- Example: `http://192.168.1.100:8000`
- To find your IP: Open Command Prompt/Terminal and run `ipconfig` (Windows) or `ifconfig` (Mac/Linux)

## Troubleshooting Steps

1. **Verify Backend is Running**

   - Make sure the backend server is running on your computer
   - Visit `http://127.0.0.1:8000` in your browser to confirm

2. **Check Network Connection**

   - Ensure your mobile device/emulator is connected to the same network as the backend server
   - For physical devices, both devices must be on the same WiFi network

3. **Firewall Settings**

   - Make sure Windows Firewall or antivirus software is not blocking the connection
   - Allow Python or the specific port (8000) through the firewall

4. **Update Configuration**
   - Modify `lib/constants/api_constants.dart` with the correct URL for your setup

## Common Issues

- **Connection Timeout**: Backend server not running or wrong IP address
- **Network Error**: Device not on the same network or firewall blocking
- **404 Error**: Wrong API endpoint path
- **CORS Error**: Backend CORS settings not configured for mobile access
