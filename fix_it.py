import os

path = r'c:\유투브소재채굴기\youtube_discovery_tool.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: The corrupted Shorts Category filter and renderResults start
bad1 = """                    // Shorts Category (under 1                        <div class="stat-grid grid grid-cols-2 gap-x-3 gap-y-2 mt-auto pt-3 border-t border-gray-700/50">"""
good1 = """                    // Shorts Category (under 180s)
                    if (video.durationSec < 180 && shortsType !== 'all') {
                        if (video.shortsCategory !== shortsType) return false;
                    }
                }

                return true;
            });

            // Sort
            if (sortOrder === 'date') {
                filtered.sort((a, b) => b.publishedAtRaw - a.publishedAtRaw);
            } else if (sortOrder === 'viewCount') {
                filtered.sort((a, b) => b.views - a.views);
            } else if (sortOrder === 'subs_desc') {
                filtered.sort((a, b) => (b.subs || 0) - (a.subs || 0));
            } else if (sortOrder === 'relevance' && !keyword) {
                if (currentResultsType === 'channel') {
                    filtered.sort((a, b) => (b.subs || 0) - (a.subs || 0));
                }
            }

            // Render
            renderResults(filtered, keyword, isTagModeActive);
            showLoading(false);
        }

        // Core: Render Results
        function renderResults(data, kw, isTagMode = false) {
            lastFilteredVideos = data; // Store latest filtered data
            const actionsDiv = document.getElementById('resultsActions');
            if (data.length === 0) {
                if (actionsDiv) actionsDiv.classList.add('hidden');
                resultsGrid.innerHTML = '<p class="col-span-full text-center text-gray-500 py-10">조건에 맞는 결과가 없습니다. 필터를 조금 완화해보세요.</p>';
                showLoading(false); // Ensure loader is hidden
                return;
            }

            if (actionsDiv) {
                actionsDiv.classList.remove('hidden');
                
                const resultLabel = currentResultsType === 'video' ? '영상' : '채널';
                if (currentSearchMode === 11) {"""

# Fix 2: The corrupted Grid Card stats section
bad2 = """                                <span clas                             <div class="flex flex-col cursor-help" title="[참여도 분석]&#10;참여도(%) = (좋아요 수 + 댓글 수) ÷ 전체 조회수 × 100&#10;시청자들이 영상을 단순히 보기만 한 것이 아니라 얼마나 적극적으로 소통했는지 나타내는 지표입니다.">"""
good2 = """                                <div class="flex flex-col cursor-help" title="[참여도 분석]&#10;참여도(%) = (좋아요 수 + 댓글 수) ÷ 전체 조회수 × 100&#10;시청자들이 영상을 단순히 보기만 한 것이 아니라 얼마나 적극적으로 소통했는지 나타내는 지표입니다.">"""

# Fix 3: Remove potential double-counting or extra closures from previous failed attempts
# We'll do a few more cleanups if needed.

# Execute replacements
new_content = content.replace(bad1, good1)
new_content = new_content.replace(bad2, good2)

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Double fix complete.")
