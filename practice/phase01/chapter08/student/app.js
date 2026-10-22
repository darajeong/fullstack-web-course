// HTML 요소 가져오기
const form = document.querySelector('#calculator-form');
const firstInput = document.querySelector('#first-number');
const secondInput = document.querySelector('#second-number');
const operatorSelect = document.querySelector('#operator');

// 계산 버튼을 누르거나 Enter를 누르면 실행
form.addEventListener('submit', function (event) {
    // 폼 제출로 페이지가 새로고침되는 것을 막기
    event.preventDefault();

    // 입력값의 앞뒤 공백 제거
    const firstText = firstInput.value.trim();
    const secondText = secondInput.value.trim();

    // 1. 빈 입력 검사
    if (firstText === '') {
        alert('첫 번째 숫자를 입력하세요.');
        firstInput.focus();
        return;
    }

    if (secondText === '') {
        alert('두 번째 숫자를 입력하세요.');
        secondInput.focus();
        return;
    }

    // 입력값은 문자열이므로 숫자로 변환
    const firstNumber = Number(firstText);
    const secondNumber = Number(secondText);

    // 2. 숫자인지 검사 (NaN, Infinity 등 제외)
    if (!Number.isFinite(firstNumber)) {
        alert('첫 번째 입력칸에 올바른 숫자를 입력하세요.');
        firstInput.focus();
        return;
    }

    if (!Number.isFinite(secondNumber)) {
        alert('두 번째 입력칸에 올바른 숫자를 입력하세요.');
        secondInput.focus();
        return;
    }

    const operator = operatorSelect.value;

    // 3. 나누기에서 분모가 0인지 검사
    if (operator === '/' && secondNumber === 0) {
        alert('0으로 나눌 수 없습니다. 두 번째 숫자를 바꿔주세요.');
        secondInput.focus();
        return;
    }

    // 4. 선택한 연산자로 계산
    let result;

    if (operator === '+') {
        result = firstNumber + secondNumber;
    } else if (operator === '-') {
        result = firstNumber - secondNumber;
    } else if (operator === '*') {
        result = firstNumber * secondNumber;
    } else if (operator === '/') {
        result = firstNumber / secondNumber;
    } else {
        alert('올바른 연산자를 선택하세요.');
        return;
    }

    // 계산 결과가 표현 가능한 범위를 넘었는지 검사
    if (!Number.isFinite(result)) {
        alert('계산 결과가 너무 큽니다. 더 작은 숫자를 입력하세요.');
        return;
    }

    // 5. 결과 표시
    alert(`${firstNumber} ${operator} ${secondNumber} = ${result}`);
});