# ABI Bot Sync 🤖📅

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Google Calendar](https://img.shields.io/badge/Google_Calendar-Integration-4285F4?style=for-the-badge&logo=google-calendar&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-Scraper-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**ABI Bot Sync** is a powerful, automated tool designed to bridge the gap between your **ABI MasterMind (ESS)** work schedule and your **Google Calendar**. Say goodbye to manual entry and missed shifts—this bot scrapes your latest schedule and seamlessly syncs it to your personal calendar.

---

## ✨ Key Features

*   🔄 **Smart Synchronization**: Automatically detects new shifts and adds them to Google Calendar.
*   🚫 **Duplicate Prevention**: Intelligently skips events that are already on your calendar.
*   🖥️ **System Tray Agent**: Runs silently in the background with a convenient system tray icon for status updates and manual controls.
*   ⚙️ **User-Friendly Settings**: Built-in GUI to easily manage your credentials and preferences without touching code.
*   👻 **Headless Operation**: The scraper runs invisibly in the background so it doesn't interrupt your workflow.
*   📊 **Rich CLI Interface**: Beautiful terminal output with progress bars and status tables for manual runs.

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

*   **Python 3.10** or higher
*   **Google Cloud Project** with the **Google Calendar API** enabled (you'll need the `credentials.json` file).

---

## 🚀 Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Snapwave333/abi-bot.git
    cd abi-bot
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    playwright install chromium
    ```

3.  **Setup Google Credentials**
    *   Go to the [Google Cloud Console](https://console.cloud.google.com/).
    *   Create a new project and enable the **Google Calendar API**.
    *   Create OAuth 2.0 Client ID credentials (Desktop App).
    *   Download the JSON file, rename it to `credentials.json`, and place it in the project root directory.

---

## ⚙️ Configuration

You can configure the bot using the built-in GUI or by manually editing the `.env` file.

### Option 1: GUI (Recommended)
Run the settings UI to input your details:
```bash
python settings_ui.py
```
*   **Venue ID**: Your specific ABI MasterMind venue ID.
*   **ESS Username/Password**: Your login credentials for the employee portal.
*   **Sync Interval**: How often (in hours) the bot should check for updates (default: 24).

### Option 2: Manual .env
Create a `.env` file in the root directory:
```ini
ESS_VENUE_ID=your_venue_id
ESS_USERNAME=your_username
ESS_PASSWORD=your_password
SYNC_INTERVAL_HOURS=24
HEADLESS=True
```

---

## 🖥️ Usage

### ▶️ Run Manually
To perform a one-time sync immediately:
```bash
python main.py
```
*   *First Run Note*: You will be redirected to your browser to authorize access to your Google Calendar. This creates a `token.json` file for future automatic logins.*

### 🕒 Run in Background (System Tray)
To keep the bot running in the background:
```bash
python tray.py
```
*   A 🤖 icon will appear in your system tray.
*   **Right-click** the icon to:
    *   **Sync Now**: Force an immediate update.
    *   **Settings**: Open the configuration window.
    *   **Exit**: Close the application.

---

## 📂 Project Structure

*   `main.py`: Core logic for scraping and syncing.
*   `scraper.py`: Handles browser automation with Playwright.
*   `gcal.py`: Manages Google Calendar API interactions.
*   `tray.py`: System tray application logic.
*   `settings_ui.py`: CustomTkinter GUI for configuration.

---

## ⚠️ Disclaimer

This project is an independent tool and is **not affiliated, associated, authorized, endorsed by, or in any way officially connected with ABI MasterMind or its subsidiaries**. Use this tool responsibly and in accordance with your employer's IT policies.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/Snapwave333">Snapwave333</a>
</p>
