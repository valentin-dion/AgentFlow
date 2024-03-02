import os
from openai import OpenAI
from agentflow import tool, Conversation
from rich import print

_DEBUG = os.getenv('AGENTFLOW_DEBUG')

@tool
def llm(conversation: Conversation, model='gpt-4') -> Conversation:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))



    response = client.chat.completions.create(model=model,
            messages=conversation.openai(), 
            max_tokens=4000,
            temperature=0,
            stream=True)

    
    _DEBUG and print('\n\n')
    msg = ''
    for message in response:

        mm = message.choices[0].delta.content
                

        if mm:                    
            msg += mm
            _DEBUG and print(f"[red]{mm}",end='')
            with open('/tmp/agentflow3.inf','w') as f:
                f.write(msg)
                
    print('\n____[green]____')
                    
    return msg