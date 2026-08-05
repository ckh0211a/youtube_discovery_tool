import re

file_path = r'c:\유투브소재채굴기\youtube_discovery_tool.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add HTML UI right before <div class="flex flex-col items-center mb-12 w-full"> (Line 1282)
# Or right after <div id="clockDisplay"... </div>
ui_html = """                <!-- Live Issue Ticker (Top-Right under Clock) -->
                <div id="liveIssueTicker" 
                    class="absolute right-6 top-[62px] w-[280px] flex items-center gap-2 bg-white/90 backdrop-blur border border-red-200/50 p-2 px-3 rounded-xl shadow-sm z-[600] cursor-pointer hover:border-red-400 hover:bg-white transition-all overflow-hidden h-[36px] group"
                    style="display: none;">
                    <div class="relative flex h-2 w-2 shrink-0 ml-1">
                      <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                      <span class="relative inline-flex rounded-full h-2 w-2 bg-red-500"></span>
                    </div>
                    <span class="text-[10px] font-black text-red-600 shrink-0 uppercase tracking-widest bg-red-50 px-1.5 py-0.5 rounded-md">LIVE</span>
                    <div class="overflow-hidden w-full h-[18px] relative ml-1">
                        <div id="tickerContent" class="text-[12px] font-bold text-gray-700 whitespace-nowrap absolute top-0 left-0 transition-transform duration-500 w-full flex flex-col flex-nowrap" style="transform: translateY(0%);">
                            <span class="h-[18px] flex items-center text-gray-400 text-[11px]">이슈 불러오는 중...</span>
                        </div>
                    </div>
                </div>

"""

content = content.replace("<!-- Title at the absolute top (Custom Serif Font) -->", ui_html + "                <!-- Title at the absolute top (Custom Serif Font) -->")


# 2. Add JS Logic and Initialization 
js_code = """

        // --- Live Issue Ticker Functionality ---
        let tickerTimer = null;
        async function initLiveTicker() {
            const tickerEl = document.getElementById('liveIssueTicker');
            const contentEl = document.getElementById('tickerContent');
            if (!tickerEl || !contentEl) return;
            
            const ytKey = getYouTubeKey();
            if (!ytKey) return; // Hide silently if no key

            try {
                // Fetch daily trending from Korea using mostPopular API (which relates to issues)
                const url = `http://127.0.0.1:5001/api/proxy/google/youtube/v3/videos?part=snippet&chart=mostPopular&regionCode=KR&maxResults=15&key=${ytKey}`;
                const res = await fetch(url).then(r => r.json());
                
                if (res.items && res.items.length > 0) {
                    const uniqueTitles = [...new Set(res.items.map(item => item.snippet.title))].slice(0, 10);
                    
                    let html = '';
                    uniqueTitles.forEach((title, idx) => {
                        const cleanTitle = title.replace(/'/g, "\\'").replace(/"/g, '&quot;');
                        // Click searches the keyword on general mode
                        html += `<div class="h-[18px] flex items-center px-1 truncate w-full cursor-pointer hover:text-red-500 transition-colors" onclick="document.getElementById('searchInput').value='${cleanTitle}'; switchSearchMode(1); searchVideos();" title="${cleanTitle}"><span class="text-[10px] text-gray-400 mr-2 font-black">${idx+1}</span> ${cleanTitle}</div>`;
                    });
                    
                    contentEl.innerHTML = html;
                    tickerEl.style.display = 'flex'; // show when ready
                    
                    let currentIndex = 0;
                    const totalItems = uniqueTitles.length;
                    
                    if (tickerTimer) clearInterval(tickerTimer);
                    tickerTimer = setInterval(() => {
                        currentIndex = (currentIndex + 1) % totalItems;
                        contentEl.style.transform = `translateY(-${currentIndex * 18}px)`;
                    }, 3500);
                }
            } catch (err) {
                console.error("Live Ticker init failed:", err);
            }
        }
        
        // Execute after a slight delay to not block main loading
        setTimeout(initLiveTicker, 2000);
        
        // --- End Live Issue Ticker ---

"""

# Insert JS before existing `async function searchVideos`
content = content.replace("async function searchVideos(", js_code + "async function searchVideos(")


with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Added Live Ticker UI and JS.")
