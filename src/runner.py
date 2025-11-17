"""
GLAIP SDK Runner Module

A reusable module for running agent queries using the GLAIP SDK.
Can be used independently or by the executor.
"""

import asyncio
import json
import os
import traceback
from typing import Optional, Dict, Any, AsyncIterator, List

from dotenv import load_dotenv
from glaip_sdk.client.agents import AgentClient

load_dotenv()

# Constants
SEPARATOR_WIDTH = 80
DEFAULT_TIMEOUT = 500


class AIPRunner:
    """Runner class for executing agent queries using GLAIP SDK"""

    def __init__(
        self,
        aip_api_url: Optional[str] = None,
        aip_api_key: Optional[str] = None,
        bosa_token: Optional[str] = None,
        bosa_api_key: Optional[str] = None,
    ):
        """
        Initialize the AIP Runner.

        Args:
            aip_api_url: AIP API base URL (defaults to AIP_API_URL env var)
            aip_api_key: AIP API key (defaults to AIP_API_KEY env var)
            bosa_token: BOSA authentication token (defaults to BOSA_USER_TOKEN env var)
            bosa_api_key: BOSA API key (defaults to BOSA_API_KEY env var)
        """
        self.aip_api_url = aip_api_url or os.getenv("AIP_API_URL")
        self.aip_api_key = aip_api_key or os.getenv("AIP_API_KEY")
        self.bosa_token = bosa_token or os.getenv("BOSA_USER_TOKEN")
        self.bosa_api_key = bosa_api_key or os.getenv("BOSA_API_KEY")

        self._validate_config()
        self.client = AgentClient(api_url=self.aip_api_url, api_key=self.aip_api_key)

    def _validate_config(self) -> None:
        """Validate that required configuration is present."""
        if not self.aip_api_url or not self.aip_api_key:
            raise ValueError("AIP_API_URL and AIP_API_KEY must be set")

    def _build_tool_configs(self, tool_ids: List[str]) -> Dict[str, Dict[str, str]]:
        """Build tool configuration dictionary."""
        return {tool_id: {"bosa_token": self.bosa_token} for tool_id in tool_ids}

    def _build_mcp_configs(self, mcp_ids: List[str]) -> Dict[str, Dict[str, Any]]:
        """Build MCP configuration dictionary."""
        return {
            mcp_id: {
                "authentication": {
                    "type": "custom-header",
                    "headers": {
                        "X-Api-Key": self.bosa_api_key,
                        "Authorization": f"Bearer {self.bosa_token}",
                    },
                }
            }
            for mcp_id in mcp_ids
        }

    def _build_payload(
        self, query: str, tool_ids: List[str], mcp_ids: List[str]
    ) -> Dict[str, Any]:
        """Build the payload for agent execution."""
        payload = {"input": query}

        if self.bosa_token:
            payload["tool_configs"] = self._build_tool_configs(tool_ids)

            if self.bosa_api_key:
                payload["mcp_configs"] = self._build_mcp_configs(mcp_ids)

        return payload

    def _get_agent_config_ids(self, agent_id: str) -> tuple[List[str], List[str]]:
        """Get tool IDs and MCP IDs from agent configuration."""
        agent_config = self.client.get_agent_by_id(agent_id=agent_id)
        tool_ids = [tool["id"] for tool in agent_config.tools]
        mcp_ids = [mcp["id"] for mcp in agent_config.mcps]
        return tool_ids, mcp_ids

    async def run_agent_streaming(
        self, agent_id: str, query: str, timeout: int = DEFAULT_TIMEOUT
    ) -> AsyncIterator[Dict[str, Any]]:
        """
        Run an agent query with streaming responses.

        Args:
            agent_id: The agent ID (UUID)
            query: The query/prompt to send to the agent
            timeout: Timeout in seconds (default: 500)

        Yields:
            Streaming response data as dictionaries
        """
        tool_ids, mcp_ids = self._get_agent_config_ids(agent_id)
        payload = self._build_payload(query, tool_ids, mcp_ids)

        response = self.client.arun_agent(
            agent_id=agent_id,
            message=payload.pop("input", ""),
            timeout=timeout,
            **payload,
        )

        async for data in response:
            yield data

    def _is_final_response(self, data: Dict[str, Any]) -> bool:
        """Check if the response is a final response."""
        return data.get("final") is True or data.get("event_type") == "final_response"

    def _extract_final_content(self, data: Dict[str, Any]) -> Optional[Any]:
        """Extract and parse final content from response data."""
        content = data.get("content")
        if not content:
            return None

        if isinstance(content, str):
            try:
                return json.loads(content)
            except (json.JSONDecodeError, TypeError):
                return content

        return content

    def _format_streaming_responses(self, responses: List[Dict[str, Any]]) -> str:
        """Format streaming responses with separators."""
        if not responses:
            return ""

        json_responses = [json.dumps(response, indent=2) for response in responses]
        separator = f"\n{'─' * SEPARATOR_WIDTH}\n"
        return separator.join(json_responses)

    def _format_final_content_box(self, final_content: Any) -> str:
        """Format final content in a box."""
        final_content_json = json.dumps(final_content, indent=2, ensure_ascii=False)
        border = "═" * SEPARATOR_WIDTH
        return f"\n\n{border}\nFINAL CONTENT\n{border}\n{final_content_json}\n{border}"

    def _extract_final_content_from_data(self, data: Dict[str, Any]) -> Optional[Any]:
        """
        Extract final content from response data if it's a final response.

        Returns:
            Final content if this is a final response, None otherwise
        """
        if self._is_final_response(data):
            return self._extract_final_content(data)
        return None

    async def run_agent(
        self, agent_id: str, query: str, timeout: int = DEFAULT_TIMEOUT
    ) -> Dict[str, Any]:
        """
        Run an agent query and collect all streaming responses.

        Args:
            agent_id: The agent ID (UUID)
            query: The query/prompt to send to the agent
            timeout: Timeout in seconds (default: 500)

        Returns:
            Dictionary with 'success', 'stdout', 'stderr', 'return_code', and 'final_content'
        """
        responses: List[Dict[str, Any]] = []
        final_content: Optional[Any] = None
        error_messages: List[str] = []

        try:
            async for data in self.run_agent_streaming(agent_id, query, timeout):
                responses.append(data)
                extracted_final = self._extract_final_content_from_data(data)
                if extracted_final is not None:
                    final_content = extracted_final

        except Exception as stream_error:
            error_messages.append(f"Error during streaming: {str(stream_error)}")
            error_messages.append(traceback.format_exc())

        stdout_content = self._format_streaming_responses(responses)

        if final_content is not None:
            stdout_content += self._format_final_content_box(final_content)

        stderr_content = "\n".join(error_messages) if error_messages else ""
        success = len(responses) > 0

        return {
            "success": success,
            "stdout": stdout_content,
            "stderr": stderr_content,
            "return_code": 0 if success else -1,
            "final_content": final_content,
        }

    def run_agent_sync(
        self, agent_id: str, query: str, timeout: int = DEFAULT_TIMEOUT
    ) -> Dict[str, Any]:
        """
        Synchronous wrapper for run_agent.

        Args:
            agent_id: The agent ID (UUID)
            query: The query/prompt to send to the agent
            timeout: Timeout in seconds (default: 500)

        Returns:
            Dictionary with 'success', 'stdout', 'stderr', and 'return_code'
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            return loop.run_until_complete(self.run_agent(agent_id, query, timeout))
        finally:
            loop.close()


def print_raw_response(data: dict) -> None:
    """Print raw response data in a box."""
    border = "─" * SEPARATOR_WIDTH
    print(f"\n{border}")
    print(json.dumps(data, indent=2))
    print(border)


async def main():
    """Main function to run GLAIP agent query (for standalone use)."""
    query = "List all my upcoming meetings today"
    agent_id = "d7391163-9ac9-4026-98aa-c1b8b138fe8a"

    try:
        runner = AIPRunner()
        print(f"Running agent {agent_id} with query: {query}")
        async for data in runner.run_agent_streaming(agent_id, query):
            print_raw_response(data)

    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
