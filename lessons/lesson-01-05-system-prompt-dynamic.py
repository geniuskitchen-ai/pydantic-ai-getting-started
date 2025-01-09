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
from datetime import date

from openai import AsyncAzureOpenAI
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from colorama import Fore, Back
from pydantic_ai.models.openai import OpenAIModel

from services import OfferService, TravelOffer, OfferSearch


class OfferSearchResults(BaseModel):
    travel_offers: list[TravelOffer]

# Set up the Client
client = AsyncAzureOpenAI()

# Set up a model
model = OpenAIModel('gpt-4o', openai_client=client)

system_prompts = [
    "You are a very polite travel agent.",
    "Mention the customer name when providing responses.",
    "Sound very enthusiastic when you provide responses."
]
# Create an instance of a PydanticAI Agent
agent = Agent(
            model,
            # result_type=OfferSearchResults
            system_prompt=system_prompts,
            deps_type=str,
        )

@agent.tool_plain
def get_available_travel_offers() -> list[TravelOffer]:
    """Returns a list of travel offers available"""
    service: OfferService = OfferService()
    return service.get_available_offers()

@agent.tool_plain
def search_customer_travel_needs(customer_id: str, destination: str, num_people:int) -> bool:
    """Searches if the specific destination is available for this customer id and travel party size

    :param customer_id: The customer id
    :param destination: The destination city
    :param num_people: How many people are traveling
    :return:
    """
    service: OfferService = OfferService()
    offer_search: OfferSearch = OfferSearch(
        customer_id=customer_id,
        destination=destination,
        passenger_count=num_people
    )
    return service.offer_is_available(offer_search)


@agent.system_prompt
def add_the_date() -> str:
    return f'The date is {date.today()}.'

@agent.system_prompt
def inject_customer_profile_data() -> str:
    customer_identifier = "12345"
    full_name = "James Garden"
    travel_party_size = 3
    return f"The customer id is {customer_identifier}. The customer name is {full_name} and has a travel party of {travel_party_size}"

#user_prompt:str = 'What are the available travel offers available today?'
user_prompt:str = 'Do you have offers to Chicago for me?'

result = agent.run_sync(user_prompt=user_prompt)

print(Fore.CYAN, result.data)

print(Back.BLUE, result.usage())