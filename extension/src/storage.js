set = (k, v) => {
    let obj = {};
    obj[k] = v;
    chrome.storage.sync.set(obj);
}

get = (k, callback) => {
    chrome.storage.sync.get(k, (result) => {
        for (var key in result) {
            callback(result[key]);
            return 0;
        }
        callback(null);
    });
}

rm = (k) => {
    set(k, null);
}
