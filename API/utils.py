import requests 


def make_payment(merchant_id, amount, callback_url ):
    """
    Function to make a payment request.

    Parameters:
    merchant_id (str): The merchant ID for authentication.
    amount (int): The amount of the transaction in Rials.
    callback_url (str): The URL to which the payment gateway will send the response.

    Returns:
    dict: The response from the payment gateway.
    """
    url = "https://gateway.zibal.ir/v1/request"
    data = {
        "merchant": merchant_id,  # Merchant ID
        "amount": amount,  # Example amount in Rials
        "callbackUrl": callback_url,  # Your callback URL
        # Optional fields can be added here if needed
    }

    # Making the POST request
    response = requests.post(url, json=data)

    # Checking the response
    if response.ok:
        request_result = response.json()
        return request_result
    else:
        request_result = "Error in request: " + response.text
        return request_result



def process_payment_response(response):
    """
    Process the response from the make_payment function.

    Parameters:
    response (dict): The response dictionary from the make_payment function.

    Returns:
    dict: A dictionary containing the outcome of the processing.
    """
    # Check if the response contains an error
    if "error" in response:
        return {"status": "error", "message": response["error"]}

    # Check for a successful payment initiation
    if response.get("message") == "success" and response.get("result") == 100:
        track_id = response.get("trackId")
        # Process the successful payment initiation here
        # For example, you might save the trackId to your database
        return {"status": "success", "trackId": track_id, "message": "Payment initiated successfully."}

    # Handle other scenarios (like different result codes)
    else:
        return {"status": "failed", "message": "Payment initiation failed", "details": response}