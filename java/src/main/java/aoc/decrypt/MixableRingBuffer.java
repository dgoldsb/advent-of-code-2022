package aoc.decrypt;

import aoc.structures.RingBuffer;

import java.math.BigInteger;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.util.stream.Stream;

public class MixableRingBuffer extends RingBuffer<Integer> {
    // TODO: keep ringbuffer of identifiers.
    // TODO: keep map to value.
    // TODO: for fast find, ...

    HashMap<Integer, BigInteger> indexValueMap = new HashMap<>();

    public MixableRingBuffer(List<BigInteger> valueList) {
        super(IntStream.range(0, valueList.size()).boxed().toList());
        int i = 0;
        for (BigInteger value : valueList) {
            this.indexValueMap.put(i, value);
            i++;
        }
    }

    public void mix(int identifier) {
        int currentHead = this.peek();
        BigInteger value = this.indexValueMap.get(identifier);
        int rotation = this.normalize(value);

        this.putFirst(identifier);
        this.removeLeft();

        // Figure out the rotation, without overflowing the integer.
        // TODO: Cache normalization.
        this.rotate(rotation);

        this.appendLeft(identifier);
        this.putFirst(currentHead);
    }

    public BigInteger peekValue() {
        return this.indexValueMap.get(this.peek());
    }

    private Integer fetchValue(BigInteger value) {
        Stream<Integer> stream = this.indexValueMap.entrySet().stream().filter(val -> val.getValue().equals(value)).map(Map.Entry::getKey);
        return stream.findFirst().orElseThrow();
    }

    public void putZeroFirst() {
        BigInteger zero = new BigInteger("0");
        Integer zeroIdentifier = this.fetchValue(zero);
        this.putFirst(zeroIdentifier);
    }

    public List<BigInteger> toValueList() {
        return this.toList().stream().map(m -> this.indexValueMap.get(m)).collect(Collectors.toList());
    }
}
