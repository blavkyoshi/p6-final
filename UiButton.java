import greenfoot.*;
import java.awt.*;

public class UIButton extends Actor {

    private String text;
    private int fontSize;
    private Color color;

    public UIButton(String text, int fontSize, Color color) {
        this.text = text;
        this.fontSize = fontSize;
        this.color = color;
        updateImage();
    }

    public void act() {}

    private void updateImage() {
        GreenfootImage img = new GreenfootImage(text.length() * fontSize, fontSize + 20);
        img.setColor(color);
        img.fillRect(0, 0, img.getWidth(), img.getHeight());
        img.setColor(Color.BLACK);
        img.setFont(new Font("Arial", Font.BOLD, fontSize));
        img.drawString(text, 10, fontSize);
        setImage(img);
    }

    public void setText(String t) {
        this.text = t;
        updateImage();
    }

    public void setColor(Color c) {
        this.color = c;
        updateImage();
    }
}
