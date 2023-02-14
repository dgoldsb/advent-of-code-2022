package aoc.aoc2022;

import aoc.DayInterface;
import aoc.geode.BluePrint;
import aoc.input.InputParser;

import java.io.IOException;
import java.util.List;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;


public class Day19 implements DayInterface {
    public String partA() throws IOException {
        InputParser parser = new InputParser(19, 2022);
        List<Integer> values = parser.readLines().map(BluePrint::new).map(b -> b.getQuality(24)).toList();
        return ((Integer) values.stream().mapToInt(Integer::intValue).sum()).toString();
    }

    public String partB() throws IOException {
        ExecutorService service = Executors.newFixedThreadPool(3);
        InputParser parser = new InputParser(19, 2022);
        List<Future<Integer>> futures = parser.readLines().limit(3).map(BluePrint::new).map(b -> service.submit(() -> b.getGeodes(32))).toList();
        String result = ((Integer) futures.stream().map(f -> {
            try {
                return f.get();
            } catch (InterruptedException | ExecutionException e) {
                throw new RuntimeException(e);
            }
        }).mapToInt(Integer::intValue).reduce(1, (x, y) -> x * y)).toString();
        service.shutdown();
        return result;
    }
}
