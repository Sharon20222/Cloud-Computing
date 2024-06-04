import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;

public class GenerateRandomNumbers {
    public static void main(String[] args) {
        try {
            Scanner scanner = new Scanner(System.in);

            // Prompt for the number of random numbers to generate
            System.out.println("How many random numbers to generate:");
            int randomNumCount = scanner.nextInt();

            // Prompt for the radius
            System.out.println("What's the radius number?");
            int radius = scanner.nextInt();
            int diameter = radius * 2;

            // Generate random numbers
            int[] num = new int[randomNumCount];
            for (int i = 0; i < randomNumCount; i++) {
                num[i] = (int) (Math.random() * diameter);
            }

            // Save the random numbers to a text file
            FileWriter writer = new FileWriter("random_numbers.txt");
            for (int i = 0; i < randomNumCount; i++) {
                writer.write(num[i] + " ");
            }
            writer.close();

            System.out.println("Random numbers generated and saved to file successfully.");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
