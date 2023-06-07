class AutoSolve:

    def __init__(self, game):
        self.game = game

    def solve(self):
        moved = False

        while moved:
            moved = False

            for table in self.game.tables:

                card = table.bottom_card()
                if card is not None:
                    moved = self.bottom_card_foundation(card, table, moved)
                    if not moved:
                        moved = self.bottom_card_table(card, table, moved)

    def bottom_card_foundation(self, card, table, moved):
        for foundation in self.game.foundations:
            if foundation.get_suit() == card.get_suit():
                if foundation.get_top_card() is None or foundation.get_top_card().get_value() == card.get_value() + 1:
                    foundation.add_card(card)
                    table.remove_card(card)
                    moved = True
                    break
        return moved

    def bottom_card_table(self, card, table, moved):
        for table_index in range(len(self.game.tables) - 1, -1, -1):
            other_table = self.game.tables[table_index]
            if other_table != table:
                other_card = other_table.bottom_card()
                if other_card is not None and other_card.get_color() != card.get_color() and other_card.get_value() == card.get_value() - 1:
                    other_table.remove_card(other_card)
                    table.add_cards([card, other_card])
                    moved = True
                    break
        return moved