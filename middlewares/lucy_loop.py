from agentflow import mw,Tool, Agent 


@mw
def lucy_loop(ctx, conv):
    last_msg = conv[-1]
    
    #return last_msg.content + ' popo'
    
    agentName, content = last_msg.content.split(':',1)
    
    if agentName == 'user':
        return content
    else:
        try:
            return conv.rehop(f"{agentName}:{Agent[agentName](content)}")
        except:
            return conv.rehop(f"{agentName} is sick today, please inform user he won't come to work")
        
        
@mw
def shell_loop(ctx, conv):
    return "it's done :)"