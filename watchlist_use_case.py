from watchlist_repository import WatchlistRepository


class WatchlistUseCase:
    def __init__(self) -> None:
        self.watchlist_repository = WatchlistRepository()

    def get_watchlist(self):
        watchlist = self.watchlist_repository.get_all()
        filtered_watchlist = []
        for stock in watchlist:
            filtered_watchlist.append([
                stock.symbol,
                stock.expected_price,
            ])