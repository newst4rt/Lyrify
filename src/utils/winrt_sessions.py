from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager
import asyncio

async def main():
    manager = await GlobalSystemMediaTransportControlsSessionManager.request_async()
    sessions = manager.get_sessions()
    return sessions

sessions = asyncio.run(main())
for x in sessions:
    print(x.source_app_user_model_id)



