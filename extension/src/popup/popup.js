numberWithCommas = (x) => {
    // f(1234) -> '1,234'
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

turnOn = () => {
    document.body.className = document.body.className.replace("off", "on");
    document.getElementsByClassName("toggle-status")[0].textContent = "ON";
    set('turn', 'on');
}
turnOff = () => {
    document.body.className = document.body.className.replace("on", "off");
    document.getElementsByClassName("toggle-status")[0].textContent = "OFF";
    set('turn', 'off');
}
setCount = () => {
    get('count', (count) => {
        if (count == null) {
            count = 0;
        }
        document.getElementById("count").textContent = numberWithCommas(count);
    });
}

get('turn', (turn) => {
    if (turn == 'on') {
        turnOn();
    } else if (turn == 'off') {
        turnOff();
    } else {
        set('turn', 'on');
        turnOn();
    }
})

setCount();
setInterval(setCount, 1000);

document.getElementById('back-off').ondragstart = function() { return false; };
document.getElementsByClassName('onoffToggle')[0].ondragstart = function() { return false; };
document.getElementsByClassName('toggle-status')[0].ondragstart = function() { return false; };
document.getElementsByClassName('onoffToggle')[0].addEventListener("mousedown", (e) => {
    for (var target of e.path) {
        try {
            if (target.className.includes("onoffToggle")) {
                if (document.body.className.includes("on")) {
                    // document.body.className = document.body.className.replace("on", "off");
                    // console.log(target.getElementsByClassName("toggle-status")[0], '!!!')
                    // target.getElementsByClassName("toggle-status")[0].textContent = "OFF";
                    turnOff();
                } else {
                    // document.body.className = document.body.className.replace("off", "on");
                    // console.log(target.getElementsByClassName("toggle-status")[0], 'nnn')
                    // target.getElementsByClassName("toggle-status")[0].textContent = "ON";
                    turnOn();
                }
                break;
            }
        } catch(_) {}
    }
    
});
