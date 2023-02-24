package aoc.aoc2022;

import aoc.DayInterface;
import aoc.decrypt.MixableRingBuffer;
import aoc.input.InputParser;

import java.io.IOException;
import java.math.BigInteger;
import java.util.List;
import java.util.stream.Stream;


public class Day20 implements DayInterface {
    private BigInteger MAGIC_NUMBER = new BigInteger("811589153");

    private void applyMixRound(MixableRingBuffer buffer, int size) {
        for (int i = 0; i < size; i++) {
            buffer.mix(i);
        }
    }

    public BigInteger solve(MixableRingBuffer buffer, int mix_count) {
        for (int i = 0; i < mix_count; i++) {
            applyMixRound(buffer, buffer.toList().size());
        }

        buffer.putZeroFirst();

        BigInteger result = new BigInteger("0");
        for (int i = 0; i < 3; i++) {
            buffer.rotate(1000);
            result = result.add(buffer.peekValue());
        }
        return result;
    }

    public String partA() throws IOException {
        InputParser parser = new InputParser(20, 2022);
        var startSequence = parser.readIntegers().toList();
        Stream<BigInteger> bigIntegerStream = startSequence.stream().map(integer -> new BigInteger(integer.toString()));
        MixableRingBuffer buffer = new MixableRingBuffer(bigIntegerStream.toList());
        return solve(buffer, 1).toString();
    }

    public String partB() throws IOException {
        InputParser parser = new InputParser(20, 2022);
        List<BigInteger> bigIntegerList = parser.readIntegers().map(i -> new BigInteger(i.toString()).multiply(MAGIC_NUMBER)).toList();
        MixableRingBuffer buffer = new MixableRingBuffer(bigIntegerList);
        return solve(buffer, 10).toString();
    }
}
