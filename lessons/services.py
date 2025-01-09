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
from typing import Literal

from pydantic import BaseModel, Field


class TravelOffer(BaseModel):
    """ Represents current offers available in the database """
    destination: str #= Literal['New York', 'Paris', 'London', 'Rome', 'Chicago', 'Seattle', 'Hong Kong', 'Tokyo']
    available_seats: int = Field(ge=0, le=256)

class SelectedOffer(BaseModel):
    """ Represents the selected destination from the search """
    customer_id: str
    destination: str #= Literal['New York', 'Paris', 'London', 'Rome', 'Chicago', 'Seattle', 'Hong Kong', 'Tokyo']

class OfferSearch(BaseModel):
    """ Represents a search from a customer for a specific destination for their travel party """
    customer_id: str
    destination: str #= Literal['New York', 'Paris', 'London', 'Rome', 'Chicago', 'Seattle', 'Hong Kong', 'Tokyo']
    passenger_count: int = Field(ge=1, le=16)


class IzzyCustomerWishlistOfferSearch(BaseModel):
    """ Represents a customer request searching for available offers """
    customer_id: str
    travel_party_size: int = Field(ge=1, le=16)
    top_3_destinations: list[str]


class CustomerProfile(BaseModel):
    """ Represents a customer in the database and their profile information """
    customer_id: str
    name: str
    phone_number: str
    email: str
    destination_wishlist: list[str] # all the locations the customer would love to travel to
    travel_party_count: int = Field(ge=1, le=16)


class CustomerDatabase(BaseModel):
    """Customer database"""
    customers: dict[str, CustomerProfile]


class FinalCustomerReport(BaseModel):
    """Final customer report containing the selected destination and final message to the customer"""
    customer_id: str = None
    selected_destination: str = None | Literal['New York', 'Paris', 'London', 'Rome', 'Chicago', 'Seattle', 'Hong Kong', 'Tokyo']
    final_message: str = None



class CustomerRequestStateTracking(BaseModel):
    """This is the scratch pad used to track changes in the state machine/graph"""
    search_choice_position: int = 0  # index of the choice ( 0 through 2) for the top 3 choices
    search_completed: bool = False
    search_successful: bool = False
    selected_choice: int = -1  # the index of the choice selected


class OfferService:
    """A service used to check for offer available in the database """

    def __init__(self):
        """The constructor for the OfferService class"""
        self.offers: list[TravelOffer] = []
        self.__load_offers()

    def __load_offers(self):
        registered_offers: list[TravelOffer] = [
            TravelOffer(destination='Orlando', available_seats=1),
            TravelOffer(destination='New York', available_seats=4),
            TravelOffer(destination='Paris', available_seats=0),
            TravelOffer(destination='London', available_seats=1),
            TravelOffer(destination='Rome', available_seats=0),
            TravelOffer(destination='Chicago', available_seats=36),
            TravelOffer(destination='Seattle', available_seats=9),
            TravelOffer(destination='Hong Kong', available_seats=1),
            TravelOffer(destination='Tokyo', available_seats=9),
        ]

        self.offers = registered_offers

    def get_available_offers(self):
        """Returns available offers"""
        return self.offers

    def offer_is_available(self, offer_search: OfferSearch) -> bool:
        """Checks if the specified destination is available for the travel party size """

        destination_city: str = offer_search.destination
        number_of_seats: int = offer_search.passenger_count

        for travel_offer in self.offers:
            current_city = travel_offer.destination
            current_available_seats = travel_offer.available_seats

            if current_city == destination_city and number_of_seats <= current_available_seats:
                return True

        return False

async def fetch_customer_database() -> CustomerDatabase :

    customer_db: CustomerDatabase = CustomerDatabase(
        customers={
            "12345": CustomerProfile(
                customer_id="12345",
                name="James Garden",
                phone_number="407-555-1212",
                email="james.garden@izzyacademy.example",
                destination_wishlist=["Orlando", "New York", "Chicago", "Rome", "Tokyo"],
                travel_party_count=3
            ),
            "67890": CustomerProfile(
                customer_id="67890",
                name="Sofia Angel",
                phone_number="425-555-1212",
                email="sofia.angel@izzyacademy.example",
                destination_wishlist=["Paris", "London", "Seattle", "Hong Kong", "Orlando"],
                travel_party_count=2
            ),
            "34567": CustomerProfile(
                customer_id="34567",
                name="Solomon David",
                phone_number="212-555-1212",
                email="solomon.david@izzyacademy.example",
                destination_wishlist=["Orlando", "New York", "Seattle", "Hong Kong"],
                travel_party_count=1
            ),
            "77005": CustomerProfile(
                customer_id="77005",
                name="Esther David",
                phone_number="212-555-1212",
                email="e.david@izzyacademy.example",
                destination_wishlist=["Paris", "Rome", "Hong Kong", "Seattle", "Orlando"],
                travel_party_count=4
            ),
        }
    )

    return customer_db