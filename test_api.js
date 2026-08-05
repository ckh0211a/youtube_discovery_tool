const https = require('https');

const ytKey = 'AIzaSyCiqpIPc3a0VqZHhRhPL6jmF6Oi6_mpVys';
const q = '#김건희 OR #윤석열';
const url = `https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=5&q=${encodeURIComponent(q)}&key=${ytKey}&regionCode=KR&relevanceLanguage=ko`;

https.get(url, (res) => {
    let data = '';
    res.on('data', (chunk) => { data += chunk; });
    res.on('end', () => {
        const json = JSON.parse(data);
        console.log('Status:', res.statusCode);
        if (json.items) {
            console.log('Found items:', json.items.length);
            json.items.forEach(item => {
                console.log('- ', item.snippet.title);
            });
        } else {
            console.log('No items found or error:', json);
        }
    });
}).on('error', (err) => {
    console.error('Error:', err.message);
});
