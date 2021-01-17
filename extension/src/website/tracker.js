for (var ele of document.getElementsByClassName("shhit-subtitle")) {
    ele.remove();
}

videoE = document.getElementsByTagName('video')[0];
progressBarE = document.getElementsByClassName('ytp-chrome-bottom')[0];
subBtnE = document.getElementsByClassName("ytp-subtitles-button")[0];

WebFont.load({
    google: {
        families: ['Noto Sans KR']
    }
});

var subtitleDiv = document.createElement("div");
subtitleDiv.id = "shhit-subtitle";
subtitleDiv.setAttribute('count', '0');
subtitleDiv.style.color = "white";
subtitleDiv.style.position = "fixed";
subtitleDiv.style.zIndex = "100";
subtitleDiv.style.fontSize = "3rem";
subtitleDiv.style.backgroundColor = "rgba(0,0,0,0.6)";
subtitleDiv.style.fontFamily = "Noto Sans KR";
subtitleDiv.style.padding = "0.5rem 1.5rem";
subtitleDiv.className = "shhit-subtitle";
document.body.appendChild(subtitleDiv);


currentSubI = 0;
sub = [];

document.getelement

var ws = new WebSocket("wss://2runo.com:2001");
ws.onopen = () => {
    ws.send(window.location.href);  // url 전송
}
ws.onmessage = (m) => {
    ws.send('ok');
    for (var line of m.data.split('\n')) {
        var json = JSON.parse(line);
        sub.push(json);
        if (json.curse == '1') {
            // 차단한 욕설의 개수 + 1
            subtitleDiv.setAttribute('count', Number(subtitleDiv.getAttribute('count'))+1);
        }
    }
}
ws.onerror = () => {
    alert("'쉿' 오류: 서버에 연결할 수 없습니다.");
}

isYtSubtitle = () => {
    // 유튜브 영상 자막이 켜져 있는가?
    return subBtnE.ariaPressed;
}

isBar = () => {
    // progress-bar가 나와 있는가?
    return Boolean(Number(getComputedStyle(progressBarE).opacity));
}

isMuted = () => {
    return videoE.muted;
}

mute = () => {
    document.getElementsByClassName("ytp-mute-button")[0].click();
}

mutedBegin = isMuted();
mutedJust = false;

getSubtitlePos = (text) => {
    var rect = videoE.getBoundingClientRect();
    subtitleDiv.style.maxWidth = rect.width * 0.8;
    subtitleDiv.textContent = text;
    var subrect = subtitleDiv.getBoundingClientRect();
    var left = rect.x + rect.width / 2 - subrect.width / 2;
    var top = rect.y + rect.height - rect.height/250*subrect.height;
    if (isBar()) {
        top = top - progressBarE.offsetHeight;
    }
    return [left, top]
}

setInterval(() => {
    // 자막 표시
    if (isYtSubtitle() === 'true') {
        subBtnE.click();
    }
    if (sub.length == 0) {
        return 0;
    }
    while (currentSubI >= sub.length) {
        currentSubI -= 1;
    }
    if (videoE.currentTime+0.1 >= Number(sub[currentSubI].start)) {
        if (videoE.currentTime+0.1 <= Number(sub[currentSubI].start) + Number(sub[currentSubI].dur)) {
            if (sub[currentSubI].curse == "1") {
                // 욕설 순화 표시
                if (!mutedBegin && !mutedJust) {
                    mutedJust = true;
                    mute();
                }
                subtitleDiv.textContent = sub[currentSubI].purified;
                subtitleDiv.style.backgroundColor = "rgba(255,0,0,0.6)";
            } else {
                // 일반 자막 표시
                if (mutedJust) {
                    mutedJust = false;
                    mute();
                }
                subtitleDiv.textContent = sub[currentSubI].text;
                subtitleDiv.style.backgroundColor = "rgba(0,0,0,0.6)";
            }
            var [left, top] = getSubtitlePos(subtitleDiv.textContent);
            subtitleDiv.style.left = left + 'px';
            subtitleDiv.style.top = top + 'px';
        } else {
            while (videoE.currentTime+0.1 > Number(sub[currentSubI].start) + Number(sub[currentSubI].dur)) {
                currentSubI += 1;
            }
        }
    } else {
        if (currentSubI == 0) {
            return 0;
        }
        currentSubI -= 1;
        while (videoE.currentTime+0.1 < Number(sub[currentSubI].start)) {
            currentSubI -= 1;
        }
        currentSubI += 1;
    }
}, 50);
