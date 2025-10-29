from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timedelta

"""
    Output parser used by the LLM to classify the nature of the client's requests
"""
class Output(BaseModel):
    # client intent
    schedule : Optional[bool] = Field(default=False, description="Determines if the request is a scheduling")
    cancel : Optional[bool] = Field(default=False, description="Determines if the request is a canceling")

    # datetime
    schedule_datetime : Optional[datetime] = Field(default=None, description="Scheduling datetime")
    cancel_datetime : Optional[datetime] = Field(default=None, description="Canceling datetime")

    # duration of event (1 hour by default)
    duration : Optional[timedelta] = Field(default=timedelta(hours=1), description="Duration")

    # out-of-context
    invalid_request : bool = Field(description="If the request does not fit the format")