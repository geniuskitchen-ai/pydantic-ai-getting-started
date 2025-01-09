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

from __future__ import annotations

import asyncio
from typing import Union

from colorama import Fore
from pydantic_ai_graph.graph import Graph
from pydantic_ai_graph.nodes import BaseNode, GraphContext, End

from services import OfferService, OfferSearch, CustomerRequestStateTracking, CustomerProfile, \
    IzzyCustomerWishlistOfferSearch, CustomerDatabase, FinalCustomerReport, SelectedOffer, fetch_customer_database


class TravelRequestResetAgent(
    BaseNode[OfferSearch, FinalCustomerReport, CustomerDatabase, CustomerRequestStateTracking]):

    async def run(self, ctx: GraphContext) -> Union[TravelRequestPreparerAgent, AvailabilityReporterAgent]:
        database: CustomerDatabase = ctx.deps
        current_search: OfferSearch = self.input_data
        customer_id = current_search.customer_id
        customer_profile: CustomerProfile = database.customers[customer_id]

        top_destinations = customer_profile.destination_wishlist[0:3]

        graph_state: CustomerRequestStateTracking = ctx.state

        graph_state.search_choice_position = graph_state.search_choice_position + 1

        offer_search: IzzyCustomerWishlistOfferSearch = IzzyCustomerWishlistOfferSearch(
            customer_id=current_search.customer_id,
            travel_party_size=current_search.passenger_count,
            top_3_destinations=top_destinations
        )

        current_destination_index = graph_state.search_choice_position

        if current_destination_index < 3:
            return TravelRequestPreparerAgent(offer_search)
        else:
            graph_state.search_completed = True
            graph_state.search_successful = False
            return AvailabilityReporterAgent(SelectedOffer(customer_id=customer_id, destination=''))

class AvailabilityReporterAgent(
    BaseNode[SelectedOffer, FinalCustomerReport, CustomerDatabase, CustomerRequestStateTracking]):
    async def run(self, ctx: GraphContext) -> End[FinalCustomerReport]:
        offer = self.input_data
        destination = offer.destination
        graph_state: CustomerRequestStateTracking = ctx.state

        destination_index_names: list[str] = ["1st", "2nd", "3rd"]
        selected_destination_index = graph_state.search_choice_position

        if graph_state.search_successful:
            destination_index_name = destination_index_names[selected_destination_index]
            final_message = f"Dear Customer, your {destination_index_name} preferred destination {destination} was available"
        else:
            final_message = "None of your preferred destinations were available"

        final_report: FinalCustomerReport = FinalCustomerReport(customer_id=offer.customer_id,
                                                                selected_destination=offer.destination,
                                                                final_message=final_message)
        return End(final_report)

class OfferSearchAgent(BaseNode[OfferSearch, FinalCustomerReport, CustomerDatabase, CustomerRequestStateTracking]):
    async def run(self, ctx: GraphContext) -> AvailabilityReporterAgent | TravelRequestResetAgent:
        service: OfferService = OfferService()
        offer_search: OfferSearch = self.input_data
        customer_id: str = offer_search.customer_id
        destination_is_available: bool = service.offer_is_available(offer_search)
        graph_state: CustomerRequestStateTracking = ctx.state

        if destination_is_available:
            graph_state.search_completed = True
            graph_state.search_successful = True
            graph_state.selected_choice = graph_state.search_choice_position

            selected_offer = SelectedOffer(customer_id=customer_id, destination=offer_search.destination)
            return AvailabilityReporterAgent(selected_offer)
        else:
            return TravelRequestResetAgent(offer_search)


class TravelRequestPreparerAgent(
    BaseNode[IzzyCustomerWishlistOfferSearch, FinalCustomerReport, CustomerDatabase, CustomerRequestStateTracking]):
    async def run(self, ctx: GraphContext) -> OfferSearchAgent:
        offer_search: OfferSearch = self.prepare_offer_search(wishlist=self.input_data, graph_state=ctx.state)
        return OfferSearchAgent(offer_search)

    @staticmethod
    def prepare_offer_search(wishlist: IzzyCustomerWishlistOfferSearch, graph_state: CustomerRequestStateTracking):
        destination_index = graph_state.search_choice_position
        selected_destination = wishlist.top_3_destinations[destination_index]

        return OfferSearch(
            customer_id=wishlist.customer_id,
            destination=selected_destination,
            passenger_count=wishlist.travel_party_size
        )

class ConciergeAgent(BaseNode[CustomerProfile, FinalCustomerReport, CustomerDatabase, CustomerRequestStateTracking]):
    async def run(self, ctx: GraphContext) -> TravelRequestPreparerAgent:
        customer_profile: CustomerProfile = self.input_data
        customer_id: str = customer_profile.customer_id
        party_size: int = customer_profile.travel_party_count
        top_3_destination_cities = customer_profile.destination_wishlist[0:3]

        offer_search: IzzyCustomerWishlistOfferSearch = IzzyCustomerWishlistOfferSearch(
            customer_id=customer_id,
            travel_party_size=party_size,
            top_3_destinations=top_3_destination_cities
        )

        return TravelRequestPreparerAgent(offer_search)


class CallCenterGreeterAgent(BaseNode[str, FinalCustomerReport, CustomerDatabase, CustomerRequestStateTracking]):
    """The entry point and starting point in the graph and state machine"""

    async def run(self, ctx: GraphContext) -> ConciergeAgent:
        customer_id: str = self.input_data
        customer_database: CustomerDatabase = ctx.deps
        customer_profile: CustomerProfile = await self.retrieve_customer_profile(customer_id, customer_database)
        return ConciergeAgent(customer_profile)

    @staticmethod
    async def retrieve_customer_profile(customer_id: str, db: CustomerDatabase) -> CustomerProfile:
        customer_profile: CustomerProfile = db.customers[customer_id]
        return customer_profile


async def pydantic_ai_graph_state_machine():

    customer_db = await fetch_customer_database()

    customer_ids: list[str] = [
        "12345", # James Garden has a travel party of 3 & prefers: Orlando", "New York", "Chicago"
        "67890", # Sofia Angel has a travel party of 2 and prefers: "Paris", "London", "Seattle"
        "34567", # Solomon David has a travel party of 1 and prefers: "Orlando", "New York", "Seattle"
        "77005", # Esther David has a travel party of 4 and prefers: "Paris", "Rome", "Hong Kong"
    ]
    graph_input_data: str = customer_ids[0]  # the customer identifier
    graph_dependency: CustomerDatabase = customer_db


    g = Graph[str, FinalCustomerReport, CustomerDatabase, CustomerRequestStateTracking](
        CallCenterGreeterAgent,
        ConciergeAgent, TravelRequestPreparerAgent,
        OfferSearchAgent, AvailabilityReporterAgent, TravelRequestResetAgent,
    )

    graph_state = CustomerRequestStateTracking()
    graph_output, final_graph_state = await g.run(graph_input_data, graph_dependency, graph_state)

    # Print out the final output of the graph
    print(Fore.YELLOW,"\nGraph Output")
    print(Fore.YELLOW, graph_output)

    # Print out the state transitions that led to the output
    print(Fore.BLUE, "\nFinal Graph State")
    print(Fore.BLUE, final_graph_state)

    print(Fore.GREEN, "\nMermaid Code")
    print(Fore.GREEN, g.mermaid_code())


# Run the graph
asyncio.run(pydantic_ai_graph_state_machine())
