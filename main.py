import Google_APIs_Tools as google_api_tools



def main():
    # Create an instance of ApiKeys
    api_keys = google_api_tools.ApiKeys()
    
    # Create an instance of SessionTokenRequest
    session_request = google_api_tools.SessionTokenRequest(api_keys)
    
    try:
        # Request a session token
        session_request_response = session_request.request_session_token()
        print(session_request_response)
    except google_api_tools.SessionTokenRequest.SessionTokenError as e:
        print(f"{e.args[0]}: {e.args[1]}")

if __name__ == "__main__":
    main()