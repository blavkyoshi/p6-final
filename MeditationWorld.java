import greenfoot.*;   // (World, Actor, GreenfootImage, Greenfoot and GreenfootSound)
import java.awt.*;

public class MeditationWorld extends World {

    private int totalSeconds = 600;        // default: 10 min
    private int remainingSeconds = 600;
    private boolean isRunning = false;
    private boolean musicOn = false;

    // UI Elements
    private Label timerLabel;
    private Label statusLabel;
    private Label durationLabel;

    private UIButton startButton;
    private UIButton resetButton;
    private UIButton musicButton;

    private String[] durations = {"5", "10", "15", "20", "30"};
    private int durationIndex = 1; // start with "10"

    private GreenfootSound music = new GreenfootSound("lofi.mp3");

    public MeditationWorld() {    
        super(600, 400, 1);  // width, height, cell size

        timerLabel = new Label("10:00", 60);
        addObject(timerLabel, 300, 80);

        durationLabel = new Label("Duration: 10 min (press LEFT/RIGHT)", 30);
        addObject(durationLabel, 300, 150);

        startButton = new UIButton("Start", 28, Color.GREEN);
        resetButton = new UIButton("Reset", 28, Color.RED);
        musicButton = new UIButton("Music: OFF", 28, Color.YELLOW);

        addObject(startButton, 180, 230);
        addObject(resetButton, 420, 230);
        addObject(musicButton, 300, 300);

        statusLabel = new Label("Ready to meditate", 28);
        addObject(statusLabel, 300, 360);
    }

    public void act() {
        handleDurationSelection();

        if (Greenfoot.mouseClicked(startButton) && !isRunning) {
            startTimer();
        }

        if (Greenfoot.mouseClicked(resetButton)) {
            resetTimer();
        }

        if (Greenfoot.mouseClicked(musicButton)) {
            toggleMusic();
        }

        if (isRunning) {
            tickTimer();
        }
    }

    private void handleDurationSelection() {
        if (!isRunning) {
            if (Greenfoot.isKeyDown("right")) {
                changeDuration(1);
                Greenfoot.delay(10);
            }
            if (Greenfoot.isKeyDown("left")) {
                changeDuration(-1);
                Greenfoot.delay(10);
            }
        }
    }

    private void changeDuration(int dir) {
        durationIndex += dir;

        if (durationIndex < 0) durationIndex = durations.length - 1;
        if (durationIndex >= durations.length) durationIndex = 0;

        int minutes = Integer.parseInt(durations[durationIndex]);
        totalSeconds = minutes * 60;
        remainingSeconds = totalSeconds;

        timerLabel.setValue(formatTime(remainingSeconds));
        durationLabel.setValue("Duration: " + minutes + " min (press LEFT/RIGHT)");
    }

    private void startTimer() {
        isRunning = true;
        startButton.setText("Meditating...");
        statusLabel.setValue("Meditation in progress");

        startButton.setColor(Color.GRAY);
    }

    private void resetTimer() {
        isRunning = false;
        remainingSeconds = totalSeconds;

        timerLabel.setValue(formatTime(remainingSeconds));
        statusLabel.setValue("Timer reset");

        startButton.setText("Start");
        startButton.setColor(Color.GREEN);

        if (musicOn) {
            music.stop();
            musicOn = false;
            musicButton.setText("Music: OFF");
        }
    }

    private void toggleMusic() {
        musicOn = !musicOn;
        if (musicOn) {
            music.playLoop();
            musicButton.setText("Music: ON");
            statusLabel.setValue("Music playing");
        } else {
            music.stop();
            musicButton.setText("Music: OFF");
            statusLabel.setValue("Music stopped");
        }
    }

    private void tickTimer() {
        if (remainingSeconds > 0) {
            if (Greenfoot.getRandomNumber(60) == 0) {
                remainingSeconds--;
                timerLabel.setValue(formatTime(remainingSeconds));
            }
        } else {
            finishMeditation();
        }
    }

    private void finishMeditation() {
        isRunning = false;

        timerLabel.setValue("Done!");
        statusLabel.setValue("Meditation complete");

        startButton.setText("Start");
        startButton.setColor(Color.GREEN);

        if (musicOn) {
            music.stop();
            musicOn = false;
            musicButton.setText("Music: OFF");
        }
    }

    private String formatTime(int sec) {
        int mins = sec / 60;
        int secs = sec % 60;
        return String.format("%02d:%02d", mins, secs);
    }
}
