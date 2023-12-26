import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;

public class UnoPlayer {
    ArrayList<UnoCard> hand = new ArrayList<>();
    UnoDeck deck;
    Boolean saidUno = false;
    private int playerNo;


    /**
     * constructs a new uno player
     *
     * @param playerNo                 which player is this?
     * @param deck                     the deck the player will be drawing from
     * @param amountOfCardsToStartWith default to 7, the cards the player will be starting with
     */
    public UnoPlayer(int playerNo, UnoDeck deck, int amountOfCardsToStartWith) {
        this.playerNo = playerNo;
        this.deck = deck;
        for (int i = 0; i < amountOfCardsToStartWith; i++) {
            drawCard();
        }
    }


    public UnoPlayer(int playerNo, UnoDeck deck) {
        this(playerNo, deck, 7);
    }


    public int getHandSize() {
        return hand.size();
    }


    @Override
    public String toString() {
        return "Player " + (this.playerNo + 1) + "\nhand size : " + this.hand.size() + "\n" + this.hand;
    }


    /**
     * draw a card from deck and adds it to this hand
     */
    public void drawCard() {
        this.hand.add(this.deck.drawACard());
    }


    /**
     * gets the user to choose a card from there hand
     * and plays that card
     *
     * @param topUnoCard the card that is at the top in the list
     * @param caller     the Game that is calling this function, it is used to replace the top card with the card that is played
     */
    public void play(UnoCard topUnoCard, UnoGame caller) throws IOException {
        resetUnoCounter();
        BufferedReader input = new BufferedReader(new InputStreamReader(System.in));
        System.out.printf("the top card is: %s\n%s\nCard Index =", topUnoCard, this);
        String tempInput = input.readLine();
        if (tempInput.isEmpty()) {
            this.drawCard();
            System.out.println();
            this.play(topUnoCard, caller);
            return;
        } else if (tempInput.toLowerCase().contains("uno")) {
            this.saidUno = true;
            System.out.print("UNO!\nCard Index =");
            tempInput = input.readLine();
            if (tempInput.isEmpty()) {
                this.drawCard();
                System.out.println();
                this.play(topUnoCard, caller);
                return;
            }
        }
        int playCardIndex;
        try {
            playCardIndex = Integer.parseInt(tempInput);
        } catch (NumberFormatException e) {
            System.out.println("\nyou need to enter a number\ntry again");
            this.play(topUnoCard, caller);
            return;
        }
        UnoCard playUnoCard;
        try {
            playUnoCard = this.hand.get(playCardIndex - 1);
        } catch (IndexOutOfBoundsException e) {
            System.out.println("\nthe index you entered dose not correspond to a card");
            this.play(topUnoCard, caller);
            return;
        }
        if (playUnoCard.canBePlayedOnBy(topUnoCard)) {
            this.hand.remove(playCardIndex - 1);
            caller.setTopCard(playUnoCard);
            if (!playUnoCard.isNormal()) {
                switch (playUnoCard.getType()) {
                    case "\uD83D\uDEAB":
                        caller.setSkipNextPlayer();
                        break;
                    case "\uD83D\uDD04":
                        caller.reversGameDirection();
                        break;
                    case "+2":
                        caller.setNextPlayerDrawCardAmount(2);
                        break;
                }
            }
        } else {
            System.out.println("\nyou cant play the card " + playUnoCard);
            this.play(topUnoCard, caller);
            return;
        }

        if (hand.size() == 1 && !this.saidUno) {
            this.drawCard();
            this.drawCard();
        }
    }


    /**
     * resets the variable keeping track if the player has said "uno"
     */
    private void resetUnoCounter() {
        if (hand.size() > 1) {
            this.saidUno = false;
        }
    }
}
