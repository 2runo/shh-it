
async function filtering(tab) {
    chrome.tabs.executeScript(tab.id, {code: window['webfont']});  // 탭에서 webfont.js 실행
    chrome.tabs.executeScript(tab.id, {code: window['jquery']});  // 탭에서 jquery 실행
    chrome.tabs.executeScript(tab.id, {code: window['tracker']});  // 탭에서 /src/website/tracker.js 실행
    
    setInterval(() => {
        // 지금까지 차단한 욕설의 개수 업데이트
        chrome.tabs.executeScript(tab.id, {
            "code": "a=document.getElementById('shhit-subtitle').getAttribute('count');document.getElementById('shhit-subtitle').setAttribute('count', '0');a"
        }, (alpha) => {
            get("count", (count) => {
                if (count == null) {
                    count = 0;
                }
                set("count", Number(count)+Number(alpha));
            })
        });
    }, 1000);
}
