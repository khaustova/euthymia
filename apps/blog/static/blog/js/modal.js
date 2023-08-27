'use strict'; 

const modalFeedback = document.getElementsByClassName('feedback-modal')[0];

function openFeedbackModal() {
    modalFeedback.style.display = 'flex';
}
function closeFeedbackModal() {
    modalFeedback.style.display = 'none';
}

window.onclick = function(event) {
    if (event.target == modalFeedback) {
        modalFeedback.style.display = 'none';
    }
}