# Copyright 2025 Google LLC
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

import json
import logging
from collections.abc import Sequence
from typing import Any

from google.cloud import logging as google_cloud_logging
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.sdk.trace.export import SpanExportResult


class CloudTraceLoggingSpanExporter(CloudTraceSpanExporter):
    """
    A simplified version of CloudTraceSpanExporter that logs span data to Google Cloud Logging.

    This class logs spans to Cloud Logging while keeping them within size limits by truncating
    large attribute values instead of using Cloud Storage.
    """

    def __init__(
        self,
        logging_client: google_cloud_logging.Client | None = None,
        debug: bool = False,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the exporter with Google Cloud clients and configuration.

        :param logging_client: Google Cloud Logging client
        :param debug: Enable debug mode for additional logging
        :param kwargs: Additional arguments to pass to the parent class
        """
        super().__init__(**kwargs)
        self.debug = debug
        self.logging_client = logging_client or google_cloud_logging.Client(
            project=self.project_id
        )
        self.logger = self.logging_client.logger(__name__)

    def export(self, spans: Sequence[ReadableSpan]) -> SpanExportResult:
        """
        Export the spans to Google Cloud Logging and Cloud Trace.

        :param spans: A sequence of spans to export
        :return: The result of the export operation
        """
        for span in spans:
            span_context = span.get_span_context()
            trace_id = format(span_context.trace_id, "x")
            span_id = format(span_context.span_id, "x")
            span_dict = json.loads(span.to_json())

            span_dict["trace"] = f"projects/{self.project_id}/traces/{trace_id}"
            span_dict["span_id"] = span_id

            span_dict = self._process_large_attributes(span_dict)

            if self.debug:
                print(span_dict)

            # Log the span data to Google Cloud Logging
            self.logger.log_struct(
                span_dict,
                labels={
                    "type": "agent_telemetry",
                    "service_name": "researcher-agent",
                },
                severity="INFO",
            )
        # Export spans to Google Cloud Trace using the parent class method
        return super().export(spans)

    def _process_large_attributes(self, span_dict: dict) -> dict:
        """
        Process large attribute values by truncating them if they exceed Cloud Logging size limits.

        :param span_dict: The span data dictionary
        :return: The updated span dictionary with truncated attributes if needed
        """
        attributes = span_dict["attributes"]
        max_size = 200 * 1024  # 200 KB limit to stay well under Cloud Logging's 256KB limit
        
        if len(json.dumps(attributes).encode()) > max_size:
            # Truncate large attribute values
            truncated_attributes = {}
            for key, value in attributes.items():
                if isinstance(value, str) and len(value.encode()) > 10000:  # 10KB per attribute
                    truncated_value = value[:9900] + "... [truncated]"
                    truncated_attributes[key] = truncated_value
                    logging.info(f"Truncated large attribute '{key}' to stay within logging limits")
                else:
                    truncated_attributes[key] = value

            span_dict["attributes"] = truncated_attributes
            logging.info("Processed large span attributes by truncating to fit Cloud Logging limits")

        return span_dict
