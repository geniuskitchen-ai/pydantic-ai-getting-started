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
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from colorama import Fore, Back
from pydantic_ai.models.openai import OpenAIModel

from services import OfferService, TravelOffer


class OfferSearchResults(BaseModel):
    travel_offers: list[TravelOffer]

# Set up the Client
client = AsyncAzureOpenAI()

# Set up a model
model = OpenAIModel('gpt-4o', openai_client=client)

# Create an instance of a PydanticAI Agent
agent = Agent(
            model,
            # result_type=OfferSearchResults
        )

@agent.tool_plain
def get_available_travel_offers() -> list[TravelOffer]:
    """Returns a list of travel offers available"""
    service: OfferService = OfferService()
    return service.get_available_offers()


user_prompt:str = 'What are the available travel offers available today?'

result = agent.run_sync(user_prompt=user_prompt)

print(Fore.CYAN, result.data)

print(Back.BLUE, result.usage())