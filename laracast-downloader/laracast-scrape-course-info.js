let myconsole = [];


// #region ==================== INFO

let courseInfo = {
    "Title"       : null,
    "Description" : null,
    "Skill"       : null,
    "Episodes"    : null,
    "Duration"    : null,
    "Teacher"     : null,
    "Contents"    : [],
};

//#endregion


// #region ==================== FUNCTIONS: TOOLS

const qs = (s, b) => (b ?? document).querySelector(s);
const qsa = (s, b = null) => (b ?? document).querySelectorAll(s);

//#endregion


// #region ==================== FUNCTIONS: GETTERS

function getTitle() {
    return qs(".series-banner:nth-child(3) h1")?.innerText ?? null;
}

function getDescription() {
    return qs(".series-banner:nth-child(3) .generic-content")?.innerText ?? null;
}

function getSkill() {
    return qsa(".series-banner-meta .level-item")[0]?.innerText ?? null;
}

function getEpisodes() {
    let eps = qsa(".series-banner-meta .level-item")[1]?.innerText ?? null;
    if (eps) {
        eps = eps.match(/\d+/)[0] ?? null;
    }
    return eps;
}

function getDuration() {
    return qsa(".series-banner-meta .level-item")[2]?.innerText ?? null;
}

function getTeacher() {
    return qs("h2 strong").innerText ?? null;
}

function getContents() {
    let chapters = [];
    let chapterEls = qsa(".episode-list > li");
    chapterEls.forEach(chapterEl => {
        let chapterHeader = qs("header", chapterEl);
        let chapter = {
            no     : "",
            title  : "",
            videos : [],
        };
        if (chapterHeader) {
            chapter = {
                no     : qs("header span:first-child", chapterEl).innerText.match(/\d+/)[0] ?? null,
                title  : qs("header span:last-child", chapterEl).innerText ?? null,
                videos : [],
            };
        }
        if (chapter.no) {
            chapter.no = chapter.no.padStart(2, "0");
        }
        let episodeEls = qsa("ol > li", chapterEl);
        episodeEls.forEach((episodeEl, index) => {
            let video = {
                no       : (index + 1).toString().padStart(2, "0"),
                title    : qs(".episode-list-title", episodeEl).innerText ?? null,
                duration : qs("span + span", episodeEl).innerText.match(/\d+:\d+/)[0] ?? null,
            };
            let duration = video.duration.split(":");
            duration[0] = duration[0].padStart(2, "0");
            duration[1] = duration[1].padStart(2, "0");
            video.duration = duration.join(":");
            chapter.videos.push(video);
        });
        chapters.push(chapter);
    });
    return chapters;
}

//#endregion


// #region ==================== SCRAPE

courseInfo = {
    "Title"       : getTitle(),
    "Description" : getDescription(),
    "Skill"       : getSkill(),
    "Episodes"    : getEpisodes(),
    "Duration"    : getDuration(),
    "Teacher"     : getTeacher(),
    "Contents"    : getContents(),
};

//#endregion


// #region ==================== CALCULATIONS

let TAB = "    ";
let longestAttr = "Released";
// let maxAttrLength = longestAttr.length + (4 - longestAttr.length % 4);
let maxAttrLength = longestAttr.length + 1;
let maxVideoTitleLength = 0;
let videoTitlePadLength = null;
let videoNoLength = "00. ".length;

courseInfo["Contents"].forEach(chapter => {
    chapter.duration = [];
    if (chapter.title.length > maxVideoTitleLength) {
        maxVideoTitleLength = chapter.title.length;
    }
    chapter.videos.forEach(video => {
        chapter.duration.push(video.duration);
        if (video.title.length > maxVideoTitleLength) {
            maxVideoTitleLength = video.title.length;
        }
    });
    let totalChapterDuration = 0;
    chapter.duration.forEach(dur => {
        let [_, min, sec] = /(?:(\d+):)?(?:(\d+))?/.exec(dur) ?? [null, null, null];
        let durSec = (parseInt(min) || 0) * 60 + (parseInt(sec) || 0);
        totalChapterDuration += durSec;
    });
    let h = Math.floor(totalChapterDuration / 60 / 60);
    if (h != 0) {
        totalChapterDuration = totalChapterDuration - (h * 60 * 60);
    }
    let m = Math.floor(totalChapterDuration / 60);
    if (m != 0) {
        totalChapterDuration = totalChapterDuration - (m * 60);
    }
    let s = totalChapterDuration;
    chapter.duration = [];
    if (h != 0) {
        chapter.duration.push(h.toString().padStart(2, "0"));
    }
    if (m != 0) {
        chapter.duration.push(m.toString().padStart(2, "0"));
    }
    chapter.duration.push(s.toString().padStart(2, "0"));
    chapter.duration = chapter.duration.join(":");
});
videoTitlePadLength = videoNoLength + maxVideoTitleLength + (4 - maxVideoTitleLength % 4);

//#endregion


// #region ==================== PRINT

let outputLines = [];

for (let attr in courseInfo) {
    if (["Description", "Contents"].includes(attr)) continue;
    let value = courseInfo[attr] ?? "";
    let line = attr.padEnd(maxAttrLength) + ": " + value;
    outputLines.push(line);
}

outputLines.push("");
outputLines.push("Description");
outputLines.push("");
outputLines.push(courseInfo["Description"]);

outputLines.push("");
outputLines.push("Contents");
outputLines.push(TAB);

let doubleDigitPad = courseInfo["Contents"].length > 9;

for (let chapterIndex = 0; chapterIndex < courseInfo["Contents"].length; chapterIndex++) {
    let chapter = courseInfo["Contents"][chapterIndex];
    let chapterTitle = chapter.no + ". " + chapter.title;
    chapterTitle = chapterTitle.padEnd(
        chapter.duration.length > "00:00".length
            ? videoTitlePadLength - "00:".length
            : videoTitlePadLength
    );
    outputLines.push(TAB + chapterTitle + TAB + chapter.duration);
    for (let videoIndex = 0; videoIndex < chapter.videos.length; videoIndex++) {
        let video = chapter.videos[videoIndex];
        let videoTitle = video.no + ". " + video.title;
        videoTitle = videoTitle.padEnd(videoTitlePadLength);
        outputLines.push(TAB + TAB + videoTitle + video.duration);
    }
    outputLines.push(TAB);
}

//#endregion


// #region ==================== OUTPUT

console.clear();
console.dir(outputLines.join("\n"));
copy(outputLines.join("\n"))
for (let item of myconsole) console.log(item);

//#endregion