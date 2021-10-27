const today = new Date();
const hours = today.getHours();
const minits = today.getMinutes();
const seconds = today.getSeconds();

const stayedList = [`${hours}:${minits}:${seconds}`];
const stayedGapList = [];


const img_list = document.getElementsByName("imgList");
const img = document.getElementById('img_content');
let page_num = parseInt(document.getElementById('page_num').value);
let start = 0;


$(document).ready(function () {
    $('img').css('width', '100%');
});

function delete_modal() {
    location.replace('/edu/{{ notice.id }}/delete/');
}

function prev_page() {
    const prev_page_num = page_num - 1;
    if (prev_page_num < 0){
        alert("첫 번째 페이지 입니다.")
    } else {
        const new_src = img_list[prev_page_num].value
        img.src = new_src
        page_num = prev_page_num
    }

}

function next_page() {
    const next_page_num = page_num + 1;
    if (next_page_num === img_list.length){
        alert("마지막 페이지 입니다.")
        sendStayedTimeToDB()

    } else {
        const new_src = img_list[next_page_num].value
        img.src = new_src
        page_num = next_page_num
    }
}
document.addEventListener('keydown', function(event) {
if(event.keyCode == 37) {
    prev_page();
    timeCheck();
}
else if(event.keyCode == 39) {
    next_page();
    timeCheck();
}

function timeCheck(){
    const today = new Date();
    const hours = today.getHours();
    const minits = today.getMinutes();
    const seconds = today.getSeconds();
    current = `${hours}:${minits}:${seconds}`;
    stayedList.push(current);
    if(stayedList.length > 1){
        stayed = formatTime(timestrToSec(stayedList[stayedList.length - 1]) - timestrToSec(stayedList[stayedList.length - 2]));
        stayedGapList.push(stayed);
        start += timestrToSec(stayed)

    }
}

function timestrToSec(timestr) {
    var parts = timestr.split(":");
    return (parts[0] * 3600) +
            (parts[1] * 60) +
            (+parts[2]);
}

function pad(num) {
    if(num < 10) {
        return "0" + num;
    } else {
        return "" + num;
    }
}

function formatTime(seconds) {
    return [pad(Math.floor(seconds/3600)),
            pad(Math.floor(seconds/60)%60),
            pad(seconds%60),
            ].join(":");
}

function drawTime(){
    if(start){
            document.querySelector('div#stayed').innerHTML = `누적시간 : ${start}초`;
    }
}
});

function sendStayedTimeToDB(){
    alert(window.location.pathname + 'savetime')
    $.ajax({
        type: "GET",
        url: "{% url 'edu_save' %}",
        data: {
            "result": stayedGapList,
        },
        dataType: "json",
        success: function (data) {
            // any process in data
            alert("successfull")
        },
        failure: function () {
            alert("failure");
        }
    });
}