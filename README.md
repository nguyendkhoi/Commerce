# Commerce
Auction website,  built using the Django framework. Users can list products for sale, place bids, add items to their watchlist, and comment on auction listings.

## Key Features

## Models:
- **User**: (Django default) - Represents a registered user.
- **AuctionListings**: Represents an auction listing, including title, description, starting price, current price, category, image (optional), creator, status (active/closed), and winner (if any).
- **Bids**: Represents a bid, including the bid amount, bidder, and corresponding auction listing.
- **Comments**: Represents a comment on an auction listing, including comment content, commenter, and corresponding auction listing.
- **WatchList**: Represents a user's watchlist, allowing users to keep track of auction listings.

## Create Listing:
- Logged-in users can create new auction listings.
- Requires title, description, and starting price.
- Optionally add an image URL and category (e.g., Fashion, Toys, Electronics, Home Appliances).

## Active Listings Page:
- Displays all active auction listings.
- Shows title, description, current price, and image (if available) for each listing.
- This is the default homepage of the application.

## Listing Page:
- Displays full details of an auction listing.
- Allows logged-in users to add/remove the listing from their watchlist.
- Allows logged-in users to place bids higher than the current price (and at least equal to the starting price).
- Displays errors if the bid is invalid.
- Allows the listing creator (if logged in) to close the auction and select the highest bidder as the winner.
- Notifies logged-in users if they have won a closed auction.
- Displays all comments for the auction listing.

## Categories:
- Displays a list of all auction categories.
- Allows filtering active auction listings by category.

## Login/Register:
- Supports user authentication via login and registration forms.
- Protects certain features (creating listings, placing bids, commenting, etc.) to logged-in users only.
