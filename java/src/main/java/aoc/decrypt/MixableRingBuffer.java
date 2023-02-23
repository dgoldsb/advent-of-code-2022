package aoc.decrypt;

import aoc.structures.RingBuffer;

import java.math.BigInteger;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class MixableRingBuffer extends RingBuffer<MixItem> {

    public MixableRingBuffer(Stream<MixItem> stream) {
        super(stream);
    }

    public void mix(int mixItemIdentifier) {
        int size = this.toList().size();
        int currentHeadIdentifier = this.peek().identifier;
        this.putFirst(mixItemIdentifier);
        MixItem mixItem = this.removeLeft();

        // Figure out the rotation, without overflowing the integer.
        int rotation = Integer.parseInt(mixItem.value.mod(new BigInteger(Integer.toString(size))).toString());
        if (mixItem.value.toString().charAt(0) == '-') {
            rotation -= 1;
        }
        this.rotate(rotation);

        this.appendLeft(mixItem);
        this.putFirst(currentHeadIdentifier);
    }

    public void putFirst(int mixItemIdentifier) {
        while (this.peek().identifier != mixItemIdentifier) {
            this.rotate(1);
        }
    }

    public List<BigInteger> toValueList() {
        return this.toList().stream().map(m -> m.value).collect(Collectors.toList());
    }
}
