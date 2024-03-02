"""
Defines the Conversation class, which represents a sequence of messages between a user and a system.
"""
import os
from copy import deepcopy
from typing import List
from .message import Message


SEP = '\n__-__\n'


        
class Conversation:
    """
    Represents a conversation, which is a sequence of messages.
    Conversations can be created from strings or files and manipulated programmatically.
    """
    @classmethod
    def from_file(cls, path:str):
        assert os.path.isfile(path), f"No conversation found at {path}"
        with open(path) as f:
            return cls.from_str(f.read())
    
    @classmethod
    def from_str(cls, conv_str: str) -> 'Conversation':
        msgs = [Message(role=role, content=content)
                for msg_str in conv_str.split(SEP)
                for role, content in [msg_str.strip().split(':', 1)]]
        
        return cls(msgs)
    
    def openai(self) -> List[dict]:
        return [msg.to_dict(True) for msg in self.msgs]
        
    
    def __init__(self, msgs: List[Message], flags: dict= None) -> None:
        self._msgs = msgs
        self._flags = flags or {'should_infer': False}
        self._llm = os.getenv('AGENTFLOW_MODEL') or 'gpt-4'

    @property
    def should_infer(self) -> bool:
        return self._flags.get('should_infer', False)

    @should_infer.setter
    def should_infer(self, value: bool):
        self._flags['should_infer'] = value

    @property
    def llm(self) -> str:
        return self._llm

    @llm.setter
    def llm(self, value: str):
        self._llm = value
    @property
    def msgs(self) -> List[Message]:
        return self._msgs
    

    def __add__(self, msg: Message) -> 'Conversation':
        """Returns a new Conv instance with the given message added, as Conv instances are immutable."""
        new_msgs = deepcopy(self.msgs)  # Deep copy the list of messages
        new_msgs.append(msg)  # Append the new message
        return Conversation(new_msgs)  # Return a new Conv instance with updated messages and flags
    
    def __repr__(self):
        return '\n\n______________\n\n'.join(f"{m.role}:{m.content}" for m in self.msgs)


    def __getitem__(self, key):
        return deepcopy(self.msgs[key])
    
    def rehop(self, message_str, role='system'):
        new_conv = self + Message(role, message_str)
        new_conv.should_infer = True 
        
        return new_conv