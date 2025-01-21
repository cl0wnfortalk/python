// Highing scoring word

function high(x) {
    let maxScore = 0;
    let result;
    const getStringCode = function (string) {
        let sumScore = 0;
        for (let i=0; i<string.length;i++) {
            sumScore += string[i].toLowerCase().charCodeAt(0) - 96;
        }
        return sumScore;
    };
    let list = x.split(" ");
    let map = new Map();
    for (let i=0; i < list.length; i++) {
        map.set(list[i], getStringCode(list[i]));
    }
    for (let [k, v] of map) {
        if (v > maxScore) {
            maxScore = v;
            result = k;
        }
    };

    return result;
}

// Tribonacci

function tribonacci(signature,n){
    if (signature.length === 0) return [];
    if (n === 0) return [];
    if (n === 1) return [signature[0]];
    if (n === 2) return signature.slice(0, 2);
    let count = 0;
    for (let i = 0; i < signature.length; i++) {
        if (signature[i] === 1) count++;
        if (count === 3 && n === 1) return [1];
    }
    while (n > 3) {
        n--;
        signature.push(signature.slice(-3).reduce((x, y) => x + y));
    }
    return signature;
}

// Unique in order

var uniqueInOrder=function(iterable){
    if (iterable.length === 0) return [];
    let res = [iterable[0]];
    for (let i = 1; i < iterable.length; i++) {
        if (res[res.length - 1] !== iterable[i]) {
            res.push(iterable[i]);
        }
    }
    return res;
}

// Two Sum

function twoSum(numbers, target) {
    let map = new Map();
    for (let i = 0; i < numbers.length; i++) {
        let complement = target - numbers[i];
        if (map.has(complement)) {
            return [map.get(complement), i];
        }
        map.set(numbers[i], i);
    }
    return null;
}

function twoSum(numbers, target) {
    for (let i = 0; i <= numbers.length -1 ; i++) {
        for (let j = i + 1; j <= numbers.length; j++) {
            if (numbers[i] + numbers[j] === target) return [i, j];
        }
    }
    return -1;
}

// Shortest word

function findShort(s){
    return Math.min(...s.split(" ").map(word => word.length));
}

// Find the next perfect square

function findNextSquare(sq) {
    const root = Math.sqrt(sq);
    if (Number.isInteger(root)) {
      return (root + 1) ** 2; 
    }
    return -1;
}

// Your Order, please

function order(words){
    return words.split(" ").sort((rowA, rowB) => {return parseInt(rowA.match(/\d+/), 10) - parseInt(rowB.match(/\d+/), 10)}).join(" ");
  }

// Binary addition

function addBinary(a,b) {
    let decimal = a + b;
    let binary = [];
    while (decimal > 0) {
        let remains = decimal % 2;
        decimal = Math.floor(decimal / 2);
        binary.push(remains);
    }
    return binary.reverse().join("");
}

// Create phone number

function createPhoneNumber(numbers){
    // if array's length is less than 10 then an error raised
    if (numbers.length !== 10) throw new Error("Array numbers must have exactly 10 numbers");
    let areaCode = numbers.slice(0, 3).join("");
    let firstPart = numbers.slice(3, 6).join("");
    let secondPart = numbers.slice(6).join("");
    return `(${areaCode}) ${firstPart}-${secondPart}`;
}

// Roman Numerals Decoder

function solution(roman) {
    // Функция для получения целочисленного значения римского символа
    let getRoman = function (index) {
        switch (index) {
            case "I": return 1;
            case "V": return 5;
            case "X": return 10;
            case "L": return 50;
            case "C": return 100;
            case "D": return 500;
            case "M": return 1000;
            default: return 0; // Если символ не римский, возвращаем 0
        }
    };

    let decimal = 0;
    
    for (let i = 0; i < roman.length; i++) {
        let curr = getRoman(roman[i]);
        let prev = getRoman(roman[i - 1]);

        // Проверяем, если есть предшествующий элемент
        if (prev < curr) {
            // Если предыдущий символ меньше текущего, вычитаем значение предыдущего
            decimal += curr - prev - prev; // вычитаем prev, так как он уже добавлен
        } else {
            // В противном случае, добавляем текущее значение
            decimal += curr;
        }
    }
    
    return decimal;
}

console.log(solution("MDCLXVI")); // 1666