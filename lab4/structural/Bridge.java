interface Device {
    void print(String data);
}

class Monitor implements Device {
    @Override
    public void print(String data) {
        System.out.println("Displaying on monitor: " + data);
    }
}

class Printer implements Device {
    @Override
    public void print(String data) {
        System.out.println("Printing to paper: " + data);
    }
}

abstract class Output {
    protected Device device;

    public Output(Device device) {
        this.device = device;
    }

    public abstract void render(String data);
}

class TextOutput extends Output {
    public TextOutput(Device device) {
        super(device);
    }

    @Override
    public void render(String data) {
        device.print("Text: " + data);
    }
}

class ImageOutput extends Output {
    public ImageOutput(Device device) {
        super(device);
    }

    @Override
    public void render(String data) {
        device.print("Image: [Binary data: " + data + "]");
    }
}

public class Main {
    public static void main(String[] args) {
        Device monitor = new Monitor();
        Device printer = new Printer();

        Output textOnMonitor = new TextOutput(monitor);
        Output textOnPrinter = new TextOutput(printer);

        textOnMonitor.render("Hello, world!");
        textOnPrinter.render("Hello, world!");

        Output imageOnMonitor = new ImageOutput(monitor);
        imageOnMonitor.render("101010101");
    }
}