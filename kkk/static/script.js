let canvas = document.getElementById('canvas');
let ctx = canvas.getContext('2d');

// 기본 그리기 기능
let drawing = false;
let lastX = 0;
let lastY = 0;
let color = 'black';
let eraser = false;
let lineWidth = 5;

// 색상 선택 버튼
document.getElementById('colorPicker').addEventListener('click', function() {
    color = prompt('색상을 선택하세요 (예: red, blue, #ff0000 등):', color);
});

// 지우개 버튼
document.getElementById('eraser').addEventListener('click', function() {
    eraser = !eraser;
    if (eraser) {
        document.getElementById('eraser').style.backgroundColor = 'gray';
    } else {
        document.getElementById('eraser').style.backgroundColor = '';
    }
});

// 초기화 버튼
document.getElementById('clear').addEventListener('click', function() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
});

// 그리기 기능
canvas.addEventListener('mousedown', function(e) {
    drawing = true;
    lastX = e.offsetX;
    lastY = e.offsetY;
});

canvas.addEventListener('mousemove', function(e) {
    if (drawing) {
        ctx.beginPath();
        ctx.moveTo(lastX, lastY);

        if (eraser) {
            ctx.globalCompositeOperation = 'destination-out';
            ctx.arc(e.offsetX, e.offsetY, lineWidth, 0, Math.PI * 2);
            ctx.fill();
        } else {
            ctx.globalCompositeOperation = 'source-over';
            ctx.lineTo(e.offsetX, e.offsetY);
            ctx.lineWidth = lineWidth;
            ctx.strokeStyle = color;
            ctx.stroke();
        }

        lastX = e.offsetX;
        lastY = e.offsetY;
    }
});

canvas.addEventListener('mouseup', function() {
    drawing = false;
});

canvas.addEventListener('mouseout', function() {
    drawing = false;
});

// 텍스트 추가 버튼 클릭 시
function openTextModal() {
    document.getElementById("textInputModal").style.display = "block";
}

// 텍스트 모달 닫기
function closeModal() {
    document.getElementById("textInputModal").style.display = "none";
}

// 텍스트 추가
function submitText() {
    const text = document.getElementById("textInput").value;
    if (text) {
        ctx.font = '20px Arial';
        ctx.fillStyle = 'black';
        ctx.fillText(text, 100, 100);  // 텍스트는 (100, 100) 위치에 그려짐
    }
    closeModal();
}
