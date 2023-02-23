package aoc.decrypt;

import java.math.BigInteger;

public class MixItem {
    public int identifier;
    public BigInteger value;

    public MixItem(int identifier, BigInteger value) {
        this.identifier = identifier;
        this.value = value;
    }
}
