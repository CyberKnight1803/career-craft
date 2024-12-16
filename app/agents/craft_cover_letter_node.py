from typing import Dict, Any, List
import json 
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from google.cloud import secretmanager
from google.oauth2 import service_account
from googleapiclient.discovery import build

from app.types.node_state import NodeState 
from app.config import settings

class CraftCoverLetterNode: 
    def __init__(self):
        # Default scopes
        credentials = self.authenticate() 
        self.doc_client = build("docs", "v1", credentials=credentials)
        self.drive_client = build("drive", "v3", credentials=credentials)


    def __call__(self, state: NodeState, config: RunnableConfig) -> Dict[str, Any] | None:
        cover_letter_link = self.create_doc(
            cover_letter=state.cover_letter,
            organization=state.job_description.organization,
            position=state.job_description.position
        )

        return {
            "messages": [
                AIMessage(content="Shared your cover letter via email!"
                f"Here's the link to your cover letter: {cover_letter_link}"
                ),
            ]
        }


    def authenticate(self, scopes: List[str] = settings.GCP_SCOPES):
        secretmanager_client = secretmanager.SecretManagerServiceClient() 
        response = secretmanager_client.access_secret_version(name=settings.GCP_SECRET_VERSION)
        service_account_info = json.loads(response.payload.data.decode("UTF-8"))
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info, scopes=scopes
        )

        return credentials

    def create_doc(self, cover_letter: str, organization: str, position: str) -> str: 
        cover_letter_doc = self.doc_client \
                .documents() \
                .create(
                    body={
                        "title": f"{organization} - {position} Cover Letter"
                    }
                ) \
                .execute()
    
        cover_letter_doc_id = cover_letter_doc["documentId"]

        requests = [
            {
                "insertText": {
                    "location": {
                        "index": 1
                    },
                    "text": cover_letter
                }
            }
        ]

        self.doc_client.documents().batchUpdate(
            documentId=cover_letter_doc_id,
            body={
                "requests": requests
            }
        ).execute()

        drive_permission = {
            "type": "anyone",
            "role": "writer"
        }

        self.drive_client.permissions().create(
            fileId=cover_letter_doc_id,
            body=drive_permission,
            fields="id"
        ).execute()

        share_link = f"https://docs.google.com/document/d/{cover_letter_doc_id}/edit"
        return share_link 