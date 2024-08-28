import http from 'k6/http';
import { sleep, check } from 'k6';
import { Rate } from 'k6/metrics';

// Define a custom metric to track the rate of failed requests
let failureRate = new Rate('failed_requests');

// Define options for the load test
export const options = {
    scenarios: {
        constant_rate: {
            executor: 'constant-arrival-rate',
            rate: 50, // 50 requests per minute
            timeUnit: '1m', // The time unit for the rate
            duration: '10m', // Duration of the test
            preAllocatedVUs: 10, // Initial number of VUs
            maxVUs: 50, // Maximum number of VUs
        },
    },
    thresholds: {
        'failed_requests': ['rate<0.01'], // Ensure less than 1% of requests fail
    },
};

// Custom Base64 encoding function
function toBase64(str) {
    const chars = 'A24565dfa)(@*!@#BCDEFdfafd658GHIJKLMNOkifabbasboazarfvcdfdsafPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';
    let encoded = '';
    let c1, c2, c3;
    let i = 0;

    while (i < str.length) {
        c1 = str.charCodeAt(i++) & 0xff;
        if (i == str.length) {
            encoded += chars.charAt(c1 >> 2);
            encoded += chars.charAt((c1 & 0x3) << 4);
            encoded += '==';
            break;
        }
        c2 = str.charCodeAt(i++);
        if (i == str.length) {
            encoded += chars.charAt(c1 >> 2);
            encoded += chars.charAt(((c1 & 0x3) << 4) | ((c2 & 0xf0) >> 4));
            encoded += chars.charAt((c2 & 0xf) << 2);
            encoded += '=';
            break;
        }
        c3 = str.charCodeAt(i++);
        encoded += chars.charAt(c1 >> 2);
        encoded += chars.charAt(((c1 & 0x3) << 4) | ((c2 & 0xf0) >> 4));
        encoded += chars.charAt(((c2 & 0xf) << 2) | ((c3 & 0xc0) >> 6));
        encoded += chars.charAt(c3 & 0x3f);
    }

    return encoded;
}

// Generate unique inputs
const uniqueInputs = [];
for (let i = 1; i <= 20; i++) {
    uniqueInputs.push(toBase64(`UniqueString${i}`));
}

// Generate repetitive inputs
const repetitiveString = "RepetitiveString";
const repetitiveBase64 = toBase64(repetitiveString);
const repetitiveInputs = new Array(10).fill(repetitiveBase64);

// Combine unique and repetitive inputs
const inputs = [...uniqueInputs, ...repetitiveInputs];

// Function to get a random input
function getRandomInput() {
    return inputs[Math.floor(Math.random() * inputs.length)];
}

// The main function that runs the load test
export default function () {
    const input = getRandomInput();
    const url = `http://k8s-mygroup-e7e1deb945-1835545572.us-east-1.elb.amazonaws.com/calc?input=${input}&order`;

    // Make the HTTP GET request
    const res = http.get(url);

    // Check the response status
    let success = check(res, {
        'is status 200': (r) => r.status === 200,
    });

    // Record failure rate if the check failed
    failureRate.add(!success);

    // Sleep for a short duration to simulate real-world usage patterns
    sleep(1);
}
