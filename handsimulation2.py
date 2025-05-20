import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from treys import Card, Deck, Evaluator

def simulate_once(hero_hand, n_opponents):
    evaluator = Evaluator()
    deck = Deck()
    for card in hero_hand:
        deck.cards.remove(card)
    opponents = []
    for _ in range(n_opponents):
        hand = [deck.draw(1)[0], deck.draw(1)[0]]
        opponents.append(hand)
    community = deck.draw(5)
    hero_score = evaluator.evaluate(hero_hand, community)
    results = [("Hero", hero_score)]
    for i, hand in enumerate(opponents):
        score = evaluator.evaluate(hand, community)
        results.append((f"Opponent {i+1}", score))
    results.sort(key=lambda x: x[1])
    return results[0][0] == "Hero"

def simulate_n_times(hero_hand_strs, n_opponents, n_simulations):
    hero_hand = [Card.new(card_str) for card_str in hero_hand_strs]
    win_count = 0
    for _ in range(n_simulations):
        if simulate_once(hero_hand, n_opponents):
            win_count += 1
    return win_count / n_simulations

def generate_distinct_hands():
    ranks = '23456789TJQKA'
    hands = []
    for i in range(len(ranks)):
        for j in range(i, len(ranks)):
            if i == j:
                hands.append(f"{ranks[i]}{ranks[j]}")
            else:
                hands.append(f"{ranks[j]}{ranks[i]}s")
                hands.append(f"{ranks[j]}{ranks[i]}o")
    return hands

def hand_to_cards(hand):
    r1, r2 = hand[0], hand[1]
    if len(hand) == 2:
        return [f"{r1}s", f"{r2}h"]
    elif hand[2] == 's':
        return [f"{r1}s", f"{r2}s"]
    else:
        return [f"{r1}s", f"{r2}h"]

# Start timer
start_time = time.time()

# Simulation settings
hand_types = generate_distinct_hands()
results = []

for idx, hand in enumerate(hand_types[:2]):
    hero_cards = hand_to_cards(hand)
    win_rate = simulate_n_times(hero_cards, n_opponents=2, n_simulations=1000)
    results.append({'Hand': hand, 'WinRate': win_rate})
    print(f"[{idx+1}/{169}] Processed hand {hand}: Win rate = {win_rate:.2%}")

# Create DataFrame
df = pd.DataFrame(results).sort_values(by='WinRate', ascending=False)

# Bar Plot
plt.figure(figsize=(16, 6))
plt.bar(df['Hand'], df['WinRate'])
plt.xlabel('Poker Hand')
plt.ylabel('Win Rate vs 2 Opponents')
plt.title('Estimated Win Rates of Starting Hands')
plt.xticks(rotation=90)
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# Matrix-style Heatmap with suited/offsuit labeling
ranks = list('AKQJT98765432')
rank_index = {r: i for i, r in enumerate(ranks)}
matrix = np.full((13, 13), np.nan)

for entry in results:
    hand = entry["Hand"]
    win_rate = entry["WinRate"]
    r1, r2 = hand[0], hand[1]

    if len(hand) == 2:  # Pair
        i = j = rank_index[r1]
    elif hand[2] == 's':  # Suited
        i = rank_index[r2]
        j = rank_index[r1]
    else:  # Offsuit
        i = rank_index[r1]
        j = rank_index[r2]

    matrix[i][j] = win_rate

df_matrix = pd.DataFrame(matrix, index=ranks, columns=ranks)

plt.figure(figsize=(12, 10))
ax = sns.heatmap(df_matrix, annot=True, fmt=".2f", cmap="YlGnBu", cbar_kws={'label': 'Win Rate'})
plt.title("Grid of Poker Hand Win Rates vs 2 Opponents")
plt.xlabel("Second Card (Columns)")
plt.ylabel("First Card (Rows)")

# Highlighting the suited / offsuit / pair regions
plt.text(0.5, 12.6, "⬆ Suited hands", fontsize=10, ha='left', va='center', color='green')
plt.text(11.5, 0.2, "⬇ Offsuit hands", fontsize=10, ha='right', va='center', color='purple')
plt.text(6.5, 6.5, "⬌ Pairs (diagonal)", fontsize=10, ha='center', va='center', color='black')

plt.tight_layout()
plt.show()

# End timer
end_time = time.time()
elapsed = end_time - start_time
print(f"\n✅ All simulations complete in {elapsed:.2f} seconds.")

# Save CSV
df.to_csv("poker_hand_winrates.csv", index=False)
