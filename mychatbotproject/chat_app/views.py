# chat_app/views.py
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import MiceInfoAgent

# Instantiate the agent once for efficiency
AGENT_INSTANCE = MiceInfoAgent()

class AgentWebhookView(APIView):
    """
    Handles incoming POST requests from Telex.im (A2A protocol) at the public webhook URL.
    """
    
    # Required to allow external POST requests
    authentication_classes = [] 
    permission_classes = []     

    def post(self, request, *args, **kwargs):
        data = request.data
        
        # 1. Input Parsing (Extracting critical A2A fields)
        try:
            user_message_text = data['message']['content']['text']
            conversation_id = data['conversation_id']
            incoming_message_id = data['message']['message_id']
        except KeyError as e:
            # Log error for debugging
            print(f"A2A Payload Error: Missing key {e}")
            return Response(
                {"error": "Invalid A2A payload format."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Core Logic Execution
        ai_response_text = AGENT_INSTANCE.get_mouse_info(user_message_text)

        # 3. Output Formatting (Construct the required A2A response payload)
        response_payload = {
            "role": "agent",
            "content": {
                "type": "text",
                "text": ai_response_text
            },
            # CRUCIAL: IDs must match the incoming message for Telex.im to route the reply
            "parent_message_id": incoming_message_id, 
            "conversation_id": conversation_id,
            "message_id": os.urandom(16).hex() # Generate a simple unique response ID
        }

        # Return the A2A JSON payload with a 200 OK status
        return Response(response_payload, status=status.HTTP_200_OK)