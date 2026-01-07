# OpenSpec Specification - MTG Deck Creator

## Introduction

This system is a Magic: The Gathering deck creation software. It helps users generate decks that are playable, competitive, and fun using MTGJson API.

## Terminology

Here are some terms frequently used in this document,

1. **Deck**: A collection of MTG cards a player will use in a game.
2. **MTG**: Magic: The Gathering, a collectible and digital collectible card game.
3. **API**: Application Programming Interface, a software intermediary that allows two applications to talk to each other.

## System Components

### Deck Creator

This part of the software is responsible for generating MTG decks. It uses the MTGJson API to access a vast database of cards and select those that work best with the chosen strategy. Decks created by this component should be playable, competitive, and fun.

### Strategy Selector

This component is focused on choosing the most effective and synergy-rich strategies for the deck. The strategy chosen by the Strategy Selector will greatly influence which cards the Deck Creator ultimately includes in the created deck.

### Evolutionary Testing Algorithm

To ensure that the generated decks are effective, we will also include an Evolutionary Testing Algorithm. This algorithm will simulate various gameplay scenarios to assess and refine the deck's performance. Based on the results of these simulations, the algorithm will iteratively modify the deck to enhance its competitiveness and fun factor.

## Interface

The software should have an interface that allows users to start the deck creation process, adjust preferences for their deck (such as favored strategies, themes, or colors), and run the evolutionary testing algorithm on resulting decks. The results of the evolutionary testing algorithm should be displayed in a meaningful and user-friendly way.