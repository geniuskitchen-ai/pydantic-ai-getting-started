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

from openai import AsyncAzureOpenAI
from pydantic_ai import Agent
from pydantic_ai.models import KnownModelName
from colorama import Fore, Back
from pydantic_ai.models.openai import OpenAIModel

# Set up the Client
client = AsyncAzureOpenAI()

# Set up a model
model = OpenAIModel('gpt-4o', openai_client=client)

# Create an instance of a PydanticAI Agent
agent = Agent(model)

user_prompt:str = 'List the names of the current the governors of Florida, New York, Georgia and California in the United States?'

result = agent.run_sync(user_prompt=user_prompt)

print(Fore.CYAN, result.data)

print(Back.BLUE, result.usage())

