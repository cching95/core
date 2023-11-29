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

SERVER_HOSTNAME = "mock.cloud.databricks.com"
HTTP_PATH = "sql/mock/mock-test"
ACCESS_TOKEN = "mock_databricks_token"
DATABRICKS_SQL_CONNECT = "databricks.sql.connect"
DATABRICKS_SQL_CONNECT_CURSOR = "databricks.sql.connect.cursor"

MOCKED_PARAMETER_DICT = {
    "business_unit": "mocked-buiness-unit",
    "region": "mocked-region",
    "asset": "mocked-asset",
    "data_security_level": "mocked-data-security-level",
    "data_type": "mocked-data-type",
    "tag_names": ["MOCKED-TAGNAME"],
    "start_date": "2011-01-01",
    "end_date": "2011-01-02",
    "include_bad_data": True,
}


RAW_MOCKED_QUERY = 'SELECT DISTINCT from_utc_timestamp(to_timestamp(date_format(`EventTime`, \'yyyy-MM-dd HH:mm:ss.SSS\')), "+0000") AS `EventTime`, `TagName`,  `Status`,  `Value` FROM `mocked-buiness-unit`.`sensors`.`mocked-asset_mocked-data-security-level_events_mocked-data-type` WHERE `EventTime` BETWEEN to_timestamp("2011-01-01T00:00:00+00:00") AND to_timestamp("2011-01-02T23:59:59+00:00") AND `TagName` IN (\'MOCKED-TAGNAME\') ORDER BY `TagName`, `EventTime` '
MOCKED_QUERY_OFFSET_LIMIT = "LIMIT 10 OFFSET 10 "
MOCKED_QUERY_PIVOT = 'WITH raw_events AS (SELECT DISTINCT from_utc_timestamp(to_timestamp(date_format(`EventTime`, \'yyyy-MM-dd HH:mm:ss.SSS\')), "+0000") AS `EventTime`, `TagName`,  `Status`,  `Value` FROM `mocked-buiness-unit`.`sensors`.`mocked-asset_mocked-data-security-level_events_mocked-data-type` WHERE `EventTime` BETWEEN to_timestamp("2011-01-01T00:00:00+00:00") AND to_timestamp("2011-01-02T23:59:59+00:00") AND `TagName` IN (\'MOCKED-TAGNAME\') ) ,date_array AS (SELECT explode(sequence(from_utc_timestamp(to_timestamp("2011-01-01T00:00:00+00:00"), "+0000"), from_utc_timestamp(to_timestamp("2011-01-02T23:59:59+00:00"), "+0000"), INTERVAL \'15 minute\')) AS timestamp_array) ,window_buckets AS (SELECT timestamp_array AS window_start, LEAD(timestamp_array) OVER (ORDER BY timestamp_array) AS window_end FROM date_array) ,resample AS (SELECT /*+ RANGE_JOIN(d, 900 ) */ d.window_start, d.window_end, e.`TagName`, avg(e.`Value`) OVER (PARTITION BY e.`TagName`, d.window_start ORDER BY e.`EventTime` ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS `Value` FROM window_buckets d INNER JOIN raw_events e ON d.window_start <= e.`EventTime` AND d.window_end > e.`EventTime`) ,project AS (SELECT window_start AS `EventTime`, `TagName`, `Value` FROM resample GROUP BY window_start, `TagName`, `Value` ORDER BY `TagName`, `EventTime` ) ,pivot AS (SELECT * FROM project PIVOT (FIRST(`Value`) FOR `TagName` IN (\'MOCKED-TAGNAME\'))) SELECT * FROM pivot ORDER BY `EventTime` '
RESAMPLE_MOCKED_QUERY = 'WITH raw_events AS (SELECT DISTINCT from_utc_timestamp(to_timestamp(date_format(`EventTime`, \'yyyy-MM-dd HH:mm:ss.SSS\')), "+0000") AS `EventTime`, `TagName`,  `Status`,  `Value` FROM `mocked-buiness-unit`.`sensors`.`mocked-asset_mocked-data-security-level_events_mocked-data-type` WHERE `EventTime` BETWEEN to_timestamp("2011-01-01T00:00:00+00:00") AND to_timestamp("2011-01-02T23:59:59+00:00") AND `TagName` IN (\'MOCKED-TAGNAME\') ) ,date_array AS (SELECT explode(sequence(from_utc_timestamp(to_timestamp("2011-01-01T00:00:00+00:00"), "+0000"), from_utc_timestamp(to_timestamp("2011-01-02T23:59:59+00:00"), "+0000"), INTERVAL \'15 minute\')) AS timestamp_array) ,window_buckets AS (SELECT timestamp_array AS window_start, LEAD(timestamp_array) OVER (ORDER BY timestamp_array) AS window_end FROM date_array) ,resample AS (SELECT /*+ RANGE_JOIN(d, 900 ) */ d.window_start, d.window_end, e.`TagName`, avg(e.`Value`) OVER (PARTITION BY e.`TagName`, d.window_start ORDER BY e.`EventTime` ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS `Value` FROM window_buckets d INNER JOIN raw_events e ON d.window_start <= e.`EventTime` AND d.window_end > e.`EventTime`) ,project AS (SELECT window_start AS `EventTime`, `TagName`, `Value` FROM resample GROUP BY window_start, `TagName`, `Value` ORDER BY `TagName`, `EventTime` ) SELECT * FROM project '
