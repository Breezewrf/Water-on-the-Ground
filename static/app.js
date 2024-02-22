// Get video element
const video = document.getElementById('video');
let interactionOccurred = false;
document.addEventListener("mousemove", function () {
    interactionOccurred = true;
})
function showAlarm_nofify() {
    Swal.fire({
        title: "撥打火警熱線電話",
        imageUrl: "static/images/fire-alarm.png",
        imageWidth: 491,
        imageHeight: 491,
    });
}
// Stream video
// const stream = getStream();
// video.srcObject = stream;
// video.play();
function showAlarm() {
    const audioElement = document.getElementById('myAudio');
    if (interactionOccurred){
        audioElement.play().then(() => {
            console.log("Audio playback started.");
        }).catch(error => {
            console.log('Error: Autoplay is not allowed.');
        });
    } else {
      console.log("User interaction not detected. Audio playback not initiated.");
    }

    const alertContainer = document.getElementById('myAlertContainer');
    const alertElement = alertContainer.querySelector('.alert');
    alertElement.classList.remove('alert-success');
    alertElement.classList.add('alert-danger');
    // const alertText = document.querySelector('#myAlertContainer .alert .mb-0');
    // alertText.style.color = 'red';
    // alertText.textContent = '注意！臥室內存在潛在的火災危險!';

    const iconElement = document.getElementById('showIcon');
    const textElement = document.getElementById('showText');

    // Change the source of the image to the local SVG file
    iconElement.src = './static/images/fire.png';
    iconElement.alt = 'Danger Icon';

    // Update the text to reflect the change
    textElement.textContent = '注意！臥室內存在潛在的火災危險!';
    showAlarm_nofify();
    
}

function cancelAlarm(){
    const audioElement = document.getElementById('myAudio');

    if (audioElement.play)
        audioElement.pause();
    const alertContainer = document.getElementById('myAlertContainer');
    const alertElement = alertContainer.querySelector('.alert');
    alertElement.classList.remove('alert-danger');
    alertElement.classList.add('alert-success');
  //  const alertText = document.querySelector('#myAlertContainer .alert .mb-0');
   // alertText.style.color = 'green';
    // alertText.textContent = '你好.';
    const iconElement = document.getElementById('showIcon');
    const textElement = document.getElementById('showText');

    // Change the source of the image to the local SVG file
    iconElement.src = './static/images/hand-shake.png';
    iconElement.alt = 'Safe Icon';

    // Update the text to reflect the change
    textElement.textContent = '你好!';
    
}
// Function to send the signal and update the image
function sendSignalAndUpdateImage() {
    fetch('/alarm')
        .then(function (response) {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Failed to send signal');
            }
        })
        .then(function (data) {
            if (data.success) {
                // Update the image in the HTML document
                showAlarm();
                document.getElementById('image').src = './static/images/alarm.png';
                console.log('Signal sent successfully and image updated');
                // var alarmImage = document.querySelector('.alarm-image');
                // alarmImage.style.display = 'block';
            } else {
                document.getElementById('image').src = './static/images/robot.png';
                console.log('Signal sent but image not updated');
                cancelAlarm()
            }
        })
        .catch(function (error) {
            console.log('Error:', error.message);
        });
}

// Call the function to send the signal and update the image.
setInterval(function () {
    sendSignalAndUpdateImage();

}, 1000);

function openModal() {
    var modal = document.getElementById("custom-modal");
    modal.style.display = "flex";
}

// Function to close the custom modal
function closeModal() {
    var modal = document.getElementById("custom-modal");
    modal.style.display = "none";
}