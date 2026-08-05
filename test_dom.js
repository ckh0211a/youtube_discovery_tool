const { JSDOM } = require("jsdom");
const fs = require("fs");
const html = fs.readFileSync("youtube_discovery_tool.html", "utf8");
const dom = new JSDOM(html);
const btn = dom.window.document.querySelector('button[onclick="searchPoliticsChannels()"]');
if (btn) {
    console.log("Button FOUND!");
    console.log(btn.outerHTML);
} else {
    console.log("Button NOT FOUND!");
}
