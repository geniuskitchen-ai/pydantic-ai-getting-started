# MIT License
#
# Copyright (c) 2024 to present. IzzyAcademy.AI
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from pydantic import BaseModel
from pydantic_ai import Agent
from colorama import Fore, Back
from pydantic_ai.models.ollama import OllamaModel, OllamaModelName

class GovernorEntry(BaseModel):
    governor_name: str
    state_name: str

class ResultList(BaseModel):
    states: list[GovernorEntry]

# Specify the model name
model_name:OllamaModelName = 'llama3.2'

model = OllamaModel(model_name)

# Create an instance of a PydanticAI Agent
agent = Agent(model, result_type=GovernorEntry)

user_prompt:str = 'Who is the governor of Florida?'

result = agent.run_sync(user_prompt=user_prompt)

print(Fore.BLUE, result.data)

print(Back.GREEN, result.usage())

