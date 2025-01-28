from typing import List

from pydantic.v1 import BaseModel, Field


class Issue(BaseModel):
    issue_title: str = Field(description="A concise title for the issue")
    issue_description: str = Field(description="A description of the issue from the user’s perspective. "
                                               "You can use the following points as a guidance on what to write, but you’re not limited to these: "
                                               "How the user found the issue, why they thought it is an issue, and how it affected them. "
                                               "You can refer to UI elements of the software in describing the issue.")
    timestamps: List[str] = Field(description="Instances in the transcript where this issue was mentioned. "
                                              "There can be more than one timestamp for one issue, in case the same issue is being reported multiple times during the user study.")
    wcag: str = Field(description="Reference to the WCAG guideline that is being violated.")
    # internal: str = Field(description="Reference to the \'Takeaway\' or \'Best Practice\' from the internal guidelines that is related.")


class Report(BaseModel):
    issues: List[Issue] = Field(description="A list of issues.")