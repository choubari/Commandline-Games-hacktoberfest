import java.io.IOException;
import java.util.ArrayList;

public class UnoGame {
    private UnoDeck deck = new UnoDeck(true);
    private ArrayList<UnoPlayer> unoPlayers = new ArrayList<>();
    private UnoCard topUnoCard;
    private int turn = 0;
    private Boolean isGameDirectionRevers = false;
    private Boolean skipNextPlayer = false;
    private int nextPlayerDrawCardAmount = 0;


    public UnoGame(int numberOfPlayers) {
        for (int i = 0; i < numberOfPlayers; i++) {
            unoPlayers.add(new UnoPlayer(i, deck));
        }
        setTopCardFromDeck();
    }


    private static void clearConsole() {
        for (int i = 0; i < 50; ++i) System.out.println();
    }


    public void setTopCardFromDeck() {
        topUnoCard = deck.drawACard();
        if (!topUnoCard.isNormal()) {
            deck.putCardBack(topUnoCard);
            this.setTopCardFromDeck();
        }
    }


    public void setTopCard(UnoCard topUnoCard) {
        this.topUnoCard = topUnoCard;
    }


    public void reversGameDirection() {
        this.isGameDirectionRevers = !this.isGameDirectionRevers;
    }


    public void setSkipNextPlayer() {
        this.skipNextPlayer = true;
    }


    public void setNextPlayerDrawCardAmount(int nextPlayerDrawCardAmount) {
        this.nextPlayerDrawCardAmount = nextPlayerDrawCardAmount;
    }


    @Override
    public String toString() {
        return "Game{" +
                "deck=" + deck +
                ",\nplayers=" + unoPlayers +
                ",\ntopCard=" + topUnoCard +
                ", turn=" + turn +
                ", numberOfPlayers=" + unoPlayers.size() +
                "\n";
    }


    /**
     * the games main loop
     */
    public void startGame() throws IOException {
        while (!isGameOver()) {
            clearConsole();

            //player plays
            if (this.skipNextPlayer) {
                this.skipNextPlayer = false;
            } else {
                for (; nextPlayerDrawCardAmount > 0; nextPlayerDrawCardAmount--)
                    this.unoPlayers.get(this.turn).drawCard();
                this.unoPlayers.get(this.turn).play(topUnoCard, this);
            }

            //find the next player
            if (this.isGameDirectionRevers) {
                if (this.unoPlayers.size() != 2) {
                    if (this.turn == 0) this.turn = unoPlayers.size() - 1;
                    else this.turn--;
                }
            } else {
                if (this.turn == unoPlayers.size() - 1) this.turn = 0;
                else this.turn++;
            }
        }
        System.out.println("game over\n player " + (this.turn + 1) + " wins");
    }


    public boolean isGameOver() {
        for (UnoPlayer unoPlayer : unoPlayers)
            if (unoPlayer.getHandSize() <= 0)
                return true;
        return false;
    }
}
