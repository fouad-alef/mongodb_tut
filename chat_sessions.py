import asyncio
import logging
import os
from datetime import datetime
from typing import Optional

from beanie import Document, init_beanie
from pydantic import BaseModel, Field
