
const https = require('https');

function get(url) {
    return new Promise((resolve, reject) => {
        const options = {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        };
        https.get(url, options, (res) => {
            let data = '';
            res.on('data', (chunk) => data += chunk);
            res.on('end', () => resolve(data));
        }).on('error', reject);
    });
}

async function testTranscript(videoId) {
    const url = `https://www.youtube.com/watch?v=${videoId}`;
    try {
        console.log(`Fetching ${url}...`);
        const html = await get(url);
        const regex = /"captionTracks":\s*(\[.*?\])/;
        const match = html.match(regex);
        if (match) {
            const captionTracks = JSON.parse(match[1]);
            console.log("Caption Tracks Found:", captionTracks.length);
            let selectedTrack = captionTracks.find(t => t.languageCode === 'ko') ||
                captionTracks.find(t => t.languageCode === 'en') ||
                captionTracks[0];

            console.log("Selected Language:", selectedTrack.name.simpleText || selectedTrack.languageCode);
            const transcriptUrl = selectedTrack.baseUrl + '&fmt=json3';
            console.log("Fetching Transcript from:", transcriptUrl.substring(0, 100) + "...");

            const tDataStr = await get(transcriptUrl);
            try {
                const tData = JSON.parse(tDataStr);
                if (tData.events) {
                    console.log("SUCCESS: Transcript events found:", tData.events.length);
                    const firstLines = tData.events.slice(0, 5).filter(e => e.segs).map(e => e.segs.map(s => s.utf8).join('')).join(' ');
                    console.log("Sample Text:", firstLines);
                }
            } catch (je) {
                console.log("Transcript content was not valid JSON. Response length:", tDataStr.length);
                console.log("Response start:", tDataStr.substring(0, 200));
            }
        } else {
            console.log("FAILURE: No captionTracks found in HTML.");
        }
    } catch (e) {
        console.error("Error:", e);
    }
}

testTranscript('ERGfzInUxeE');
