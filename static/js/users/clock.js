function time() {
    const date = new Date();
    const hour = String(date.getHours()).padStart(2, "0");
    const mins = String(date.getMinutes()).padStart(2, "0");
    const secs = String(date.getSeconds()).padStart(2, "0");
    document.querySelector('div#clock').innerHTML = `${hour}:${mins}:${secs}`;
    }

    setInterval(time, 1000);