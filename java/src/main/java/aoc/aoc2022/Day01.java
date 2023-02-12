package aoc.aoc2022;

import aoc.DayInterface;
import aoc.input.InputParser;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.io.IOException;

public class Day01 implements DayInterface {
    private ArrayList<Integer> getBackpacks() throws IOException {
        InputParser parser = new InputParser(1, 2022);
        List<String> lines = parser.readLines().toList();

        int backpack = 0;
        ArrayList<Integer> backpacks = new ArrayList<>();
        for (String line : lines) {
            try {
                int calories = Integer.parseInt(line);
                backpack += calories;
            } catch (NumberFormatException ex) {
                backpacks.add(backpack);
                backpack = 0;
            }
        }
        backpacks.add(backpack);
        return backpacks;
    }

    public String partA() throws IOException {
        return getBackpacks().stream().max(Integer::compare).orElseThrow().toString();
    }

    public String partB() throws IOException {
        ArrayList<Integer> backpacks = getBackpacks();
        backpacks.sort(Collections.reverseOrder());
        return ((Integer) backpacks.stream().limit(3).mapToInt(Integer::intValue).sum()).toString();
    }
}
