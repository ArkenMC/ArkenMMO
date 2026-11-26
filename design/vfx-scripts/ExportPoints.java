import dev.casperrs.arkenMMO.vfx.Shapes;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.List;

/**
 * Run by plot_previews.py against target/classes. Each input line is tab separated:
 * id, layer, shape, points, delay, duration, motion, lift, then the shape's six numbers.
 */
public class ExportPoints {

    public static void main(String[] args) throws IOException {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in, StandardCharsets.UTF_8));
        for (String line = in.readLine(); line != null; line = in.readLine()) {
            String[] field = line.split("\t");
            Shapes.Timing timing = new Shapes.Timing(integer(field[3]), integer(field[4]), integer(field[5]));
            Shapes.Movement movement =
                    new Shapes.Movement(Shapes.Motion.valueOf(field[6]), Double.parseDouble(field[7]));
            double[] n = new double[6];
            for (int i = 0; i < n.length; i++) {
                n[i] = Double.parseDouble(field[8 + i]);
            }
            List<Shapes.Point> points = field[2].equals("arc")
                    ? Shapes.arc(n[0], n[1], n[2], n[3], n[4], n[5], timing, movement)
                    : Shapes.line(new Shapes.Vec(n[0], n[1], n[2]), new Shapes.Vec(n[3], n[4], n[5]),
                            timing, movement);
            for (Shapes.Point point : points) {
                // Yaw 0: the caster looks along +z and their right is -x
                double[] world = Shapes.toWorld(point.position(), 0);
                System.out.println(field[0] + "," + point.tick() + "," + world[0] + "," + world[1] + ","
                        + world[2] + "," + field[1]);
            }
        }
    }

    private static int integer(String text) {
        return Integer.parseInt(text);
    }
}
