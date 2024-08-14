const propertyElement = document.querySelector('.info-window.for-property');
const propertyName = propertyElement.querySelector('h4').innerText;
const propertyAddress = propertyElement.querySelector('.building-info p').innerText;
const propertyPhone = propertyElement.querySelector('.building-info .phone').innerText;

console.log(propertyName, propertyAddress, propertyPhone);
