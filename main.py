from openai import OpenAI
import os, sys, asyncio
signal = False

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Set Model/Parameters
model = 'gpt-4o-mini'
temperature = 0.5
max_tokens = 250 # unused by default
messages = []


async def chatgpt(prompt) -> None:
    from functools import partial
    def sync_chatgpt_call():
        messages.append({"role": "user", "content": prompt})
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature
            )
            msg = response.choices[0].message
            messages.append({"role": msg.role, "content": msg.content})
            return msg.content
        except Exception as e:
            print(e)
            return None
    
    # Offload the blocking call to a thread
    return await asyncio.to_thread(sync_chatgpt_call)


async def load_anim() -> None:
    animation = ['⣾', '⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽']
    i = 0
    while True:
        print(animation[i], end='\r')
        i = (i + 1) % len(animation)
        await asyncio.sleep(0.1)

def get_prompt() -> None:
    try:
        with open('/home/delloid/projects/python/cmfind/.prompt', 'r') as file:
            prompt = file.read()
        prompt += ''.join([arg + ' ' for arg in sys.argv[1:]])
    except FileNotFoundError as f:
        print('Can\'t find prompt file')
    return prompt


async def main() -> None:
    anim_task = asyncio.create_task(load_anim())
    prompt = get_prompt()
    chatbot_task = asyncio.create_task(chatgpt(prompt))
    output = await chatbot_task
    print(output)
    anim_task.cancel()
    

if __name__ == "__main__":
    asyncio.run(main())
