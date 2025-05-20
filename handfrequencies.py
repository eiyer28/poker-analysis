import random
from collections import Counter
import pandas as pd

def generate_deck():
    """Generate a standard 52-card deck."""
    ranks = '23456789TJQKA'
    suits = 'cdhs'
    return [r + s for r in ranks for s in suits]

def card_rank_index(card):
    """Numerical index of card rank."""
    ranks = '23456789TJQKA'
    return ranks.index(card[0])

def normalize_hand(card1, card2):
    """Return canonical form (e.g., AKs, 55, QJo)."""
    r1, s1 = card1[0], card1[1]
    r2, s2 = card2[0], card2[1]

    if r1 == r2:
        return r1 + r2  # Pair

    if card_rank_index(card1) > card_rank_index(card2):
        high, low = r1, r2
    else:
        high, low = r2, r1

    suited = 's' if s1 == s2 else 'o'
    return high + low + suited

def simulate_starting_hands(n):
    """Simulate n random 2-card hands and tally canonical types."""
    freq = Counter()

    for _ in range(n):
        deck = generate_deck()
        hand = random.sample(deck, 2)
        label = normalize_hand(hand[0], hand[1])
        freq[label] += 1

    return freq

def generate_hand_table(n=1_000_000):
    frequencies = simulate_starting_hands(n)

    ranks = 'AKQJT98765432'
    ordered_labels = []

    # Pairs
    ordered_labels += [r + r for r in ranks]

    # Suited and offsuit hands
    for i, r1 in enumerate(ranks):
        for r2 in ranks[i+1:]:
            ordered_labels.append(r1 + r2 + 's')
    for i, r1 in enumerate(ranks):
        for r2 in ranks[i+1:]:
            ordered_labels.append(r1 + r2 + 'o')

    data = {
        'Hand': ordered_labels,
        'Count': [frequencies[label] for label in ordered_labels],
        'Percentage': [frequencies[label] / n * 100 for label in ordered_labels]
    }

    df = pd.DataFrame(data)
    return df

# Generate and print the table
table = generate_hand_table()
print(table.to_string(index=False))
