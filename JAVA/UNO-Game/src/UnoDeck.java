import java.util.ArrayList;
import java.util.Collections;

public class UnoDeck {
    private ArrayList<UnoCard> deck = new ArrayList<>();


    /**
     * creates a deck and shuffles it
     *
     * @param addActionCards decides whether to add action cards into the deck
     */
    public UnoDeck(boolean addActionCards) {
        deck.add(new UnoCard(0, "red"));
        deck.add(new UnoCard(0, "yellow"));
        deck.add(new UnoCard(0, "blue"));
        deck.add(new UnoCard(0, "green"));
        for (int i = 1; i < 10; i++) {
            for (int j = 0; j < 2; j++) {
                deck.add(new UnoCard(i, "red"));
                deck.add(new UnoCard(i, "yellow"));
                deck.add(new UnoCard(i, "blue"));
                deck.add(new UnoCard(i, "green"));
            }
        }
        if (addActionCards) {
            for (int j = 0; j < 2; j++) {
                deck.add(new UnoCard("\uD83D\uDEAB", "red"));
                deck.add(new UnoCard("\uD83D\uDEAB", "yellow"));
                deck.add(new UnoCard("\uD83D\uDEAB", "blue"));
                deck.add(new UnoCard("\uD83D\uDEAB", "green"));
            }
            for (int j = 0; j < 2; j++) {
                deck.add(new UnoCard("\uD83D\uDD04", "red"));
                deck.add(new UnoCard("\uD83D\uDD04", "yellow"));
                deck.add(new UnoCard("\uD83D\uDD04", "blue"));
                deck.add(new UnoCard("\uD83D\uDD04", "green"));
            }
            for (int j = 0; j < 2; j++) {
                deck.add(new UnoCard("+2", "red"));
                deck.add(new UnoCard("+2", "yellow"));
                deck.add(new UnoCard("+2", "blue"));
                deck.add(new UnoCard("+2", "green"));
            }

//        deck.add(new UnoCard("Wild", ""));
//        deck.add(new UnoCard("Wild", ""));
//        deck.add(new UnoCard("Wild", ""));
//        deck.add(new UnoCard("Wild", ""));
//
//        deck.add(new UnoCard("Wild +4", ""));
//        deck.add(new UnoCard("Wild +4", ""));
//        deck.add(new UnoCard("Wild +4", ""));
//        deck.add(new UnoCard("Wild +4", ""));

        }

        shuffleDeck();
    }


    public ArrayList<UnoCard> getDeck() {
        return deck;
    }


    public int getLength() {
        return this.deck.size();
    }


    /**
     * shuffles this deck
     */
    public void shuffleDeck() {
        Collections.shuffle(this.deck);
    }


    @Override
    public String toString() {
        return "DeckOfUno{" +
                "deck= " + getLength() + deck +
                '}';
    }


    /**
     * puts a card into a deck and shuffles this deck
     *
     * @param putBackUnoCard the card you want to put into the deck
     */
    public void putCardBack(UnoCard putBackUnoCard) {
        deck.add(putBackUnoCard);
        this.shuffleDeck();
    }


    /**
     * draws the top card from the deck
     *
     * @return the top card in this deck
     */
    public UnoCard drawACard() {
        UnoCard returnUnoCard = this.deck.get(0);
        this.deck.remove(0);
        return returnUnoCard;
    }

}
