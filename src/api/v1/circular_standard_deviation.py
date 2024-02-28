# Copyright 2022 RTDIP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import logging
from typing import Union
import numpy as np
from requests import request
from src.api.FastAPIApp import api_v1_router
from fastapi import HTTPException, Depends, Body, Response
import nest_asyncio
from pandas.io.json import build_table_schema
from src.sdk.python.rtdip_sdk.queries.time_series import circular_standard_deviation
from src.api.v1.models import (
    BaseQueryParams,
    BaseHeaders,
    FieldSchema,
    ResampleInterpolateResponse,
    PivotResponse,
    HTTPError,
    RawQueryParams,
    TagsQueryParams,
    TagsBodyParams,
    PivotQueryParams,
    LimitOffsetQueryParams,
    CircularAverageQueryParams,
)
from src.api.v1.common import common_api_setup_tasks, pagination

nest_asyncio.apply()


def circular_standard_deviation_events_get(
    base_query_parameters,
    raw_query_parameters,
    tag_query_parameters,
    circular_standard_deviation_query_parameters,
    pivot_parameters,
    limit_offset_parameters,
    base_headers,
):
    try:
        (connection, parameters) = common_api_setup_tasks(
            base_query_parameters,
            raw_query_parameters=raw_query_parameters,
            tag_query_parameters=tag_query_parameters,
            circular_standard_deviation_query_parameters=circular_standard_deviation_query_parameters,
            pivot_query_parameters=pivot_parameters,
            limit_offset_query_parameters=limit_offset_parameters,
            base_headers=base_headers,
        )

        data = circular_standard_deviation.get(connection, parameters)

        return Response(
            "{"
            + '"schema":{},"data":{},"pagination":{}'.format(
                FieldSchema.model_validate(
                    build_table_schema(data, index=False, primary_key=False),
                ).model_dump_json(),
                data.replace({np.nan: None}).to_json(
                    orient="records", date_format="iso", date_unit="us"
                ),
                pagination(limit_offset_parameters, data).model_dump_json(),
            )
            + "}",
        )
    except Exception as e:
        logging.error(str(e))
        raise HTTPException(status_code=400, detail=str(e))


get_description = """
## Circular Standard Deviation

Circular Standard Deviation of timeseries data.
"""


@api_v1_router.get(
    path="/events/circularstandarddeviation",
    name="Circular Standard Deviation GET",
    description=get_description,
    tags=["Events"],
    responses={
        200: {"model": Union[ResampleInterpolateResponse, PivotResponse]},
        400: {"model": HTTPError},
    },
    openapi_extra={
        "externalDocs": {
            "description": "RTDIP Circular Standard Deviation Query Documentation",
            "url": "https://www.rtdip.io/sdk/code-reference/query/functions/time_series/circular-standard-deviation/",
        }
    },
)
async def circular_standard_deviation_get(
    base_query_parameters: BaseQueryParams = Depends(),
    raw_query_parameters: RawQueryParams = Depends(),
    tag_query_parameters: TagsQueryParams = Depends(),
    circular_standard_deviation_parameters: CircularAverageQueryParams = Depends(),
    pivot_parameters: PivotQueryParams = Depends(),
    limit_offset_parameters: LimitOffsetQueryParams = Depends(),
    base_headers: BaseHeaders = Depends(),
):
    return circular_standard_deviation_events_get(
        base_query_parameters,
        raw_query_parameters,
        tag_query_parameters,
        circular_standard_deviation_parameters,
        pivot_parameters,
        limit_offset_parameters,
        base_headers,
    )


post_description = """
## Circular Standard Deviation 

Circular Standard Deviation of timeseries data via a POST method to enable providing a list of tag names that can exceed url length restrictions via GET Query Parameters.
"""


@api_v1_router.post(
    path="/events/circularstandarddeviation",
    name="Circular Standard Deviation POST",
    description=post_description,
    tags=["Events"],
    responses={
        200: {"model": Union[ResampleInterpolateResponse, PivotResponse]},
        400: {"model": HTTPError},
    },
    openapi_extra={
        "externalDocs": {
            "description": "RTDIP Circular Standard Deviation Query Documentation",
            "url": "https://www.rtdip.io/sdk/code-reference/query/functions/time_series/circular-standard-deviation/",
        }
    },
)
async def resample_post(
    base_query_parameters: BaseQueryParams = Depends(),
    raw_query_parameters: RawQueryParams = Depends(),
    tag_query_parameters: TagsBodyParams = Body(default=...),
    circular_standard_deviation_parameters: CircularAverageQueryParams = Depends(),
    pivot_parameters: PivotQueryParams = Depends(),
    limit_offset_parameters: LimitOffsetQueryParams = Depends(),
    base_headers: BaseHeaders = Depends(),
):
    return circular_standard_deviation_events_get(
        base_query_parameters,
        raw_query_parameters,
        tag_query_parameters,
        circular_standard_deviation_parameters,
        pivot_parameters,
        limit_offset_parameters,
        base_headers,
    )
