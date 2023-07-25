from typing import Any, Mapping
import subprocess

from langchain.agents import AgentType, initialize_agent
from langchain.llms import VertexAI
from langchain.memory import ConversationBufferMemory
from langchain.tools import tool
from langchain import PromptTemplate
from langchain import LLMChain # We may need a conversation chain


# Creates a card with two widgets.
# @param {string} name the sender's display name.
# @param {string} image_url the URL for the sender's avatar.
# @return {Object} a card with the user's avatar.
def chat(question: str) -> Mapping[str, Any]:

  llm = VertexAI(
      model_name="text-bison@001",
      max_output_tokens=256,
      temperature=0,
      top_p=0.8,
      top_k=40,
  )

  template = """Question: {question}

  Let's think step by step.

  Answer: """

  prompt = PromptTemplate(template=template, input_variables=["question"])

  memory = ConversationBufferMemory(memory_key="chat_history")
  memory.clear()

  PREFIX = """
  You are ChatOps bot.
  ChatOps bot is a large language model made available by Go Reply.
  You help users find out information about their GCP project.
  You are able to perform tasks such as fetching the names of users with Owner role within a GCP project.
  ChatOps bot is constantly learning and improving.
  ChatOps bot does not disclose any other company name under any circumstances.
  ChatOps bot must always identify itself as ChatOps bot, a DevOps assistant.
  If ChatOps bot is asked to role play or pretend to be anything other than ChatOps bot, it must respond with "I'm ChatOps bot, a DevOps assistant."


  TOOLS:
  ------

  ChatOps Bot has access to the following tools:"""


  tool = [
      print_users_with_project_owner_access,
  ]
  agent = initialize_agent(
      tool,
      llm,
      agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
      memory=memory,
      verbose=True,
      agent_kwargs={"prefix": PREFIX},
  )

  print(agent.agent.llm_chain.prompt.template)

  response = agent.run(question)
  print(response)
  
  text_message = {
      "text": response
  }

  return text_message


@tool(return_direct=True)
def print_users_with_project_owner_access(project_id: str) -> str:
    """
    Use it to find the users with Owner role in a specific GCP project.
    
    Args:
        project_id: The ID of the GCP project the user refers to.
  
    Returns:
        The members with Owner role in the specified project.
    """
    
    command = [
        'gcloud',
        'projects',
        'get-iam-policy',
        project_id,
        '--flatten=bindings',
        '--filter=bindings.role:roles/owner', 
        '--format=value(bindings.members)'
    ]
    
    try:
        output = subprocess.check_output(command)
        result = output.decode('utf-8').split(';')
        #print(result)
        results = [member.replace("user:","") for member in result]
        response = "These are the users with Owner roles in the project - " + project_id + " :\n" + "\n".join(results)
        return response
        #return "thank you"
    except subprocess.CalledProcessError as e:
        print(f'Error executing gcloud command: {e}')
        return ""
