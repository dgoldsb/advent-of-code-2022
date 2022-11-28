package aoc;

import java.util.stream.IntStream;
import java.lang.ClassNotFoundException;

public interface Runner {
    static void runChallenges(int year) {
        IntStream.rangeClosed(1, 25)
                .forEachOrdered(day -> {
                    runDay(year, day);
                });
    }

    static void runDay(int year, int day) {
        String classPath = String.format("aoc.aoc%04d.Day%02d", year, day);
        try {
            DayInterface dayChallenge = (DayInterface) Class.forName(classPath)
                    .getDeclaredConstructor()
                    .newInstance();
            System.out.println(dayChallenge.partA());
            System.out.println(dayChallenge.partB());
        } catch (ClassNotFoundException e) {
            // Days are added one-by-one, for the time being this is expected.
        } catch (Exception e) {
            // Not so nice, should probably declare what may be thrown.
            e.printStackTrace();
        }
    }
}