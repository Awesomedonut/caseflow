"""SSE streaming helpers for agent status updates."""

import json
import asyncio
from collections.abc import AsyncGenerator


class SSEEmitter:
    """Emits Server-Sent Events to a connected client."""

    def __init__(self):
        self._queue: asyncio.Queue[dict | None] = asyncio.Queue()

    def emit(self, event_type: str, data: dict) -> None:
        """Queue an SSE event to send to the client."""
        self._queue.put_nowait({"event": event_type, "data": data})

    def done(self) -> None:
        """Signal that no more events will be sent."""
        self._queue.put_nowait(None)

    async def stream(self) -> AsyncGenerator[dict, None]:
        """Yield SSE events as dicts for sse-starlette."""
        while True:
            item = await self._queue.get()
            if item is None:
                break
            yield item


async def run_workflow_with_sse(
    query: str,
    jurisdiction: str = "",
    practice_area: str = "",
) -> AsyncGenerator[dict, None]:
    """Run the CaseFlow workflow and yield SSE events as each agent completes."""
    from graph.workflow import build_workflow

    emitter = SSEEmitter()

    initial_state = {
        "query": query,
        "jurisdiction": jurisdiction,
        "practice_area": practice_area,
        "search_queries": [],
        "raw_search_results": [],
        "case_references": [],
        "memo": None,
        "cited_cases": [],
        "verification_results": [],
        "agent_statuses": [],
        "errors": [],
        "iteration_count": 0,
    }

    async def run_graph():
        try:
            workflow = build_workflow()

            # Stream events from each node as it completes
            last_agent_statuses = []
            async for event in workflow.astream(initial_state):
                # LangGraph astream yields {node_name: state_update} dicts
                for node_name, state_update in event.items():
                    if node_name == "__end__":
                        continue

                    # Emit new agent status updates
                    new_statuses = state_update.get("agent_statuses", [])
                    for status in new_statuses:
                        if status not in last_agent_statuses:
                            emitter.emit("agent_status", status)
                            last_agent_statuses.append(status)

                    # Emit node-specific events
                    if "case_references" in state_update:
                        emitter.emit(
                            "research_complete",
                            {"case_references": state_update["case_references"]},
                        )

                    if "memo" in state_update and state_update["memo"]:
                        emitter.emit(
                            "synthesis_complete",
                            {"memo": state_update["memo"]},
                        )

                    if "verification_results" in state_update:
                        for vr in state_update["verification_results"]:
                            emitter.emit("verification_update", {"result": vr})

            # Get the final state by running the workflow again
            # (astream doesn't give us the final merged state easily)
            final_result = await workflow.ainvoke(initial_state)
            emitter.emit("complete", {"memo": final_result.get("memo", {})})

        except Exception as e:
            emitter.emit("error", {"message": str(e)})
        finally:
            emitter.done()

    # Start the graph in the background
    asyncio.create_task(run_graph())

    # Yield SSE events as they arrive
    async for event in emitter.stream():
        yield {
            "event": event["event"],
            "data": json.dumps(event["data"]),
        }
