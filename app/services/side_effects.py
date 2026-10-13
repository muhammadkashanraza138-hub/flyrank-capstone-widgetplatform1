import asyncio
async def send_confirmation(submission_id,email=None):
    last=None
    for attempt in range(1,3):
        try:
            await asyncio.sleep(0)
            print(f'[SIDE EFFECT] confirmation attempt={attempt} submission={submission_id} email={email}')
            return True
        except Exception as exc:
            last=exc
    print(f'[SIDE EFFECT ALERT] confirmation failed after retries: {last}')
    return False
