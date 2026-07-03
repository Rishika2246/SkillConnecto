// Function to send OTP
async function sendOtp() {
    const aadhaarNumber = document.getElementById('aadhaarNumber').value;
  
    if (aadhaarNumber === "") {
      alert("Please enter your Aadhaar number.");
      return;
    }
  
    const response = await fetch('http://localhost:8000/send-otp', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ aadhaarNumber: aadhaarNumber }),
    });
  
    const data = await response.json();
  
    if (response.status === 200) {
      document.getElementById('otp-section').style.display = 'none';
      document.getElementById('otp-verify-section').style.display = 'block';
      document.getElementById('message').innerHTML = 'OTP sent successfully. Please enter the OTP.';
      localStorage.setItem('requestId', data.requestId); // Store requestId for OTP verification
    } else {
      alert('Failed to send OTP: ' + data.detail);
    }
  }
  
  // Function to verify OTP
  async function verifyOtp() {
    const otp = document.getElementById('otp').value;
    const requestId = localStorage.getItem('requestId'); // Retrieve requestId from localStorage
  
    if (otp === "") {
      alert("Please enter the OTP.");
      return;
    }
  
    const response = await fetch('http://localhost:8000/verify-otp', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        requestId: requestId,
        otp: otp,
        isAadhaarMasked: false
      }),
    });
  
    const data = await response.json();
  
    if (response.status === 200) {
      document.getElementById('message').innerHTML = 'Aadhaar Verified Successfully!';
      document.getElementById('otp-verify-section').style.display = 'none';
    } else {
      alert('OTP Verification Failed: ' + data.detail);
    }
  }
  