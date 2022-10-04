from fastapi import FastAPI, Request, status, Header
from dateutil import parser

from enum import Enum
from typing import Union, Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
from pydantic.datetime_parse import parse_datetime
from datetime import datetime
import os
import jwt
import pytz
import logging


class StringDateTime(datetime):
    @classmethod
    def __get_validators__(cls):
        yield parse_datetime
        yield cls.validate

    @classmethod
    def validate(cls, v: datetime):
        return v.isoformat()


class ShareType(str, Enum):
    osimis_viewer_publication = 'osimis-viewer-publication'    # a link to open the Osimis viewer valid for a long period
    meddream_instant_link = 'meddream-instant-link'     # a direct link to MedDream viewer that is valid only a few minutes for immediate publication
    meddream_viewer_publication = 'meddream-viewer-publication'       # a link to open the MedDream viewer valid for a long period


class ShareRequest(BaseModel):
    id: str
    dicom_uid: Optional[str] = Field(alias="dicom-uid", default=None)
    orthanc_id: Optional[str] = Field(alias="orthanc-id", default=None)
    anonymized: bool = False
    type: ShareType
    expiration_date: Union[StringDateTime, None] = None

    class Config:    # allow creating object from dict (used when deserializing the JWT)
        allow_population_by_field_name = True


class Share(BaseModel):
    request: ShareRequest
    token: str
    url: str


class ShareValidationRequest(BaseModel):
    dicom_uid: Optional[str] = Field(alias="dicom-uid", default=None)
    orthanc_id: Optional[str] = Field(alias="orthanc-id", default=None)
    identifier: Optional[str]
    level: str
    method: str


class ShareValidationResponse(BaseModel):
    granted: bool
    validity: int