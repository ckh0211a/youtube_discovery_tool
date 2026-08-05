# YouTube Discovery Tool (v1.7.0) - Working Status

## 📌 Project Overview
A sophisticated tool for discovering and analyzing YouTube content for creators, specifically optimized for finding "Moul-gae" (shorts material) and successful content patterns.

## 🚀 Current Status (v1.7.0)
- **Latest Update**: Fixed auto-scroll issue in Monetization Checker, added search input validation to prevent empty searches, and refined help text.
- **Stability**: Search modes 1, 2, 7, 8, 9, 11, and the Monetization Checker are functional.
- **Key Decoupling**: Bookmarks are now fully offline-capable, rendered from `localStorage` without API calls.

## 🧠 Core Logic & Architecture

### 1. Quota Management System
- **Daily Reset**: Automatically resets to 10,000 points at **5:00 PM KST (17:00)** daily.
- **Estimation Logic**: Since exact quota from API is hard to fetch, the tool estimates consumption based on usage patterns.
- **Persistence**: Quota state is saved in `localStorage` to survive refreshes.

### 2. Search Modes & Engine (v1.7.5 Highlight)
- **Mode 0 (Home)**: Central dashboard for navigation.
- **Mode 4 (Monetization Checker)**: **[FIXED]** Analyzes video/channel for monetization status without disruptive auto-scrolling. Keeps viewport static for better UX.
- **Mode 11 (Bookmarks)**: Uses `saveBookmark(videoData)` to store full JSON metadata in `localStorage`. Rendering is done via `renderBookmarks()` which works offline.

### 3. API & Security (Current)
- **Dynamic Keys**: Users can update YouTube Data V3 and Gemini AI keys via the UI (Settings cog).
- **Test Logic**: Includes a connection test function to verify API key validity before starting heavy tasks.

### 4. UI/UX Design System
- **Framework**: HTML5, TailwindCSS (for layout), Vanilla JS.
- **Aesthetics**: Premium Dark/Light hybrid mode, high-quality typography (Outfit, Playfair Display), and rich micro-interactions.
- **Auto-Scroll Behavior**: Specifically disabled for report generation in Monetization Checker to prevent layout jumps.
- **Improved Tooltips**: Refined the Channel In-depth Search guide to emphasize exact channel names (with spacing) for more accurate results.

## 🛠️ Upcoming / Future Tasks
- [ ] Optimize transcript extraction (Python script integration).
- [ ] Refine Gemini AI integration for script summarization.
- [ ] Implement advanced filtering for Mode 8 (Channel Search).

## 💡 How to Resume Work
- **API Quota Empty?**: If the current API key is exhausted, replace the key in the Settings (cog icon at top left). The tool will then function immediately.
- **Restarting Work**: Read `youtube_discovery_tool.html` to see the initialization scripts (search for `DOMContentLoaded`). All critical state is in `localStorage`.

---
*Last updated: 2026-04-04 20:58 KST*
