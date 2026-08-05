
const API_KEY = 'AIzaSyCiqpIPc3a0VqZHhRhPL6jmF6Oi6_mpVys';
const QUERY = '@MBCNEWS11';

async function testSearch() {
    const url = `https://www.googleapis.com/youtube/v3/search?part=snippet&q=${encodeURIComponent(QUERY)}&type=video&maxResults=50&order=viewCount&key=${API_KEY}`;
    try {
        const res = await fetch(url);
        const data = await res.json();
        if (!data.items) {
            console.log("Error or No Items found:", JSON.stringify(data, null, 2));
            return;
        }
        const found = data.items.some(item => item.id.videoId === 'ERGfzInUxeE');
        console.log(`Video found: ${found}`);
        if (!found) {
            console.log("Top 5 videos found:");
            data.items.slice(0, 5).forEach(item => console.log(`- ${item.snippet.title} (${item.id.videoId})`));
        }
    } catch (e) {
        console.error(e);
    }
}

testSearch();
