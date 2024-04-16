from test import *
import asyncio

async def test():
    await test_basic_input_functions.run_tests()
    await test_spoofer_resources.run_tests()
    await test_message_responder_statics.run_tests()

asyncio.run(test())
