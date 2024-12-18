from typing import Dict, Any, List
import json 
import base64
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from google.cloud import secretmanager
from google.oauth2 import service_account
from googleapiclient.discovery import build

from email.message import EmailMessage

from app.types.node_state import NodeState 
from app.config import settings

class CraftCoverLetterNode: 
    """
    A node responsible for creating a Google Doc containing a crafted cover letter
    and optionally sending the link to the user via email. This utilizes Google Cloud
    services such as Docs, Drive, and Gmail APIs.

    Attributes:
        doc_client: Google Docs API client for document creation and updates.
        drive_client: Google Drive API client for managing permissions and sharing links.
        email_client: Gmail API client for sending emails.
    """

    def __init__(self):
        """
        Initializes the node by authenticating with Google Cloud and creating API clients
        for Docs, Drive, and Gmail.
        """
        # Authenticate and set up API clients for Google services
        credentials = self.authenticate() 
        self.doc_client = build("docs", "v1", credentials=credentials)
        self.drive_client = build("drive", "v3", credentials=credentials)
        self.email_client = build("gmail", "v1", credentials=credentials)

    def __call__(self, state: NodeState, config: RunnableConfig) -> Dict[str, Any] | None:
        """
        Creates a Google Doc for the cover letter and returns a link to the document.
        Optionally, an email with the link can be sent to the user.

        Args:
            state (NodeState): Contains the crafted cover letter and job details.
            config (RunnableConfig): Additional runtime configurations.

        Returns:
            Dict[str, Any] | None: A dictionary containing a link to the created document
            and an acknowledgment message.
        """
        # Create a Google Doc for the cover letter
        cover_letter_link = self.create_doc(
            cover_letter=state.cover_letter,
            organization=state.job_description.organization,
            position=state.job_description.position
        )

        return {
            "messages": [
                AIMessage(content=f"I have crafted a draft cover letter. Here's the link to your cover letter:\n{cover_letter_link}")
            ]
        }

    def authenticate(self, scopes: List[str] = settings.GCP_SCOPES):
        """
        Authenticates with Google Cloud using a service account and retrieves credentials.

        Args:
            scopes (List[str]): The scopes required for Google Cloud API access.

        Returns:
            Credentials: Google Cloud service account credentials.
        """
        secretmanager_client = secretmanager.SecretManagerServiceClient() 
        response = secretmanager_client.access_secret_version(name=settings.GCP_SECRET_VERSION)
        
        # Decode the service account JSON stored in Secret Manager
        service_account_info = json.loads(response.payload.data.decode("UTF-8"))
        
        # Create credentials for Google Cloud APIs
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info, scopes=scopes
        )

        return credentials

    def create_doc(self, cover_letter: str, organization: str, position: str) -> str: 
        """
        Creates a Google Doc containing the cover letter and grants public write access.

        Args:
            cover_letter (str): The text of the cover letter.
            organization (str): The name of the organization.
            position (str): The job position.

        Returns:
            str: A sharable link to the created Google Doc.
        """
        try:
            # Create a new Google Doc with the specified title
            cover_letter_doc = self.doc_client \
                .documents() \
                .create(
                    body={
                        "title": f"{organization} - {position} Cover Letter"
                    }
                ) \
                .execute()
        
            cover_letter_doc_id = cover_letter_doc["documentId"]

            # Add the cover letter content to the Google Doc
            requests = [
                {
                    "insertText": {
                        "location": {
                            "index": 1  # Insert text at the beginning of the document
                        },
                        "text": cover_letter
                    }
                }
            ]

            # Execute the batch update to insert text into the document
            self.doc_client.documents().batchUpdate(
                documentId=cover_letter_doc_id,
                body={
                    "requests": requests
                }
            ).execute()

            # Grant public write access to the document
            drive_permission = {
                "type": "anyone",
                "role": "writer"
            }

            self.drive_client.permissions().create(
                fileId=cover_letter_doc_id,
                body=drive_permission,
                fields="id"
            ).execute()

            # Generate a sharable link to the Google Doc
            share_link = f"https://docs.google.com/document/d/{cover_letter_doc_id}/edit"
            return share_link 

        except Exception as e:
            print(f"Exception: {e}")

    def send_email(self, user_email: str, position: str, organization: str, cover_letter_link: str):
        """
        Sends an email to the user containing a link to the crafted cover letter.

        Args:
            user_email (str): The recipient's email address.
            position (str): The job position.
            organization (str): The organization name.
            cover_letter_link (str): The link to the Google Doc with the cover letter.
        """
        # Create the email content
        mail_data = EmailMessage()

        mail_data["to"] = user_email 
        mail_data["subject"] = f"[Cover Letter]: {position} at {organization}"
        mail_data["from"] = settings.SERVICE_ACCOUNT

        mail_data.set_content(
            f"Here is your link to the cover letter crafted for {position} at {organization}: {cover_letter_link}"
        )

        # Encode the email message in base64
        encoded_message = base64.urlsafe_b64encode(mail_data.as_bytes()).decode()
        create_message = {"raw": encoded_message}
        
        try:
            # Send the email using the Gmail API
            send_message = (
                self.email_client.users()
                .messages()
                .send(userId="me", body=create_message)
                .execute()
            )
        except Exception as e:
            print(f"Exception: {e}")
