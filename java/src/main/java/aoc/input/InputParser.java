package aoc.input;

import java.io.IOException;
import java.net.URI;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.stream.Stream;

public class InputParser {
    int day;
    int year;
    String INPUT_ROOT = "/Users/dylangoldsborough/Repositories/advent-of-code-2022/pyo3/inputs";

    public InputParser(int day, int year) {
        this.day = day;
        this.year = year;
    }

    public Stream<String> readLines() throws IOException {
        URI fileName = URI.create(("file://%s/%d/%d.txt").formatted(INPUT_ROOT, year, day));
        return Files.lines(Paths.get(fileName));
    }
}
