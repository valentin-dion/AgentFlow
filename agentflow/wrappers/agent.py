import os
import glob

from .instances_store import InstancesStore
from .middleware import MW, mw
from .tool import Tool, tool
from agentflow.entities import Conversation
from rich import print

_DEBUG = os.getenv('AGENTFLOW_DEBUG')

    
class Agent(metaclass=InstancesStore):
    def __init__(self, name: str, middlewares: str):
        """
        Initialize a new Agent instance.

        :param name: The name of the Agent.
        :param middlewares: A list of middleware instances to be used by the Agent.
        :raises Exception: If an Agent with the given name already exists.
        """

        _DEBUG and print(f"init Agent [green b]{name}[/] with [blue i]{middlewares}")
        self.name = name 
        
        if name in Agent:
            raise Exception(f"Agent with name '{name}' already exists.")
        
        Agent[name] = self
        
        self._middlewares = [MW[name.strip()] for name  in middlewares.split('|')]
        
    @property
    def base_prompt(self):
        grandparent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
        pattern = grandparent_path + f"/**/prompts/{self.name}.conv"

        for file_path in glob.glob(pattern):
            return Conversation.from_file(file_path)
        
        raise FileNotFoundError(f"Did not find {self.name}.conv")
  
        
    def __repr__(self):
        return f"Agent({self.name}):\t" + ' -> '.join([f"{mw}" for mw in self._middlewares])
    
    def __call__(self, input_str:str):
        """
        """
        ctx = {'agent': self, 'user_input': input_str, 'hops':0}
        
        #FIXME Should be done in a middleware
        conv = Tool['tpl'](self.base_prompt, **ctx)

        for mware in self._middlewares:
            
            conv = mware(ctx, conv)

            while isinstance(conv, Conversation) and conv.should_infer:
                _DEBUG and print(f"🤖[blue u b]{self.name}[/]_____\n{conv[-3:]}")
                #FIXME add a method that doesn't set should_infer to True
                conv = conv.rehop(
                    Tool['llm'](conv, conv._llm),
                    'assistant'
                    )
                ctx['hops'] += 1
                conv.should_infer = False
                conv = mware(ctx, conv)
                
        return conv
