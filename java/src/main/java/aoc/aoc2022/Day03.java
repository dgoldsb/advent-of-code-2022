package aoc.aoc2022;

import aoc.DayInterface;
import aoc.input.InputParser;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

public class Day03 implements DayInterface {
    public Integer charToInt(Character c) {
        if ((int) c > 96) {
            return (int) c - 96;
        } else {
            return (int) c - 38;
        }
    }

    public Character findA(String s) {
        HashSet<Character> first = new HashSet<>();
        HashSet<Character> second = new HashSet<>();

        int targetSize = s.length() / 2;
        int counter = 0;
        for (Character c : s.toCharArray()) {
            if (counter < targetSize) {
                first.add(c);
                counter += 1;
            } else {
                second.add(c);
            }
        }
        first.retainAll(second);
        return first.stream().findAny().orElseThrow();
    }

    public Character findB(String a, String b, String c) {
        Set<Character> first = a.chars().mapToObj(i -> (char) i).collect(Collectors.toSet());
        Set<Character> second = b.chars().mapToObj(i -> (char) i).collect(Collectors.toSet());
        Set<Character> third = c.chars().mapToObj(i -> (char) i).collect(Collectors.toSet());
        first.retainAll(second);
        first.retainAll(third);
        return first.stream().findAny().orElseThrow();
    }

    public String partA() throws IOException {
        InputParser parser = new InputParser(3, 2022);
        List<Integer> values = parser.readLines().map(this::findA).map(this::charToInt).toList();
        return ((Integer) values.stream().mapToInt(Integer::intValue).sum()).toString();
    }

    public String partB() throws IOException {
        InputParser parser = new InputParser(3, 2022);

        // No nice way to functionally reduce with 3 lines, resorting to iterating with a `for`.
        ArrayList<String> buffer = new ArrayList<>();
        ArrayList<Integer> results = new ArrayList<>();
        for (String s : parser.readLines().toList()) {
            if (buffer.size() == 3) {
                results.add(charToInt(findB(buffer.remove(2), buffer.remove(1), buffer.remove(0))));
            }
            buffer.add(s);
        }
        results.add(charToInt(findB(buffer.remove(2), buffer.remove(1), buffer.remove(0))));

        return ((Integer) results.stream().mapToInt(Integer::intValue).sum()).toString();
    }
}
