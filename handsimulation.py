from treys import Card, Deck, Evaluator

def simulate_once(hero_hand_strs, n_opponents):
    evaluator = Evaluator()
    deck = Deck()

    # Convert strings like ['As', 'Kd'] to Card objects
    hero_hand = [Card.new(card_str) for card_str in hero_hand_strs]

    # Remove hero cards from deck
    for card in hero_hand:
        deck.cards.remove(card)

    # Deal opponent hands and remove from deck
    opponents = []
    for _ in range(n_opponents):
        hand = [deck.draw(1)[0], deck.draw(1)[0]]
        opponents.append(hand)

    # Deal 5 community cards
    community = deck.draw(5)

    # Evaluate hero and opponent hands
    hero_score = evaluator.evaluate(hero_hand, community)
    results = [("Hero", hero_score)]

    for i, hand in enumerate(opponents):
        score = evaluator.evaluate(hand, community)
        results.append((f"Opponent {i+1}", score))

    # Determine winner (lowest score wins)
    results.sort(key=lambda x: x[1])
    winner = results[0][0]
    return winner == "Hero"

def simulate_n_times(hero_hand_strs, n_opponents, n_simulations):
    win_count = 0
    for _ in range(n_simulations):
        if simulate_once(hero_hand_strs, n_opponents):
            win_count += 1
    win_rate = win_count / n_simulations
    print(f"Hero hand {hero_hand_strs} won {win_count} out of {n_simulations} games with {n_opponents} opponents")
    print(f"Estimated win rate: {win_rate * 100:.2f}%")

# Example: simulate As Ad vs 1-6 opponents over 1,000 games each
for i in range(1, 7):
    simulate_n_times(hero_hand_strs=['As', 'Ad'], n_opponents=i, n_simulations=1000)