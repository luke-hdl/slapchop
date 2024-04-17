from test import *
import asyncio

async def test():
    await test_basic_input_functions.run_tests()
    await test_spoofer_resources.run_tests()
    await test_message_responder_statics.run_tests()
    await test_message_responder_challenges.run_tests()

    if len(test_results[LogMessageType.FAILED]) > 0:
        exit(1)
    else:
        exit(0)

asyncio.run(test())
