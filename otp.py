import requests

def generate_and_send_otp(key, number):
    # Define the API key
    API_KEY = 'kCHQwOS38EXR3zi2kMVYWzBCyHxQ5HKjGYZjkXVHjNfOEeIIJJOE35IN9tnK'

    # Ensure the number is not empty
    if not number:
        print("No phone number found.")
        return

    # Define the parameters
    params = {
        "authorization": API_KEY,
        "route": "otp",
        "variables_values": key,  # Use the user-entered key as the OTP
        "numbers": number,        # Recipient number
        "flash": "1"
    }

    # Construct the URL
    url = "https://www.fast2sms.com/dev/bulkV2"

    # Send the GET request
    response = requests.get(url, params=params)

    # Check the response
    if response.ok:
        print("OTP:", key)
        print("OTP sent successfully to:", number)
    else:
        print("Failed to send OTP. Response:", response.text)
