public class UnoCard {
    private boolean normal;
    private int rank;
    private char color;

    private String colorCode;


    /*
    type can be;
    🚫
    🔄
    +2
     */
    private String type;


    /**
     * creates a new number card
     *
     * @param rank  the numerical number of the card
     * @param color the color of the card in String
     */
    public UnoCard(int rank, String color) {
        this.normal = true;
        this.rank = rank;
        color = color.toLowerCase();
        this.color = color.charAt(0);
        this.colorCode = switch (color) {
            case "red" -> "\033[31m";
            case "yellow" -> "\033[38;2;255;255;0m";
            case "blue" -> "\033[34m";
            case "green" -> "\033[32m";
            default -> "\033[0m";
        };
    }


    /**
     * creates a new action card
     *
     * @param type  the kind of action card can be 🚫, 🔄, +2
     * @param color the color of the card in String
     */
    public UnoCard(String type, String color) {
        this.normal = false;
        this.type = type;
        color = color.toLowerCase();
//        if (!this.type.startsWith("Wild"))
        this.color = color.toUpperCase().charAt(0);
        this.colorCode = switch (color) {
            case "red" -> "\033[31m";
            case "yellow" -> "\033[38;2;255;255;0m";
            case "blue" -> "\033[34m";
            case "green" -> "\033[32m";
            default -> "\033[0m";
        };
    }


    @Override
    public String toString() {
        if (normal) {
            return this.colorCode + this.rank + "\033[0m";
        } else if (this.type.charAt(0) == '+')
            return this.colorCode + this.type + "\033[0m";
//        else if (this.type.startsWith("Wild")) {
//            return "\033[31mW\033[38;2;255;255;0mi\033[34ml\033[32md\033[0m"+ (this.type.contains("+4") ? " +4" : "");
//        }
        return this.colorCode + this.color + this.type + "\033[0m";
    }


    public int getRank() {
        return this.rank;
    }


    public char getColor() {
        return color;
    }


    public String getType() {
        return type;
    }


    public Boolean isNormal() {
        return this.normal;
    }


    /**
     * checks if a card can be played on another card
     *
     * @param unoCard the card that will be played onto of this card
     * @return true if you can play, false if you cannot
     */
    public Boolean canBePlayedOnBy(UnoCard unoCard) {
        if (this.type == null) {
            return Character.toLowerCase(this.color) == Character.toLowerCase(unoCard.getColor()) || this.rank == unoCard.getRank();
        }
        return Character.toLowerCase(this.color) == Character.toLowerCase(unoCard.getColor()) || this.type.equals(unoCard.getType());
    }


}
