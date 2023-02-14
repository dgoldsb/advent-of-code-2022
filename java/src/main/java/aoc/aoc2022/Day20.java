package aoc.aoc2022;

import aoc.DayInterface;
import aoc.decrypt.MixItem;
import aoc.decrypt.MixableRingBuffer;
import aoc.geode.BluePrint;
import aoc.input.InputParser;

import java.io.IOException;
import java.util.List;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.stream.IntStream;
import java.util.stream.Stream;


public class Day20 implements DayInterface {
    private void applyMixRound(MixableRingBuffer buffer, List<Integer> originalOrder) {
        for (Integer value : originalOrder) {
            buffer.mix(value);
        }
    }

    public Integer solve(MixableRingBuffer buffer, int mix_count) {
        List<Integer> originalOrder = buffer.toValueList();

        for (int i = 0; i < mix_count; i++) {
            applyMixRound(buffer, originalOrder);
        }

        buffer.putFirst(0);

        Integer result = 0;
        for (int i = 0; i < 3; i++) {
            buffer.rotate(1000);
            result += buffer.peek().value;
        }
        return result;
    }

    public String partA() throws IOException {
        InputParser parser = new InputParser(20, 2022);
        var startSequence = parser.readIntegers().toList();
        Stream<MixItem> mixItemStream = IntStream
                .range(0, startSequence.size())
                .mapToObj(i -> new MixItem(i, startSequence.get(i)));
        MixableRingBuffer buffer = new MixableRingBuffer(mixItemStream);
        return solve(buffer, 1).toString();
    }

    public String partB() throws IOException {
        return "WIP";
    }
}
