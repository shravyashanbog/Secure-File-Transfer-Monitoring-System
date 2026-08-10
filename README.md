# Secure File Transfer Monitoring System (SFTMS)

A real-time security monitoring system designed to track file activity, detect suspicious file movement, verify file integrity, and generate security audit reports.

## 📌 Project Overview

The Secure File Transfer Monitoring System (SFTMS) is a Python-based security monitoring application developed to improve visibility into file-system activity.

The system monitors file events, records security activity, performs integrity verification using SHA-256 hashing, detects suspicious file movement, and presents the results through a web-based security console.

## 🎯 Objectives

- Monitor file-system activities in real time
- Record file transfer and movement events
- Detect suspicious or unauthorized file movement
- Verify file integrity using SHA-256 hashing
- Maintain security audit logs
- Display security statistics through dashboards
- Generate security reports
- Provide a centralized monitoring interface

## 🔐 Key Features

### Real-Time File Monitoring
Uses Python Watchdog to monitor file-system activity and detect events such as:

- File creation
- File movement
- File renaming
- File deletion
- File modification

### File Integrity Verification

SHA-256 hashing is used to verify file integrity and identify potential changes or tampering.

### Security Audit Logs

Security events are recorded with information such as:

- Event type
- File name
- File path
- Source path
- Destination path
- Risk level
- Authorization status
- Username
- Event timestamp

### Security Dashboard

The web interface provides:

- Total file/event statistics
- High-risk event counts
- Secure event counts
- File monitoring information
- Security status indicators

### Security Reports

The reporting interface provides a consolidated view of monitored files and security activity.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core application and monitoring logic |
| Flask | Web application framework |
| Watchdog | Real-time file-system monitoring |
| SQLite | Local database and event storage |
| SHA-256 | File integrity verification |
| HTML | Web interface |
| CSS | Dashboard and UI styling |

## 🏗️ System Workflow

```text
File System Activity
        ↓
Real-Time Monitoring
        ↓
Event Classification
        ↓
Integrity Verification
        ↓
Authorization / Risk Check
        ↓
Database Logging
        ↓
Security Alert
        ↓
Dashboard & Reports
