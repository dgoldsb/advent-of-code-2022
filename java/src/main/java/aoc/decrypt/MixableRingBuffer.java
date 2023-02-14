package aoc.decrypt;

import aoc.structures.RingBuffer;

import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class MixableRingBuffer extends RingBuffer<MixItem> {

    public MixableRingBuffer(Stream<MixItem> stream) {
        super(stream);
    }

    public void mix(int mixItemIdentifier) {
        int currentHeadValue = this.peek().value;
        this.putFirst(mixItemIdentifier);
        MixItem mixItem = this.removeLeft();
        this.rotate(mixItem.value);
        this.appendLeft(mixItem);
        this.putFirst(currentHeadValue);
    }

    public void putFirst(int mixItemvalue) {
        // TODO: Test, then optimize.
        while (this.peek().value != mixItemvalue) {
            this.rotate(1);
        }
    }

    public List<Integer> toValueList() {
        return this.toList().stream().map(m -> m.value).collect(Collectors.toList());
    }
}
