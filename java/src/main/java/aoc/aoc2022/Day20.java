package aoc.aoc2022;

import aoc.DayInterface;
import aoc.decrypt.MixItem;
import aoc.decrypt.MixableRingBuffer;
import aoc.geode.BluePrint;
import aoc.input.InputParser;

import java.io.IOException;
import java.math.BigInteger;
import java.util.List;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.stream.IntStream;
import java.util.stream.Stream;


public class Day20 implements DayInterface {
    private BigInteger MAGIC_NUMBER = new BigInteger("811589153");

    private void applyMixRound(MixableRingBuffer buffer, int size) {
        for (int i = 0;i<size;i++) {
            buffer.mix(i);
        }
    }

    public BigInteger solve(MixableRingBuffer buffer, int mix_count) {
        for (int i = 0; i < mix_count; i++) {
            applyMixRound(buffer, buffer.toList().size());
        }

        BigInteger zero = new BigInteger("0");
        for (MixItem item : buffer.toList()) {
            if (item.value.equals(zero)) {
                buffer.putFirst(item.identifier);
            }
        }

        BigInteger result = new BigInteger("0");
        for (int i = 0; i < 3; i++) {
            buffer.rotate(1000);
            result = result.add(buffer.peek().value);
        }
        return result;
    }

    public String partA() throws IOException {
        InputParser parser = new InputParser(20, 2022);
        var startSequence = parser.readIntegers().toList();
        Stream<MixItem> mixItemStream = IntStream
                .range(0, startSequence.size())
                .mapToObj(i -> new MixItem(i, new BigInteger(startSequence.get(i).toString())));
        MixableRingBuffer buffer = new MixableRingBuffer(mixItemStream);
        // TODO: Currently slow, but correct. Challenge is fast lookups, linked list is not suitable.
        return solve(buffer, 1).toString();
    }

    public String partB() throws IOException {
        InputParser parser = new InputParser(20, 2022);
        var startSequence = parser.readIntegers().map(i -> new BigInteger(i.toString()).multiply(MAGIC_NUMBER)).toList();
        Stream<MixItem> mixItemStream = IntStream
                .range(0, startSequence.size())
                .mapToObj(i -> new MixItem(i, startSequence.get(i)));
        MixableRingBuffer buffer = new MixableRingBuffer(mixItemStream);
        // TODO: Currently slow, but correct. Challenge is fast lookups, linked list is not suitable.
        return solve(buffer, 10).toString();
    }
}
