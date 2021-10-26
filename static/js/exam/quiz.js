
$(document).ready(function () {
    $('img').css('width', '100%');
});

function delete_modal() {
    location.replace('/exam/{{ exam.id }}/delete/');
}

function boxChecked(){

}



var total_seconds = 1 * 1;
var c_minutes = parseInt(total_seconds / 60);
var c_seconds = parseInt(total_seconds % 60);
var timer;

function CheckTime() {
    document.getElementById("quiz-time-left").innerHTML = 'Time Left: ' + c_minutes + ' minutes ' + c_seconds + ' seconds ';

    if (total_seconds <= 0) {
            score();
    } else {
        total_seconds = total_seconds - 1;
        c_minutes = parseInt(total_seconds / 60);
        c_seconds = parseInt(total_seconds % 60);
        timer = setTimeout(CheckTime, 1000);
    }
}

timer = setTimeout(CheckTime, 1000);

function score(){
    let quizs = document.getElementById('overlay');
    let popup = document.getElementById('popup');

    quizs.classList.add('blur-in')
    popup.classList.remove('popup-hidden')
}