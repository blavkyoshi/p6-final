import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)


public class Label extends Actor
{
    public Label(String text, int size)
    {
        setImage(new GreenfootImage(text, size, Color.DARK_GRAY, Color.WHITE));
    }
    
    public void update(String text)
    {
        GreenfootImage img = getImage();
        if (img != null) img.clear();
        setImage(new GreenfootImage(text, 30, Color.WHITE, null));
    }
    public void setValue(String text)
    {
        GreenfootImage img = getImage();
        if (img != null) img.clear();
        setImage(new GreenfootImage(text, 30, Color.WHITE, null));
    }
}   
