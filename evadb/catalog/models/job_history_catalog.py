# coding=utf-8
# Copyright 2018-2023 EvaDB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint

from evadb.catalog.models.base_model import BaseModel
from evadb.catalog.models.utils import JobHistoryCatalogEntry


class JobHistoryCatalog(BaseModel):
    """The `JobHistoryCatalog` stores the execution history of jobs .
    `_row_id:` an autogenerated unique identifier.
    `_job_id:` job id.
    `_job_name:` job name.
    `_execution_start_time:` start time of this run
    `_execution_end_time:` end time for this run
    `_created_at:` entry creation time
    `_updated_at:` entry last update time
    """

    __tablename__ = "job_history_catalog"

    _job_id = Column(
        "job_id", Integer, ForeignKey("job_catalog._row_id", ondelete="CASCADE")
    )
    _job_name = Column("job_name", String(100))
    _execution_start_time = Column("execution_start_time", DateTime)
    _execution_end_time = Column("execution_end_time", DateTime)
    _created_at = Column("created_at", DateTime, default=datetime.datetime.now)
    _updated_at = Column(
        "updated_at",
        DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
    )

    __table_args__ = (UniqueConstraint("job_id", "execution_start_time"), {})

    def __init__(
        self,
        job_id: int,
        job_name: str,
        execution_start_time: datetime,
        execution_end_time: datetime,
    ):
        self._job_id = job_id
        self._job_name = job_name
        self._execution_start_time = execution_start_time
        self._execution_end_time = execution_end_time

    def as_dataclass(self) -> "JobHistoryCatalogEntry":
        return JobHistoryCatalogEntry(
            row_id=self._row_id,
            job_id=self._job_id,
            job_name=self._job_name,
            execution_start_time=self._execution_start_time,
            execution_end_time=self._execution_end_time,
            created_at=self._created_at,
            updated_at=self._updated_at,
        )