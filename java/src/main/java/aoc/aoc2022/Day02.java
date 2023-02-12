package aoc.aoc2022;

import aoc.DayInterface;
import aoc.input.InputParser;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Day02 implements DayInterface {
    private Integer scoreA(String outcome) {
        int outcomeValue = switch (outcome) {
            case "A X", "B Y", "C Z" -> 3;
            case "A Y", "B Z", "C X" -> 6;
            case "A Z", "B X", "C Y" -> 0;
            default -> 0;
        };
        int playedValue = switch (outcome.charAt(2)) {
            case 'X' -> 1;
            case 'Y' -> 2;
            case 'Z' -> 3;
            default -> 0;
        };
        return outcomeValue + playedValue;
    }

    private Integer scoreB(String outcome) {
        int outcomeValue = switch (outcome) {
            case "A Y", "B X", "C Z" -> 1;
            case "A Z", "B Y", "C X" -> 2;
            case "A X", "B Z", "C Y" -> 3;
            default -> 0;
        };
        int playedValue = switch (outcome.charAt(2)) {
            case 'X' -> 0;
            case 'Y' -> 3;
            case 'Z' -> 6;
            default -> 0;
        };
        return outcomeValue + playedValue;
    }

    public String partA() throws IOException {
        InputParser parser = new InputParser(2, 2022);
        return ((Integer) parser.readLines().map(this::scoreA).mapToInt(Integer::intValue).sum()).toString();
    }

    public String partB() throws IOException {
        InputParser parser = new InputParser(2, 2022);
        return ((Integer) parser.readLines().map(this::scoreB).mapToInt(Integer::intValue).sum()).toString();
    }
}
