// 1. 함수: 이름을 받아 인사말을 반환합니다.
function greet(name) {
    return `안녕하세요, ${name}님! 환영합니다.`;
}

const message = greet('김코딩');

const greetingBox = document.getElementById('greeting-box');
greetingBox.textContent = message;

console.log(message);


// 2. 객체와 배열: 회원 정보를 저장합니다.
const users = [
    { id: 1, name: '김철수', age: 25, isActive: true },
    { id: 2, name: '이영희', age: 30, isActive: false },
    { id: 3, name: '박민수', age: 28, isActive: true },
    { id: 4, name: '최지우', age: 24, isActive: false }
];


// 3. map(): 모든 회원을 목록으로 표시합니다.
const userListEl = document.getElementById('user-list');

const userHtmls = users.map(user => {
    return `<li>이름: ${user.name} / 나이: ${user.age}세</li>`;
});

userListEl.innerHTML = userHtmls.join('');


// 4. filter(): 활동 중인 회원만 골라 표시합니다.
const activeUserListEl = document.getElementById('active-user-list');

const activeUsers = users.filter(user => user.isActive);

const activeUserHtmls = activeUsers.map(user => {
    return `<li>활성 회원 이름: ${user.name}</li>`;
});

activeUserListEl.innerHTML = activeUserHtmls.join('');


// 5. 확인 버튼: 입력한 이름과 나이를 출력합니다.
const ageInput = document.getElementById('age');
const nameInput = document.getElementById('name');
const button = document.getElementById('btn');

button.addEventListener('click', function () {
    const age = ageInput.value.trim();
    const name = nameInput.value.trim();

    if (age === '' || name === '') {
        alert('나이와 이름을 모두 입력해 주세요.');
        return;
    }

    const result = `이름: ${name} / 나이: ${age}세`;

    alert(result);
    console.log(result);
});